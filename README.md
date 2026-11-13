# gerador-cto

Gerador de Certificados e Histórico Olímpico do CTO (Centro de Treinamento Olímpico — Colégio Presbiteriano Mackenzie Brasília).

**Acesso:** https://ctomackenziebrasilia.github.io/gerador-cto/

O app roda inteiramente no navegador: a planilha é carregada pelo próprio usuário e os dados ficam apenas no navegador dele.

**Atenção:** este repositório é público. Envie aqui somente o código do app (`index.html`). Nunca envie planilhas, Painéis de Consulta exportados, PDFs ou relatórios com dados de alunos.

## Bibliotecas (`vendor/`)
Cópias fixas das bibliotecas usadas pelo app, carregadas com verificação de integridade (SRI) pelo `index.html`:
SheetJS 0.20.3, JSZip 3.10.1, html2canvas 1.4.1 e jsPDF 4.2.1. Licenças em `vendor/licencas/`.
Ao trocar uma versão, substitua o arquivo e recalcule o `integrity` (sha384) no `index.html`.
