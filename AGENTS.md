# Instruções para IAs e pessoas que forem modificar este repositório

Gerador de Certificados e Histórico Olímpico do CTO (Colégio Presbiteriano Mackenzie Brasília).
Site: https://ctomackenziebrasilia.github.io/gerador-cto/ (GitHub Pages, branch `main`, raiz).

A documentação completa (regras, layouts aprovados, decisões, histórico) fica no projeto interno do CTO,
fora deste repositório. Peça ao responsável o arquivo `Documentacao_Geral_CTO.md` antes de mudanças grandes.
Responda em português do Brasil, em linguagem simples: o responsável não é programador.

## Regras que nenhuma mudança pode quebrar
1. **Repositório público: nunca enviar dados de alunos.** Nada de planilhas, PDFs, CSVs, ZIPs, Painéis
   exportados ou rubricas (imagens de assinatura). Testar só com dados fictícios (ver `testes/`).
2. **Privacidade:** planilha, rubricas e dados de alunos ficam só na memória da aba. Não gravar nada disso
   em `localStorage`, `sessionStorage`, IndexedDB ou cookies. O que pode ser salvo está na documentação (2.5).
3. **Colunas da aba `Geral` são lidas pela posição** (A–L, dados a partir da linha 4). Não presumir outra ordem.
4. **Segurança:**
   - todo texto vindo da planilha passa por `escapeHtml()` antes de virar HTML;
   - manter a CSP (`<meta http-equiv="Content-Security-Policy">`) e o `<meta name="referrer" content="no-referrer">`;
   - bibliotecas só da pasta `vendor/`, por URL absoluta, com `integrity` (sha384) e `crossorigin="anonymous"`;
   - sem `eval`, `new Function`, `document.write` nem CDNs novos;
   - endereço externo novo só entra se for acrescentado à CSP (e combinado com o responsável).
5. **Visual aprovado:** não mudar cores, layout dos documentos (Certificado, Histórico, Folha de controle)
   nem a interface sem combinar antes.
6. **Arquivo único:** o app é só o `index.html` (HTML + CSS + JS). Não dividir em vários arquivos nem
   introduzir etapa de build obrigatória.

## Detalhes técnicos que costumam pegar
- **Tailwind 3.4.17 pré-gerado** no bloco `<style id="twBuiltCss">`, só com as classes usadas.
  Classe nova só funciona depois de regenerar: `npx tailwindcss@3.4.17 --content index.html --minify`
  e substituir o conteúdo do bloco. Alternativa simples: usar `style="…"`.
- **Ícones:** mapa `ICONS` no início do `<script>` (Lucide 0.460.0). Ícone novo precisa ser acrescentado ao mapa.
- **Texto na Folha de controle:** usar `csT()` / `CS_LIFT` (corrige o deslocamento do texto no html2canvas).
- **Trocar biblioteca:** novo arquivo em `vendor/`, licença em `vendor/licencas/` e `integrity` recalculado:
  `openssl dgst -sha384 -binary arquivo.js | openssl base64 -A`
- **Versão:** número no `<title>` do `index.html` (ex.: `v11.4`) e no `README.md`. Mensagem de commit
  começando pela versão (ex.: `v11.5: …`).

## Antes de publicar
1. Rodar o teste automático (`testes/LEIAME.md`) ou seguir o checklist manual da documentação (6.6).
2. Console do navegador (F12) sem erros vermelhos.
3. Conferir que a CSP, os `integrity` e o `escapeHtml` continuam no arquivo.
4. Depois de publicar, o responsável atualiza o arquivo do Gerador e a documentação no projeto interno.
