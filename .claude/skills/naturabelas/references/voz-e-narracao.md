# Voz e narração

## Antes de gerar, pergunte

1. "A voz vai ser a sua gravada ou a de IA?" A voz dela vende mais e evita erro de pronúncia. A IA é para testar rápido.
2. Se for IA: "Você já tem conta na ElevenLabs? Qual plano?" No plano grátis **não pode usar em anúncio** (ver `ferramentas-e-links.md`).
3. "Quer ouvir antes um exemplo?" Se sim, gere só o gancho (economiza crédito).

## Preparar o texto para a IA

- Escreva **"Bélas Emágri"** no lugar de "Bellas Emagry" (senão a IA fala "Bella Zé Magre").
- Números por extenso: "dezessete mil", "dez quilos", "quarenta por cento".
- Reticências (…) para pausa. Uma frase por linha.
- Entregue o texto num bloco pronto para copiar.

## No site da ElevenLabs (Claude do site ou do app)

1. Abra https://elevenlabs.io/app/speech-synthesis/text-to-speech
2. Cole o texto na caixa.
3. Escolha a voz (canto inferior esquerdo). Use uma voz **nativa em português do Brasil**, feminina, calorosa. A voz usada nos criativos de Natal foi a **Bella**.
4. Modelo: **Multilingual v2** (ou o mais novo multilíngue). Teste os dois se o sotaque ficar estranho.
5. Clique em **Generate**, ouça e, se gostar, clique no **download** (canto inferior direito) para baixar o MP3.
6. Se uma palavra sair errada, troque a grafia (ex.: "Emágri") e gere só aquele trecho.

Créditos acabaram: ver `ferramentas-e-links.md` (upgrade ou Pay As You Go).

## Clonar a voz dela (recomendado)

A partir do plano Starter. Assim a IA fala com a voz da própria Geicy.
1. Grave 1 a 2 minutos falando natural, sozinha, sem eco nem barulho (pode ser no celular, num quarto com roupas e cortinas).
2. No site: **Voices** > **+** > **Instant Voice Clone**.
3. Envie a gravação, dê o nome "Geicy" e confirme que a voz é dela.
4. Clique em **Save voice**. Depois é só escolher "Geicy" na hora de gerar.

## No computador (Claude Code)

Com a chave no `.env` (ver `instalar-no-computador.md`), o Claude gera sozinho:

```bash
python3 .claude/skills/naturabelas/scripts/narrar.py VOICE_ID "texto" criativos/<id>/assets/narracao-1
python3 .claude/skills/naturabelas/scripts/tempos.py criativos/<id>/assets/narracao-1.align.json > criativos/<id>/assets/narracao-1.words.json
```

- Voz Bella: `hpp4J3VqNfWAUOO0d1Us`. Se ela clonar a voz, pegue o ID em **My Voices** > a voz > **ID**.
- Erro 401: a chave está errada ou sem permissão de Text to Speech. Erro 402 ou "quota": acabou o crédito.

## A voz gravada dela

Peça para ela gravar no celular, em lugar silencioso, um áudio por roteiro, devagar e com pausa nas reticências. Para usar a voz dela com legenda palavra por palavra no computador, transcreva com a ElevenLabs Speech to Text (`scribe_v1`, com tempos por palavra) e gere o `words.json` no mesmo formato.
