"""Ejecuta CP funcionales por API contra un servidor local con BD temporal y datos sinteticos.
Uso: cd 01_Software && python qa_scripts/ejecutar_casos_funcionales_api.py"""
import subprocess,os,sys,time,json,tempfile,datetime,platform,pathlib,httpx,secrets
from datetime import timezone,timedelta
root=pathlib.Path(__file__).resolve().parents[2];sw=root/'01_Software';ev=root/'04_Evidencias'
py=sys.executable;port=8011;host=f'http://127.0.0.1:{port}'
pw=secrets.token_urlsafe(8)
tmp=tempfile.mkdtemp()
env={**os.environ,'DATABASE_URL':f'sqlite:///{tmp}/qa.db','ADMIN_USER':'qa_local','ADMIN_PASSWORD':pw,'SECRET_KEY':secrets.token_hex(16)}
subprocess.run([py,'-c','import seed;seed.inicializar()'],cwd=sw,env=env,check=True)
def start():
    s=subprocess.Popen([py,'-m','uvicorn','app.main:app','--port',str(port)],cwd=sw,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for _ in range(100):
        try:
            if httpx.get(host+'/api/health',timeout=.3).status_code==200:return s
        except Exception:time.sleep(.1)
    raise SystemExit('no inicia')
commit=subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=root,text=True).strip()
envtxt=f"{platform.system()} {platform.release()}, Python {platform.python_version()}, SQLite temporal, servidor Uvicorn local {host}"
logs={};cur=[None];res={}
def log(cp,t):logs.setdefault(cp,[]).append(t)
def call(cp,cli,m,u,**k):
    r=cli.request(m,u,**k);body=r.text[:300].replace('\n',' ')
    log(cp,f"{m} {u} {json.dumps(k.get('json'),ensure_ascii=False) if k.get('json') else ''} -> {r.status_code} {body}");return r
def check(cp,desc,cond):
    log(cp,f"VERIFICACIÓN: {desc} -> {'CUMPLE' if cond else 'NO CUMPLE'}");res.setdefault(cp,[]).append(bool(cond))
srv=start();c=httpx.Client(base_url=host)
r=c.post('/api/auth/login',json={'username':'qa_local','password':pw});assert r.status_code==200
iso=lambda d:d.isoformat()
now=datetime.datetime.now(timezone.utc)
# CP-008
cp='CP-008'
p1=call(cp,c,'POST','/api/proveedores',json={'nombre':'Tecnología Norte S.A.'}).json()
p2=call(cp,c,'POST','/api/proveedores',json={'nombre':'Servicios del Valle'}).json()
L={'codigo':'LIC-2026-001','titulo':'Equipo tecnológico','presupuesto_crc':'10000000.00','cierre':iso(now+timedelta(hours=48))}
r=call(cp,c,'POST','/api/licitaciones',json=L);check(cp,'alta de L1 responde 201 en Borrador',r.status_code==201 and r.json()['estado']=='Borrador');lid=r.json()['id']
r=call(cp,c,'PATCH',f'/api/licitaciones/{lid}/estado',json={'estado':'Publicada'});check(cp,'publicar L1 responde 200 y estado Publicada',r.status_code==200 and r.json()['estado']=='Publicada')
r=call(cp,c,'POST','/api/licitaciones',json={**L,'codigo':'  lic-2026-001  '});check(cp,'código repetido (otras mayúsculas/espacios) responde 409',r.status_code==409)
# CP-021
cp='CP-021'
for desc,mod in [('título vacío',{'titulo':''}),('presupuesto 0',{'presupuesto_crc':'0'}),('cierre pasado',{'cierre':iso(now-timedelta(hours=1))})]:
    r=call(cp,c,'POST','/api/licitaciones',json={**L,'codigo':'LIC-X-'+desc[:3],**mod});check(cp,f'{desc} rechazado (4xx)',400<=r.status_code<500)
# ofertas
for p,m in [(p1,'9000000.00'),(p2,'9500000.00')]:
    call('CP-019',c,'POST','/api/ofertas',json={'licitacion_id':lid,'proveedor_id':p['id'],'monto_crc':m})
# CP-019
cp='CP-019'
r=call(cp,c,'POST','/api/tasas',json={'crc_por_usd':'500'});check(cp,'tasa 500 registrada (201)',r.status_code==201)
usd=call(cp,c,'GET','/api/moneda?moneda=USD').json()
check(cp,'oferta de P1 se visualiza como 18000.00 USD',any(o['monto']=='18000.00' for o in usd['ofertas']))
crc=call(cp,c,'GET','/api/moneda?moneda=CRC').json()
check(cp,'al volver a CRC la oferta de P1 sigue siendo 9000000.00',any(o['monto']=='9000000.00' for o in crc['ofertas']))
check(cp,'se muestran tasa y fecha utilizadas',bool(usd['tasa'] and usd['tasa']['fecha'] and usd['tasa']['crc_por_usd']=='500'))
lo=call(cp,c,'GET','/api/ofertas?licitacion_id=%d'%lid).json()
check(cp,'importes guardados en la BD (API de ofertas) permanecen en CRC',any('9000000' in str(o) for o in lo))
# CP-022
cp='CP-022'
for v in ['0','-5']:
    r=call(cp,c,'POST','/api/tasas',json={'crc_por_usd':v});check(cp,f'tasa {v} rechazada (400)',r.status_code==400)
r=call(cp,c,'GET','/api/tasas');check(cp,'la lista de tasas conserva solo la tasa válida 500',len(r.json())==1)
# CP-007 persistencia
cp='CP-007'
srv.terminate();srv.wait();log(cp,'--- servidor detenido y reiniciado (misma base de datos) ---');srv=start()
c=httpx.Client(base_url=host);call(cp,c,'POST','/api/auth/login',json={'username':'qa_local','password':pw})
r=call(cp,c,'GET','/api/proveedores');check(cp,'los 2 proveedores persisten tras reiniciar',len(r.json())==2)
r=call(cp,c,'GET','/api/licitaciones');check(cp,'L1 persiste con estado Publicada',any(l['codigo']=='LIC-2026-001' and l['estado']=='Publicada' for l in r.json()))
r=call(cp,c,'GET','/api/ofertas');check(cp,'las 2 ofertas persisten',len(r.json())==2)
r=call(cp,c,'POST','/api/ofertas',json={'licitacion_id':lid,'proveedor_id':p1['id'],'monto_crc':'9000000.00'});check(cp,'oferta duplicada de P1 rechazada también tras reiniciar (409)',r.status_code==409)
srv.terminate();srv.wait()
plan=[('EV-047','CP-007'),('EV-048','CP-008'),('EV-049','CP-019'),('EV-050','CP-021'),('EV-051','CP-022')]
out=[]
for evid,cp in plan:
    ok=all(res[cp]);start=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name=f"{evid}-{cp.lower()}-funcional.txt"
    (ev/name).write_text(f"EVIDENCIA {evid} — {cp} (Funcional por API sobre servidor local)\nFecha: {start}\nCommit: {commit}\nEntorno: {envtxt}\nBase de datos: temporal, solo datos sintéticos (P1, P2, L1)\nEjecutor: Claude Code (IA-050); revisión humana pendiente\n\n"+'\n'.join(logs[cp])+f"\n\nRESULTADO: {'PASA' if ok else 'FALLA'} ({sum(res[cp])}/{len(res[cp])} verificaciones)\n")
    out.append(dict(ev=evid,cp=cp,start=start,ok=ok,n=len(res[cp]),file=name,commit=commit,env=envtxt));print(cp,ok,res[cp])
json.dump(out,open(root/'04_Evidencias'/'ejecucion_funcional_resumen.json','w'),ensure_ascii=False,indent=1)
