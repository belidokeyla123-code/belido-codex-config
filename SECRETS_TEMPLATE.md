# SECRETS_TEMPLATE.md — Credenciais para setup do Codex

Preencha as variáveis abaixo antes de ativar os MCPs que dependem de credenciais.

## Dropbox (MCP obrigatório)
```bash
export DROPBOX_APP_KEY="sua_app_key"
export DROPBOX_APP_SECRET="seu_app_secret"
export DROPBOX_REFRESH_TOKEN="seu_refresh_token"
```

## GitHub (MCP opcional)
```bash
export GITHUB_TOKEN="seu_token_ghp_xxx"
```

## Onde obter
- **Dropbox App:** https://www.dropbox.com/developers/apps
- **GitHub Token:** https://github.com/settings/tokens
- **Chave EC2:** Dropbox `/Public/IA/CHAVES DE ACESSO/cerebro-ec2-keyla.pem`
