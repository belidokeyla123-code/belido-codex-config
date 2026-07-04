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
REPO="https://raw.githubusercontent.com/belidokeyla123-code/opencode-skills/main"
for f in codex/linux/mcp-dropbox-lite.py codex/linux/mcp-fallback.py codex/linux/dropbox-refresh.py; do
    curl -fsSL "$REPO/$f" -o "/root/.config/opencode/mcp-bin/$(basename $f)"
done
chmod +x /root/.config/opencode/mcp-bin/*.py

# 4. Baixar config do GitHub
curl -fsSL "$REPO/codex/linux/config.toml" -o /root/.codex/config.toml
curl -fsSL "$REPO/codex/linux/AGENTS.md" -o /root/.codex/AGENTS.md

# Alternativa: copiar do Dropbox (se já tiver acesso)
if [ -f /root/.dropbox-keyla.env ]; then
    python3 -c "
import dropbox, os
os.environ['DROPBOX_APP_KEY'] = '64b5pp70tvtrlpp'
os.environ['DROPBOX_APP_SECRET'] = 'm73lfdkzqtoz7z5'
os.environ['DROPBOX_REFRESH_TOKEN'] = 'JneOhzcmbccAAAAAAAAAAWxRMNfgDy1pYFiGbI1VJ-KZ4jNfPfUwY8IHXhGPF7xu'
dbx = dropbox.Dropbox(os.environ['DROPBOX_APP_KEY'], os.environ['DROPBOX_APP_SECRET'], oauth2_refresh_token=os.environ['DROPBOX_REFRESH_TOKEN'])
for f in ['config.toml', 'AGENTS.md']:
    md, res = dbx.files_download(f'/Public/IA/JAMES/opencode_config/codex-linux/{f}')
    with open(f'/root/.codex/{f}', 'wb') as out:
        out.write(res.content)
print('✅ Configs copiadas do Dropbox')
"
fi

# 5. Instalar Ollama (se não tiver)
if ! which ollama &>/dev/null; then
    echo "🔄 Instalando Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# 6. Baixar modelo gratuito
ollama pull qwen2.5-coder:1.5b

# 7. Testar Dropbox
source /root/.dropbox-keyla.env 2>/dev/null
python3 -c "
import os
os.environ['DROPBOX_APP_KEY'] = '$(grep DROPBOX_APP_KEY /root/.dropbox-keyla.env 2>/dev/null | cut -d= -f2)'
os.environ['DROPBOX_APP_SECRET'] = '$(grep DROPBOX_APP_SECRET /root/.dropbox-keyla.env 2>/dev/null | cut -d= -f2)'
os.environ['DROPBOX_REFRESH_TOKEN'] = '$(grep DROPBOX_REFRESH_TOKEN /root/.dropbox-keyla.env 2>/dev/null | cut -d= -f2)'
import dropbox
dbx = dropbox.Dropbox(os.environ['DROPBOX_APP_KEY'], os.environ['DROPBOX_APP_SECRET'], oauth2_refresh_token=os.environ['DROPBOX_REFRESH_TOKEN'])
dbx.files_list_folder('')
print('✅ Dropbox OK')
"

# 8. Copiar skills do GitHub
git clone https://github.com/belidokeyla123-code/opencode-skills.git /tmp/opencode-skills 2>/dev/null
cp -r /tmp/opencode-skills/.system/* /root/.shared-skills/.system/ 2>/dev/null || true
for skill_dir in /tmp/opencode-skills/agente-* /tmp/opencode-skills/build-* /tmp/opencode-skills/chatgpt-* /tmp/opencode-skills/circleci-* /tmp/opencode-skills/clean-* /tmp/opencode-skills/cloudflare-* /tmp/opencode-skills/code-* /tmp/opencode-skills/coderabbit-* /tmp/opencode-skills/data-* /tmp/opencode-skills/database-* /tmp/opencode-skills/deep-* /tmp/opencode-skills/deploy-* /tmp/opencode-skills/doc-* /tmp/opencode-skills/dropbox-* /tmp/opencode-skills/ec2-* /tmp/opencode-skills/expo-* /tmp/opencode-skills/figma-* /tmp/opencode-skills/game-* /tmp/opencode-skills/github-* /tmp/opencode-skills/hugging-* /tmp/opencode-skills/hyperframes-* /tmp/opencode-skills/james-* /tmp/opencode-skills/keyla-* /tmp/opencode-skills/knowledge-* /tmp/opencode-skills/mem-* /tmp/opencode-skills/memory-* /tmp/opencode-skills/multi-* /tmp/opencode-skills/neon-* /tmp/opencode-skills/netlify-* /tmp/opencode-skills/openclaw-* /tmp/opencode-skills/outlook-* /tmp/opencode-skills/pentest-* /tmp/opencode-skills/performance-* /tmp/opencode-skills/postgres-* /tmp/opencode-skills/prompt-* /tmp/opencode-skills/projeto-* /tmp/opencode-skills/quem-* /tmp/opencode-skills/refactoring-* /tmp/opencode-skills/remotion-* /tmp/opencode-skills/render-* /tmp/opencode-skills/robo-* /tmp/opencode-skills/security-* /tmp/opencode-skills/sentry-* /tmp/opencode-skills/smart-* /tmp/opencode-skills/stripe-* /tmp/opencode-skills/supabase-* /tmp/opencode-skills/superpowers-* /tmp/opencode-skills/system-* /tmp/opencode-skills/telegram-* /tmp/opencode-skills/temporal-* /tmp/opencode-skills/test-* /tmp/opencode-skills/timeline-* /tmp/opencode-skills/trading /tmp/opencode-skills/trafego-* /tmp/opencode-skills/vercel-* /tmp/opencode-skills/version-* /tmp/opencode-skills/whatsapp-* /tmp/opencode-skills/agencia-* /tmp/opencode-skills/analise-* /tmp/opencode-skills/api-* /tmp/opencode-skills/arbitragem-* /tmp/opencode-skills/arquivos-* /tmp/opencode-skills/astrea /tmp/opencode-skills/auto-* /tmp/opencode-skills/autonomous-* /tmp/opencode-skills/brlaw-* /tmp/opencode-skills/browser-* /tmp/opencode-skills/cfo-* /tmp/opencode-skills/claude-* /tmp/opencode-skills/cold-* /tmp/opencode-skills/compliance-* /tmp/opencode-skills/computer-* /tmp/opencode-skills/contabilidade-* /tmp/opencode-skills/content-* /tmp/opencode-skills/contrato-* /tmp/opencode-skills/contratos-* /tmp/opencode-skills/criativos-* /tmp/opencode-skills/devops-* /tmp/opencode-skills/direito-* /tmp/opencode-skills/do /tmp/opencode-skills/execucao-* /tmp/opencode-skills/financeiro /tmp/opencode-skills/flightclaw /tmp/opencode-skills/fluent-* /tmp/opencode-skills/framework-* /tmp/opencode-skills/fullstack-* /tmp/opencode-skills/funil-* /tmp/opencode-skills/gestao-* /tmp/opencode-skills/graphic-* /tmp/opencode-skills/growth-* /tmp/opencode-skills/inovacao-* /tmp/opencode-skills/integration-* /tmp/opencode-skills/juridico-* /tmp/opencode-skills/lead-* /tmp/opencode-skills/lean-* /tmp/opencode-skills/legal-* /tmp/opencode-skills/marketing-* /tmp/opencode-skills/monitor-* /tmp/opencode-skills/next-* /tmp/opencode-skills/nuxt-* /tmp/opencode-skills/patrimonial-* /tmp/opencode-skills/peticao-* /tmp/opencode-skills/peticoes /tmp/opencode-skills/php-* /tmp/opencode-skills/planejamento-* /tmp/opencode-skills/plugin-* /tmp/opencode-skills/power-* /tmp/opencode-skills/previdencia-* /tmp/opencode-skills/privacy-* /tmp/opencode-skills/projudi-* /tmp/opencode-skills/projuris-* /tmp/opencode-skills/prontuario-* /tmp/opencode-skills/propriedade-* /tmp/opencode-skills/protocolo-* /tmp/opencode-skills/psi-* /tmp/opencode-skills/raspberry-* /tmp/opencode-skills/react-* /tmp/opencode-skills/recursos-* /tmp/opencode-skills/revisao-* /tmp/opencode-skills/rust-* /tmp/opencode-skills/saas-* /tmp/opencode-skills/seo-* /tmp/opencode-skills/servicos-* /tmp/opencode-skills/solid-* /tmp/opencode-skills/sql-* /tmp/opencode-skills/story-* /tmp/opencode-skills/tdd-* /tmp/opencode-skills/tese-* /tmp/opencode-skills/trabalhista-* /tmp/opencode-skills/ui-* /tmp/opencode-skills/video-* /tmp/opencode-skills/vue-* /tmp/opencode-skills/web-* /tmp/opencode-skills/wordpress-*; do
    [ -d "$skill_dir" ] && cp -r "$skill_dir" /root/.shared-skills/ 2>/dev/null || true
done
rm -rf /tmp/opencode-skills
```

### 📦 MCPs ATIVOS (leves)
- **filesystem**: ler/escrever arquivos
- **sequential-thinking**: raciocínio estruturado
- **dropbox-lite**: API Dropbox (refresh automático — nunca expira)
- **fallback-model**: troca de provedor quando o limite acabar

> MCPs pesados inativos. Se precisar: fale "ativa MCP [NOME]" ou rode manualmente.

### 🧠 Provedores
1. **Groq** — `groq/llama-3.1-8b-instant` (cloud, padrão)
2. **OpenRouter** — `openrouter/meta-llama/llama-3.1-8b-instruct`
3. **Cerebras** — `cerebras/llama-3.1-8b`
4. **Google Gemini** — `google/gemini-1.5-flash`
5. **Fireworks** — `fireworks/accounts/fireworks/models/llama-v3p1-8b-instruct`
6. **Ollama local** — `ollama/qwen2.5-coder:1.5b` (gratuito, offline)

### 🚀 Uso
- `codex` → modo cloud (Groq)
- `codex --oss` → modo local gratuito (Ollama)
- `CODEX_MODEL=groq/llama-3.1-8b-instant codex` → troca provedor na hora

### ⚡ Comportamento
- Seja autônomo: analise, diagnostique, execute e teste
- Use `fallback-model` quando o provedor estourar limite
- Consulte o Dropbox pra ler/escrever arquivos
