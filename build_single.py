"""Собирает однофайловую версию суфлёра: suffler-single.html
(index.html + style.css + app.js в одном файле). Запуск: python build_single.py
"""
import os
import re

here = os.path.dirname(os.path.abspath(__file__))
read = lambda n: open(os.path.join(here, n), encoding="utf-8").read()

html = read("index.html")
css = read("style.css")
js = read("app.js")

body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
body = body.replace('<script src="app.js"></script>', "")

# приложение всегда тёмное — объявляем это явно
css = css.replace("  --font-ui:", "  color-scheme: dark;\n  --font-ui:", 1)

out = (
    '<meta charset="utf-8">\n'
    "<title>Суфлёр</title>\n"
    '<meta name="theme-color" content="#000000">\n'
    f"<style>\n{css}\n</style>\n"
    f"{body.strip()}\n"
    "<script>window.__SUFFLER_EMBEDDED = true;</script>\n"
    f"<script>\n{js}\n</script>\n"
)
assert "</script>" not in js and "</style>" not in css
with open(os.path.join(here, "suffler-single.html"), "w", encoding="utf-8") as f:
    f.write(out)
print("suffler-single.html:", len(out.encode("utf-8")), "байт")
