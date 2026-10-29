#!/usr/bin/env python3
"""Gera index.html e compositions/*.html de um criativo do Corpo C (produto e objeções em rajada "sim ou não").
O gancho de cada versão fica em roteiro.json. Rode de novo sempre que trocar a narração."""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(AQUI, "compositions"), exist_ok=True)
CFG = json.load(open(os.path.join(AQUI, "roteiro.json")))
VO1_EM = 0.25

def palavras(arq, desloc):
    return [dict(w, start=round(w["start"] + desloc, 3), end=round(w["end"] + desloc, 3))
            for w in json.load(open(os.path.join(AQUI, "assets", arq)))]

vo1 = palavras("narracao-1.words.json", VO1_EM)
FALA_EM = round(vo1[-1]["end"] + 0.3, 3)
# fala real dela (trecho 0.3–5.75 s do vídeo original): "Eu já ajudei mais de dezessete mil mulheres no emagrecimento e você será a próxima."
FALA = [("Eu", .5, .6), ("já", .6, .7), ("ajudei", .7, 1.0), ("mais", 1.0, 1.2), ("de", 1.25, 1.3), ("dezessete", 1.4, 1.9),
        ("mil", 2.1, 2.2), ("mulheres", 2.2, 2.7), ("no", 3.0, 3.1), ("emagrecimento", 3.2, 4.2), ("e", 4.4, 4.5),
        ("você", 4.6, 4.9), ("será", 4.9, 5.1), ("a", 5.1, 5.15), ("próxima.", 5.2, 5.6)]
fala = [{"text": t, "start": round(s - .3 + FALA_EM, 3), "end": round(e - .3 + FALA_EM, 3)} for t, s, e in FALA]
VO2_EM = round(FALA_EM + 5.6, 3)
vo2 = palavras("narracao-2.words.json", VO2_EM)
TOTAL = round(vo2[-1]["end"] + 1.3, 2)
todas = vo1 + fala + vo2

def limpa(x):
    return re.sub(r"\W", "", x.lower())

def em(lista, palavra, n=0):  # início da n-ésima ocorrência da palavra
    achadas = [w["start"] for w in lista if limpa(w["text"]) == palavra]
    return achadas[n]

# ---------- legenda ----------
TROCA = {"dez": "10", "trinta": "30", "cinco": "5", "bélas": "BELLAS", "emágri.": "EMAGRY.", "dezessete": "17"}
DOURADO = {"TEM!", "TOMO.", "10", "QUILOS", "30", "DIAS.", "5", "17", "MIL", "WHATSAPP.", "VERSÃO", "BELLAS", "EMAGRY."} | set(CFG.get("dourado", []))
grupos, atual = [], []
for i, w in enumerate(todas):
    atual.append(w)
    prox = todas[i + 1] if i + 1 < len(todas) else None
    if len(atual) == 3 or w["text"][-1] in ".,?!…" or prox is None or prox["start"] - w["end"] >= 0.15:
        grupos.append(atual); atual = []
hg, jg = [], []
for n, g in enumerate(grupos):
    ini = max(g[0]["start"] - 0.05, 0.15)
    fim = grupos[n + 1][0]["start"] - 0.02 if n + 1 < len(grupos) and grupos[n + 1][0]["start"] - g[-1]["end"] < 0.6 else g[-1]["end"] + 0.25
    spans = []
    for w in g:
        txt = TROCA.get(w["text"].lower(), w["text"]).upper()
        cls = ' class="ouro"' if txt in DOURADO else ""
        spans.append(f"<span{cls}>{txt}</span>")
    hg.append(f'    <div id="leg-{n}" class="grupo">{" ".join(spans)}</div>')
    jg.append(f'  mostra("#leg-{n}", {ini:.3f}, {fim:.3f});')
open(os.path.join(AQUI, "compositions", "legendas.html"), "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .grupo {{ position: absolute; left: 0; width: 100%; top: 1150px; text-align: center; opacity: 0;
      font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 84px; line-height: 1.05;
      letter-spacing: -0.02em; color: #F7F0E1; -webkit-text-stroke: 12px #072A1F; paint-order: stroke fill; padding: 0 70px; }}
    .grupo .ouro {{ color: #D4AF5A; }}
  </style>
  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
{chr(10).join(hg)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    function mostra(sel, ini, fim) {{
      tl.fromTo(sel, {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.09, ease: "power4.out" }}, ini);
      tl.to(sel, {{ opacity: 0, duration: 0.06, ease: "power2.in" }}, fim - 0.06);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, fim);
    }}
{chr(10).join(jg)}
    window.__timelines["legendas"] = tl;
  </script>
</template>
""")

# ---------- cenas ----------
q1 = em(vo1, "tem", 0) - 0.12
q2 = em(vo1, "e", 0) - 0.1          # "E pra quem já toma outro?"
q3 = em(vo1, "tratamento") - 0.1
q4 = [w["start"] for w in vo1 if w["text"] == "E"][1] - 0.1   # "E eu tomo?"
q5 = em(vo1, "foi") - 0.08
CENAS = [("c-gancho", 0, q1), ("c-q1", q1, q2), ("c-q2", q2, q3), ("c-q3", q3, q4), ("c-q4", q4, q5),
         ("c-resultado", q5, FALA_EM), ("c-prova", FALA_EM, VO2_EM - 0.15), ("c-whatsapp", VO2_EM - 0.15, TOTAL)]
INI = {c: a for c, a, b in CENAS}
DUR = {c: round(b - a, 3) for c, a, b in CENAS}
L = lambda c, x: round(x - INI[c], 3)

BASE = """#root { position: absolute; inset: 0; overflow: hidden; background: #0D3B2C; }
    .cam { position: absolute; inset: 0; }
    .cam img, .cam video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    .mont { font-family: "Montserrat", sans-serif; font-weight: 900; letter-spacing: -0.02em; }
    .contorno { -webkit-text-stroke: 12px #072A1F; paint-order: stroke fill; }"""

def cena(cid, css, corpo, js):
    return f"""<template>
  <style>
    {BASE}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{corpo}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""

def video(id_, src, ini, dur, ms=0, som=False):
    audio = 'playsinline data-has-audio="true" data-volume="1"' if som else "muted playsinline"
    return f'      <video id="{id_}" class="clip" data-start="{ini:.3f}" data-duration="{dur:.3f}" data-media-start="{ms}" src="assets/{src}" {audio}></video>'

arq = {}

# gancho: três tipos (ritual, contagem para o Natal, salada)
c = "c-gancho"; d = DUR[c]; M1, M2, M3 = CFG["manchete"]; soco = L(c, em(vo1, CFG["soco"]))
CSS_TIT = f"""
    #g-scrim {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1000px;
      background: linear-gradient(180deg, rgba(7,42,31,.92) 0%, rgba(7,42,31,.7) 50%, rgba(7,42,31,0) 100%); }}
    #g-tit {{ position: absolute; left: 70px; top: 210px; width: 940px; color: #F7F0E1; }}
    #g-l1, #g-l3 {{ font-size: 88px; line-height: 1; display: block; }}
    #g-l2 {{ font-size: {CFG.get("tam_destaque", 160)}px; white-space: nowrap; line-height: .95; color: #D4AF5A; display: block; margin: 6px 0 10px; }}"""
TIT = f"""    <div id="g-tit" class="mont"><span id="g-l1">{M1}</span><span id="g-l2">{M2}</span><span id="g-l3">{M3}</span></div>"""
if CFG["gancho"] == "contagem":
    # só motion: os dias até o Natal caindo de 90 até o número da manchete
    alvo = int(re.sub(r"\D", "", M2))
    arq[c] = cena(c, CSS_TIT + """
    #g-num { position: absolute; left: 0; width: 1080px; top: 480px; text-align: center; color: #D4AF5A; font-size: 420px; line-height: 1; }
    #g-dias { position: absolute; left: 0; width: 1080px; top: 900px; text-align: center; color: #F7F0E1; font-size: 64px; letter-spacing: .14em; }
    #g-l2 { display: none; }""",
f"""    <div id="g-tudo" class="cam">
{TIT}
    <div id="g-num" class="mont">90</div>
    <div id="g-dias" class="mont">DIAS PRO NATAL</div>
    </div>""",
f"""    const n = {{ v: 90 }}, el = document.querySelector("#g-num");
    tl.fromTo("#g-tudo", {{ scale: 1 }}, {{ scale: 1.06, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo(n, {{ v: 90 }}, {{ v: {alvo}, duration: {max(soco - 0.2, 0.8):.3f}, ease: "power3.out", onUpdate: () => {{ el.textContent = Math.round(n.v); }} }}, 0.1);
    tl.fromTo("#g-num", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }}, {soco:.3f});""")
else:
    src, ms = {"ritual": ("mesa-pote.mp4", 4.2), "salada": ("pose.mp4", 0)}[CFG["gancho"]]
    arq[c] = cena(c, CSS_TIT, f"""    <div id="g-cam" class="cam">
{video("g-v", src, 0, d, ms)}
    </div>
    <div id="g-scrim"></div>
{TIT}""",
f"""    tl.fromTo("#g-cam", {{ scale: 1 }}, {{ scale: 1.08, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#g-l2", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "0 50%" }}, {soco:.3f});""")

# as quatro perguntas: pergunta no topo, carimbo da resposta no "Tem!"
PERG = [("c-q1", "PRA QUEM NUNCA TOMOU?", "TEM!", "parque-pote.mp4", 0.5, em(vo1, "tem", 1)),
        ("c-q2", "PRA QUEM JÁ TOMA OUTRO?", "TEM!", "mesa-pote.mp4", 0.2, em(vo1, "tem", 2)),
        ("c-q3", "TRATAMENTO DE 5 DIAS?", "TEM!", "parque-pote.mp4", 6.0, em(vo1, "tem", 3)),
        ("c-q4", "E EU, TOMO?", "TOMO.", "mesa-pote.mp4", 10.0, em(vo1, "tomo", 1))]
for cid, perg, resp, src, ms, t_resp in PERG:
    d = DUR[cid]; r = L(cid, t_resp)
    arq[cid] = cena(cid, """
    #p-box { position: absolute; left: 70px; top: 230px; width: 940px; padding: 34px 40px; background: #0D3B2C; border-left: 14px solid #D4AF5A; }
    #p-txt { color: #F7F0E1; font-size: 72px; line-height: 1.02; }
    #p-resp { position: absolute; left: 560px; top: 560px; padding: 8px 36px; border: 12px solid #D4AF5A; color: #D4AF5A; background: rgba(7,42,31,.9);
      font-size: 150px; line-height: 1; }""",
f"""    <div id="p-cam" class="cam">
{video("p-v", src, 0, d, ms)}
    </div>
    <div id="p-box"><div id="p-txt" class="mont">{perg}</div></div>
    <div id="p-resp" class="mont">{resp}</div>""",
f"""    tl.fromTo("#p-cam", {{ scale: 1.1 }}, {{ scale: 1, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#p-box", {{ x: -1000 }}, {{ x: 0, duration: 0.3, ease: "power4.out" }}, 0.03);
    tl.fromTo("#p-resp", {{ opacity: 0, scale: 1.8, rotation: -8 }}, {{ opacity: 1, scale: 1, rotation: -8, duration: 0.18, ease: "back.out(2)" }}, {r:.3f});""")

# resultado: −10 KG EM 30 DIAS
c = "c-resultado"; d = DUR[c]; dz = L(c, em(vo1, "dez"))
arq[c] = cena(c, """
    #r-num { position: absolute; left: 70px; top: 700px; color: #D4AF5A; font-size: 230px; line-height: .9; -webkit-text-stroke: 14px #072A1F; paint-order: stroke fill; }
    #r-lab { position: absolute; left: 80px; top: 920px; color: #F7F0E1; font-size: 70px; -webkit-text-stroke: 10px #072A1F; paint-order: stroke fill; }""",
f"""    <div id="r-cam" class="cam">
{video("r-v1", "virada.mp4", 0, min(1.7, d))}
{video("r-v2", "giro.mp4", 1.7, max(d - 1.7, 0.1), 0.3)}
    </div>
    <div id="r-num" class="mont">−0 KG</div>
    <div id="r-lab" class="mont">EM 30 DIAS</div>""",
f"""    const n = {{ v: 0 }}, el = document.querySelector("#r-num");
    tl.fromTo("#r-cam", {{ scale: 1.06 }}, {{ scale: 1, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#r-num", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power4.out" }}, {max(dz - 0.1, 0):.3f});
    tl.fromTo(n, {{ v: 0 }}, {{ v: 10, duration: 0.8, ease: "power2.out", onUpdate: () => {{ el.textContent = "−" + Math.round(n.v) + " KG"; }} }}, {dz:.3f});
    tl.fromTo("#r-lab", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {dz + 0.5:.3f});""")

# prova: a fala real dela + 17.000+
c = "c-prova"; d = DUR[c]; dzs = L(c, em(fala, "dezessete"))
arq[c] = cena(c, """
    #v-cont { position: absolute; left: 0; width: 1080px; top: 820px; text-align: center; }
    #v-num { display: block; color: #D4AF5A; font-size: 190px; line-height: .95; -webkit-text-stroke: 14px #072A1F; paint-order: stroke fill; }
    #v-lab { display: block; color: #F7F0E1; font-size: 56px; letter-spacing: .12em; -webkit-text-stroke: 9px #072A1F; paint-order: stroke fill; }""",
f"""    <div id="v-cam" class="cam">
{video("v-v", "fala-proxima.mp4", 0, min(d, 5.45), 0, som=True)}
    </div>
    <div id="v-cont" class="mont"><span id="v-num">0</span><span id="v-lab">MULHERES AJUDADAS</span></div>""",
f"""    const n = {{ v: 0 }}, el = document.querySelector("#v-num");
    tl.fromTo("#v-cam", {{ scale: 1 }}, {{ scale: 1.07, duration: 0.3, ease: "power3.out" }}, {dzs:.3f});
    tl.fromTo("#v-cont", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {dzs - 0.25:.3f});
    tl.fromTo(n, {{ v: 0 }}, {{ v: 17000, duration: 0.9, ease: "power2.out", onUpdate: () => {{ el.textContent = Math.round(n.v).toLocaleString("pt-BR") + (n.v > 16999 ? "+" : ""); }} }}, {dzs:.3f});""")

# WhatsApp (mesma cena do Corpo A)
c = "c-whatsapp"; d = DUR[c]
ver, toca, botao, whats = (L(c, em(vo2, x)) for x in ("versão", "toca", "botão", "whatsapp"))
arq[c] = cena(c, """
    #w-q { position: absolute; left: 70px; top: 250px; color: #F7F0E1; font-size: 60px; -webkit-text-stroke: 9px #072A1F; paint-order: stroke fill; }
    .ver { position: absolute; left: 70px; padding: 22px 40px; background: #0D3B2C; border-left: 12px solid #D4AF5A; color: #D4AF5A; font-size: 64px; line-height: 1; border-radius: 6px; }
    #w-v1 { top: 360px; } #w-v2 { top: 490px; } #w-v3 { top: 620px; }
    #w-btn { position: absolute; left: 90px; width: 900px; top: 370px; height: 150px; border-radius: 28px; background: #25D366; color: #fff;
      display: flex; align-items: center; justify-content: center; gap: 28px; font-size: 58px; box-shadow: 0 18px 40px rgba(0,0,0,.35); }
    #w-btn svg { width: 74px; height: 74px; }
    #w-toque { position: absolute; left: 760px; top: 415px; width: 60px; height: 60px; border-radius: 50%; border: 8px solid #fff; opacity: 0; }""",
f"""    <div id="w-cam" class="cam">
{video("w-va", "parque-pote.mp4", 0, 3, 1)}
{video("w-vb", "mesa-pote.mp4", 3, d - 3, 19.2)}
    </div>
    <div id="w-q" class="mont">QUAL É A SUA?</div>
    <div id="w-v1" class="ver mont">INICIANTE</div>
    <div id="w-v2" class="ver mont">JÁ TOMO OUTRO</div>
    <div id="w-v3" class="ver mont">TRATAMENTO 5 DIAS</div>
    <div id="w-btn" class="mont">
      <svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>
      <span>FALAR NO WHATSAPP</span>
    </div>
    <div id="w-toque"></div>""",
f"""    tl.fromTo("#w-cam", {{ scale: 1 }}, {{ scale: 1.12, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#w-q", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power4.out" }}, 0.1);
    ["#w-v1", "#w-v2", "#w-v3"].forEach((s, i) => tl.fromTo(s, {{ x: -900 }}, {{ x: 0, duration: 0.3, ease: "power4.out" }}, {ver - 0.35:.3f} + i * 0.22));
    tl.to(["#w-q", "#w-v1", "#w-v2", "#w-v3"], {{ x: -1000, duration: 0.25, ease: "power2.in", stagger: 0.04 }}, {toca - 0.2:.3f});
    tl.fromTo("#w-btn", {{ y: 600, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }}, {toca - 0.1:.3f});
    tl.fromTo("#w-toque", {{ opacity: 0.9, scale: 0.4 }}, {{ opacity: 0, scale: 3.2, duration: 0.5, ease: "power2.out", immediateRender: false }}, {botao:.3f});
    tl.to("#w-btn", {{ scale: 0.94, duration: 0.08, ease: "power2.out", yoyo: true, repeat: 1 }}, {botao:.3f});
    tl.to("#w-btn", {{ scale: 1.06, duration: 0.22, ease: "power2.inOut", yoyo: true, repeat: 3 }}, {whats + 0.3:.3f});""")

for cid, html in arq.items():
    open(os.path.join(AQUI, "compositions", f"{cid}.html"), "w").write(html)

# ---------- sons ----------
SONS = [("whoosh", "sfx_001", INI[c], .3, 0) for c, _, _ in CENAS[1:]]
SONS += [("impacto", "sfx_003", t + .02, .4, 0) for *_, t in PERG]
SONS += [("impacto", "sfx_003", em(vo1, CFG["soco"]), .4, 0),
         ("clique", "sfx_002", em(vo1, "dez") + .7, .5, .8),
         ("notificacao", "sfx_004", em(fala, "dezessete") + .9, .4, 0), ("notificacao", "sfx_004", em(vo2, "toca") + .25, .4, 0),
         ("clique", "sfx_002", em(vo2, "botão"), .6, .8)]
DUR_SOM = {"sfx_001": .6, "sfx_002": .15, "sfx_003": 1.6, "sfx_004": 1.0}
sons = [f'      <audio id="som-{i}-{n}" class="clip" data-start="{a:.3f}" data-duration="{DUR_SOM[s]}" data-media-start="{ms}" '
        f'data-volume="{v}" data-track-index="{12 + i}" src=".media/audio/sfx/{s}.mp3"></audio>'
        for i, (n, s, a, v, ms) in enumerate(SONS)]
hosts = [f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a:.3f}" '
         f'data-duration="{b - a:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>'
         for c, a, b in CENAS]
open(os.path.join(AQUI, "index.html"), "w").write(f"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0D3B2C; }}
      #root {{ position: relative; width: 1080px; height: 1920px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0"
        data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 5"></div>
      <audio id="narracao-1" class="clip" data-start="{VO1_EM}" data-volume="1" data-track-index="10" src="assets/narracao-1.mp3"></audio>
      <audio id="narracao-2" class="clip" data-start="{VO2_EM}" data-volume="1" data-track-index="11" src="assets/narracao-2.mp3"></audio>
{chr(10).join(sons)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("cenas:", [(c, round(a, 2), round(b, 2)) for c, a, b in CENAS], "total", TOTAL)
