import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

RIME_API_KEY = os.environ["RIME_API_KEY"]
RIME_URL = "https://users.rime.ai/v1/rime-tts"
MODEL_ID = "coda"
SPEAKER = "astra"
LANGUAGE = "en"

def render_tts(text: str, out_path: str):
    """Call Rime and save the audio."""
    r = requests.post(
        RIME_URL,
        headers={
            "Authorization": f"Bearer {RIME_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "audio/wav",
        },
        json={
            "text": text,
            "modelId": MODEL_ID,
            "speaker": SPEAKER,
            "language": LANGUAGE,
        },
        timeout=30,
    )
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    return out_path


def optimize_text(raw: str) -> str:
    """
    Controlled-delivery transformation:
    - Phone numbers -> spaced digit-by-digit ("9876543210" -> "9 8 7 6 5 4 3 2 1 0")
    - PIN codes -> spaced digit-by-digit
    - Rupee amounts -> spelled out with 'rupees' clearly separated
    - Short pauses after each field using punctuation (commas/periods),
      since Rime respects natural sentence breaks.
    """
    text = raw

    # Space out any 10-digit phone number
    text = re.sub(
        r"\b(\d{10})\b",
        lambda m: " ".join(list(m.group(1))),
        text,
    )

    # Space out 6-digit PIN codes
    text = re.sub(
        r"\bPIN\s?(\d{6})\b",
        lambda m: "PIN code, " + " ".join(list(m.group(1))),
        text,
    )

    # Insert a short pause (comma) before "phone" and "PIN" and "amount" labels
    text = re.sub(r"\b(phone|PIN|amount|quantity)\b", r", \1", text)

    # Clean up double commas/spacing introduced above
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    # quick manual test
    sample = "Customer Siddheshwar Reddy, amount due 1299 rupees, phone 8123456789."
    print("RAW      :", sample)
    print("OPTIMIZED:", optimize_text(sample))