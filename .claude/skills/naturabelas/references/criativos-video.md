# Criativos em vídeo

## Os 9 criativos prontos (Natal 2026)

Ficam em `criativos/<id>/` no repositório e os vídeos finais em `~/Downloads/bellas-videos-narrar/` (lista em `CRIATIVOS.md`).

| Pasta | Arquivo final | Gancho |
|---|---|---|
| piloto-a1 | A1-10kg-ate-o-natal | "Se você quer perder até 10 quilos até o Natal… olha essa foto." |
| a2 | A2-essa-mulher-sou-eu | "Essa mulher sou eu. E eu tinha vergonha dessa foto." |
| a3 | A3-casamento-acabando | "Meu casamento tava acabando. E eu culpava o espelho." |
| b1 | B1-17-mil-mulheres | "17 mil mulheres não podem estar erradas." |
| b2 | B2-chegou-no-whatsapp | "Olha o que chegou no meu WhatsApp hoje." |
| b3 | B3-elas-tambem-duvidavam | "Elas também achavam que não ia funcionar." |
| c1 | C1-meu-ritual | "Esse é o meu ritual pra emagrecer. Leva menos de um minuto." |
| c2 | C2-dias-pro-natal | "Faltam menos de 60 dias pro Natal. Ainda dá tempo?" |
| c3 | C3-sem-salada | "Você não precisa viver de salada pra emagrecer." |

Todos fecham com a fala real dela ("17 mil mulheres") e com "Quer saber qual versão é a sua? Toca no botão e fala comigo no WhatsApp."

## O que prende atenção

- **Legenda palavra por palavra** o tempo todo (Montserrat 900, caixa alta, contorno verde-escuro), palavras-chave em dourado ("10 quilos", "Natal", "17 mil"). A maioria assiste sem som.
- **Movimento a cada 1,5 a 2 s:** corte, punch-in, elemento entrando. Nenhuma foto parada. Foto vira vídeo com zoom lento.
- **Números que contam:** −10 KG, 17.000+, dias para o Natal.
- **Cenas só de motion** entre os takes dela: calendário SEG/TER/QUA riscado, lista DIETA/CHÁ/JEJUM riscada, carimbos ANSIOSA/GORDA, cartões das versões, botão do WhatsApp com toque.
- **Depoimentos como bolhas de WhatsApp** refeitas a partir dos prints, com "digitando…" animado.
- **Sons:** whoosh nos cortes, clique, impacto nos carimbos, notificação nas bolhas. Música entra no app do Instagram (trilha em alta).

## Roteiro para a Geicy gravar

Formato de entrega: tabela Tempo | Tela | Narração. Marque **[VOZ DELA]** onde já existe fala gravada e ela deve ficar em silêncio. Dica para ela: gravar no celular, em lugar silencioso, um áudio por criativo, devagar e com pausa nas reticências.

## Como editar no HyperFrames

Cada pasta tem:

- `roteiro.json`: id, narração, manchete (3 linhas), gancho e palavra do "soco".
- `gerar.py`: monta `index.html` e `compositions/*.html` a partir dos tempos da narração. Os corpos A, B e C têm cada um o seu `gerar.py`.
- `assets/`: `narracao-1.mp3` + `narracao-1.words.json`, `narracao-2` (o fecho do WhatsApp) e os clipes.

Para mudar texto ou trocar a voz:

```bash
cd criativos/<id>
# 1. nova narração (IA provisória) ou a voz da Geicy transcrita
python3 ../../.claude/skills/naturabelas/scripts/narrar.py hpp4J3VqNfWAUOO0d1Us "texto" assets/narracao-1
python3 ../../.claude/skills/naturabelas/scripts/tempos.py assets/narracao-1.align.json > assets/narracao-1.words.json
# 2. remontar e conferir
python3 gerar.py
npx hyperframes check
npx hyperframes snapshot --at 0.2,5,15,25
# 3. renderizar SEMPRE em SDR
npx hyperframes render --sdr -o renders/<nome>.mp4
```

Quando a Geicy mandar a voz dela, transcreva com a ElevenLabs speech-to-text (`scribe_v1`, com tempos por palavra) e gere o `words.json` no mesmo formato.

Na narração por IA, escreva "Bélas Emágri" para a pronúncia sair certa. Na legenda, o `gerar.py` mostra "BELLAS EMAGRY".

## Regras técnicas que não mudam

- **Clipes do iPhone vêm em HDR (HLG, bt2020).** Converter para SDR antes de pôr em `assets/`, senão o render sai em HEVC 10 bits, fica verde e trava no celular e no WhatsApp:

  ```bash
  bash -c 'ffmpeg -init_hw_device videotoolbox=vt -filter_hw_device vt -i IN.MOV \
    -vf "format=p010le,hwupload,scale_vt=color_matrix=bt709:color_primaries=bt709:color_transfer=bt709,hwdownload,format=p010le,format=yuv420p" \
    -c:v libx264 -crf 18 -color_primaries bt709 -color_trc bt709 -colorspace bt709 OUT.mp4'
  ```

- **Render sempre com `--sdr`.**
- **Conferir antes de entregar:** `ffprobe` (h264, yuv420p, bt709) e quadro travado:

  ```bash
  ffmpeg -i video.mp4 -vf freezedetect=n=0.003:d=0.5 -an -f null - 2>&1 | grep freeze_start
  ```

  Nada pode aparecer.
- 9:16, 1080 × 1920, 30 fps. Texto entre 168 px do topo e 1330 px (fora da área dos botões do Reels).
- Vídeos `.mp4` de `assets/` e as pastas `renders/`, `.media/` e `.hyperframes/` não vão para o git.

## Sem HyperFrames (corte rápido)

Para cortes limpos sem motion, para narrar por cima no CapCut ou no Instagram: corte com ffmpeg em 9:16, sem o som de fundo original, e entregue o roteiro de narração ao lado.
