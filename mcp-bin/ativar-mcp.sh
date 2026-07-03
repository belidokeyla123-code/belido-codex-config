#!/bin/bash
# ativar-mcp.sh — Ativa MCP sob demanda no OpenCode
# Uso: bash ativar-mcp.sh <nome_do_mcp>
# Ex:  bash ativar-mcp.sh dropbox
#      bash ativar-mcp.sh github
#      bash ativar-mcp.sh postgres
#
# Depois de executar, REINICIE a sessão do OpenCode.

set -euo pipefail
CONFIG="$HOME/.config/opencode/opencode.jsonc"
MCP_NAME="${1:-}"

if [ -z "$MCP_NAME" ]; then
    echo "Uso: bash ativar-mcp.sh <nome>"
    echo "Ex:  bash ativar-mcp.sh dropbox"
    echo ""
    echo "MCPs disponiveis: github, dropbox, outlook, postgres, vault-brain, vault-brain-public, docker-http, datajud-http, telegram-http, aws-http"
    exit 1
fi

if grep -q "\"$MCP_NAME\"" "$CONFIG"; then
    # Troca enabled false -> true (ou habilita se nao existir)
    sed -i "s/\"$MCP_NAME\": {\n.*\"enabled\": false/\"$MCP_NAME\": {\n      \"enabled\": true/" "$CONFIG" 2>/dev/null || \
    python3 -c "
import json, sys
with open('$CONFIG') as f:
    cfg = json.load(f)
if '$MCP_NAME' in cfg.get('mcp', {}):
    cfg['mcp']['$MCP_NAME']['enabled'] = True
    with open('$CONFIG', 'w') as f:
        json.dump(cfg, f, indent=2)
    print('[OK] MCP $MCP_NAME ativado. Reinicie a sessao do OpenCode.')
else:
    print('[ERRO] MCP $MCP_NAME nao encontrado no opencode.jsonc')
    sys.exit(1)
"
else
    echo "[ERRO] MCP '$MCP_NAME' nao encontrado no opencode.jsonc"
    exit 1
fi
