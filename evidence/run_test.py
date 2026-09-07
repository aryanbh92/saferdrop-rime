import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from speak import render_tts, optimize_text

CLIPS_DIR = "static/clips"
os.makedirs(CLIPS_DIR, exist_ok=True)

with open("fixtures.json") as f:
    fixtures = json.load(f)

manifest = []

for fx in fixtures:
    fid = fx["id"]
    raw = fx["raw"]
    optimized = optimize_text(raw)

    baseline_path = f"{CLIPS_DIR}/{fid}_baseline.wav"
    optimized_path = f"{CLIPS_DIR}/{fid}_optimized.wav"

    print(f"[{fid}] rendering baseline...")
    render_tts(raw, baseline_path)
    print(f"[{fid}] rendering optimized...")
    render_tts(optimized, optimized_path)

    manifest.append({
        "id": fid,
        "raw_text": raw,
        "optimized_text": optimized,
        "baseline_clip": baseline_path,
        "optimized_clip": optimized_path,
        "listener_preference": None  # fill in after blind test
    })

with open("evidence/results.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("\nDone. Now run the blind listening test and fill in listener_preference in evidence/results.json")