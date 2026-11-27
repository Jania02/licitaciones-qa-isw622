(()=>{
const $=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e;};
const DESC=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value');

/* ---------- Desplegable propio (reemplaza <select>) ---------- */
function select(sel){
  if(sel._ui)return;sel._ui=true;
  const w=$('div','dd');sel.before(w);w.append(sel);sel.classList.add('dd-native');sel.tabIndex=-1;
  const b=$('button','dd-btn');b.type='button';const m=$('div','dd-menu');m.setAttribute('role','listbox');w.append(b,m);
  let foco=-1;
  const items=()=>[...m.children];
  const pinta=()=>{m.replaceChildren();[...sel.options].forEach((o,i)=>{const d=$('div','dd-item'+(o.selected?' sel':''),o.textContent);d.setAttribute('role','option');
    d.onmousedown=e=>{e.preventDefault();elige(i);};m.append(d);});
    b.textContent=sel.selectedOptions[0]?.textContent||'Seleccionar';};
  const elige=i=>{sel.selectedIndex=i;sel.dispatchEvent(new Event('change',{bubbles:true}));cierra();pinta();b.focus();};
  const abre=()=>{document.querySelectorAll('.dd.abierto').forEach(x=>x!==w&&x.classList.remove('abierto'));w.classList.add('abierto');foco=sel.selectedIndex;marca();m.children[foco]?.scrollIntoView({block:'nearest'});};
  const cierra=()=>w.classList.remove('abierto');
  const marca=()=>items().forEach((d,i)=>d.classList.toggle('foco',i===foco));
  b.onclick=()=>w.classList.contains('abierto')?cierra():abre();
  b.onblur=cierra;
  b.onkeydown=e=>{const n=items().length;
    if(['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();if(!w.classList.contains('abierto'))return abre();foco=Math.max(0,Math.min(n-1,foco+(e.key==='ArrowDown'?1:-1)));marca();m.children[foco]?.scrollIntoView({block:'nearest'});}
    else if(e.key==='Enter'||e.key===' '){e.preventDefault();w.classList.contains('abierto')&&foco>=0?elige(foco):abre();}
    else if(e.key==='Escape')cierra();};
  new MutationObserver(pinta).observe(sel,{childList:true,characterData:true,subtree:true});
  sel.addEventListener('change',pinta);
  sel.form?.addEventListener('reset',()=>setTimeout(pinta));
  pinta();
}

/* ---------- Selector de fecha y hora propio (reemplaza datetime-local) ---------- */
const MES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
const p2=n=>String(n).padStart(2,'0');
function fecha(inp){
  if(inp._ui)return;inp._ui=true;
  const w=$('div','dt');inp.before(w);w.append(inp);inp.classList.add('dd-native');inp.tabIndex=-1;
  const b=$('button','dd-btn');b.type='button';w.append(b);
  const pop=$('div','dt-pop');w.append(pop);
  let sel=null,vista=new Date();
  const lee=()=>{const v=DESC.get.call(inp);sel=v?new Date(v):null;if(sel&&isNaN(sel))sel=null;};
  const pinta=()=>{lee();b.textContent=sel?`${p2(sel.getDate())}/${p2(sel.getMonth()+1)}/${sel.getFullYear()}  ${p2(sel.getHours())}:${p2(sel.getMinutes())}`:'Seleccionar fecha y hora';};
  Object.defineProperty(inp,'value',{get(){return DESC.get.call(inp);},set(v){DESC.set.call(inp,v);pinta();},configurable:true});
  const guarda=()=>{DESC.set.call(inp,`${sel.getFullYear()}-${p2(sel.getMonth()+1)}-${p2(sel.getDate())}T${p2(sel.getHours())}:${p2(sel.getMinutes())}`);pinta();inp.dispatchEvent(new Event('change',{bubbles:true}));};
  const dibuja=()=>{
    pop.replaceChildren();
    const cab=$('div','dt-cab');const mv=d=>{const x=$('button','',d<0?'‹':'›');x.type='button';x.onmousedown=e=>{e.preventDefault();vista=new Date(vista.getFullYear(),vista.getMonth()+d,1);dibuja();};return x;};
    cab.append(mv(-1),$('span','',`${MES[vista.getMonth()]} ${vista.getFullYear()}`),mv(1));
    const g=$('div','dt-grid');['L','M','M','J','V','S','D'].forEach(d=>g.append($('span','',d)));
    const ini=(new Date(vista.getFullYear(),vista.getMonth(),1).getDay()+6)%7;
    for(let i=0;i<ini;i++)g.append($('span'));
    const dias=new Date(vista.getFullYear(),vista.getMonth()+1,0).getDate(),hoy=new Date();
    for(let d=1;d<=dias;d++){const x=$('button','',d);x.type='button';
      if(sel&&sel.getFullYear()===vista.getFullYear()&&sel.getMonth()===vista.getMonth()&&sel.getDate()===d)x.classList.add('sel');
      if(hoy.getFullYear()===vista.getFullYear()&&hoy.getMonth()===vista.getMonth()&&hoy.getDate()===d)x.classList.add('hoy');
      x.onmousedown=e=>{e.preventDefault();const base=sel||new Date(hoy.getFullYear(),hoy.getMonth(),hoy.getDate(),12,0);sel=new Date(vista.getFullYear(),vista.getMonth(),d,base.getHours(),base.getMinutes());guarda();dibuja();};g.append(x);}
    const h=$('div','dt-hora');
    const mk=(n,val,cb)=>{const s=document.createElement('select');for(let i=0;i<n;i++){const o=$('option','',p2(i));o.value=i;s.append(o);}s.value=val;s.onchange=()=>cb(+s.value);return s;};
    const hs=mk(24,sel?sel.getHours():12,v=>{sel=sel||new Date(vista.getFullYear(),vista.getMonth(),hoy.getDate());sel.setHours(v);guarda();});
    const ms=mk(60,sel?sel.getMinutes():0,v=>{sel=sel||new Date(vista.getFullYear(),vista.getMonth(),hoy.getDate());sel.setMinutes(v);guarda();});
    h.append(hs,$('span','',':'),ms);
    const ok=$('button','dt-ok','Listo');ok.type='button';ok.onmousedown=e=>{e.preventDefault();cierra();};
    pop.append(cab,g,h,ok);select(hs);select(ms);
  };
  const abre=()=>{lee();vista=sel?new Date(sel):new Date();dibuja();w.classList.add('abierto');};
  const cierra=()=>w.classList.remove('abierto');
  b.onclick=()=>w.classList.contains('abierto')?cierra():abre();
  document.addEventListener('mousedown',e=>{if(!w.contains(e.target))cierra();});
  b.onkeydown=e=>{if(e.key==='Escape')cierra();};
  inp.form?.addEventListener('reset',()=>setTimeout(pinta));
  pinta();
}

/* ---------- Diálogos propios (reemplazan confirm / prompt) ---------- */
function dialogo(texto,{input=false,valor='',ok='Aceptar'}={}){
  return new Promise(res=>{
    const f=$('div','modal-fondo'),m=$('div','modal');m.append($('p','',texto));
    let i=null;if(input){i=document.createElement('input');i.value=valor;m.append(i);}
    const bs=$('div','btns');const c=$('button','sec','Cancelar'),a=$('button','',ok);c.type=a.type='button';bs.append(c,a);m.append(bs);f.append(m);document.body.append(f);
    requestAnimationFrame(()=>f.classList.add('v'));(i||a).focus();
    const fin=v=>{f.classList.remove('v');setTimeout(()=>f.remove(),200);document.removeEventListener('keydown',k);res(v);};
    const k=e=>{if(e.key==='Escape')fin(input?null:false);if(e.key==='Enter')a.click();};document.addEventListener('keydown',k);
    c.onclick=()=>fin(input?null:false);a.onclick=()=>fin(input?i.value:true);f.onmousedown=e=>{if(e.target===f)c.click();};
  });
}
window.UI={confirm:t=>dialogo(t,{ok:'Confirmar'}),prompt:(t,v)=>dialogo(t,{input:true,valor:v,ok:'Guardar'})};

document.addEventListener('submit',async e=>{const f=e.target;if(f.dataset.confirm&&!f._ok){e.preventDefault();if(await UI.confirm(f.dataset.confirm)){f._ok=true;f.submit();}}},true);

const init=r=>{r.querySelectorAll('select:not(.dd-native)').forEach(select);r.querySelectorAll('input[type=datetime-local]').forEach(fecha);};
document.addEventListener('DOMContentLoaded',()=>{
  init(document);
  document.querySelectorAll('.barra nav a').forEach(a=>{if(a.getAttribute('href')===location.pathname)a.classList.add('activo');});
});
})();
document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('.nav-item').forEach(a=>{const h=a.getAttribute('href');if(h===location.pathname||(h!=='/'&&location.pathname.startsWith(h)))a.classList.add('activo');});});
