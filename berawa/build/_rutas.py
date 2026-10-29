"""Rutas y utilidades comunes de los scripts de berawa/build. TODO se resuelve desde la raiz del repositorio
(nunca rutas absolutas): funciona igual desde cualquier clon. Entradas externas opcionales por variable de entorno."""
import os,sys
from pathlib import Path
BUILD=Path(__file__).resolve().parent          # berawa/build
ROOT=BUILD.parents[1]                          # raiz del repositorio
EVIDENCE=ROOT/'berawa'/'evidence'
SOURCE_TEXT=EVIDENCE/'source-text.json'   # texto de las paginas fuente guardado en el repo (fecha de lectura en berawa/sources.json)
if str(BUILD) not in sys.path: sys.path.insert(0,str(BUILD))

def axe_dir():
    """axe-core instalado con `npm install` en berawa/build (ver README.md). AXE_DIR permite apuntar a otra carpeta."""
    d=Path(os.environ.get('AXE_DIR') or BUILD/'node_modules'/'axe-core')
    if not (d/'axe.min.js').is_file(): sys.exit(f'Falta axe-core en {d}. Ejecuta: cd berawa/build && npm install  (ver berawa/build/README.md)')
    return d
def axe_js(): return (axe_dir()/'axe.min.js').read_text()
def axe_version():
    import json; return json.loads((axe_dir()/'package.json').read_text())['version']

def lanzar_navegador(p):
    """Chromium de Playwright (`playwright install chromium`). CHROME_PATH permite usar otro Chrome/Chromium ya instalado."""
    kw=dict(args=['--no-proxy-server','--no-sandbox'])
    if os.environ.get('CHROME_PATH'): kw['executable_path']=os.environ['CHROME_PATH']
    return p.chromium.launch(**kw)

def entrada_externa(var,descripcion):
    """Entradas que NO estan en el repo (material crudo del generador). Solo las usan los scripts de generacion, no las comprobaciones."""
    v=os.environ.get(var)
    if not v or not Path(v).exists(): sys.exit(f'Este script de generacion necesita {descripcion}: define {var} con su ruta (ver berawa/build/README.md). No hace falta para verificar la demo.')
    return Path(v)
