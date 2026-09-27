"""Pre-records a male American voice (Kokoro-82M, voice am_michael) for every word into audio/<id>.mp3."""
import json, os, re, hashlib, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "audio")


def audio_id(word):
    return hashlib.sha1(word.strip().lower().encode("utf-8")).hexdigest()[:12]


def speak_text(word):
    t = re.sub(r"[^\w\s'?!.,-]", "", word).strip()
    return {"Ms.": "Miz", "Mrs.": "Missus", "PE": "P E"}.get(t, t)


if __name__ == "__main__":
    import numpy as np, soundfile as sf
    from kokoro import KPipeline
    os.makedirs(AUDIO, exist_ok=True)
    pipe = KPipeline(lang_code="a")  # American English
    students = json.load(open(os.path.join(ROOT, "students.json"), encoding="utf-8"))
    made = 0
    for s in students.values():
        for w in json.load(open(os.path.join(ROOT, s["folder"], "words.json"), encoding="utf-8")):
            mp3 = os.path.join(AUDIO, audio_id(w["word"]) + ".mp3")
            if os.path.exists(mp3):
                continue
            parts = [a for _, _, a in pipe(speak_text(w["word"]), voice="am_michael", speed=0.9)]
            if not parts:
                print("no audio for", w["word"])
                continue
            wav = mp3[:-4] + ".wav"
            sf.write(wav, np.concatenate([np.asarray(p) for p in parts]), 24000)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav,
                            "-af", "adelay=100,apad=pad_dur=0.2", "-ac", "1", "-b:a", "64k", mp3], check=True)
            os.remove(wav)
            made += 1
    print("new audio files:", made)
