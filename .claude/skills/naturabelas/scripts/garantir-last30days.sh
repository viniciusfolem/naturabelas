#!/usr/bin/env bash
# Garante que a skill last30days (github.com/mvanhorn/last30days-skill) está
# instalada e na última versão. Instala se faltar, atualiza se estiver velha.
# Uso: bash garantir-last30days.sh
set -u

REPO="mvanhorn/last30days-skill"
RAW="https://raw.githubusercontent.com/$REPO/main/skills/last30days/SKILL.md"
BACKUP_DIR="$HOME/.claude/skills-backup"

versao() { grep -m1 '^version:' 2>/dev/null | sed 's/[^0-9.]//g'; }

# 1. Instalado como plugin do marketplace: o próprio Claude Code atualiza.
if ls -d "$HOME"/.claude/plugins/cache/last30days-skill/last30days/* >/dev/null 2>&1; then
  claude plugin update last30days@last30days-skill >/dev/null 2>&1 || true
  echo "last30days: ok (plugin do marketplace, atualizado pelo Claude Code)"
  exit 0
fi

# 2. Instalado como skill: compara a versão local com a do GitHub.
LOCAL=""
for d in "$HOME/.claude/skills/last30days" "$HOME/.agents/skills/last30days"; do
  if [ -f "$d/SKILL.md" ]; then LOCAL="$d"; break; fi
done

ATUAL=""
[ -n "$LOCAL" ] && ATUAL=$(versao < "$LOCAL/SKILL.md")
REMOTA=$(curl -fsSL --max-time 20 "$RAW" 2>/dev/null | versao)

if [ -n "$ATUAL" ] && [ -z "$REMOTA" ]; then
  echo "last30days: v$ATUAL instalada (sem internet para checar atualização, seguindo assim)"
  exit 0
fi
if [ -n "$ATUAL" ] && [ "$(printf '%s\n%s\n' "$ATUAL" "$REMOTA" | sort -V | tail -1)" = "$ATUAL" ]; then
  echo "last30days: ok (v$ATUAL, a mais recente)"
  exit 0
fi

# 3. Falta ou está desatualizada: guarda a cópia antiga fora da pasta de skills e instala a nova.
if [ -n "$LOCAL" ] && [ ! -L "$LOCAL" ]; then
  mkdir -p "$BACKUP_DIR"
  BK="$BACKUP_DIR/last30days-v${ATUAL:-desconhecida}-$(date +%Y%m%d%H%M%S)"
  mv "$LOCAL" "$BK"
fi

if [ -n "$ATUAL" ]; then
  echo "last30days: atualizando v$ATUAL -> v${REMOTA:-mais recente}..."
else
  echo "last30days: não encontrada, instalando v${REMOTA:-mais recente}..."
fi
if npx -y skills add "$REPO" -g -a claude-code -s last30days -y >/dev/null 2>&1 \
   && [ -f "$HOME/.claude/skills/last30days/SKILL.md" ]; then
  echo "last30days: ok (v$(versao < "$HOME/.claude/skills/last30days/SKILL.md")). Reinicie a sessão do Claude Code para carregar a versão nova."
  exit 0
fi

# Falhou: devolve a versão antiga.
if [ -n "${BK:-}" ] && [ ! -e "$LOCAL" ]; then mv "$BK" "$LOCAL"; fi
echo "last30days: falha ao instalar/atualizar. Rode manualmente: npx skills add $REPO -g -a claude-code -s last30days"
exit 1
