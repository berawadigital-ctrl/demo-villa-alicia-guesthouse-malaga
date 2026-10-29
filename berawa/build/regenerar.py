#!/usr/bin/env python3
"""Regenera TODO lo generado de la demo en la raiz del repo: ilustraciones (img/), index.html, app.js, styles.css, robots.txt,
berawa/knowledge.json, berawa/sources.json, berawa/asset_manifest.json y berawa/project.json. Es determinista (misma entrada = mismos bytes).
Uso: python3 berawa/build/regenerar.py [--solo-web]"""
import sys,shutil,tempfile,subprocess
from pathlib import Path
from _rutas import ROOT,BUILD
py=sys.executable
tmp=tempfile.mkdtemp(prefix='demo-build-')
subprocess.check_call([py,str(BUILD/'run_stage.py'),'--out='+tmp])
for f in ('index.html','app.js','styles.css','robots.txt'): shutil.copy(Path(tmp)/f,ROOT/f)
(ROOT/'fonts').mkdir(exist_ok=True)
subprocess.check_call([py,str(BUILD/'make_art.py'),'--out='+str(ROOT)])
if '--solo-web' not in sys.argv:
    subprocess.check_call([py,str(BUILD/'make_kb_files.py')]); subprocess.check_call([py,str(BUILD/'make_docs.py')]); subprocess.check_call([py,str(BUILD/'finalize_villa_alicia_guesthouse_malaga.py')])
