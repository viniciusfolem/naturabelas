# Instalar no computador (para o Claude editar o vídeo sozinho)

Só é preciso para **gerar a voz direto da ElevenLabs** e **editar com motion no HyperFrames** (legenda palavra por palavra, cenas animadas, como nos criativos de Natal). Para roteiro e texto, o Claude do site ou do app já basta.

Antes de mandar qualquer passo, pergunte: **"Seu computador é Mac ou Windows?"** Mande **um passo de cada vez** e espere ela dizer "foi" antes do próximo. Se der erro, peça um print da tela.

## O que vai ser instalado (explique assim)

| Programa | Para que serve, em 5 palavras |
|---|---|
| App Claude (aba **Code**) | o Claude mexe nos arquivos |
| Node.js | motor que roda o HyperFrames |
| ffmpeg | programa que mexe no vídeo |
| Python | roda o script da voz |
| Skills do HyperFrames | ensinam o Claude a editar |
| A pasta `naturabelas` | a skill, os scripts e os criativos |
| Chave da ElevenLabs no `.env` | liga o Claude à voz |

## Passo a passo (Mac)

1. **App Claude:** baixe em https://claude.ai/download, instale e entre com a conta dela. Abra a aba **Code**. Precisa de plano pago (Pro ou Max).
2. **Terminal:** aperte **Cmd + Espaço**, digite **Terminal** e dê Enter. Explique: "é uma janela onde a gente cola comandos; cola, aperta Enter e espera".
3. **Homebrew** (o instalador de programas do Mac): cole o comando que aparece em https://brew.sh. Ele pede a **senha do computador**: ela digita e não aparece nada na tela, é normal. No fim, se ele mostrar "Next steps", rode as 2 linhas que ele indicar.
4. **Node, ffmpeg e Python:**
   ```
   brew install node ffmpeg python
   ```
5. **Conferir:** `node -v` (tem que ser 22 ou mais), `ffmpeg -version` e `python3 --version`. Se os três responderem com um número, deu certo.
6. **Skills do HyperFrames:**
   ```
   npx skills add heygen-com/hyperframes --all
   ```
   Se perguntar algo, aperte Enter para aceitar o padrão.
7. **A pasta do projeto:** baixe https://github.com/viniciusfolem/naturabelas/archive/refs/heads/main.zip, descompacte e mova a pasta para **Documentos** com o nome `naturabelas`. No app Claude, aba **Code**, abra essa pasta.
8. **Chave da ElevenLabs:** pegue a chave (ver `ferramentas-e-links.md`). Na pasta `naturabelas`, crie um arquivo chamado `.env` com uma linha só:
   ```
   ELEVENLABS_API_KEY=cole_a_chave_aqui
   ```
   Peça para ela fazer isso sozinha. **Nunca peça a chave no chat.** Se ela colar a chave no chat mesmo assim, avise para apagar essa chave na ElevenLabs e criar outra.
9. **Teste:** peça "gera a voz de teste: Oi, eu sou a Geicy". Se sair um `.mp3`, está tudo pronto.

## Passo a passo (Windows)

1. App Claude: https://claude.ai/download (aba **Code**).
2. Node.js: https://nodejs.org, botão **LTS**, depois avançar até o fim.
3. Python: https://www.python.org/downloads. **Marque "Add Python to PATH"** antes de instalar.
4. ffmpeg: abra o **PowerShell** (menu Iniciar, digite PowerShell) e cole `winget install ffmpeg`.
5. Feche e abra o PowerShell de novo. Depois siga do passo 5 do Mac em diante. No Windows, o comando do Python é `python`, e não `python3`.

## Problemas que já aconteceram (não repetir)

- **Vídeo travado, verde ou que não abre no WhatsApp:** clipe do iPhone em HDR. Converter para SDR antes e renderizar com `--sdr` (ver `criativos-video.md`).
- **Cena toda verde:** faltou imagem em `assets/`. Conferir os arquivos antes de renderizar.
- **A IA fala "Bella Zé Magre":** no texto da narração, escrever "Bélas Emágri".
- **ElevenLabs dá erro 401 ou 402:** a chave está errada ou acabou o crédito. Mande o link da assinatura (`ferramentas-e-links.md`).
- **Plano grátis da ElevenLabs:** não usa vozes da Biblioteca pela API e não pode ir para anúncio. O mínimo é o Starter.
