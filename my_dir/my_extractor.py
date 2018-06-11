#coding=utf-8
import urllib,operator,json


#import numpy as np

from xml.etree import ElementTree
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import urlparse
def get_payload(url):
    parser=urlparse.urlparse(url)
    # 从urlstring中取得URL，并返回元组 (scheme, netloc, path, parameters, query, fragment)
    # <fragment>不会发到web服务器上
    payload = parser.query
    return payload
def get_path(url):
    parser=urlparse.urlparse(url)
#<scheme>://<netloc>/<path>;<params>?<query>#<fragment>解析成一个6元组：(scheme, netloc, path, params, query, fragment)。
    return parser.path

import hashlib,chardet
def get_md5(s):
    md5= hashlib.md5()
    md5.update(s.encode("utf-8"))
    return md5.hexdigest()
def is_chinese(s):
    #s=s.decode("utf-8")
    if s>=u"\u4e00" and s<=u"\u9fa6":
        return True
    else:return False
def decode(s):
    if isinstance(s,type(u"")):
        return s
    encoding=chardet.detect(s)["encoding"]
    if encoding:
        return s.decode(encoding)
    else:
        return s.decode("utf-8")

class Extractor(object):
    def __init__(self,data):
        self.parameter={}
        self.data=data
        #self.url = urllib.unquote(data["url"].encode("utf-8"))  #urlencode逆向
	self.url = data["url"]
#       <scheme>://<user>:<password>@<host>:<port>/<path>;<params>?<query>#<fragment>

#        print("my_test******self.url:***** ")
#	print(self.url)
        #self.path = decode(get_path(self.url))
	self.path = get_path(self.url)
#        print("my_test******self.path: ********")
#	print(self.path)
        self.payload = get_payload(self.url).strip("?")   #去除首尾字符'?'  ???
#        print("my_test******self.payload: ************")
#	print(self.payload)

        self.get_parameter()
    def get_parameter(self):
        if self.payload.strip():  #去除首尾空格
#        if True:
            for (p_id,p_state,p_type,p_name) in self.query_f():
                #<query>内每一个参数名字  p_id=get_md5(self.data["host"]+self.path+decode(p_name)+self.data["method"])  改成 +p_type
                #p_type="query"
                self.parameter[p_id]={}
                self.parameter[p_id]["p_state"]=p_state
                self.parameter[p_id]["p_type"]=p_type
                self.parameter[p_id]["p_name"]=p_name
            (p_id,p_state,p_type,p_name)=self.query_p_name()
            #<query>内所有的参数名字符串拼接  p_id = get_md5(self.data["host"] + self.path + self.data["method"]+p_type)
            #p_type="query_pname"
            self.parameter[p_id] = {}
            self.parameter[p_id]["p_state"] = p_state
            self.parameter[p_id]["p_type"] = p_type
            self.parameter[p_id]["p_name"] = p_name
        if self.path.strip():
#        if True:
            (p_id,p_state,p_type,p_name)=self.path_p()
            #p_id=get_md5(self.data["host"]+self.data["method"]+p_type) 
	    #p_type="url_path"
            self.parameter[p_id] = {}
            self.parameter[p_id]["p_state"] = p_state
            self.parameter[p_id]["p_type"] = p_type
            self.parameter[p_id]["p_name"] = p_name

#        if self.data["http_type"].strip():
#            (p_id,p_state,p_type,p_name)=self.http_type()
#            # p_id = get_md5(self.data["host"] + self.path + http_type + self.data["method"])
#            # p_type="http_type"
#            self.parameter[p_id] = {}
#            self.parameter[p_id]["p_state"] = p_state
#            self.parameter[p_id]["p_type"] = p_type
#            self.parameter[p_id]["p_name"] = p_name

#        if self.data["content_length"]:
#            (p_id, p_state,p_type,p_name) = self.content_length()
#            #p_id = get_md5(self.data["host"] + self.path + content_length + self.data["method"])
#            #p_type="content_length"
#            self.parameter[p_id] = {}
#            self.parameter[p_id]["p_state"] = p_state
#            self.parameter[p_id]["p_type"] = p_type
#            self.parameter[p_id]["p_name"] = p_name

        if self.data["cookie"].strip():
#        if True:
            for (p_id,p_state,p_type,p_name) in self.cookie_f():
                #针对每一个键值对
                # p_id = get_md5(self.data["host"] + self.path + decode(p_name) + self.data["method"]+p_type)
                # p_type = "cookie"
                self.parameter[p_id] = {}
                self.parameter[p_id]["p_state"] = p_state
                self.parameter[p_id]["p_type"] = p_type
                self.parameter[p_id]["p_name"] = p_name
            (p_id,p_state,p_type,p_name)=self.cookie_p_name()
            # 针对所有键值对的key
            #p_id = get_md5(self.data["host"] + self.path + self.data["method"]+p_type)
            # p_type = "cookie_pname"
            self.parameter[p_id] = {}
            self.parameter[p_id]["p_state"] = p_state
            self.parameter[p_id]["p_type"] = p_type
            self.parameter[p_id]["p_name"] = p_name
        if self.data["data"].strip():
#        if True:
            p_names=""
            for (p_id, p_state, p_type, p_name) in self.post_f():
                #针对每一个键值对   三种编码方式
                #p_id = get_md5(self.data["host"] + self.path + decode(p_name) + self.data["method"]+p_type)
                #p_type = "post"

                self.parameter[p_id] = {}
                self.parameter[p_id]["p_state"] = p_state
                self.parameter[p_id]["p_type"] = p_type
                self.parameter[p_id]["p_name"] = p_name
                p_names+=p_name
            (p_id, p_state, p_type, p_name)=self.post_p_name(p_names)
            #p_id = get_md5(self.data["host"] + self.path + self.data["method"]+p_type)
            #p_type = "post_pname"
            self.parameter[p_id] = {}
            self.parameter[p_id]["p_state"] = p_state
            self.parameter[p_id]["p_type"] = p_type
            self.parameter[p_id]["p_name"] = p_name
    def get_Ostate(self,s):
        """
        字母 =》'A'
        数字 =》'N'
        中文 =》'C'
        特殊字符 =》'T'

        :param s:
        :return:
        """
        A=self.get_num('A')  #返回对应的 ASCII 数值，或者 Unicode 数值
        N=self.get_num("N")
        C=self.get_num("C")
	T=self.get_num("T")
        state=[]
        if not isinstance(s,unicode):  #一个对象是否是一个已知的类型
            s=decode(str(s))
        if len(s)==0:
        #空字符串取0
        #    state.append([0])

	#空串就等于空
            return state
        #s=str(s).decode("utf-8","ignore")
        for i in s:
            if i.encode("utf-8").isalpha():
                state.append(0)
            elif i.isdigit():
                state.append(1)
            elif is_chinese(i):
                state.append(2)
            else:
                state.append(3)
        return state
    def get_num(self,s):
        return ord(s)  #以一个字符（长度为1的字符串）作为参数，返回对应的 ASCII 数值，或者 Unicode 数值
    def query_f(self):
        for p in self.payload.split("&"):    
            p_list=p.split("=")
            p_name=p_list[0]
            if len(p_list)>1:
                p_value=reduce(operator.add,p_list[1:])   #对参数序列中元素进行累积
                p_type="query"
                p_id=get_md5(self.data["dst_ip"]+self.path+decode(p_name)+self.data["method"]+p_type)
                p_state=self.get_Ostate(p_value)
                yield (p_id,p_state,p_type,p_name)
    def path_p(self):
        p_state=self.get_Ostate(self.path)
        p_type="url_path"
	p_id=get_md5(self.data["dst_ip"]+self.data["method"]+p_type+self.path)
        p_name = self.path
        return (p_id,p_state,p_type,p_name)
    def post_f(self):
        #post_data=urllib.unquote(urllib.unquote(self.data["data"]))   #???urlencode逆向
        post_data=urllib.unquote(self.data["data"])
#	print('my_test*******post_data=urllib.unquote(self.data["data"])')
#	print(post_data)
        content_t=self.data["content_type"]
        def ex_urlencoded(post_data):
            for p in post_data.split("&"):
                p_list = p.split("=")
                p_name = p_list[0]
                if len(p_list) > 1:
                    p_type = "post"
                    p_value = reduce(operator.add, p_list[1:])
                    p_id = get_md5(self.data["dst_ip"] + self.path + decode(p_name) + self.data["method"]+p_type)
                    p_state = self.get_Ostate(p_value)
                    
                    yield (p_id, p_state, p_type, p_name)
        def ex_json(post_data):
            post_data=json.loads(post_data)
            for p_name,p_value in post_data.items():
                p_type = "post"
                p_id = get_md5(self.data["dst_ip"] + self.path + decode(p_name) + self.data["method"]+p_type)
                p_state=self.get_Ostate(str(p_value))
                
                yield (p_id, p_state, p_type, p_name)
        def ex_xml(post_data):
            tree=ElementTree.fromstring(post_data)
            elements=[]
            p_names=[]
            def get_item(tree,parent_tag=""):
                #树中只有叶子节点才有value
                if tree.getchildren():
                    if parent_tag:
                        parent_tag += "/" + tree.tag
                    else:
                        parent_tag = tree.tag
                    for t in tree.getchildren():
                        get_item(t,parent_tag)
                else:
                    elements.append(tree.text)
                    p_names.append(parent_tag+"/"+tree.tag)
            get_item(tree)
            for (p_name,p_value) in zip(p_names,elements):    # 对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表
                p_state=self.get_Ostate(p_value)
                p_type="post"
                p_id = get_md5(self.data["dst_ip"] + self.path + decode(p_name) + self.data["method"]+p_type)
                yield (p_id, p_state, p_type, p_name)
        if "application/x-www-form-urlencoded" in content_t:  #浏览器的原生 form 表单 Ajax 提交数据
            return ex_urlencoded(post_data)
        elif "application/json" in content_t:  #告诉服务端消息主体是序列化后的 JSON 字符串
            return ex_json(post_data)
        elif "text/xml" in content_t:   #XML 作为编码方式  请求体
            return ex_xml(post_data)
        else:return None
    def http_type(self):
        http_type=self.data["http_type"]
        p_id=get_md5(self.data["host"]+self.path+"http_type"+self.data["method"])

        p_state=self.get_Ostate(http_type)
        p_type="http_type"
        p_name=""
        return (p_id,p_state,p_type,p_name)
    def content_length(self):
        content_length=self.data["content_length"]
        p_id = get_md5(self.data["host"] + self.path + "content_length"+ self.data["method"] )

        p_state = self.get_Ostate(content_length)
        p_type="content_length"
        p_name=content_length
        return (p_id, p_state,p_type,p_name)
    def cookie_f(self):
        #cookies=urllib.unquote(self.data["cookie"].encode("utf-8"))
	cookies=self.data["cookie"]
#	print('my_test******cookies=self.data["cookie"])')
#	print(cookies)
        for p in cookies.split("; "):
            if p.strip():
                p_list=p.split("=")
                p_name=p_list[0]
                if len(p_list)>1:
                    p_type="cookie"
                    p_value=reduce(operator.add,p_list[1:])
                    p_id=get_md5(self.data["dst_ip"]+self.path+decode(p_name)+self.data["method"]+p_type)
                    p_state=self.get_Ostate(p_value)
                    yield (p_id,p_state,p_type,p_name)
    def query_p_name(self):
        p_name=""
        for p in self.payload.split("&"):
            p_name+=p.split("=")[0]
        p_state=self.get_Ostate(p_name)
        p_type="query_pname"
        p_id = get_md5(self.data["dst_ip"] + self.path + self.data["method"]+p_type)
        p_name=""
        return (p_id, p_state,p_type,p_name)
    def cookie_p_name(self):
        #cookie = urllib.unquote(self.data["cookie"].encode("utf-8"))
	cookie = self.data["cookie"]
        p_name=""
        for p in cookie.split("; "):
            if p.strip():
                p_name+=p.split("=")[0]
        p_type = "cookie_pname"
        p_id = get_md5(self.data["dst_ip"] + self.path + self.data["method"]+p_type)
        p_state = self.get_Ostate(p_name)
        p_name=""
        return (p_id, p_state,p_type,p_name)
    def post_p_name(self,p_names):
        p_state = self.get_Ostate(p_names)
        p_type = "post_pname"
        p_name = ""
        p_id = get_md5(self.data["dst_ip"] + self.path + self.data["method"]+p_type)
        return (p_id, p_state, p_type, p_name)



def main():
    #data={'content_length': 43, 'status': '', 'src_port': '59474', 'cookie': 'JSESSIONID%3Da449d6d0-a91d-4db4-a619-ed55239675e9%3B%20socm4ia%3D33SdLeElYV-1ES4bZEzfJ2msWUzGyf8G%257Cguoweibo01.3QGvYoBnZm98bE%252B6w%252B6e1RMN%252BY6x1H4YjY%252FQ5lfKKZU%3B%20connectId%3Ds%253A33SdLeElYV-1ES4bZEzfJ2msWUzGyf8G.8AqrleZu1lQY%252BvV2sakGkiUNdtcyB6WNYf1HfK%252FaPpA%3B%20socm4ts%3D0p4JtcIKKScCOzTN1ZJ_0kCoUVelMBsu%257Cguoweibo01.1zRT7PIXe9CrS2Pn5kBTCQsKpwPydoKf0KaieeHD1I8%3B%20tsConnectId%3Ds%253A0p4JtcIKKScCOzTN1ZJ_0kCoUVelMBsu.7Z7vNkjVarRmFz0czSHUxEoMNzXnE69iYXxJWnKSkds', 'url': '/portal/logins/checklogin', 'http_type': 'Request', 'server': '', 'src_ip': '192.168.126.131', 'host': '10.10.10.1:8888', 'referer': 'http://10.10.10.1:8888/portal/logins/login', 'flow_time': 1493966490L, 'content_type': 'text/xml', 'date': '', 'dst_ip': '10.10.10.1.180', 'dst_port': '8888', 'data': '%3Croot%3E%3Cheader%3E%3Ctype%3Efetch%3C/type%3E%3C/header%3E%3Ccontent%3E%3Cprogram%3Etest%3C/program%3E%3C/content%3E%3C/root%3E', 'method': 'POST', 'user_agent': ' Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
#    data ={'content_length': 363, 'status': '', 'src_port': '8232', 'url': '/online/setpoint', 'http_type': 'Request',
#     'server': '', 'src_ip': '10.108.39.194', 'host': 'task.browser.360.cn', 'referer': '',
#     'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE',
#     'content_type': 'application/x-www-form-urlencoded', 'dst_ip': '123.125.54.231', 'date': '',
#     'cookie': '__huid%3D11g3AIgZDC6qlrRA1gcHTxvitMSbtANbGA8GKc7nr5mDM%3D%3B%20__guid%3D132730903.2093671922316579000.1516245069310.37%3B%20__DC_gid%3D59612149.90150474.1516245354712.1516245354712.1%3B%20__gid%3D54771369.901120895.1520252993163.1520253002716.2%3B%20Q%3Du%253D360H3003731637%2526n%253D%2526le%253DAmp1BGH4AmpkWGDjpKRhL29g%2526m%253D%2526qid%253D3003731637%2526im%253D1_t011655040b3ed000bf%2526src%253D360se%2526t%253D1%3B%20T%3Ds%253D327f27f22a7d3473c0e8f236a139cc4c%2526t%253D1516245626%2526lm%253D%2526lf%253D1%2526sk%253Dbbc80f0a3526e86910f54b556054f408%2526mt%253D1516245626%2526rc%253D3%2526v%253D2.0%2526a%253D1',
#     'dst_port': '80',
#     'data': 'stamp%3D1523950159%26qt%3DQ%253Du%253D360H3003731637%2526n%253D%2526le%253DAmp1BGH4AmpkWGDjpKRhL29g%2526m%253D%2526qid%253D3003731637%2526im%253D1_t011655040b3ed000bf%2526src%253D360se%2526t%253D1%250D%250AT%253Ds%253D327f27f22a7d3473c0e8f236a139cc4c%2526t%253D1516245626%2526lm%253D%2526lf%253D1%2526sk%253Dbbc80f0a3526e86910f54b556054f408%2526mt%253D1516245626%2526rc%253D3%2526v%253D2.0%2526a%253D1%26verify%3D14e85aed1b2243aee8db5ce4e86a25',
#     'method': 'POST', 'flow_time': 1523949274L}

    data = {'content_length': 363, 'status': '', 'src_port': '5533', 'url': '/online/setpoint', 'http_type': 'Request', 'server': '', 'src_ip': '10.108.39.194', 'host': 'task.browser.360.cn', 'referer': '', 'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE', 'content_type': 'application/x-www-form-urlencoded', 'dst_ip': '123.125.54.231', 'date': '', 'cookie': '__huid=11g3AIgZDC6qlrRA1gcHTxvitMSbtANbGA8GKc7nr5mDM=; __guid=132730903.2093671922316579000.1516245069310.37; __DC_gid=59612149.90150474.1516245354712.1516245354712.1; __gid=54771369.901120895.1520252993163.1520253002716.2; Q=u%3D360H3003731637%26n%3D%26le%3DAmp1BGH4AmpkWGDjpKRhL29g%26m%3D%26qid%3D3003731637%26im%3D1_t011655040b3ed000bf%26src%3D360se%26t%3D1; T=s%3D327f27f22a7d3473c0e8f236a139cc4c%26t%3D1516245626%26lm%3D%26lf%3D1%26sk%3Dbbc80f0a3526e86910f54b556054f408%26mt%3D1516245626%26rc%3D3%26v%3D2.0%26a%3D1', 'dst_port': '80', 'data': 'stamp=1524015665&qt=Q%3Du%3D360H3003731637%26n%3D%26le%3DAmp1BGH4AmpkWGDjpKRhL29g%26m%3D%26qid%3D3003731637%26im%3D1_t011655040b3ed000bf%26src%3D360se%26t%3D1%0D%0AT%3Ds%3D327f27f22a7d3473c0e8f236a139cc4c%26t%3D1516245626%26lm%3D%26lf%3D1%26sk%3Dbbc80f0a3526e86910f54b556054f408%26mt%3D1516245626%26rc%3D3%26v%3D2.0%26a%3D1&verify=b292f5613ece004212afe3487e888c', 'method': 'POST', 'flow_time': 1524014779L}


    ps=Extractor(data).parameter
    #print ps
    for key in ps.keys():
        print(key + " ---------- ")
	print(ps[key])
        # if ps[key]["p_type"]=="post_pname":
        #     print ps[key]
if __name__ =="__main__":
    main()
