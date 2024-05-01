import os
import json
from dataclass import Abstract
###########load paper in vnexpress ###################
def load_vnexpress():
    path = os.getcwd()
    paper_path = path+"\\IRS_Course-master\\data\\vnexpress"
    list_dir = [paper_path]
    list_paper = []
    for p in list_dir:
        sps = os.listdir(p)
        for sp in sps:
            fp = os.path.join(p,sp)
            if os.path.isdir(fp):
                list_dir.append(fp)
            else:
                list_paper.append(fp)
    return list_paper


#### load paper in DANeS ################
def load_DANeS():
    path = os.getcwd()
    data_path = os.path.join(path, "DANeS-main\\raw_data")
    ldf = os.listdir(data_path)
    with open(os.path.join(data_path,ldf[0]),encoding='utf-8') as f:

        datas = json.load(f)
    idx = 1
    class_data = []
    for d in datas:
        title = d["text"]
        description = d["meta"]["description"]
        url = d["meta"]["uri"]
        class_data.append(Abstract(ID=idx, title=title, abstract=description, url=url))
        idx+=1
    return class_data
print(len(load_DANeS()))   
            
