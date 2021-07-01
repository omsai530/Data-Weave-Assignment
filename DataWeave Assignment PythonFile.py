import json
from collections import Counter

with open('yesterday.json','r') as y:
    yes_data=[json.loads(rec) for rec in y]
    
with open('today.json','r') as t:
    tday_data=[json.loads(rec) for rec in t]


def is_type(x, t):
    try:
        t(x)
        return True
    except:
        return False

def to_type(data):
    for loaded_json in data:
        for k, v in loaded_json.items():
            if is_type(v, int):
                loaded_json[k] = int(v)
            elif is_type(v, float):
                loaded_json[k] = float(v)
            elif v == 'true':
                loaded_json[k] = True
            elif v == 'false':
                loaded_json[k] = False
    return data

y_data = to_type(yes_data)
t_data = to_type(tday_data)

for i in y_data:
    if i['available_price'] is None:
        i['available_price']=0
for i in t_data:
    if i['available_price'] is None:
        i['available_price']=0

## 1. Number of URLH which are overlapping (Common) in two files

y_urlh = {i['urlh']:i['available_price'] for i in y_data}
t_urlh = {i['urlh']:i['available_price'] for i in t_data}

comm_urlh = y_urlh.keys() & t_urlh.keys()
comm_count=len(comm_urlh)

print("Overlapping URLH's in both files :",comm_count)

## 2. For all the URLH which are overlapping, calculate the price difference (wrt available_price) if there is any between yesterday's and today's crawls (scraped data). There might be duplicate URLHs in which case you can choose the first valid (with http_status 200) record

price_diff = {i:(t_urlh[i]-y_urlh[i]) for i in comm_urlh}

price_diff

## 3. Number of Unique categories in both files.

yuniq_cat={i["category"] for i in y_data}
tuniq_cat={i["category"] for i in t_data}

print("Number of Unique Categories in Yesterday file are:",len(yuniq_cat))
print("Number of Unique Categories in Today file are:",len(tuniq_cat))

## 4. Display List of categories which is not overlapping (Common) from two given files.

print("List of Categories that are not common in two files are : ",list(yuniq_cat-tuniq_cat))

## 5. Generate the stats with count of urlh for all taxonomies (taxonomy is concatenation of category and subcategory separated by " > ") for today's file.

taxonamy = {cat:[i['subcategory'] for i in t_data if i['category'] == cat] for cat in tuniq_cat}

temp={}
for cat,sblst in taxonamy.items():
    a=dict(Counter(sblst))
    for i,j in a.items():
        temp[i]=j
        print(cat,">",i,":",j)

## 8. Display the top 5 subcategory having highest items.

top_subcat = sorted(temp.items(),key = lambda a:a[1], reverse = True)
for i,j in enumerate(top_subcat[:5]):
    print(i+1,'.',j[0],"-->",j[1],"items")

## 6. Generate a new file where mrp is normalized. If there is a 0 or a non-float value or the key doesn't exist, make it "NA".

y = y_data.copy()
with open("yes_mrp_data.json",'w', encoding='utf-8') as f:
    for dic in y:
        if dic['mrp'] == 0 or not isinstance(dic['mrp'],float) or dic.get('mrp')==None:
            dic['mrp'] = "NA"
        json.dump(dic, f, ensure_ascii=False, indent = 6)

t = t_data.copy()
with open("tday_mrp_data.json",'w', encoding='utf-8') as f:
    for dic in t:
        if dic['mrp'] == 0 or not isinstance(dic['mrp'],float) or dic.get('mrp')==None:
            dic['mrp'] = "NA"
        json.dump(dic, f, ensure_ascii=False, indent = 6)

## 7.  Display the title and price of 10 items having least price.

t1 = t_data.copy()
temp_dic={i['title']:i['available_price'] for i in t1 if i['title'] is not None}
temp_set=set(temp_dic.keys())
t1_dic={i:temp_dic[i] for i in t1_set}
dis_dic = dict(sorted(t1_dic.items(), key=lambda item: item[1]))

for i,j in enumerate(list(dis_dic.items())[:10]):
    print(i+1,'.',j[0],"-->",j[1])

## 9. Display stats of how many items have failed status (http_status other than 200 is to be considered as failure).

lst=[]
for rec in t_data+y_data:
    if rec['http_status'] != 200:
        lst.append(rec['http_status'])
http_fail_count = dict(Counter(lst))

print("http_status\t count")
for i,j in http_fail_count.items():
    print(i,'\t\t',j)