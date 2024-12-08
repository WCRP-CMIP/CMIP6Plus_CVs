import glob,json


files = glob.glob("src-data/*/*.json")

for f in files:
    print(f)
    data = json.load(open(f,'r'))

    rewrite = False
    nd = {}
    for k,v in data.items():
    
        if isinstance(v,list) and len(v) == 1 and isinstance(v[0],dict):
            v = v[0]
            nd[k] = v
            
            rewrite = True
        
        if isinstance(v,dict):
            try:
                # if v.values are all empty dicts 
                if all([i == {} for i in v.values()]):
                    nd[k] = list(v.keys())
                    rewrite = True
                else:
                    nd[k] = v
                    
            except:
                pass
        else:
            nd[k] = v
            

    with open(f,'w') as out:
        if rewrite:
            print(f"Rewriting {f}")
            json.dump(nd,out,indent=2)
            