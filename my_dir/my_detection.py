#coding=utf-8
from __future__ import print_function
from my_extractor import Extractor
import json, pickle
from hmmlearn import hmm
import numpy as np
import optparse


models_data_path = '/my_models_data.json'
detection_out_data = '/my_detection_out_data.json'
data_doc_path = "/lua_out_dir/data.json"

def main(data_doc_path, data_id):
    # 从指定文件获取数据
    with open(data_doc_path, 'r') as f:
        for line in f.readlines():
            http_line = json.loads(line.strip())
            if http_line["method"] in ("GET", "POST") and http_line["data_id"] == data_id:
               source_data = http_line
            
        if len(source_data) == 0:
	    return        
    #格式化  处理 \/
    for key_t in source_data.keys():
	if "\/" in source_data[key_t]:
	    source_data[key_t] = source_data[key_t].replace("\/", "/")
    #格式化  因为curl 'host': '10.108.36.213' 变成测试所需的 "host": "news.qq.com"
#    source_data["host"] = "news.qq.com"

    print("my_test***********************source_data")
    print(source_data)

    #获取 models
    with open(models_data_path, 'r') as f:
        for line in f.readlines():
            models_data = json.loads(line.strip())  #一个数组

    model_keys = [0] * len(models_data)
    for index, model in enumerate(models_data):  #model 一个字典
        model_keys[index] = model["p_id"]

    #抽取参数
    parameters = Extractor(source_data).parameter  #一个字典
    print("my_test***************** parameters = Extractor(source_data).parameter")
    print(parameters)

    with open(detection_out_data, 'a') as f:
	print("my_test*************************model_keys")
        print(model_keys)
        for (p_id, p_data) in parameters.items():
            print("my_test*********************p_id")
            print(p_id)
            if p_id in model_keys:
                model_d = models_data[model_keys.index(p_id)]
#		print("my_test**********************type(model_d['model'])")
#		print(type(model_d["model"]))
		model_str = model_d["model"].encode('unicode-escape').decode('string_escape')
#               print("my_test**********************model_str")
#               print(type(model_str))
		model = pickle.loads(model_str)
                profile = model_d["profile"]
                score = model.score(np.array(p_data["p_state"]))
		
		print("my_test**********************profile and score")
		print(profile)
		print(score)
        	print("my_test**************************m.startprob_")
        	print(model.startprob_)
        	print("my_test**************************m.transmat_")
        	print(model.transmat_)
        	print("my_test**************************m.emissionprob_")
        	print(model.emissionprob_)
                
		if score < profile:
                    data = {}
		    data["data_id"] = data_id
                    data["data_type"] = "parameter_abnormal"
                    data["p_id"] = p_id
                    data["p_name"] = model_d["p_name"]
                    data["p_type"] = model_d["p_type"]
                    data["p_profile"] = profile
                    data["score"] = score
                    #保存检测结果到文件中
                    data_tmp = json.dumps(data)
		    f.write(data_tmp + "\n")
                    return
            else:
                data = {}
                data["data_id"] = data_id
                data["data_type"] = "model_not_exist"
                data_tmp = json.dumps(data)
                f.write(data_tmp + "\n")
                return
        data = {}
	data["data_id"] = data_id
        data["data_type"] = "parameter_normal"
	data_tmp = json.dumps(data)
        f.write(data_tmp + "\n")
        return

if __name__ =="__main__":
    #参数解析
    op=optparse.OptionParser()
    op.add_option("-i","--id",dest="data_id")
    options,args = op.parse_args()
    data_id = options.data_id   #唯一标识一次http请求的数据
    print("my_mytest**************data_id")
    print(data_id)
    
    main(data_doc_path, data_id)





