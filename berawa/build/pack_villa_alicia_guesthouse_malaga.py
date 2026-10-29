#!/usr/bin/env python3
"""ZIP determinista del sitio desplegable. Uso: pack_villa_alicia_guesthouse_malaga.py <carpeta_repo> <salida.zip>
Incluye solo lo necesario para servir y entender el sitio; excluye .git, AGENTS.md, docs/, .agents/, berawa/build/, evidencias de pruebas y CORRECCIONES.md."""
import sys,os,zipfile
src,out=os.path.abspath(sys.argv[1]),os.path.abspath(sys.argv[2])
INC_FILES=['index.html','styles.css','app.js','robots.txt','README.md','INSTALACION.md','LICENSES.md','berawa/project.json','berawa/asset_manifest.json','berawa/knowledge.json','berawa/sources.json','berawa/V1.0-CAMBIOS.md']
INC_DIRS=['img','fonts','berawa/evidence/assets']
files=[f for f in INC_FILES if os.path.isfile(os.path.join(src,f))]
for d in INC_DIRS:
    for r,_,fs in os.walk(os.path.join(src,d)):
        for f in fs: files.append(os.path.relpath(os.path.join(r,f),src))
os.makedirs(os.path.dirname(out),exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(files):
        zi=zipfile.ZipInfo(f.replace(os.sep,'/'),(2026,1,1,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16
        z.writestr(zi,open(os.path.join(src,f),'rb').read())
print(f'{out}: {len(files)} ficheros, {os.path.getsize(out)//1024} KB')
