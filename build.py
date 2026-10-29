"""Build a standalone, precomputed rates lookup. Requires openpyxl.
Usage: python build.py path/to/canonical.xlsx [output/index.html]
"""
import argparse,json,pathlib,re
from decimal import Decimal,ROUND_HALF_UP
BASE=pathlib.Path(__file__).resolve().parent

def cents(n):return float(Decimal(str(n)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
def build(rows,destination):
    model=json.loads((BASE/'model.json').read_text());data=[];seen=set()
    for r in rows:
        account,address,lv,cv,category=r[:5]
        if account in seen:raise ValueError(f'Duplicate account {account}')
        seen.add(account);values=None
        if isinstance(lv,(int,float)) and isinstance(cv,(int,float)) and lv>=0 and cv>0 and not re.search('rural|farmland|vacant|derelict',category,re.I):
            official=model['verified'].get(str(account))
            current=official[0] if official else cents(cv*model['current'])
            proposed=official[1] if official else cents(lv*model['land']+cv*model['sector'])
            annual=cents(current-proposed)
            values=[current,proposed,annual,cents(Decimal(str(abs(annual)))/Decimal(52)),bool(official)]
        data.append([account,address,lv,cv,category,values])
    if not data:raise ValueError('No residential accounts found')
    def safe(value):return json.dumps(value,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
    s=(BASE/'template.html').read_text().replace('__DATA__',safe(data)).replace('__MODEL__',safe(model))
    pathlib.Path(destination).write_text(s)
    print(f'{len(data):,} precomputed residential accounts -> {destination}')

if __name__=='__main__':
    import openpyxl
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('workbook');p.add_argument('destination',nargs='?',default='index.html');args=p.parse_args()
    w=openpyxl.load_workbook(args.workbook,read_only=True,data_only=True)
    rows=([int(r[0]),str(r[1]),r[4],r[5],str(r[8])] for r in w['Residential Only'].iter_rows(min_row=2,values_only=True) if isinstance(r[0],(int,float)))
    build(rows,args.destination);w.close()
