import csv, sys
src, dst = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(src)))
def num(s):
    f = float(s)
    return str(int(f)) if f == int(f) else ('%.2f' % f).rstrip('0').rstrip('.')
lines = []
for a, s, cr, lr, ys, ws, lv, cv, pc in rows:
    lines.append('|'.join([a, num(cr), num(ys), str(int(float(lv))), str(int(float(cv)))]))
data = '\n'.join(lines)

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>LVR Savings - Wellington City</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f5f5f5;color:#333;padding:12px;max-width:600px;margin:0 auto}
h1{font-size:1.3em;text-align:center;padding:12px 0 4px;color:#1a5632}
.sub{text-align:center;font-size:.85em;color:#666;margin-bottom:16px}
.sb{position:sticky;top:0;background:#f5f5f5;padding:8px 0 12px;z-index:10}
input[type="text"]{width:100%;padding:14px 16px;font-size:1.1em;border:2px solid #ccc;border-radius:10px;outline:none;background:#fff}
input:focus{border-color:#1a5632}
.hint{font-size:.8em;color:#888;margin-top:4px;padding-left:4px}
.card{background:#fff;border-radius:12px;padding:16px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,.1);border-left:5px solid #ccc}
.card.w{border-left-color:#2d8a4e}
.card.l{border-left-color:#c0392b}
.addr{font-weight:600;font-size:1em;margin-bottom:2px}
.burb{font-size:.85em;color:#888;margin-bottom:10px}
.sr{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.sb2{text-align:center;flex:1}
.sl{font-size:.75em;color:#888;text-transform:uppercase;letter-spacing:.5px}
.sv{font-size:1.6em;font-weight:700}
.sv.p{color:#2d8a4e}.sv.n{color:#c0392b}
.dv{width:1px;height:40px;background:#e0e0e0}
.det{display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:.82em;color:#666;margin-top:10px;border-top:1px solid #eee;padding-top:10px}
.det span{display:flex;justify-content:space-between}
.det .lb{color:#999}.det .vl{font-weight:500;color:#333}
.nr{text-align:center;padding:40px 20px;color:#999;font-size:1.1em}
.ct{font-size:.8em;color:#888;margin-bottom:8px}
.sm{text-align:center;padding:60px 20px;color:#aaa}
.sm .ic{font-size:2.5em;margin-bottom:12px}
.ld{text-align:center;padding:40px;color:#888}
.ft{font-size:.75em;color:#999;text-align:center;padding:24px 8px 12px;line-height:1.5}
</style>
</head>
<body>
<h1>LVR Savings Calculator</h1>
<p class="sub">Wellington City &mdash; Total Annual Rates (incl. GST)</p>
<div class="sb">
  <input type="text" id="q" placeholder="Type an address..." autocomplete="off" autocapitalize="off">
  <div class="hint">e.g. "25 Collins" or "Aro Street"</div>
</div>
<div id="r"><div class="ld">Loading data...</div></div>
<p class="ft">Residential rating units only. Current rates are 2025/26 WCC + GWRC rates on 1 Sep 2024 valuations. Under LVR, the residential general rate and base sector rate are charged on land value instead of capital value, raising the same total; all other charges are unchanged.</p>

<script>
var D=[];
var RAW=`__DATA__`;

function init(){
  var lines=RAW.split("\n");
  var re=/,\s*([^,]*?)\s*(\d{4})?\s*$/;
  for(var i=0;i<lines.length;i++){
    var p=lines[i].split("|");
    if(p.length<5)continue;
    var cr=+p[1],ys=+p[2],lr=Math.round((cr-ys)*100)/100;
    var m=re.exec(p[0]);
    D.push({a:p[0],s:m?m[1]:"",cr:cr,lr:lr,ys:ys,ws:Math.round(ys/52*100)/100,lv:+p[3],cv:+p[4],pc:Math.round((lr/cr-1)*1000)/10});
  }
  RAW=null;
  document.getElementById("r").innerHTML='<div class="sm"><div class="ic">&#127968;</div>Start typing an address to see savings under Land Value Rates<br><br><small>'+D.length.toLocaleString("en-NZ")+' properties loaded</small></div>';
}

function fmt(v){
  var a=Math.abs(v);
  var s=a>=1000?a.toLocaleString("en-NZ",{minimumFractionDigits:0,maximumFractionDigits:0}):a.toFixed(2);
  return(v<0?"-":"")+"$"+s;
}

function render(m){
  var el=document.getElementById("r");
  if(!m){el.innerHTML='<div class="sm"><div class="ic">&#127968;</div>Start typing an address to see savings under Land Value Rates</div>';return}
  if(m.length===0){el.innerHTML='<div class="nr">No properties found</div>';return}
  var sh=m.slice(0,30);
  var h='<div class="ct">'+m.length.toLocaleString("en-NZ")+' result'+(m.length>1?'s':'')+(m.length>30?' (showing first 30)':'')+'</div>';
  for(var i=0;i<sh.length;i++){
    var p=sh[i];var w=p.ys>0;
    var lbl=w?"Saving":"Increase";
    var yv=Math.abs(p.ys),wv=Math.abs(p.ws);
    var vc=w?"p":"n";
    var sign=w?"":"+";
    h+='<div class="card '+(w?"w":"l")+'">'
      +'<div class="addr">'+p.a.replace(/\s+\d{4}$/,"")+'</div>'
      +'<div class="burb">'+p.s+'</div>'
      +'<div class="sr">'
      +'<div class="sb2"><div class="sl">'+lbl+' / Year</div><div class="sv '+vc+'">'+sign+' '+fmt(yv)+'</div></div>'
      +'<div class="dv"></div>'
      +'<div class="sb2"><div class="sl">'+lbl+' / Week</div><div class="sv '+vc+'">'+sign+' '+fmt(wv)+'</div></div>'
      +'</div>'
      +'<div class="det">'
      +'<span><span class="lb">Current rates</span><span class="vl">'+fmt(p.cr)+'</span></span>'
      +'<span><span class="lb">Under LVR</span><span class="vl">'+fmt(p.lr)+'</span></span>'
      +'<span><span class="lb">Land value</span><span class="vl">'+fmt(p.lv)+'</span></span>'
      +'<span><span class="lb">Capital value</span><span class="vl">'+fmt(p.cv)+'</span></span>'
      +'<span><span class="lb">Change</span><span class="vl">'+p.pc+'%</span></span>'
      +'</div></div>';
  }
  el.innerHTML=h;
}

var tid=null;
document.getElementById("q").addEventListener("input",function(){
  clearTimeout(tid);
  var q=this.value.trim().toLowerCase();
  if(q.length<2){render(null);return}
  tid=setTimeout(function(){
    var terms=q.split(/\s+/);
    var res=[];
    for(var i=0;i<D.length;i++){
      var addr=D[i].a.toLowerCase();
      var ok=true;
      for(var j=0;j<terms.length;j++){if(addr.indexOf(terms[j])<0){ok=false;break}}
      if(ok){var k=addr.indexOf(q);D[i].x=k===0?0:(k>0?1:2);res.push(D[i])}
    }
    res.sort(function(a,b){return a.x-b.x||b.ys-a.ys});
    render(res);
  },150);
});

setTimeout(init,50);
</script>
</body>
</html>
'''
open(dst, 'w').write(html.replace('__DATA__', data))
print(len(lines), 'rows ->', dst)
