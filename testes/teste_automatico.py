"""Teste automático do Gerador CTO com dados FICTÍCIOS.

Uso (na raiz do repositório):
    pip install playwright openpyxl
    python -m playwright install chromium
    python testes/teste_automatico.py

O teste cria uma planilha fictícia em testes/saida/ (nunca usar dados reais),
abre o index.html local num navegador invisível, servindo as bibliotecas de vendor/,
e confere: carregamento, PDFs (certificado, histórico, todos), folha de controle com
3 mesas, Painel de Consulta sem e-mails/termo/turma, nada gravado no navegador,
celular sem rolagem lateral, proteção contra HTML vindo da planilha e console sem erros.
Termina com "TUDO CERTO" ou com a lista de falhas.
"""
import asyncio, json, os, re, sys
from pathlib import Path

import openpyxl
from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'testes' / 'saida'
SAIDA.mkdir(parents=True, exist_ok=True)
URL_VENDOR = 'https://ctomackenziebrasilia.github.io/gerador-cto/vendor/'

CABECALHO = ['STATUS', 'TERMO', 'E-MAIL ALUNO', 'ALUNO', 'S/T', 'OLIMPÍADA', 'SIGLA', 'ANO',
             'PREMIAÇÃO', 'E-MAIL 1', 'E-MAIL 2', 'OBSERVAÇÃO']
OBMEP = 'Olimpíada Brasileira de Matemática das Escolas Públicas'
LINHAS = [
    ('realizada', 'aceito', 12345, 'Ana Fictícia Souza', '1A', OBMEP, 'OBMEP', 2026, 'Ouro', 'resp1@exemplo.invalid', 'resp2@exemplo.invalid', ''),
    ('realizada', 'pendente', 23456, 'Bruno Teste Lima', '2B', 'Olimpíada Brasileira de Física', 'OBF', 2026, 'Prata', 'b@exemplo.invalid', '', ''),
    ('aguardando', 'revogado', 34567, 'Carla <b>Exemplo</b>', '3C', 'Olimpíada Brasileira de Química', 'OBQ', 2025, 'Bronze', '', '', ''),
    ('aguardando', 'aceito', 45678, 'Daniel Modelo', '1A', OBMEP, 'OBMEP', 2026, 'Menção Honrosa', 'd@exemplo.invalid', '', ''),
    ('realizada', 'aceito', 12345, 'Ana Fictícia Souza', '1A', 'Olimpíada Brasileira de Física', 'OBF', 2025, 'Bronze', 'resp1@exemplo.invalid', '', ''),
    ('realizada', 'aceito', 56789, 'Eduardo Ficção', '2A', 'Olimpíada Brasileira de Informática', 'OBI', 2026, '', '', '', ''),
    ('realizada', 'aceito', 67890, 'Fernanda Simulada', '3A', 'Olimpíada Brasileira de Biologia', 'OBB', 2026, 'Ouro', 'f@exemplo.invalid', '', ''),
    ('realizada', 'aceito', 78901, 'Gabriel Inventado', '2C', 'Olimpíada Brasileira de Astronomia', 'OBA', 2026, 'Prata', 'g@exemplo.invalid', 'g2@exemplo.invalid', ''),
    ('realizada', 'pendente', 89012, 'Helena Hipotética', '1B', OBMEP, 'OBMEP', 2026, 'Bronze', 'h@exemplo.invalid', '', ''),
    ('realizada', 'aceito', 90123, 'Igor Imaginário', '3B', 'Olimpíada Brasileira de Física', 'OBF', 2026, 'Ouro', 'i@exemplo.invalid', '', ''),
]


def criar_planilha():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Geral'
    ws['A1'] = 'Planilha FICTÍCIA de teste'
    for j, h in enumerate(CABECALHO, 1):
        ws.cell(row=3, column=j, value=h)
    for i, linha in enumerate(LINHAS):
        for j, v in enumerate(linha, 1):
            ws.cell(row=4 + i, column=j, value=v)
    caminho = SAIDA / 'planilha_ficticia.xlsx'
    wb.save(caminho)
    return str(caminho)


async def main():
    xlsx = criar_planilha()
    falhas, avisos, info = [], [], {}

    def checar(cond, msg):
        if not cond:
            falhas.append(msg)

    async with async_playwright() as p:
        navegador = await p.chromium.launch()

        async def rota(r):
            u = r.request.url
            if u.startswith(URL_VENDOR):
                await r.fulfill(path=str(RAIZ / 'vendor' / u.rsplit('/', 1)[1]),
                                headers={'Content-Type': 'application/javascript', 'Access-Control-Allow-Origin': '*'})
            elif u.startswith('http://teste.local/'):
                await r.fulfill(path=str(RAIZ / 'index.html'), headers={'Content-Type': 'text/html'})
            elif 'fonts.g' in u:
                await r.fulfill(body='', headers={'Content-Type': 'text/css', 'Access-Control-Allow-Origin': '*'})
            else:
                await r.abort()

        async def nova_pagina(**kw):
            ctx = await navegador.new_context(accept_downloads=True, **kw)
            pg = await ctx.new_page()
            await pg.route('**/*', rota)
            pg.on('pageerror', lambda e: falhas.append(f'Erro de JavaScript: {e}'))
            pg.on('console', lambda m: avisos.append(m.text) if m.type == 'error' else None)
            await pg.goto('http://teste.local/index.html')
            await pg.wait_for_timeout(1200)
            await pg.set_input_files('#GlobalQuickFileInput', xlsx)
            await pg.wait_for_timeout(1500)
            return pg

        async def baixar(pg, seletor, nome, menu=False):
            try:
                async with pg.expect_download(timeout=180000) as d:
                    if menu:
                        await pg.click('#btnMoreMenu')
                        await pg.wait_for_timeout(300)
                    await pg.click(seletor)
                arq = await d.value
                destino = SAIDA / f'{nome}_{arq.suggested_filename}'
                await arq.save_as(destino)
                tam = destino.stat().st_size
                info[nome] = f'{arq.suggested_filename} ({tam // 1024} KB)'
                checar(tam > 1000, f'{nome}: arquivo vazio')
                return destino
            except Exception as e:
                falhas.append(f'{nome}: não baixou ({e})')

        pg = await nova_pagina(viewport={'width': 1400, 'height': 900})
        checar(not await pg.evaluate("!!document.querySelector('#studentList b')"),
               'HTML da planilha foi interpretado (falha no escapeHtml)')
        await pg.screenshot(path=str(SAIDA / '1_certificado.png'))
        await baixar(pg, '#btnPrintSingle', 'certificado')
        await pg.click('#tabModeHist')
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=str(SAIDA / '2_historico.png'))
        await baixar(pg, '#btnPrintSingle', 'historico')
        await baixar(pg, '#btnPrintAllFiltered', 'todos', menu=True)

        pg = await nova_pagina(viewport={'width': 1400, 'height': 900})
        await pg.click('#btnMoreMenu')
        await pg.click('#btnOpenControlSheet')
        await pg.wait_for_timeout(600)
        mesas = pg.locator('#csMesas')
        if await mesas.evaluate('e => e.tagName') == 'SELECT':
            await mesas.select_option('3')
        else:
            await mesas.fill('3')
        await pg.wait_for_timeout(500)
        resumo = await pg.inner_text('#csSummary')
        info['folha_resumo'] = resumo.replace('\n', ' | ')
        checar(len(re.findall(r'Mesa \d+', resumo)) == 3, 'Folha de controle: não formou 3 mesas')
        await baixar(pg, '#btnConfirmControlSheet', 'folha_controle')

        pg = await nova_pagina(viewport={'width': 1400, 'height': 900})
        await pg.click('#btnMoreMenu')
        await pg.click('#btnOpenExportPanel')
        await pg.wait_for_timeout(500)
        painel = await baixar(pg, '#btnConfirmExportPanel', 'painel')
        if painel:
            txt = painel.read_text(encoding='utf-8')
            m = re.search(r'window\.CTO_READONLY = (\{.*?\});?\s*</script>', txt, re.S)
            dados = m.group(1) if m else txt
            checar('exemplo.invalid' not in dados, 'Painel contém e-mails')
            checar('"termo"' not in dados and '"st"' not in dados, 'Painel contém termo ou S/T')
            checar('revogado' not in dados and '3C' not in dados, 'Painel contém termo ou S/T')
        guardado = await pg.evaluate(
            "JSON.stringify([Object.entries(localStorage), Object.entries(sessionStorage)])")
        checar('Ana' not in guardado and 'exemplo' not in guardado, 'Dados de aluno gravados no navegador')

        cel = await nova_pagina(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        checar(not await cel.evaluate('document.documentElement.scrollWidth > window.innerWidth'),
               'Celular: rolagem lateral')
        await cel.screenshot(path=str(SAIDA / '3_celular.png'))
        await navegador.close()

    for k, v in info.items():
        print(f'- {k}: {v}')
    erros_console = [a for a in avisos if 'favicon' not in a]
    if erros_console:
        falhas.append('Erros no console: ' + json.dumps(erros_console, ensure_ascii=False))
    print()
    if falhas:
        print('FALHAS:')
        for f in falhas:
            print(' -', f)
        sys.exit(1)
    print(f'TUDO CERTO. Arquivos gerados em {SAIDA} (confira o visual dos PDFs e das imagens).')


if __name__ == '__main__':
    asyncio.run(main())
