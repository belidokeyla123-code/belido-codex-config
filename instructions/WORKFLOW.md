# WORKFLOW.md — Fluxo de Trabalho Codex

## Verificação Inicial (SEMPRE antes de qualquer ação)

```bash
# 1. Garantir acesso SSH
bash /home/ubuntu/setup_ec2.sh

# 2. Auditoria rápida completa
ssh ec2-keyla "bash ~/audit_rapido.sh"

# 3. Estado detalhado quando necessário
ssh ec2-keyla "
  systemctl list-units --type=service --state=failed --no-pager
  journalctl -p err --since '30 min ago' --no-pager | tail -15
"
```

## Estrutura de Resposta Obrigatória (tarefa técnica)

1. **DIAGNÓSTICO** — Estado atual + problema central + causa raiz provável
2. **PLANO DE AÇÃO** — Passos em ordem segura
3. **IMPLEMENTAÇÃO** — Código completo e comandos executados
4. **VALIDAÇÃO** — Prova concreta de que funcionou
5. **PRÓXIMO PASSO** — O que fazer a seguir

## NUNCA CONCLUIR "ESTÁ TUDO CERTO" SEM PROVA
Valide com sinais concretos: logs, status, memória, processos, portas, resposta real do serviço.
