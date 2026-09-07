# saferdrop-rime
# SafeDrop Voice-Native Delivery Confirmation

## Problem
Delivery agents can't look at a screen while riding or handling packages. Text-based
order confirmations get skipped or misread. Spoken confirmation is essential — this
product has no non-voice equivalent.

## Hard voice problem addressed
**Pronunciation and controlled delivery.** Rime's default rendering of Indian phone
numbers, PIN codes, and uncommon names is inconsistent. We test this with 10 realistic
delivery-order fixtures, comparing a baseline render against a controlled-delivery
optimized render (digit-spacing, pause insertion via punctuation).

## Architecture
- `speak.py` — calls Rime's HTTP TTS endpoint (`/v1/rime-tts`), plus `optimize_text()`
  which reformats digits/labels for clearer delivery.
- `app.py` — Flask server, two routes: play baseline or optimized audio for any fixture.
- `static/index.html` — single-page UI, no build step.
- `evidence/run_test.py` — batch-generates all baseline/optimized clips for the blind test.

## Rime configuration (exact)
- Model: `coda`
- Speaker: `astra`
- Language: `en`
- Endpoint: `https://users.rime.ai/v1/rime-tts`
- Audio format: WAV
- Transport: HTTP POST, one request per utterance (non-streaming)

## Setup
\`\`\`bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # paste your RIME_API_KEY
python app.py
\`\`\`
Visit http://localhost:5000

## Reproducing the evidence
\`\`\`bash
python evidence/run_test.py
\`\`\`
Generates 20 clips in `static/clips/` and `evidence/results.json`.

## Known limitations
- Tested only on English text with Indian names/numbers; not tested on noisy/telephony audio.
- Blind listening test sample size is small (N=[1]); result are exploratory, not
  statistically significant.
- `optimize_text()` uses regex heuristics, not a general NLP pronunciation model — it
  may not generalize to name patterns outside the fixture set.

## AI assistance disclosure
README and code scaffolding drafted with AI assistance; all logic reviewed and tested by the team before submission.
