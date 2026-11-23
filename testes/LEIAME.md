# Testes do Gerador

Sempre com dados **fictícios**. Nunca colocar planilhas reais aqui (a pasta `testes/saida/` é ignorada pelo git).

## Teste automático (para o Claude, outra IA ou quem tiver Python)
Na raiz do repositório:

```
pip install playwright openpyxl
python -m playwright install chromium
python testes/teste_automatico.py
```

O script cria uma planilha fictícia, abre o `index.html` num navegador invisível e confere:
carregamento da planilha, PDF do certificado, do histórico e de todos, folha de controle com 3 mesas,
Painel de Consulta sem e-mails, termo ou turma, nada de aluno gravado no navegador, celular sem rolagem
lateral, proteção contra HTML vindo da planilha e console sem erros.
Termina com **TUDO CERTO** ou com a lista de falhas. Os PDFs e as imagens ficam em `testes/saida/`
para conferir o visual a olho.

## Teste manual (sem instalar nada)
Seguir o checklist da documentação interna (seção 6.6) com uma cópia do modelo vazio da planilha
preenchida com 5 a 10 linhas inventadas.
