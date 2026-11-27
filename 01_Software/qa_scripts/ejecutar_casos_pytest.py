"""Ejecuta los CP automatizados con pytest y guarda cada salida real como evidencia EV-NNN.
Uso: cd 01_Software && python qa_scripts/ejecutar_casos_pytest.py"""
import json,subprocess,sys,datetime,time,pathlib,platform
root=pathlib.Path(__file__).resolve().parents[2]
sw=root/'01_Software'; ev=root/'04_Evidencias'
T='tests/'
runs=[ # (EV, CP, tipo, nodeids)
 ('EV-030','CP-001','Unitaria',[T+'test_proveedores_reglas.py::test_clave_ignora_mayusculas_y_espacios',T+'test_proveedores_seguridad_qa.py::test_variantes_de_p1_comparten_clave',T+'test_proveedores_seguridad_qa.py::test_nombres_distintos_no_comparten_clave']),
 ('EV-031','CP-002','Integración/API',[T+'test_proveedores_api.py::test_crear_proveedor_valido',T+'test_proveedores_api.py::test_duplicado_por_mayusculas_o_espacios_se_rechaza',T+'test_proveedores_api.py::test_bd_rechaza_duplicado_aunque_se_salte_la_validacion']),
 ('EV-032','CP-003','Unitaria',[T+'test_proveedores_reglas.py::test_caracteres_no_permitidos_se_rechazan',T+'test_proveedores_seguridad_qa.py::test_simbolo_no_admitido_se_rechaza']),
 ('EV-033','CP-004','Seguridad',[T+'test_proveedores_api.py::test_web_muestra_script_rechazado_como_texto_escapado',T+'test_qa_seguridad_controlada.py::test_nombre_rechazado_en_api']),
 ('EV-034','CP-005','Seguridad',[T+'test_proveedores_api.py::test_error_interno_no_expone_detalles',T+'test_qa_seguridad_controlada.py::test_error_validacion_no_refleja_entrada']),
 ('EV-035','CP-009','Unitaria',[T+'test_licitaciones_ofertas.py::test_transiciones']),
 ('EV-036','CP-013','Integración/API',[T+'test_licitaciones_ofertas.py::test_api_ofertas',T+'test_licitaciones_ofertas.py::test_api_licitacion_duplicada']),
 ('EV-037','CP-014','Integración/API',[T+'test_licitaciones_ofertas.py::test_api_ofertas',T+'test_proveedores_api.py::test_crear_proveedor_valido',T+'test_proveedores_api.py::test_listar_proveedores']),
 ('EV-038','CP-015','Integración/API',[T+'test_proveedores_api.py::test_editar_inexistente_responde_404',T+'test_bug_001_cierre.py::test_regresion_monto_invalido_se_rechaza',T+'test_qa_seguridad_controlada.py::test_api_sin_sesion']),
 ('EV-039','CP-016','Unitaria',[T+'test_evaluacion_moneda.py::test_mejor_y_empate']),
 ('EV-040','CP-017','Unitaria',[T+'test_evaluacion_moneda.py::test_ahorro']),
 ('EV-041','CP-018','Unitaria',[T+'test_evaluacion_moneda.py::test_aprobadores']),
 ('EV-042','CP-023','Unitaria',[T+'test_bug_001_cierre.py::test_regresion_antes_del_cierre_se_acepta',T+'test_bug_001_cierre.py::test_regresion_despues_del_cierre_se_rechaza']),
 ('EV-043','CP-010','Regresión',[T+'test_bug_001_cierre.py::test_cp010_unitaria_exactamente_al_cierre_se_rechaza',T+'test_bug_001_cierre.py::test_cp010_api_exactamente_al_cierre_se_rechaza']),
 ('EV-044','CP-011','Regresión',[T+'test_bug_001_cierre.py::test_cp011_api_oferta_en_estado_no_publicado_se_rechaza',T+'test_bug_001_cierre.py::test_regresion_estado_no_publicado_se_rechaza']),
 ('EV-045','CP-012','Regresión',[T+'test_bug_001_cierre.py::test_cp012_montos_en_los_limites',T+'test_licitaciones_ofertas.py::test_montos']),
 ('EV-046','CP-023','Regresión',[T+'test_bug_001_cierre.py::test_regresion_antes_del_cierre_se_acepta',T+'test_bug_001_cierre.py::test_regresion_despues_del_cierre_se_rechaza',T+'test_licitaciones_ofertas.py::test_vencimiento']),
]
commit=subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=root,text=True).strip()
env=f"{platform.system()} {platform.release()}, Python {platform.python_version()}, pytest 8.3.4, SQLite temporal"
out=[]
for evid,cp,tipo,ids in runs:
    t0=time.time(); start=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd=[sys.executable,'-m','pytest','-q','-p','no:warnings','-rA']+ids
    r=subprocess.run(cmd,cwd=sw,capture_output=True,text=True); dur=time.time()-t0
    last=[l for l in r.stdout.strip().splitlines() if ' passed' in l or ' failed' in l or 'error' in l][-1]
    name=f"{evid}-{cp.lower()}-{'regresion' if tipo=='Regresión' else 'pytest'}.txt"
    (ev/name).write_text(f"EVIDENCIA {evid} — {cp} ({tipo})\nFecha: {start}\nCommit: {commit}\nEntorno: {env}\nComando: cd 01_Software && {' '.join(cmd[1:])}\nCódigo de salida: {r.returncode}\n\n{r.stdout}{r.stderr}")
    out.append(dict(ev=evid,cp=cp,tipo=tipo,start=start,commit=commit,env=env,rc=r.returncode,resumen=last,dur=round(dur,2),file=name))
    print(cp,tipo,r.returncode,last)
json.dump(out,open(root/'04_Evidencias'/'ejecucion_automatizada_resumen.json','w'),ensure_ascii=False,indent=1)
