# Pesquisa de pautas

Objetivo: achar fatos e conversas recentes (últimos 30 dias) que a mulher que quer emagrecer está vivendo, e transformar em gancho para conteúdo ou criativo do Bellas Emagry.

## Fontes

1. **WebSearch em português (principal).** Notícias do Brasil. Busque com o mês e o ano atuais. Consultas sugeridas:
   - "Mounjaro" OR "caneta emagrecedora" reganho de peso [mês ano]
   - Anvisa canetas emagrecedoras [mês ano]
   - compulsão alimentar estudo [mês ano]
   - comer à noite estudo ansiedade [mês ano]
   - efeito sanfona pesquisa [mês ano]
   - menopausa peso fome estudo [mês ano]
   - dieta da moda viral [mês ano]
2. **/last30days (tendências e conversa da internet).** Antes, rode `bash scripts/garantir-last30days.sh` (na pasta da skill naturabelas): ele instala o last30days se faltar e atualiza para a última versão do GitHub (mvanhorn/last30days-skill), guardando a versão antiga em `~/.claude/skills-backup/`. Depois use a skill `last30days` quando quiser saber o que as pessoas estão FALANDO (Reddit, YouTube, TikTok, X). As fontes são mais em inglês. Bons temas: "GLP-1 food noise after stopping", "weight regain after Ozempic", "emotional eating at night". Traduza o achado para a realidade brasileira.
3. **Instagram dos concorrentes (opcional).** Com a chave `APIFY_INSTAGRAM_SCRAPER` (no `.env` do projeto, puxada do cofre), o ator `apify/instagram-scraper` traz os posts recentes de @vanessabaadnutri, @leteponto e @zanonmacedo para ver o que está viralizando. Dados antigos ficam em `pesquisa/instagram/`.

## Filtro: a pauta serve?

Uma pauta só entra se responder SIM a pelo menos uma pergunta:

- Mostra uma dor que ela sente (ansiedade, dieta que não segura, roupa, foto, data chegando)?
- Derruba uma objeção de compra ("já tentei de tudo", "é golpe", "não funciona pra mim")?
- Cria urgência real (data, tendência, estação)?

Descarte notícia que só fala de celebridade sem gancho, ou que levaria a falar do efeito da cápsula no corpo (proibido, ver `regras.md`).

## Ponte notícia → gancho

```
FATO: (o que aconteceu, com fonte)
O QUE ELA SENTE: (como isso aparece na vida dela)
ÂNGULO: história | prova | produto
VIRADA: "eu já passei por isso…"
GANCHO: (0-3 s)
```

Exemplo:

```
FATO: canetas emagrecedoras ficaram mais caras e difíceis de achar (notícia do mês).
O QUE ELA SENTE: "queria emagrecer pro fim de ano e não tenho como pagar caneta".
ÂNGULO: produto
VIRADA: "eu emagreci com um potinho, sem agulha."
GANCHO: "Não precisa de agulha pra chegar no Natal se sentindo linda."
(+ "decisão sobre medicação é sempre com o seu médico")
```

## Entrega da pesquisa

Lista de 3 a 5 pautas, cada uma com: título, fonte (link), ângulo, gancho e formato sugerido. Depois escreva as peças que a pessoa escolher.
