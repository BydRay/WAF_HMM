#coding=utf-8

#从 source_data_path 一行一行的读取数据，一行数据为：tcpflow取到的一次HTTP请求的数据k-v
#输出训练好的每个参数对应的hmm模型到/my_models_data.json
from __future__ import print_function
from my_extractor import Extractor
import numpy as np
from hmmlearn import hmm
import json, pickle
import copy


min_train_num = 1
#source_data_path = '/my_source_data.json'
source_data_path = '/my_tcpflow_out_data.json'
models_data_path = '/my_models_data.json'
#训练的数据的dst_ip 改成自己搭的服务器的地址
my_dst_ip = "10.108.36.213"

def extract(data):
    flat_data = []
    parameters=Extractor(data).parameter
    for (key,value) in parameters.items():
        flat_data.append({key:value})

    return flat_data   #[{key(参数md5):value({'p_type': 'post', 'p_name': 'qt', 'p_state':[[65], [65] ] })}, { },]


class Trainer(object):
    def __init__(self,data):
        self.p_id=data["p_id"]
        self.p_state=data["p_states"]
        # data["p_states"] = [ [[65], [65] ], [...] ]
    def get_model(self):
        self.train()
        self.get_profile()
        return (self.model,self.profile)
    def train(self):
        Hstate_num=range(len(self.p_state))  #同一个 p_id ， 每一条数据不重复的观测序列的数目
        Ostate_num=range(len(self.p_state))  #同一个 p_id ， 每一条数据观测序列的数目
        Ostate = []   #观测状态序列 集
	print("my_test********************self.p_state")
	print(self.p_state)
        for (index,value) in enumerate(self.p_state):
            #value = [[78], [46], [78]]
            Ostate.append(value)
#	    print("my_test********************value")
#	    print(value)
#	    print("my_test*****************np.array(value).reshape(1,len(value))[0]")
#	    print(np.array(value).reshape(1,len(value))[0])
	    tmp_value = copy.deepcopy(value)
	    tmp_value.pop()
	    tmp_value.pop()
	    tmp_value.pop()
	    tmp_value.pop()   #删除后面的0 1 2 3
            Hstate_num[index]=len(set(np.array(tmp_value).reshape(1,len(tmp_value))[0]))  #set() 函数创建一个无序不重复元素集
            Ostate_num[index]=len(value)

        self.Ostate=Ostate
        #[ [[78], [46], [78]](一次http请求某一个参数泛化之后的数组) ， [另外一次http请求，但参数的md5一样] ,[ ]  , ]
        self.Hstate_num=Hstate_num     #参数md5  对应的参数的状态数
        #[ [ [ [78], [46], [78] ] ] , [ ] ]  -> [ 2 , ... ]
        self.n = int(round(np.array(Hstate_num).mean()))#隐藏状态数    #round()四舍五入  mean()求均值
        print("my_test******************隐藏状态数")
	print(self.n)
        model = hmm.MultinomialHMM(n_components = self.n, n_iter = 1000, tol = 0.01)
        print("my_test************************self.Ostate")
	print(self.Ostate)
	print("my_test************************Ostate_num")
        print(Ostate_num)

#	X1 = [[0.5], [1.0], [-1.0], [0.42], [0.24]]
#	X2 = [[2.4], [4.2], [0.5], [-0.24]]
#	X = np.concatenate([X1, X2])
#	print("my_test****************************X = np.concatenate([X1, X2])")
#	print(X)
        t_list = []
	for item in self.Ostate:
	    t_list = t_list + item        
	model.fit(np.array(t_list).reshape(-1, 1), lengths=Ostate_num)
#	model.fit(np.array(self.Ostate))

#	for i in range(len(self.Ostate)):
#	    model.fit(np.array(self.Ostate[i]))	
#	    print("my_test**************************m.startprob_")
#           print(model.startprob_)
#           print("my_test**************************m.transmat_")
#           print(model.transmat_)
#           print("my_test**************************m.emissionprob_")
#           print(model.emissionprob_)


        self.model=model
	print("my_test**************************m.startprob_")
        print(model.startprob_)
        print("my_test**************************m.transmat_")
        print(model.transmat_)
        print("my_test**************************m.emissionprob_")
        print(model.emissionprob_)



    def get_profile(self):
        scores=np.array(range(len(self.p_state)),dtype="float64")
        for (index,value) in enumerate(self.p_state):
            scores[index]=self.model.score(value)
        self.profile=float(scores.min())    # profile取观察序列的最小得分。
        self.scores=scores

    def re_train(self):
        score_mean=self.scores.mean()
        sigma=self.scores.std()
        if self.profile < (score_mean-3*sigma):
            index=self.scores.tolist().index(self.profile)
            self.p_state.pop(index)
            self.train()
            self.get_profile()
            self.re_train()

def FillEmpty(data):
        #对数据没有的字段补空
        fields=['referer', 'http_type', 'host', 'cookie',
               'flow_time', 'src_port', 'uri', 'src_ip',
               'dst_port', 'dst_ip', 'method', 'user_agent',
               "content_type","content_length","status","server",
                "date","data"]
        keys=data.keys()
        empty_field=list(set(fields)^set(keys))
        for e in empty_field:
            data[e]=""
        return data




def main():
    # 获取原始数据
    # 按照参数ID分组
    p_dict={}
    with open(source_data_path, 'r') as f:
        for line in f.readlines():
            http_line = json.loads(line.strip())
            if http_line["method"] in ("GET", "POST"):
                source_data = http_line
            else:
                continue

#	    source_data =  FillEmpty(source_data)

            # 格式化，
            # source_data["dst_ip"] = "10.108.36.213"
            source_data["dst_ip"] = my_dst_ip            

	    print("my_test************************source_data")
            print(source_data)			
            extracted_data = extract(source_data)
            # [{key(参数md5):value({'p_type': 'post', 'p_name': 'qt', 'p_state':[[65], [65] ] })}, { },]
            print("my_test************************extracted_data")
       	    print(extracted_data)
            for p in extracted_data:
                if p.keys()[0] not in p_dict.keys():
                    p_dict[p.keys()[0]]={}
		     #为了hmmlearn包中的一个未知错误，没一个观测状态加上0，1，2，3
                    tmp_state = p.values()[0]["p_state"] + [0,1,2,3]
                    p_dict[p.keys()[0]]["p_states"]=[tmp_state]
                    #p_dict[p.keys()[0]]["p_states"]=[p.values()[0]["p_state"]]
                    
                    p_dict[p.keys()[0]]["p_type"]=p.values()[0]["p_type"]
                    p_dict[p.keys()[0]]["p_name"] = p.values()[0]["p_name"]
                else:
		    #为了hmmlearn包中的一个未知错误，没一个观测状态加上0，1，2，3
                    tmp_state = p.values()[0]["p_state"] + [0,1,2,3]
		    p_dict[p.keys()[0]]["p_states"].append(tmp_state)
                    #p_dict[p.keys()[0]]["p_states"].append(p.values()[0]["p_state"])
    # p_dict={key(参数md5): {p_states : [... , ...], p_type : ..., p_name : ...,},
    #         key(参数md5): {...},
    #         ... }

    #检测是否满足最小训练数   几个 p_state
    for key in p_dict.keys():
        if len(p_dict[key]["p_states"]) < min_train_num:
            p_dict.pop(key)
	    continue
	for p_state in p_dict[key]["p_states"]:
	    if len(p_state) <= 4:   #因为有加上的0 1 2 3
#		print("my_test******************************p_dict.pop(key)")
#		print(key)
		p_dict.pop(key)
		break
    # 参数训练
    models = []
    trained_num = 0
    for p_id in p_dict.keys():
        data = {}
        data["p_id"] = p_id
        data["p_states"] = p_dict[p_id]["p_states"]
        # data["p_states"] = [ [[65], [65] ], [...] ]
        trainer = Trainer(data)
        (m, p) = trainer.get_model()  # modle and profile
	
        model = {}
        model["p_id"] = p_id
        model["p_type"] = p_dict[p_id]["p_type"]
        model["p_name"] = p_dict[p_id]["p_name"]
        model["model"] = pickle.dumps(m)
        model["profile"] = p
        models.append(model)
        trained_num += 1

    #保存训练结果
    with open(models_data_path, 'w') as f:
        str_json = json.dumps(models)
	f.write(str_json+'\n')


if __name__ =="__main__":
    main()
#    print(json.dumps("你好",ensure_ascii=False))
    print("done")
















