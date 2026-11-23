# L2Remote (L2R)

Programa de suporte remoto da L2Automate, baseado no [RustDesk](https://github.com/rustdesk/rustdesk) (AGPL-3.0).

## Como funciona
- **Servidor próprio**: `remote.l2automate.com.br` (VPS, containers `l2r-id` e `l2r-relay` em `/opt/l2remote`).
- **Marca**: `l2remote/branding.py` aplica nome, ícones, servidor e chave pública no momento do build.
  O código original do RustDesk não é alterado no git, o que facilita puxar atualizações.
- **Build**: workflow `.github/workflows/l2remote-windows.yml` gera `L2Remote.exe` e publica em
  Releases (tag `l2remote-latest`).

## Consentimento
O PC acessado sempre mostra a janela de sessão ativa, com botão para desconectar.
Não altere isso: o programa é para assistência técnica legítima.

## Trocar servidor ou chave
Edite `SERVER` e `PUB_KEY` em `l2remote/branding.py` (ou use as variáveis `L2R_SERVER` / `L2R_PUB_KEY`).

## Licença
Por ser derivado do RustDesk (AGPL-3.0), o código-fonte das modificações deve ficar disponível
para quem recebe o programa. Este repositório público cumpre isso.
