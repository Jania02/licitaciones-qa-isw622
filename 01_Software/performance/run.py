"""Carga local estrictamente acotada, con base de datos desechable y medición real."""
import csv, json, os, platform, socket, subprocess, sys, tempfile, time
from pathlib import Path
import httpx, psutil

root=Path(__file__).resolve().parents[1]
output=root.parent/'04_Evidencias'/'EV-023-rendimiento';output.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    env={**os.environ,'DATABASE_URL':f'sqlite:///{Path(tmp)/"qa.db"}','ADMIN_USER':'qa_local','ADMIN_PASSWORD':'synthetic-only','SECRET_KEY':'local-performance-only'}
    subprocess.run([sys.executable,'seed.py','--reset'],cwd=root,env=env,check=True)
    with socket.socket() as s:
        s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    host=f'http://127.0.0.1:{port}'
    server=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(port)],cwd=root,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    load=None
    try:
        for _ in range(100):
            if server.poll() is not None: raise RuntimeError('Servidor no disponible')
            try:
                if httpx.get(host+'/api/health',timeout=.3).status_code==200: break
            except httpx.HTTPError: pass
            time.sleep(.1)
        else: raise RuntimeError('No inició el servidor')
        proc=psutil.Process(server.pid);proc.cpu_percent();samples=[]
        with (output/'locust.log').open('w') as log:
            load=subprocess.Popen([sys.executable,'-m','locust','-f','performance/locustfile.py','--headless','--users','5','--spawn-rate','5','--run-time','30s','--host',host,'--csv',str(output/'locust'),'--only-summary'],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
            while load.poll() is None:
                time.sleep(1);samples.append({'cpu_percent':proc.cpu_percent(),'rss_bytes':proc.memory_info().rss})
        with (output/'locust_stats.csv').open() as f:
            row=next(r for r in csv.DictReader(f) if r['Name']=='GET listado')
        count=int(row['Request Count']);fails=int(row['Failure Count']);p95=float(row['95%']);rate=100*fails/count if count else 100
        report={'users':5,'duration_seconds':30,'requests':count,'errors':fails,'error_percent':rate,'p95_ms':p95,'cpu_peak_percent':max(s['cpu_percent'] for s in samples),'ram_peak_bytes':max(s['rss_bytes'] for s in samples),'environment':platform.platform(),'logical_cpu_count':os.cpu_count(),'locust_exit':load.returncode,'passed':count>0 and p95<=1500 and rate<=5 and load.returncode==0}
        (output/'resumen.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
        if not report['passed']: raise SystemExit(1)
    finally:
        if load is not None and load.poll() is None: load.terminate();load.wait()
        server.terminate();server.wait()
