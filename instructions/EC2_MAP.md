# EC2_MAP.md — Mapa Completo da EC2

## Acesso
| Campo | Valor |
|-------|-------|
| IP público | 56.126.138.7 |
| Usuário | ubuntu |
| Alias SSH | `ec2-keyla` |
| OS | Ubuntu 22.04.5 LTS, kernel 6.8.0-1052-aws |
| CPU | 2 vCPU (Intel Xeon 8488C) |
| RAM | 7.6GB total |
| Disco | 194GB total |

## Mapa de Portas e Serviços
| Porta | Serviço | Supervisor |
|-------|---------|-----------|
| 80/443 | Nginx | systemd |
| 5432 | PostgreSQL 14 | systemd |
| 5000 | James Listener (Telegram) | systemd |
| 8083 | Filesystem MCP | systemd |
| 8086 | Evolution API (WhatsApp) | Docker |
| 8091 | Cerebro API | systemd |
| 8093 | Vault Brain MCP | systemd |
| 8094 | Serviço Node | systemd |
| 8095–8096 | Agentes Python | systemd |
| 8099–8102 | MCPs (AWS, Docker, Postgres) | systemd |
| 11434 | Ollama | systemd |
| 18208 | MATER | systemd |
| 18500 | Agente Execução | systemd |
| 18789/18791 | OpenClaw Gateway | systemd |
| 3001 | Gotenberg (PDF) | Docker |
| 2222 | TTYD (Terminal Web) | systemd |
| 9443 | Portainer | Docker |

## Projetos e Paths
| Projeto | Path | Serviço systemd |
|---------|------|----------------|
| Robô Jurídico | `~/apps/juridico/` | `robo-pauta.service` |
| RoboVânia | `~/apps/vania/` | daemon próprio |
| MATER V2 | `~/apps/mater_v2/` | `agente-redator-inicial.service` |
| James | `~/apps/james/` | `james-v2.service` |
| Atendimento | `~/apps/atendimento/` | `ia-worker.service` |
| Luiza | `~/apps/luiza/` | `luiza.service` |
| Trader Bot | `~/apps/trader_bot/` | `james-trader.service` |
| Shared | `~/apps/shared/` | `market-shared-listener.service` |
| OpenClaw MCP | `~/apps/mcp_bridge/` | `openclaw-mcp-bridge.service` |
| Vault MCP | `~/apps/vault_mcp/` | `vault-mcp.service` |
| Cerebro Vault | `~/cerebro-vault/` | sync noturno 03:30 |
