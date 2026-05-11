# Transformers — Cheatsheet

**Wann ihr das braucht:** vor Phase 3, wenn ihr die Pipeline baut. Liest sich in 5-10 min, gibt euch alles, was ihr operativ einbauen müsst.

## 1. Modell-Namen (exakt)

| Server | Modell | Wo verwendet |
|---|---|---|
| gauss | `Qwen/Qwen2.5-7B-Instruct` | Phase 3-5 (Pipeline + Iterationen) |
| euler | `Qwen/Qwen2.5-3B-Instruct` | Phase 6 (3B-Kontrast) |

Achtet auf das `-Instruct` — die Base-Variante ist nicht chat-fähig und produziert für unsere Aufgabe Müll. Außerdem sind nur die exakten Namen oben **vorab gecached** auf den Servern; jeder Tippfehler oder Variantenwechsel triggert einen 28-GB-Download und bremst die ganze Klasse aus.

## 2. Lauffähiges Mini-Beispiel

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,    # NICHT fp16/bf16 — auf V100 instabil
).to("cuda").eval()                # NICHT device_map="auto" — instabil

messages = [
    {"role": "system", "content": "Antworte nur mit JSON."},
    {"role": "user", "content": "Was ist die Hauptstadt Deutschlands?"},
]
prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=False,                          # Greedy — reproduzierbar
        pad_token_id=tokenizer.eos_token_id,
    )

response = tokenizer.decode(
    outputs[0][inputs.input_ids.shape[1]:],       # nur die Antwort, ohne Prompt
    skip_special_tokens=True,
)
print(response)   # → '{"hauptstadt": "Berlin"}'
```

Eure Pipeline ist genau dieses Skelett, nur:
- echtes Schema im System-Prompt (statt "Antworte nur mit JSON")
- Anzeigen-Text als User-Message
- Schleife über alle Anzeigen
- robustes JSON-Parsing (siehe Sektion 5)

## 3. Chat-Template — was es macht

`apply_chat_template` baut aus der `messages`-Liste einen Prompt-String mit Rollen-Markern:

```
<|im_start|>system
Antworte nur mit JSON.<|im_end|>
<|im_start|>user
Was ist die Hauptstadt Deutschlands?<|im_end|>
<|im_start|>assistant
```

Das Modell sieht *wer gerade spricht* und antwortet als `assistant`. Ohne Chat-Template (= Roh-String an den Tokenizer) verwirrt das Qwen-Instruct-Modell, Antworten werden chaotisch.

**Few-Shot-Lernen:** einfach mehrere `user`/`assistant`-Paare *vor* dem aktuellen User-Turn in die `messages`-Liste schieben — das Modell lernt aus den Beispielen.

## 4. Drei Hardware-Fallen (NICHT machen)

- **`device_map="auto"`** — HF-Doku empfiehlt das überall, aber auf V100 + ppc64le + PyTorch 1.12 kommt Token-Korruption raus. Stattdessen schlicht `.to("cuda").eval()`.
- **`torch_dtype=torch.float16` / `bfloat16`** — schneller, aber produziert Tokensalat auf unserer Hardware. Bleibt bei `float32`.
- **Ohne `model.eval()` + `torch.no_grad()`** — verbraucht GPU-Speicher, der euch in den OOM treibt.

7B fp32 braucht ~28 GB VRAM auf der 32-GB-V100 — eng, aber tragfähig.

## 5. JSON aus dem Modell-Output ziehen

Das Modell hält sich oft *fast* an "nur JSON ausgeben", schreibt aber gerne Begleittext:

```
Hier ist das extrahierte JSON:
{"homeoffice": "remote", "vertragsart": "festanstellung", ...}
Hoffe das hilft!
```

Robust parsen statt direkt `json.loads(response)`:

```python
import re, json

match = re.search(r"\{.*\}", response, re.DOTALL)
if not match:
    # Modell hat kein JSON geliefert — das ist ein Befund
    return None
data = json.loads(match.group(0))
```

Wenn `match` `None` ist, zählt die Anzeige als Fail in der Eval. Anzahl solcher Fälle separat festhalten — selbst eine Eigenschaft eurer Pipeline.

## 6. Generation-Parameter

| Parameter | Wert | Warum |
|---|---|---|
| `do_sample=False` | Greedy | Reproduzierbarkeit — gleicher Input → gleicher Output |
| `max_new_tokens=200` | Cap | reicht für unser Schema; größer = unnötig langsam |
| `pad_token_id=tokenizer.eos_token_id` | EOS als Pad | unterdrückt HF-Warnings |
| `do_sample=True` + `temperature=...` | — | NICHT für Eval — sonst ist jeder Run anders |

---

**Querverweise:** `CHEATSHEETS/gpu-zugang.md` (Spawn + GPU-Wahl), `CHEATSHEETS/jsonl.md` (Predictions schreiben).
