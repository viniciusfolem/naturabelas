#!/usr/bin/env python3
"""Gera index.html e compositions/*.html de um criativo do Corpo B (prova social: depoimentos de clientes).
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
TROCA = {"dez": "10", "trinta": "30", "oito": "8", "dezessete": "17", "bélas": "BELLAS", "emágri.": "EMAGRY.", "dezessete": "17"}
DOURADO = {"8", "QUILOS.", "ACREDITAR.", "GRATA", "DEMAIS.", "10", "QUILOS", "30", "DIAS.", "5", "17", "MIL", "WHATSAPP.", "VERSÃO", "BELLAS", "EMAGRY."} | set(CFG.get("dourado", []))
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

ZAP_SVG = '<svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>'

# ---------- cenas ----------
corpo = [w for w in vo1 if w["text"] == "Foi"][0]["start"]          # "Foi perfeito, perdi oito quilos."
pos = [w for w in vo1 if w["start"] >= corpo]                          # palavras do corpo (o gancho fica de fora)
lista = em(pos, "cada") - 0.1
produto = em(pos, "mudou") - 0.35
result = [w["start"] for w in pos if w["text"] == "E"][0] - 0.1     # "E eu mesma perdi..."
CENAS = [("b-gancho", 0, corpo - 0.15), ("b-zap", corpo - 0.15, lista), ("b-lista", lista, produto),
         ("b-produto", produto, result), ("c-resultado", result, FALA_EM),
         ("c-prova", FALA_EM, VO2_EM - 0.15), ("c-whatsapp", VO2_EM - 0.15, TOTAL)]
INI = {c: a for c, a, b in CENAS}
DUR = {c: round(b - a, 3) for c, a, b in CENAS}
L = lambda c, x: round(x - INI[c], 3)

BASE = """#root { position: absolute; inset: 0; overflow: hidden; background: #0D3B2C; }
    .cam { position: absolute; inset: 0; }
    .cam img, .cam video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    .mont { font-family: "Montserrat", sans-serif; font-weight: 900; letter-spacing: -0.02em; }"""

def cena(cid, css, corpo_html, js):
    return f"""<template>
  <style>
    {BASE}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{corpo_html}
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
M1, M2, M3 = CFG["manchete"]
CSS_TIT = f"""
    #g-tit {{ position: absolute; left: 70px; top: 210px; width: 940px; color: #F7F0E1; }}
    #g-l1, #g-l3 {{ font-size: 88px; line-height: 1; display: block; }}
    #g-l2 {{ font-size: {CFG.get("tam_destaque", 160)}px; white-space: nowrap; line-height: .95; color: #D4AF5A; display: block; margin: 6px 0 10px; }}"""
TIT = f"""    <div id="g-tit" class="mont"><span id="g-l1">{M1}</span><span id="g-l2">{M2}</span><span id="g-l3">{M3}</span></div>"""

# gancho
c = "b-gancho"; d = DUR[c]; soco = L(c, em(vo1, CFG["soco"]))
if CFG["gancho"] == "contador":
    arq[c] = cena(c, CSS_TIT + """
    #g-l2 { font-size: 230px; }
    #g-tit { top: 300px; }""",
f"""    <div id="g-tudo" class="cam">
{TIT}
    </div>""",
f"""    const n = {{ v: 0 }}, el = document.querySelector("#g-l2");
    tl.fromTo("#g-tudo", {{ scale: 1 }}, {{ scale: 1.06, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo(n, {{ v: 9000 }}, {{ v: 17000, duration: {max(soco - 0.2, 0.8):.3f}, ease: "power3.out", onUpdate: () => {{ el.textContent = Math.round(n.v).toLocaleString("pt-BR"); }} }}, 0.05);
    tl.fromTo("#g-l3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {soco:.3f});""")
else:
    src, ms = {"zap": ("parque-pote.mp4", 2.0), "frase": ("pose.mp4", 0)}[CFG["gancho"]]
    arq[c] = cena(c, CSS_TIT + """
    #g-scrim { position: absolute; left: 0; top: 0; width: 1080px; height: 1000px;
      background: linear-gradient(180deg, rgba(7,42,31,.92) 0%, rgba(7,42,31,.7) 50%, rgba(7,42,31,0) 100%); }
    #g-noti { position: absolute; left: 60px; top: 760px; width: 960px; padding: 28px 34px; border-radius: 30px; background: rgba(247,240,225,.97);
      box-shadow: 0 18px 40px rgba(0,0,0,.35); display: flex; gap: 26px; align-items: center; }
    #g-noti .ic { width: 96px; height: 96px; border-radius: 22px; background: #25D366; flex: none; display: flex; align-items: center; justify-content: center; }
    #g-noti .ic svg { width: 62px; height: 62px; }
    #g-noti b { display: block; font: 800 40px "Montserrat", sans-serif; color: #072A1F; }
    #g-noti span { display: block; font: 600 40px "Montserrat", sans-serif; color: #2b3b35; }""",
f"""    <div id="g-cam" class="cam">
{video("g-v", src, 0, d, ms)}
    </div>
    <div id="g-scrim"></div>
{TIT}
    <div id="g-noti"><div class="ic">{ZAP_SVG}</div><div><b>Cliente Bellas</b><span>Foi perfeito, perdi 8 kilos</span></div></div>""",
f"""    tl.fromTo("#g-cam", {{ scale: 1 }}, {{ scale: 1.08, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#g-l2", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "0 50%" }}, {soco:.3f});
    tl.fromTo("#g-noti", {{ y: -900, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.3)" }}, {min(soco + 0.2, d - 0.6):.3f});""")

# depoimentos: conversa de WhatsApp com as mensagens reais das clientes, entrando quando são lidas
c = "b-zap"; d = DUR[c]
MSGS = [("Olá boa tarde", None), ("Foi perfeito perdi 8 kilos", em(pos, "foi")),
        ("Não dá nem pra acreditar nisso", em(pos, "não")),
        ("Alta estima lá em cima, vcs me proporcionaram isso tudo. Sou grata, muito mesmo", em(pos, "autoestima"))]
bolhas, js_b = [], []
for i, (txt, t0) in enumerate(MSGS):
    bolhas.append(f'        <div id="z-m{i}" class="msg">{txt}<i>{["17:35", "17:36", "12:03", "09:37"][i]}</i></div>')
    quando = 0.05 if t0 is None else L(c, t0) - 0.1
    js_b.append(f'    tl.fromTo("#z-m{i}", {{ opacity: 0, y: 40, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.25, ease: "back.out(1.6)" }}, {max(quando, 0.05):.3f});')
arq[c] = cena(c, """
    #z-fundo { position: absolute; inset: 0; background: #0B141A; }
    #z-topo { position: absolute; left: 0; top: 0; width: 1080px; height: 330px; background: #1F2C34; display: flex; align-items: flex-end; padding: 0 60px 40px; gap: 28px; }
    #z-av { width: 110px; height: 110px; border-radius: 50%; background: #D4AF5A; display: flex; align-items: center; justify-content: center; font: 900 50px "Montserrat", sans-serif; color: #072A1F; }
    #z-nome { color: #E9EDEF; font: 800 50px "Montserrat", sans-serif; }
    #z-nome small { display: block; color: #8696A0; font: 600 34px "Montserrat", sans-serif; }
    #z-nome small b { display: inline-block; font-weight: 900; color: #25D366; }
    #z-lista { position: absolute; left: 60px; top: 370px; width: 960px; display: flex; flex-direction: column; gap: 18px; align-items: flex-start; }
    .msg { position: relative; max-width: 900px; padding: 20px 30px 44px; border-radius: 0 26px 26px 26px; background: #202C33; color: #E9EDEF;
      font: 600 44px/1.18 "Montserrat", sans-serif; }
    .msg i { position: absolute; right: 26px; bottom: 12px; font: 500 28px "Montserrat", sans-serif; color: #8696A0; font-style: normal; }
    #z-selo { position: absolute; left: 60px; top: 1010px; padding: 14px 26px; background: #D4AF5A; color: #072A1F; font-size: 38px; border-radius: 8px; }""",
f"""    <div id="z-fundo"></div>
    <div id="z-cam" class="cam">
      <div id="z-topo"><div id="z-av">C</div><div id="z-nome">Cliente Bellas<small>digitando<b id="z-d1">.</b><b id="z-d2">.</b><b id="z-d3">.</b></small></div></div>
      <div id="z-lista">
{chr(10).join(bolhas)}
      </div>
    </div>""",
f"""    tl.fromTo("#z-cam", {{ scale: 1, y: 0 }}, {{ scale: 1.12, y: -40, duration: {d:.3f}, ease: "none" }}, 0);
    ["#z-d1", "#z-d2", "#z-d3"].forEach((s, i) => tl.fromTo(s, {{ y: 0 }}, {{ y: -9, duration: 0.26, ease: "sine.inOut", yoyo: true, repeat: {int(d / 0.26) + 2} }}, 0.1 + i * 0.13));
{chr(10).join(js_b)}""")

# a lista do que elas já tinham tentado, riscada palavra por palavra
c = "b-lista"; d = DUR[c]
ITENS = [("DIETA", em(pos, "dieta")), ("CHÁ", em(pos, "chá")), ("JEJUM", em(pos, "jejum"))]
itens_html = "\n".join(f'      <div id="l-i{i}" class="item mont">{n}<i id="l-r{i}" class="risco"></i></div>' for i, (n, _) in enumerate(ITENS))
js_l = "\n".join(f'    tl.fromTo("#l-i{i}", {{ x: 900 }}, {{ x: 0, duration: 0.25, ease: "power4.out" }}, {max(L(c, t0) - 0.25, 0.05):.3f});\n'
                  f'    tl.fromTo("#l-r{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.2, ease: "power3.out" }}, {L(c, t0) + 0.15:.3f});' for i, (_, t0) in enumerate(ITENS))
igual = L(c, em(pos, "igual"))
arq[c] = cena(c, """
    #l-tit { position: absolute; left: 70px; top: 240px; width: 940px; color: #F7F0E1; font-size: 66px; line-height: 1.05; }
    #l-tit span { display: block; }
    #l-t2 { color: #D4AF5A; }
    #l-col { position: absolute; left: 70px; top: 440px; display: flex; flex-direction: column; gap: 30px; }
    .item { position: relative; font-size: 150px; line-height: 1; color: #F7F0E1; }
    .risco { position: absolute; left: -10px; right: -10px; top: 50%; height: 16px; margin-top: -8px; background: #B8322A; transform-origin: 0 50%; }
    #l-voce { position: absolute; left: 70px; top: 1000px; color: #D4AF5A; font-size: 90px; }""",
f"""    <div id="l-tudo" class="cam">
      <div id="l-tit" class="mont"><span id="l-t1">ELAS JÁ TINHAM</span><span id="l-t2">TENTADO DE TUDO:</span></div>
      <div id="l-col">
{itens_html}
      </div>
      <div id="l-voce" class="mont">IGUAL VOCÊ.</div>
    </div>""",
f"""    tl.fromTo("#l-tudo", {{ scale: 1, y: 0 }}, {{ scale: 1.1, y: -30, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#l-t1", {{ x: -80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power4.out" }}, 0.05);
    tl.fromTo("#l-t2", {{ x: -80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power4.out" }}, {max(L(c, em(pos, "tentado")) - 0.1, 0.4):.3f});
{js_l}
    tl.fromTo("#l-voce", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {igual:.3f});""")

# o produto
c = "b-produto"; d = DUR[c]; bel = L(c, em(pos, "bélas"))
arq[c] = cena(c, """
    #pr-marca { position: absolute; left: 0; width: 1080px; top: 230px; text-align: center; }
    #pr-m1 { display: block; font: 700 46px "Montserrat", sans-serif; letter-spacing: .5em; color: #F7F0E1; -webkit-text-stroke: 8px #072A1F; paint-order: stroke fill; }
    #pr-m2 { display: block; font: 700 168px/1 "Playfair Display", serif; color: #D4AF5A; -webkit-text-stroke: 10px #072A1F; paint-order: stroke fill; }""",
f"""    <div id="pr-cam" class="cam">
{video("pr-v", "mesa-pote.mp4", 0, d, 16.4)}
    </div>
    <div id="pr-marca"><span id="pr-m1">BELLAS</span><span id="pr-m2">EMAGRY</span></div>""",
f"""    tl.fromTo("#pr-cam", {{ scale: 1 }}, {{ scale: 1.1, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#pr-m1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {max(bel - 0.05, 0.05):.3f});
    tl.fromTo("#pr-m2", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(1.8)" }}, {bel + 0.1:.3f});""")

# resultado: −10 KG EM 30 DIAS
c = "c-resultado"; d = DUR[c]; dz = L(c, em(pos, "dez"))
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
SONS += [("notificacao", "sfx_004", t, .35, 0) for _, t in MSGS if t is not None]
SONS += [("impacto", "sfx_003", t + .15, .35, 0) for _, t in ITENS]
SONS += [("impacto", "sfx_003", em(vo1, CFG["soco"]), .4, 0), ("impacto", "sfx_003", em(pos, "bélas") + .1, .45, 0),
         ("clique", "sfx_002", em(pos, "dez") + .7, .5, .8),
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
