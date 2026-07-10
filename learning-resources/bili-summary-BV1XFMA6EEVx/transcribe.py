import sys, os
from faster_whisper import WhisperModel

def fmt(t):
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t-int(t))*1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

model = WhisperModel("base", device="cpu", compute_type="int8")
base = os.path.dirname(os.path.abspath(__file__))
parts = sys.argv[1:]
for p in parts:
    d = os.path.join(base, f"p{p}")
    audio = os.path.join(d, "audio.wav")
    out = os.path.join(d, "transcript.srt")
    if not os.path.exists(audio):
        print(f"p{p}: NO AUDIO", flush=True); continue
    if os.path.exists(out):
        print(f"p{p}: SKIP (exists)", flush=True); continue
    print(f"p{p}: transcribing...", flush=True)
    segs, info = model.transcribe(audio, language="en", vad_filter=False)
    lines=[]
    for i, s in enumerate(segs, 1):
        lines.append(f"{i}\n{fmt(s.start)} --> {fmt(s.end)}\n{s.text.strip()}\n")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"p{p}: DONE {len(lines)} segments", flush=True)
