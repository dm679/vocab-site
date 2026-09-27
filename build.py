"""Builds _site/: one self-contained page per student from template.html + <folder>/words.json."""
import json, os, shutil, html
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
tpl = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
students = json.load(open(os.path.join(ROOT, "students.json"), encoding="utf-8"))
for s in students.values():
    words = json.load(open(os.path.join(ROOT, s["folder"], "words.json"), encoding="utf-8"))
    data = json.dumps(words, ensure_ascii=False).replace("</", "<\\/")
    page = tpl.replace("{{NAME}}", html.escape(s["name"])).replace("{{WORDS}}", data)
    os.makedirs(os.path.join(OUT, s["folder"]))
    open(os.path.join(OUT, s["folder"], "index.html"), "w", encoding="utf-8").write(page)
    print(s["folder"], len(words), "words")
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
open(os.path.join(OUT, "_headers"), "w").write("/*\n  X-Robots-Tag: noindex, nofollow\n  Referrer-Policy: no-referrer\n  Cache-Control: no-cache\n")
open(os.path.join(OUT, "index.html"), "w").write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>vocab</title>\n')
