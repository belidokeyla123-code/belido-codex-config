#!/bin/bash
# setup-codex.sh — Configura Codex CLI como Agente Principal
# Keyla Belido | Advocacia Belido
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[AVISO]${NC} $1"; }
err() { echo -e "${RED}[ERRO]${NC} $1"; }

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Codex CLI — Agente Principal Keyla    ${NC}"
echo -e "${BLUE}========================================${NC}"

HOME_DIR="$HOME"
CODEX_DIR="$HOME_DIR/.codex"
SHARED_SKILLS_DIR="$HOME_DIR/.shared-skills"

info "Diretório home: $HOME_DIR"

# 1. Estrutura de diretórios
mkdir -p "$CODEX_DIR/skills"
mkdir -p "$SHARED_SKILLS_DIR"

# 2. Instalar dependências
pip3 install --break-system-packages dropbox 2>/dev/null || pip3 install dropbox 2>/dev/null

# 3. Copiar configs do bundle
if [ -f "$(pwd)/AGENTS.md" ]; then
  cp "$(pwd)/AGENTS.md" "$CODEX_DIR/AGENTS.md" 2>/dev/null || true
  log "AGENTS.md copiado"
fi

# 4. Skills compartilhadas
if [ -d "$(pwd)/skills" ]; then
  cp -r "$(pwd)/skills/"* "$SHARED_SKILLS_DIR/" 2>/dev/null || true
  log "Skills copiadas"
fi

echo -e "\n${GREEN}Codex CLI configurado como agente principal!${NC}"
