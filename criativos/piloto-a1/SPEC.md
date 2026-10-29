# SPEC: Piloto A1 (Bellas Emagry, antes e depois)

GOAL:    a mulher que quer emagrecer até o Natal se vê na Geicy de antes, acredita pelos 10 kg e pelas 17 mil e toca no botão do WhatsApp.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps (Reels e anúncio 9:16).
TIME:    28.6 s x 30 = 858 frames. Sem música (a trilha em alta entra no app do Instagram); sons em cada ação visível.
LOOK:    ground #0D3B2C (verde do pote), deep #072A1F; ink #F7F0E1 (creme); accent #D4AF5A (dourado do rótulo) só em números, no nome do produto e na palavra-chave da legenda; alerta #D9534A só nos carimbos "ANSIOSA", "GORDA" e no risco do "desisto".
         display Montserrat 900, 86 a 190 px, tracking -2%; marca Playfair Display 700, 150 px; legenda Montserrat 900, 84 px, caixa alta, contorno 12 px #072A1F.
         medium: fotografia real da Geicy (antes e depois, pote) com cartões gráficos chapados por cima; sombra 0 18 40 rgba(0,0,0,.35); sem grão.
OBJECTS: o tablet com a foto do antes; o pote verde e dourado; o botão do WhatsApp (verde #25D366, ícone de balão).
MOTION:  entrada power4.out 0.35 s; saída power2.in 0.2 s; punch-in de câmera power3.out 0.35 s; carimbo scale 1.6 → 1 em 0.18 s (back.out 2); números contam em 0.8 s power2.out.
SHOTS:
  s1 0–4.45    tablet com o antes, push 1.00→1.08; manchete "QUER PERDER / ATÉ 10 KG / ATÉ O NATAL?" já no frame 0; no "olha" (3.47) punch-in 1.45 na foto + whoosh.
  s2 4.45–8.65 foto do antes em tela cheia, push lento; etiqueta "ANTES · MANAUS"; carimbos ANSIOSA (6.74) e GORDA (7.83) com impacto.
  s3 8.65–12.2 só motion: "TODA SEMANA ERA ASSIM"; SEG "começo a dieta" (9.97), TER "aguento firme", QUA "desisto" (11.36) riscado.
  s4 12.2–14.3 Geicy aproxima o pote da câmera; "BELLAS / EMAGRY" entra no "Bélas" (13.27) com impacto.
  s5 14.3–18.5 ela hoje girando; contador −10 KG (14.66 → 15.4); corte para o giro em 16.3.
  s6 18.5–22.7 fala real dela ("Eu já ajudei mais de dezessete mil mulheres a emagrecer"); contador 17.000+ "MULHERES"; punch-in 1.06.
  s7 22.7–28.6 Geicy com o pote; "QUAL É A SUA?" + INICIANTE / JÁ TOMO / 5 DIAS; botão FALAR NO WHATSAPP sobe, pulsa e recebe o toque.
BANNED:  fundo escuro vazio com elementos pequenos no meio; brilho, neon, partículas; gradiente roxo ou azul; tudo centralizado; tudo entrando com fade ao mesmo tempo; texto que se move enquanto é lido; logo no canto; três cartões lado a lado; pílulas.
QA:      frames 0.0 (gancho legível), 3.8 (punch-in), 7.9 (dois carimbos), 11.9 (risco), 13.6 (marca), 15.5 (−10 KG), 20.8 (17.000+), 26.0 (botão); nenhum texto abaixo de 1330 px nem acima de 168 px.
