"""Pre-records a male American voice (Piper, en_US-ryan-high) for every word into audio/<id>.mp3."""
import json, os, re, hashlib, subprocess, wave, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "audio")
os.makedirs(AUDIO, exist_ok=True)

def audio_id(word):
    return hashlib.sha1(word.strip().lower().encode("utf-8")).hexdigest()[:12]

def speak_text(word):
    t = re.sub(r"[^\w\s'?!.,-]", "", word).strip()
    return {"Ms.": "Miz", "Mrs.": "Missus", "PE": "P E"}.get(t, t)

if __name__ == "__main__":
    from piper import PiperVoice
    voice = PiperVoice.load(sys.argv[1])
    students = json.load(open(os.path.join(ROOT, "students.json"), encoding="utf-8"))
    made = 0
    for s in students.values():
        for w in json.load(open(os.path.join(ROOT, s["folder"], "words.json"), encoding="utf-8")):
            mp3 = os.path.join(AUDIO, audio_id(w["word"]) + ".mp3")
            if os.path.exists(mp3):
                continue
            wav = mp3[:-4] + ".wav"
            with wave.open(wav, "wb") as f:
                text = speak_text(w["word"])
                if hasattr(voice, "synthesize_wav"):
                    from piper import SynthesisConfig
                    voice.synthesize_wav(text, f, syn_config=SynthesisConfig(length_scale=1.3))
                else:
                    voice.synthesize(text, f, length_scale=1.3)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", "adelay=120,apad=pad_dur=0.25", "-ac", "1", "-b:a", "64k", mp3], check=True)
            os.remove(wav); made += 1
    print("new audio files:", made)
