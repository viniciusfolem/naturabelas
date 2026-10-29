#!/usr/bin/env python3
"""Gera index.html e compositions/*.html de um criativo do Corpo A (antes e depois) a partir das marcações de tempo da narração.
Rode de novo sempre que trocar a narração (assets/narracao-*.words.json)."""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(AQUI, "compositions"), exist_ok=True)

# o roteiro de cada criativo (gancho, manchete, palavras-gatilho) fica em roteiro.json
CFG = json.load(open(os.path.join(AQUI, "roteiro.json")))
VO1_EM = 0.25

def palavras(arq, desloc):
    return [dict(w, start=round(w["start"] + desloc, 3), end=round(w["end"] + desloc, 3))
            for w in json.load(open(os.path.join(AQUI, "assets", arq)))]

# fala real dela (transcrição ElevenLabs do trecho 0.5–4.6 s do vídeo original)
FALA = [("Eu", .7, .8), ("já", .8, .9), ("ajudei", .9, 1.2), ("mais", 1.3, 1.5), ("de", 1.5, 1.6),
        ("dezessete", 1.7, 2.2), ("mil", 2.4, 2.5), ("mulheres", 2.6, 3.1), ("a", 3.5, 3.6), ("emagrecer.", 3.6, 4.3)]
vo1 = palavras("narracao-1.words.json", VO1_EM)
FALA_EM = round(vo1[-1]["end"] + 0.3, 3)          # a fala real entra logo depois da narração
VO2_EM = round(FALA_EM + 4.35, 3)
vo2 = palavras("narracao-2.words.json", VO2_EM)
TOTAL = round(vo2[-1]["end"] + 1.3, 2)
fala = [{"text": t, "start": round(s - .5 + FALA_EM, 3), "end": round(e - .5 + FALA_EM, 3)} for t, s, e in FALA]
todas = vo1 + fala + vo2

def t(lista, inicio):  # momento em que a palavra começa
    for w in lista:
        if re.sub(r"\W", "", w["text"].lower()).startswith(inicio):
            return w["start"]
    raise KeyError(inicio)

# como cada palavra aparece na legenda
TROCA = {"dez": "10", "trinta": "30", "bélas": "BELLAS", "emágri.": "EMAGRY.", "dezessete": "17"}
DOURADO = {"10", "QUILOS", "NATAL…", "MANAUS.", "BELLAS", "EMAGRY.", "17", "MIL", "WHATSAPP.", "VERSÃO", "ESPELHO.", "30", "DIAS."}
DOURADO |= set(CFG.get("dourado", []))

# ---------- legenda ----------
grupos, atual = [], []
for i, w in enumerate(todas):
    atual.append(w)
    prox = todas[i + 1] if i + 1 < len(todas) else None
    fim_frase = w["text"][-1] in ".,?!…"
    pausa = prox is None or prox["start"] - w["end"] >= 0.15
    if len(atual) == 3 or fim_frase or pausa:
        grupos.append(atual); atual = []

html_grupos, js_grupos = [], []
for n, g in enumerate(grupos):
    ini = max(g[0]["start"] - 0.05, 0.15)
    fim = grupos[n + 1][0]["start"] - 0.02 if n + 1 < len(grupos) and grupos[n + 1][0]["start"] - g[-1]["end"] < 0.6 else g[-1]["end"] + 0.25
    spans = []
    for w in g:
        txt = TROCA.get(w["text"].lower(), w["text"]).upper()
        cls = ' class="ouro"' if txt in DOURADO else ""
        spans.append(f"<span{cls}>{txt}</span>")
    html_grupos.append(f'    <div id="leg-{n}" class="grupo">{" ".join(spans)}</div>')
    js_grupos.append(f'  mostra("#leg-{n}", {ini:.3f}, {fim:.3f});')

legendas = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .grupo {{ position: absolute; left: 0; width: 100%; top: 1150px; text-align: center; opacity: 0;
      font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 84px; line-height: 1.05;
      letter-spacing: -0.02em; color: #F7F0E1; -webkit-text-stroke: 12px #072A1F; paint-order: stroke fill;
      padding: 0 70px; }}
    .grupo .ouro {{ color: #D4AF5A; }}
  </style>
  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
{chr(10).join(html_grupos)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    function mostra(sel, ini, fim) {{
      tl.fromTo(sel, {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.09, ease: "power4.out" }}, ini);
      tl.to(sel, {{ opacity: 0, duration: 0.06, ease: "power2.in" }}, fim - 0.06);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, fim);
    }}
{chr(10).join(js_grupos)}
    window.__timelines["legendas"] = tl;
  </script>
</template>
"""
open(os.path.join(AQUI, "compositions", "legendas.html"), "w").write(legendas)

# ---------- cenas ----------
CENAS = [  # id, início, fim
    ("s1-gancho", 0, [w for w in vo1 if w["text"] == CFG["inicio_corpo"]][0]["start"] - 0.15),  # onde o corpo começa
]
s2 = CENAS[0][2]
s3 = t(vo1, "começando") - 0.05
s4 = [w for w in vo1 if w["text"] == "Até"][0]["start"] - 0.1  # "Até eu conhecer"
s5 = t(vo1, "foram") - 0.04
s6 = FALA_EM
s7 = VO2_EM - 0.15
CENAS += [("s2-antes", s2, s3), ("s3-semana", s3, s4), ("s4-produto", s4, s5),
          ("s5-virada", s5, s6), ("s6-prova", s6, s7), ("s7-whatsapp", s7, TOTAL)]
INI = {c[0]: c[1] for c in CENAS}

def L(cena, abs_t):  # tempo local da cena
    return round(abs_t - INI[cena], 3)

BASE_CSS = """#root { position: absolute; inset: 0; overflow: hidden; background: #0D3B2C; }
    .cam { position: absolute; inset: 0; }
    .cam img, .cam video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    .mont { font-family: "Montserrat", sans-serif; font-weight: 900; letter-spacing: -0.02em; }"""

def cena(cid, dur, css, corpo, js):
    return f"""<template>
  <style>
    {BASE_CSS}
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

def dur(cid):
    for c, a, b in CENAS:
        if c == cid:
            return round(b - a, 3)

arquivos = {}

# s1: gancho no tablet
d = dur("s1-gancho"); olha = L("s1-gancho", t(vo1, CFG["soco"])); dez = L("s1-gancho", t(vo1, CFG["pulso"]))
M1, M2, M3 = CFG["manchete"]
arquivos["s1-gancho"] = cena("s1-gancho", d, f"""
    #s1-cam {{ transform-origin: 50% 58%; }}
    #s1-scrim {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1100px;
      background: linear-gradient(180deg, rgba(7,42,31,.92) 0%, rgba(7,42,31,.75) 45%, rgba(7,42,31,0) 100%); }}
    #s1-tit {{ position: absolute; left: 70px; top: 210px; width: 940px; color: #F7F0E1; }}
    #s1-l1, #s1-l3 {{ font-size: 92px; line-height: 1; display: block; }}
    #s1-l2 {{ font-size: {CFG.get("tam_destaque", 166)}px; white-space: nowrap; line-height: .95; color: #D4AF5A; display: block; margin: 6px 0 10px; transform-origin: 0 50%; }}""",
f"""    <div id="s1-cam" class="cam">
      <video id="s1-v" class="clip" data-start="0" data-duration="{d:.3f}" src="assets/tablet-antes.mp4" muted playsinline></video>
    </div>
    <div id="s1-scrim"></div>
    <div id="s1-tit" class="mont">
      <span id="s1-l1">{M1}</span>
      <span id="s1-l2">{M2}</span>
      <span id="s1-l3">{M3}</span>
    </div>""",
f"""    tl.fromTo("#s1-cam", {{ scale: 1 }}, {{ scale: 1.08, duration: {olha:.3f}, ease: "none" }}, 0);
    tl.fromTo("#s1-l2", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }}, {dez:.3f});
    tl.to("#s1-cam", {{ scale: 1.45, duration: 0.35, ease: "power3.out" }}, {olha:.3f});
    tl.to("#s1-tit", {{ y: -60, opacity: 0, duration: 0.2, ease: "power2.in" }}, {olha:.3f});
    tl.to("#s1-scrim", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {olha:.3f});""")

# s2: foto do antes com carimbos
c = "s2-antes"; d = dur(c); ans = L(c, t(vo1, "ansiosa")); gor = L(c, t(vo1, "gorda"))
arquivos[c] = cena(c, d, """
    #s2-tag { position: absolute; left: 0; top: 960px; padding: 22px 40px 22px 70px; background: #0D3B2C; color: #F7F0E1; font-size: 54px; }
    #s2-tag b { color: #D4AF5A; }
    .carimbo { position: absolute; padding: 10px 34px; border: 9px solid #B8322A; color: #B8322A; background: rgba(247,240,225,.92);
      font-size: 104px; line-height: 1; }
    #s2-c1 { left: 90px; top: 290px; }
    #s2-c2 { left: 430px; top: 520px; }""",
"""    <div id="s2-cam" class="cam"><div id="s2-in" class="cam"><img src="assets/foto-antes.jpg" alt="A Geicy antes" /></div></div>
    <div id="s2-tag" class="mont">ANTES <b>·</b> MANAUS</div>
    <div id="s2-c1" class="carimbo mont">ANSIOSA</div>
    <div id="s2-c2" class="carimbo mont">GORDA</div>""",
f"""    tl.fromTo("#s2-cam", {{ scale: 1.02, x: 30, y: 40 }}, {{ scale: 1.2, x: -30, y: -60, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#s2-in", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.16, ease: "power3.out" }}, {ans:.3f});
    tl.fromTo("#s2-in", {{ scale: 1.08 }}, {{ scale: 1.16, duration: 0.16, ease: "power3.out", immediateRender: false }}, {gor:.3f});
    tl.fromTo("#s2-tag", {{ x: -700 }}, {{ x: 0, duration: 0.35, ease: "power4.out" }}, 0.12);
    tl.fromTo("#s2-c1", {{ opacity: 0, scale: 1.6, rotation: -7 }}, {{ opacity: 1, scale: 1, rotation: -7, duration: 0.18, ease: "back.out(2)" }}, {ans:.3f});
    tl.fromTo("#s2-c2", {{ opacity: 0, scale: 1.6, rotation: 5 }}, {{ opacity: 1, scale: 1, rotation: 5, duration: 0.18, ease: "back.out(2)" }}, {gor:.3f});""")

# s3: a semana (só motion)
c = "s3-semana"; d = dur(c); qua = L(c, t(vo1, "quarta"))
seg = L(c, t(vo1, "dieta")); ter = L(c, t(vo1, "segunda"))  # um dia novo a cada ~1 s, sem trecho parado
arquivos[c] = cena(c, d, """
    #s3-tit { position: absolute; left: 70px; top: 250px; width: 940px; color: #F7F0E1; font-size: 64px; line-height: 1.05; }
    .dia { position: absolute; left: 70px; width: 940px; height: 210px; display: flex; align-items: center; gap: 44px;
      background: #072A1F; border-left: 14px solid #D4AF5A; padding-left: 44px; }
    .dia .nome { font-size: 112px; color: #D4AF5A; width: 270px; }
    .dia .txt { font-size: 60px; color: #F7F0E1; position: relative; }
    #s3-d1 { top: 420px; } #s3-d2 { top: 650px; } #s3-d3 { top: 880px; border-left-color: #B8322A; }
    #s3-d3 .nome { color: #B8322A; }
    #s3-risco { position: absolute; left: -12px; right: -12px; top: 50%; height: 12px; margin-top: -6px; background: #B8322A; transform-origin: 0 50%; }""",
"""    <div id="s3-all" class="cam">
    <div id="s3-tit" class="mont">TODA SEMANA<br />ERA ASSIM:</div>
    <div id="s3-d1" class="dia mont"><span class="nome">SEG</span><span class="txt">começo a dieta</span></div>
    <div id="s3-d2" class="dia mont"><span class="nome">TER</span><span class="txt">aguento firme</span></div>
    <div id="s3-d3" class="dia mont"><span class="nome">QUA</span><span class="txt">desisto<i id="s3-risco"></i></span></div>
    </div>""",
f"""    tl.fromTo("#s3-all", {{ scale: 1 }}, {{ scale: 1.07, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#s3-tit", {{ x: -80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power4.out" }}, 0.05);
    tl.fromTo("#s3-d1", {{ x: 1100 }}, {{ x: 0, duration: 0.35, ease: "power4.out" }}, {seg - 0.1:.3f});
    tl.fromTo("#s3-d2", {{ x: 1100 }}, {{ x: 0, duration: 0.35, ease: "power4.out" }}, {ter - 0.1:.3f});
    tl.fromTo("#s3-d3", {{ x: 1100 }}, {{ x: 0, duration: 0.35, ease: "power4.out" }}, {qua - 0.1:.3f});
    tl.fromTo("#s3-risco", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.22, ease: "power3.out" }}, {qua + 0.3:.3f});""")

# s4: produto
c = "s4-produto"; d = dur(c); bel = L(c, t(vo1, "bélas"))
arquivos[c] = cena(c, d, """
    #s4-marca { position: absolute; left: 0; width: 1080px; top: 230px; text-align: center; }
    #s4-m1 { display: block; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 46px; letter-spacing: .5em; color: #F7F0E1;
      -webkit-text-stroke: 8px #072A1F; paint-order: stroke fill; }
    #s4-m2 { display: block; font-family: "Playfair Display", serif; font-weight: 700; font-size: 168px; line-height: 1; color: #D4AF5A;
      -webkit-text-stroke: 10px #072A1F; paint-order: stroke fill; }""",
f"""    <div id="s4-cam" class="cam">
      <video id="s4-v" class="clip" data-start="0" data-duration="{d:.3f}" data-media-start="16.4" src="assets/mesa-pote.mp4" muted playsinline></video>
    </div>
    <div id="s4-marca"><span id="s4-m1">BELLAS</span><span id="s4-m2">EMAGRY</span></div>""",
f"""    tl.fromTo("#s4-cam", {{ scale: 1 }}, {{ scale: 1.1, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#s4-m1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {bel - 0.05:.3f});
    tl.fromTo("#s4-m2", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(1.8)" }}, {bel + 0.1:.3f});""")

# s5: virada + −10 KG
c = "s5-virada"; d = dur(c); dz = L(c, [w for w in vo1 if w["text"] == "dez"][-1]["start"])  # o "dez" do corpo
corte = 2.4  # o contador fica até o fim de "em trinta dias"
corte_v = 1.7  # troca de vídeo antes da mão de quem filmava entrar no quadro
arquivos[c] = cena(c, d, """
    #s5-num { position: absolute; left: 70px; top: 700px; color: #D4AF5A; font-size: 230px; line-height: .9;
      -webkit-text-stroke: 14px #072A1F; paint-order: stroke fill; }
    #s5-lab { position: absolute; left: 80px; top: 920px; color: #F7F0E1; font-size: 70px;
      -webkit-text-stroke: 10px #072A1F; paint-order: stroke fill; }""",
f"""    <div id="s5-cam" class="cam">
      <video id="s5-v1" class="clip" data-start="0" data-duration="{corte_v}" data-media-start="0" src="assets/virada.mp4" muted playsinline></video>
      <video id="s5-v2" class="clip" data-start="{corte_v}" data-duration="{d - corte_v:.3f}" data-media-start="0.3" src="assets/giro.mp4" muted playsinline></video>
    </div>
    <div id="s5-num" class="mont">−0 KG</div>
    <div id="s5-lab" class="mont">EM 30 DIAS</div>""",
f"""    const n = {{ v: 0 }}, el = document.querySelector("#s5-num");
    tl.fromTo("#s5-cam", {{ scale: 1.06 }}, {{ scale: 1 }}, 0);
    tl.fromTo("#s5-num", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power4.out" }}, {dz - 0.1:.3f});
    tl.fromTo(n, {{ v: 0 }}, {{ v: 10, duration: 0.8, ease: "power2.out", onUpdate: () => {{ el.textContent = "−" + Math.round(n.v) + " KG"; }} }}, {dz:.3f});
    tl.fromTo("#s5-lab", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {dz + 0.5:.3f});
    tl.to(["#s5-num", "#s5-lab"], {{ opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }}, {corte - 0.2:.3f});""")

# s6: fala real + 17.000+
c = "s6-prova"; d = dur(c); dzs = L(c, t(fala, "dezessete"))
arquivos[c] = cena(c, d, """
    #s6-cam { transform-origin: 50% 30%; }
    #s6-cont { position: absolute; left: 0; width: 1080px; top: 820px; text-align: center; }
    #s6-num { display: block; color: #D4AF5A; font-size: 190px; line-height: .95; -webkit-text-stroke: 14px #072A1F; paint-order: stroke fill; }
    #s6-lab { display: block; color: #F7F0E1; font-size: 56px; letter-spacing: .12em; -webkit-text-stroke: 9px #072A1F; paint-order: stroke fill; }""",
f"""    <div id="s6-cam" class="cam">
      <video id="s6-v" class="clip" data-start="0" data-duration="4.1" src="assets/fala-17mil.mp4" playsinline data-has-audio="true" data-volume="1"></video>
    </div>
    <div id="s6-cont" class="mont"><span id="s6-num">0</span><span id="s6-lab">MULHERES AJUDADAS</span></div>""",
f"""    const n = {{ v: 0 }}, el = document.querySelector("#s6-num");
    tl.fromTo("#s6-cam", {{ scale: 1 }}, {{ scale: 1.07, duration: 0.3, ease: "power3.out" }}, {dzs:.3f});
    tl.fromTo("#s6-cont", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }}, {dzs - 0.25:.3f});
    tl.fromTo(n, {{ v: 0 }}, {{ v: 17000, duration: 0.9, ease: "power2.out", onUpdate: () => {{ el.textContent = Math.round(n.v).toLocaleString("pt-BR") + (n.v > 16999 ? "+" : ""); }} }}, {dzs:.3f});""")

# s7: versões + WhatsApp
c = "s7-whatsapp"; d = dur(c); ver = L(c, t(vo2, "versão")); toca = L(c, t(vo2, "toca")); botao = L(c, t(vo2, "botão"))
whats = L(c, t(vo2, "whatsapp"))
arquivos[c] = cena(c, d, """
    #s7-cam img { object-position: 60% 50%; }
    #s7-q { position: absolute; left: 70px; top: 250px; color: #F7F0E1; font-size: 60px; -webkit-text-stroke: 9px #072A1F; paint-order: stroke fill; }
    .ver { position: absolute; left: 70px; padding: 22px 40px; background: #0D3B2C; border-left: 12px solid #D4AF5A; color: #D4AF5A;
      font-size: 64px; line-height: 1; border-radius: 6px; }
    #s7-v1 { top: 360px; } #s7-v2 { top: 490px; } #s7-v3 { top: 620px; }
    #s7-btn { position: absolute; left: 90px; width: 900px; top: 370px; height: 150px; border-radius: 28px; background: #25D366; color: #fff;
      display: flex; align-items: center; justify-content: center; gap: 28px; font-size: 58px; box-shadow: 0 18px 40px rgba(0,0,0,.35); }
    #s7-btn svg { width: 74px; height: 74px; }
    #s7-toque { position: absolute; left: 760px; top: 415px; width: 60px; height: 60px; border-radius: 50%; border: 8px solid #fff; opacity: 0; }""",
f"""    <div id="s7-cam" class="cam">
      <video id="s7-va" class="clip" data-start="0" data-duration="3" data-media-start="1" src="assets/parque-pote.mp4" muted playsinline></video>
      <video id="s7-vb" class="clip" data-start="3" data-duration="{d - 3:.3f}" data-media-start="19.2" src="assets/mesa-pote.mp4" muted playsinline></video>
    </div>
    <div id="s7-q" class="mont">QUAL É A SUA?</div>
    <div id="s7-v1" class="ver mont">INICIANTE</div>
    <div id="s7-v2" class="ver mont">JÁ TOMO OUTRO</div>
    <div id="s7-v3" class="ver mont">TRATAMENTO 5 DIAS</div>
    <div id="s7-btn" class="mont">
      <svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>
      <span>FALAR NO WHATSAPP</span>
    </div>
    <div id="s7-toque"></div>""",
f"""    tl.fromTo("#s7-cam", {{ scale: 1 }}, {{ scale: 1.12, duration: {d:.3f}, ease: "none" }}, 0);
    tl.fromTo("#s7-q", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power4.out" }}, 0.1);
    ["#s7-v1", "#s7-v2", "#s7-v3"].forEach((s, i) => tl.fromTo(s, {{ x: -900 }}, {{ x: 0, duration: 0.3, ease: "power4.out" }}, {ver - 0.35:.3f} + i * 0.22));
    tl.to(["#s7-q", "#s7-v1", "#s7-v2", "#s7-v3"], {{ x: -1000, duration: 0.25, ease: "power2.in", stagger: 0.04 }}, {toca - 0.2:.3f});
    tl.fromTo("#s7-btn", {{ y: 600, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }}, {toca - 0.1:.3f});
    tl.fromTo("#s7-toque", {{ opacity: 0.9, scale: 0.4 }}, {{ opacity: 0, scale: 3.2, duration: 0.5, ease: "power2.out", immediateRender: false }}, {botao:.3f});
    tl.to("#s7-btn", {{ scale: 0.94, duration: 0.08, ease: "power2.out", yoyo: true, repeat: 1 }}, {botao:.3f});
    tl.to("#s7-btn", {{ scale: 1.06, duration: 0.22, ease: "power2.inOut", yoyo: true, repeat: 3 }}, {whats + 0.3:.3f});""")

for cid, html in arquivos.items():
    open(os.path.join(AQUI, "compositions", f"{cid}.html"), "w").write(html)

# ---------- sons ----------
corte_s5 = INI["s5-virada"] + 2.4
SONS = [("whoosh", "sfx_001", t(vo1, "olha"), .45, 0), ("whoosh", "sfx_001", INI["s2-antes"], .3, 0),
        ("whoosh", "sfx_001", INI["s3-semana"], .3, 0), ("whoosh", "sfx_001", INI["s4-produto"], .3, 0),
        ("whoosh", "sfx_001", INI["s5-virada"], .3, 0), ("whoosh", "sfx_001", INI["s7-whatsapp"], .3, 0),
        ("impacto", "sfx_003", t(vo1, "ansiosa"), .35, 0), ("impacto", "sfx_003", t(vo1, "gorda"), .35, 0),
        ("impacto", "sfx_003", t(vo1, "quarta") + .3, .35, 0), ("impacto", "sfx_003", t(vo1, "bélas") + .1, .45, 0),
        ("clique", "sfx_002", t(vo1, "segunda") - .1, .5, .8), ("clique", "sfx_002", t(vo1, "quarta") - .1, .5, .8),
        ("clique", "sfx_002", [w for w in vo1 if w["text"] == "dez"][-1]["start"] + .7, .5, .8),
        ("notificacao", "sfx_004", t(fala, "dezessete") + .9, .4, 0), ("notificacao", "sfx_004", t(vo2, "toca") + .25, .4, 0),
        ("clique", "sfx_002", t(vo2, "botão"), .6, .8)]
sons_html = []
for i, (nome, sid, ini, vol, ms) in enumerate(SONS):
    durs = {"sfx_001": .6, "sfx_002": .15, "sfx_003": 1.6, "sfx_004": 1.0}[sid]
    sons_html.append(f'      <audio id="som-{i}-{nome}" class="clip" data-start="{ini:.3f}" data-duration="{durs}" data-media-start="{ms}" '
                     f'data-volume="{vol}" data-track-index="{12 + i % 3}" src=".media/audio/sfx/{sid}.mp3"></audio>')

hosts = []
for i, (cid, a, b) in enumerate(CENAS):
    hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{a:.3f}" '
                 f'data-duration="{b - a:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" '
                 f'style="z-index: 1"></div>')

index = f"""<!doctype html>
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
{chr(10).join(sons_html)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(os.path.join(AQUI, "index.html"), "w").write(index)
print("cenas:", [(c, round(a, 2), round(b, 2)) for c, a, b in CENAS])
print("grupos de legenda:", len(grupos))
