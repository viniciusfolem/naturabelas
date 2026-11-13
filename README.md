# Natura Bellas

Criativos, copy e conteúdo da Geicy Maralves (@geicymaralves, Instituto Natura Bellas, Manaus) para vender o emagrecedor encapsulado **Bellas Emagry Premium**.

## Pastas

| Pasta | O que tem |
|---|---|
| `.claude/skills/naturabelas/` | Skill do Claude Code: copy de anúncio, criativos, roteiros, WhatsApp e conteúdo orgânico na voz da Geicy |
| `criativos/` | Os 9 criativos de Natal 2026 no HyperFrames (3 corpos × 3 ganchos). Os vídeos `.mp4` ficam fora do git |
| `conteudo/` | Plano dos criativos, roteiros de narração e semanas de conteúdo |
| `pesquisa/` | Posts e transcrições do Instagram (concorrentes e da Geicy) |
| `estrategia/` | Estratégia antiga do método, cancelada (só histórico) |

## Geicy: como instalar no seu Claude (site ou app)

1. Baixe o arquivo **[naturabelas.zip](https://github.com/viniciusfolem/naturabelas/raw/main/naturabelas.zip)**. Não descompacte.
2. No Claude, clique no seu nome (canto de baixo, à esquerda) > **Configurações** > **Capacidades** e ligue **Criar e editar arquivos**.
3. Vá em **Personalizar** > **Skills** > **+** > **Enviar skill** e escolha o `naturabelas.zip`. Confira se a chave da skill ficou ligada.
4. Abra uma conversa nova e escreva **"oi"**. Ela pergunta o que você quer fazer: roteiro, voz ou edição de vídeo.

Para atualizar: apague a skill antiga e envie o zip novo. Precisa de plano pago do Claude.

## Usar a skill em outro computador (Claude Code)

```bash
git clone https://github.com/viniciusfolem/naturabelas.git
cp -R naturabelas/.claude/skills/naturabelas ~/.claude/skills/
```

Dentro deste repositório a skill já carrega sozinha no Claude Code.

## Chaves

O `.env` não vai para o git. Puxe do cofre: `ELEVENLABS_API_KEY` (narração e transcrição) e `APIFY_INSTAGRAM_SCRAPER` (pesquisa do Instagram).
