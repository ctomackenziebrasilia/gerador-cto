# gerador-cto

Gerador de Certificados e Histórico Olímpico do CTO (Centro de Treinamento Olímpico — Colégio Presbiteriano Mackenzie Brasília).

**Acesso:** https://ctomackenziebrasilia.github.io/gerador-cto/

O app roda inteiramente no navegador: a planilha é carregada pelo próprio usuário e os dados ficam apenas no navegador dele.

**Atenção:** este repositório é público. Envie aqui somente o código do app (`index.html`). Nunca envie planilhas, Painéis de Consulta exportados, PDFs ou relatórios com dados de alunos.

## Bibliotecas (`vendor/`)
Cópias fixas das bibliotecas usadas pelo app, carregadas com verificação de integridade (SRI) pelo `index.html`:
SheetJS 0.20.3, JSZip 3.10.1, html2canvas 1.4.1 e jsPDF 4.2.1. Licenças em `vendor/licencas/`.
Ao trocar uma versão, substitua o arquivo e recalcule o `integrity` (sha384) no `index.html`.

## Segurança
O `index.html` traz uma política de segurança (CSP) que impede o app de fazer qualquer conexão de rede: ele só carrega as bibliotecas de `vendor/` e as fontes do Google. Nada da planilha é gravado no navegador.
Se uma mudança futura precisar de outro endereço (por exemplo, Microsoft Graph), ele deve ser acrescentado à CSP no início do `<head>`.

## Manutenção
- Versão atual: **v11.3** (número no `<title>` do `index.html`).
- Para publicar uma mudança: editar ou enviar o `index.html` na branch `main`; o GitHub Pages atualiza o site em cerca de 1 minuto (abrir com Ctrl+F5).
- Para voltar a uma versão anterior: `index.html` → History → escolher a versão → copiar o conteúdo de volta.
- Testes sempre com planilha **fictícia**. Regras completas e checklist de testes ficam na documentação interna do CTO (fora deste repositório).
