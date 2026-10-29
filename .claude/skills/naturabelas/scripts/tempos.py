import json,sys
a=json.load(open(sys.argv[1])); off=float(sys.argv[2]) if len(sys.argv)>2 else 0
ch,st,en=a["characters"],a["character_start_times_seconds"],a["character_end_times_seconds"]
words=[];cur="";s=None
for c,b,e in zip(ch,st,en):
    if c.isspace():
        if cur: words.append((cur,s,pe)); cur=""
        continue
    if not cur: s=b
    cur+=c; pe=e
if cur: words.append((cur,s,pe))
print(json.dumps([{"text":w,"start":round(s+off,3),"end":round(e+off,3)} for w,s,e in words],ensure_ascii=False))
