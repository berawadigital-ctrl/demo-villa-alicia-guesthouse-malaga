#!/usr/bin/env python3
"""Lighthouse movil y escritorio, 3 pasadas cada uno, mediana. Uso: python3 berawa/build/lh3.py DIR_SITIO salida.json
Requiere Lighthouse (npx lighthouse@13.6.0, o LH_BIN=/ruta/lighthouse) y Chrome (CHROME_PATH). Sirve DIR_SITIO por http local."""
import sys,os,json,subprocess,threading,functools,http.server,socketserver,statistics,tempfile
site,outf=sys.argv[1],sys.argv[2]
class Hd(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(Hd,directory=site));threading.Thread(target=srv.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{srv.server_address[1]}/index.html'
lh=[os.environ['LH_BIN']] if os.environ.get('LH_BIN') else ['npx','-y','lighthouse@13.6.0']
res={}
for modo in ('mobile','desktop'):
    runs=[]
    for i in range(3):
        f=tempfile.mktemp(suffix='.json')
        cmd=lh+[url,'--output=json','--output-path='+f,'--quiet','--chrome-flags=--headless=new --no-sandbox','--only-categories=performance,accessibility,best-practices,seo']+(['--preset=desktop'] if modo=='desktop' else [])
        env=dict(os.environ);
        if os.environ.get('CHROME_PATH'): env['CHROME_PATH']=os.environ['CHROME_PATH']
        subprocess.run(cmd,check=True,capture_output=True,env=env)
        j=json.load(open(f));c=j['categories']
        runs.append({k:round(c[k]['score']*100) for k in ('performance','accessibility','best-practices','seo')}|{'lcp_s':round(j['audits']['largest-contentful-paint']['numericValue']/1000,2),'lh':j['lighthouseVersion']})
        seo_fail=[a for a,v in j['audits'].items() if v.get('score')==0 and a in ('is-crawlable','robots-txt','meta-description','document-title','viewport','link-text','hreflang','canonical')]
    res[modo]=dict(runs=runs,mediana={k:int(statistics.median(r[k] for r in runs)) for k in ('performance','accessibility','best-practices','seo')},seo_fallos=seo_fail)
json.dump(res,open(outf,'w'),indent=1); print(json.dumps({m:res[m]['mediana'] for m in res}),{m:res[m]['seo_fallos'] for m in res})
