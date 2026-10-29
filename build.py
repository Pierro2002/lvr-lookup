"""Build a council-sourced, precomputed lookup; no formula estimates.
Usage: python build.py council-results.json [index.html]
Input rows: account, address, status, current, proposed, checked_at.
"""
import argparse,json,pathlib,collections
from decimal import Decimal,ROUND_HALF_UP
BASE=pathlib.Path(__file__).resolve().parent
def cents(x):return float(Decimal(str(x)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
def build(source,destination):
 records=json.loads(pathlib.Path(source).read_text());data=[];seen=set();counts=collections.Counter()
 for account,address,status,current,proposed,checked_at in records:
  if account in seen:raise ValueError(f'Duplicate account {account}')
  seen.add(account);counts[status]+=1;values=None
  if status=='ok':
   if current is None or proposed is None:raise ValueError('Missing council amounts')
   annual=cents(Decimal(str(current))-Decimal(str(proposed)))
   values=[current,proposed,annual,cents(abs(Decimal(str(annual)))/52),True]
  data.append([account,address,None,None,'',values,status])
 coverage=f"{counts['ok']:,} accounts with council amounts · {len(data)-counts['pending']:,} of {len(data):,} accounts checked. "
 coverage+='Full verification is underway; unchecked amounts are hidden.' if counts['pending'] else 'Full check complete. Accounts without a usable council result show no amount.'
 s=(BASE/'template.html').read_text().replace('__DATA__',json.dumps(data,separators=(',',':'),allow_nan=False).replace('<','\\u003c')).replace('__COVERAGE__',coverage)
 pathlib.Path(destination).write_text(s)
 print(json.dumps(dict(total=len(data),counts=dict(counts),bytes=len(s))))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('destination',nargs='?',default='index.html');a=p.parse_args();build(a.source,a.destination)
