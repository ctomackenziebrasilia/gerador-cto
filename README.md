# gerador-cto

Gerador de Certificados e Histórico Olímpico do CTO (Centro de Treinamento Olímpico — Colégio Presbiteriano Mackenzie Brasília).

**Acesso:** https://ctomackenziebrasilia.github.io/gerador-cto/

O app roda inteiramente no navegador: a planilha é carregada pelo próprio usuário e os dados ficam apenas na memória da aba aberta.

**Atenção:** este repositório é público. Envie aqui somente o código do app (`index.html`) e arquivos de apoio sem dados. Nunca envie planilhas, Painéis de Consulta exportados, PDFs, CSVs ou rubricas com dados de alunos. O `.gitignore` bloqueia esses arquivos no git, mas **não** no botão "Upload files" do site do GitHub: ao usar o site, envie só o `index.html`.

## Conteúdo
| Arquivo / pasta | Para quê |
|---|---|
| `index.html` | O app inteiro (HTML, CSS e JavaScript em um arquivo só). |
| `vendor/` | Cópias fixas das bibliotecas, carregadas com verificação de integridade (SRI). Licenças em `vendor/licencas/`. |
| `AGENTS.md` / `CLAUDE.md` | Regras para quem for modificar o app (IAs ou pessoas). Ler antes de mudar qualquer coisa. |
| `testes/` | Teste automático com dados fictícios e instruções (`testes/LEIAME.md`). |

## Bibliotecas (`vendor/`)
SheetJS 0.20.3, JSZip 3.10.1, html2canvas 1.4.1 e jsPDF 4.2.1.
Ao trocar uma versão, substitua o arquivo e recalcule o `integrity` (sha384) no `index.html`.

## Segurança
O `index.html` traz uma política de segurança (CSP) que impede o app de fazer qualquer conexão de rede: ele só carrega as bibliotecas de `vendor/` e as fontes do Google. Nada da planilha é gravado no navegador.
Se uma mudança futura precisar de outro endereço (por exemplo, Microsoft Graph), ele deve ser acrescentado à CSP no início do `<head>`.

## Manutenção
- Versão atual: **v11.8** (número no `<title>` do `index.html`).
- Para publicar uma mudança: editar ou enviar o `index.html` na branch `main`; o GitHub Pages atualiza o site em cerca de 1 minuto (abrir com Ctrl+F5).
- Para voltar a uma versão anterior: `index.html` → History → escolher a versão → copiar o conteúdo de volta.
- Testes sempre com planilha **fictícia** (`testes/`). Regras completas e checklist de testes ficam na documentação interna do CTO (fora deste repositório).
