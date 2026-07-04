# AGENTS.md — Codex CLI Keyla Belido (Linux/Celular)

## 🇧🇷 REGRA ABSOLUTA
Raciocínio em português obrigatório.

## 📱 SOBRE ESTE DISPOSITIVO
Celular (Termux/Android) — Ollama local gratuito.

## 🚀 COMANDO MÁGICO: "se configura como agente principal"

QUANDO A KEYLA FALAR "SE CONFIGURA COMO AGENTE PRINCIPAL", EXECUTE ISSO TUDO:

### 🔧 PASSO A PASSO COMPLETO (fazer TUDO sozinho)

```bash
# 1. Criar pastas
mkdir -p /root/.codex /root/.config/opencode/mcp-bin /root/.config/opencode/instructions /root/.shared-skills /root/Dropbox

# 2. Credenciais Dropbox
if [ ! -f /root/.dropbox-keyla.env ]; then
    cat > /root/.dropbox-keyla.env << 'EOF'
DROPBOX_APP_KEY=64b5pp70tvtrlpp
DROPBOX_APP_SECRET=m73lfdkzqtoz7z5
DROPBOX_REFRESH_TOKEN=JneOhzcmbccAAAAAAAAAAWxRMNfgDy1pYFiGbI1VJ-KZ4jNfPfUwY8IHXhGPF7xu
EOF
    chmod 600 /root/.dropbox-keyla.env
fi

# 3. Baixar scripts MCP do GitHub
REPO="https://raw.githubusercontent.com/belidokeyla123-code/opencode-skills/main/codex/linux"
for f in mcp-dropbox-lite.py mcp-fallback.py dropbox-refresh.py; do
    curl -fsSL "$REPO/$f" -o "/root/.config/opencode/mcp-bin/$f"
done
chmod +x /root/.config/opencode/mcp-bin/*.py

# 4. Baixar config
curl -fsSL "$REPO/config.toml" -o /root/.codex/config.toml
curl -fsSL "$REPO/AGENTS.md" -o /root/.codex/AGENTS.md

# 5. Instalar Ollama (se não tiver)
if ! which ollama &>/dev/null; then
    echo "🔄 Instalando Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# 6. Baixar modelo gratuito
ollama pull qwen2.5-coder:1.5b

# 7. Testar Dropbox
python3 -c "
import os
os.environ['DROPBOX_APP_KEY'] = '64b5pp70tvtrlpp'
os.environ['DROPBOX_APP_SECRET'] = 'm73lfdkzqtoz7z5'
os.environ['DROPBOX_REFRESH_TOKEN'] = 'JneOhzcmbccAAAAAAAAAAWxRMNfgDy1pYFiGbI1VJ-KZ4jNfPfUwY8IHXhGPF7xu'
import sys
sys.path.insert(0, '/root/.config/opencode/mcp-bin')
exec(open('/root/.config/opencode/mcp-bin/mcp-dropbox-lite.py').read().split('def main')[0])
print('✅ Dropbox OK')
"

# 8. Copiar skills do GitHub
git clone https://github.com/belidokeyla123-code/opencode-skills.git /tmp/opencode-skills 2>/dev/null
cp -r /tmp/opencode-skills/skills/* /root/.shared-skills/ 2>/dev/null || true
```

### 📦 MCPs ATIVOS
- **filesystem**: ler/escrever arquivos
- **sequential-thinking**: raciocínio estruturado
- **dropbox-lite**: API Dropbox (refresh automático — nunca expira)
- **fallback-model**: troca de provedor quando o limite acabar

> MCPs pesados inativos. Se precisar: `codex mcp enable NOME`

### 🧠 Provedores
1. **Groq** — `groq/llama-3.1-8b-instant` (cloud, padrão)
2. **OpenRouter** — `openrouter/meta-llama/llama-3.1-8b-instruct`
3. **Cerebras** — `cerebras/llama-3.1-8b`
4. **Google Gemini** — `google/gemini-1.5-flash`
5. **Fireworks** — `fireworks/accounts/fireworks/models/llama-v3p1-8b-instruct`
6. **Ollama local** — `ollama/qwen2.5-coder:7b` (gratuito, offline)

### 🚀 Uso
- `codex` → modo cloud (Groq)
- `codex --oss` → modo local gratuito (Ollama)
- `CODEX_MODEL=groq/llama-3.1-8b-instant codex` → troca provedor na hora

### ⚡ Comportamento
- Seja autônomo: analise, diagnostique, execute e teste
- Use `fallback-model` quando o provedor estourar limite
- Consulte o Dropbox pra ler/escrever arquivos
