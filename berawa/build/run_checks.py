#!/usr/bin/env python3
"""Ejecuta TODAS las comprobaciones de la demo con un solo comando, desde cualquier carpeta y sin rutas absolutas.
  python3 berawa/build/run_checks.py [--site DIR] [--out DIR] [--file]
  --site DIR  carpeta del sitio a probar (por defecto, la raiz del repo; usa la carpeta descomprimida para probar el ZIP)
  --out DIR   donde escribir los JSON de resultados (por defecto, una carpeta temporal; no se escribe en el repo)
  --file      repite ademas tests_villa_alicia_guesthouse_malaga y a11y_test abriendo index.html por file:// (sin servidor)
Levanta un servidor HTTP local en un puerto libre (python http.server en un hilo): no usa red externa ni carpetas externas.
Dependencias: ver berawa/build/README.md (pip install -r requirements.txt; playwright install chromium; npm install). Codigo de salida 1 si algo falla."""
import sys,os,json,subprocess,threading,tempfile,functools,http.server,socketserver
from pathlib import Path
from _rutas import ROOT,BUILD

def main(argv):
    arg=lambda k:(argv[argv.index(k)+1] if k in argv else None)
    site=Path(arg('--site') or ROOT).resolve(); out=Path(arg('--out') or tempfile.mkdtemp(prefix='villa_alicia_guesthouse_malaga-checks-')).resolve(); out.mkdir(parents=True,exist_ok=True)
    if not (site/'index.html').is_file(): sys.exit(f'No hay index.html en {site}')
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a): pass
    socketserver.TCPServer.allow_reuse_address=True
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(H,directory=str(site)))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    py=sys.executable; res=[]
    def run(nombre,cmd,ok_fn):
        p=subprocess.run([py,str(BUILD/cmd[0]),*cmd[1:]],capture_output=True,text=True,cwd=str(out))
        ok=p.returncode==0 and ok_fn(p); res.append((nombre,ok))
        print(('OK    ' if ok else 'FALLO ')+nombre)
        if not ok: print('   '+(p.stdout+p.stderr).strip().replace('\n','\n   ')[-1500:])
    jok=lambda f:(lambda p:json.load(open(out/f)).get('ok') is True)
    run('check_kb (citas + regla de precios P1-P6) sobre berawa/knowledge.json',['check_kb.py'],lambda p:True) if site==ROOT else None
    run('tests_villa_alicia_guesthouse_malaga: 4 idiomas + chatbot contra la base (HTTP)',['tests_villa_alicia_guesthouse_malaga.py',url,str(out/'chat-i18n.json'),'--kb'],jok('chat-i18n.json'))
    run('a11y_test: axe-core + teclado (HTTP)',['a11y_test.py',url,str(out/'axe-teclado.json')],jok('axe-teclado.json'))
    run('contrast_manual: contraste de nodos «incompletos» de axe',['contrast_manual.py',url,str(out/'contraste.json')],lambda p:json.load(open(out/'contraste.json'))['fallos']==[])
    run('keys_test: claves del chat sin ambiguedad',['keys_test.py',url],lambda p:' 0 ambiguas' in p.stdout)
    run('sec_scan: revision estatica + CSP efectiva',['sec_scan.py',str(site),url,str(out/'seguridad.json')],jok('seguridad.json'))
    if '--file' in argv:
        fu=(site/'index.html').as_uri()
        run('tests_villa_alicia_guesthouse_malaga por file://',['tests_villa_alicia_guesthouse_malaga.py',fu,str(out/'file-chat-i18n.json'),'--kb'],jok('file-chat-i18n.json'))
        run('a11y_test por file://',['a11y_test.py',fu,str(out/'file-axe-teclado.json')],jok('file-axe-teclado.json'))
    srv.shutdown()
    bad=[n for n,o in res if not o]
    print(f'\n{len(res)-len(bad)}/{len(res)} comprobaciones OK · resultados en {out}')
    return 1 if bad else 0
if __name__=='__main__': sys.exit(main(sys.argv[1:]))
