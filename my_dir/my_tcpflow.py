#coding=utf-8
# data = {'content_length': 43,
#         # 服务器通过这个头，告诉浏览器回送数据的长度 HTTP消息实体的传输长度 消息实体长度和消息实体的传输长度是有区别
#         'status': '',
#         # 1xx - 信息提示 2xx - 成功 3xx - 重定向 4xx - 客户端错误 5xx - 服务器错误
#         'src_port': '59474',
#         'cookie': 'JSESSIONID%3Da449d6d0-a91d-4db4-a619-ed55239675e9%3B%20socm4ia%3D33SdLeElYV-1ES4bZEzfJ2msWUzGyf8G%257Cguoweibo01.3QGvYoBnZm98bE%252B6w%252B6e1RMN%252BY6x1H4YjY%252FQ5lfKKZU%3B%20connectId%3Ds%253A33SdLeElYV-1ES4bZEzfJ2msWUzGyf8G.8AqrleZu1lQY%252BvV2sakGkiUNdtcyB6WNYf1HfK%252FaPpA%3B%20socm4ts%3D0p4JtcIKKScCOzTN1ZJ_0kCoUVelMBsu%257Cguoweibo01.1zRT7PIXe9CrS2Pn5kBTCQsKpwPydoKf0KaieeHD1I8%3B%20tsConnectId%3Ds%253A0p4JtcIKKScCOzTN1ZJ_0kCoUVelMBsu.7Z7vNkjVarRmFz0czSHUxEoMNzXnE69iYXxJWnKSkds',
#         # 通过HTTP请求报文头的Cookie属性的jsessionid的值 让服务端知道客户端的多个请求是隶属于一个Session
#         'uri': '/portal/logins/checklogin',
#         'http_type': 'Request',
#         'server': '',
#         # 服务器通过这个头，告诉浏览器服务器的类型
#         'src_ip': '192.168.126.131',
#         'host': '10.10.10.1:8888',
#         # 客户机通过这个头告诉服务器，想访问的主机名
#         'referer': 'http://10.10.10.1:8888/portal/logins/login',
#         # 表示这个请求是从哪个URL过来的
#         'flow_time': 1493966490L,
#         'content_type': 'text/xml',
#         # 服务器通过这个头，回送数据的类型
#         # 告诉客户机，返回响应的时间。
#         'date': '',
#         # 客户机通过这个头告诉服务器，客户机当前请求时间
#         'dst_ip': '10.10.10.1.180',
#         'dst_port': '8888',
#         'data': '%3Croot%3E%3Cheader%3E%3Ctype%3Efetch%3C/type%3E%3C/header%3E%3Ccontent%3E%3Cprogram%3Etest%3C/program%3E%3C/content%3E%3C/root%3E',
#         'method': 'POST',
#         'user_agent': ' Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
#         # 客户机通过这个头告诉服务器，客户机的软件环境



from __future__ import print_function
from optparse import OptionParser
import tempfile,os,threading,pyinotify,urllib,json,logging
from multiprocessing import Process,Queue
import json
# from elasticsearch import Elasticsearch,TransportError
# from kafka import KafkaProducer

out_data_path = "/my_tcpflow_out_data.json" 
#要抓取某个服务器的流量
target_ip = "125.039.052.026"

def main():
    #Set loger
    global logger
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)
    logconsole=logging.StreamHandler()
    logconsole.setLevel(logging.INFO)
    formater=logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    logconsole.setFormatter(formater)
    logger.addHandler(logconsole)
    # Set tcpflow path
    tcpFlowPath = "/usr/local/bin/tcpflow"
    parser=OptionParser(usage="Usage:python %prog [options]")
    parser.add_option("-a","--args",dest="tcpflow_args",help='tcpflow options,Example:-a "-i eth0 port 80"',default="-i eth0 port 80",type="string")
    # parser.add_option("-e","--elasticsearch",dest="es",help="elasticsearch server ip,ip:port",type="string")
    # parser.add_option("-i", "--index", dest="index", help="elasticsearch index name", type="string")
    # parser.add_option("-t", "--type", dest="type", help="elasticsearch type name", type="string")
    # parser.add_option("-k","--kafka",dest="kafka",help="kafka server ip,ip:port",type="string")
    # parser.add_option("-T","--topic",dest="topic",help="kafka topic name",type="string")
    parser.add_option("-s", "--screen", dest="screen", help="Out data to screen,True or False", default=True)
    parser.add_option("-l","--log",dest="log",help="log file",default="/my_log", type="string")
    (options,args)=parser.parse_args()
    print("my_test******" + options.tcpflow_args)
    if not options:
        parser.print_help()
    tcpflow_args=options.tcpflow_args
    if options.log:
        logfile=logging.FileHandler(options.log,mode="w")
        logfile.setLevel(logging.INFO)
        logfile.setFormatter(formater)
        logger.addHandler(logfile)
        logger.info("[+]Write log in :%s"%options.log)
    queue = Queue()
    # if [bool(options.es),bool(options.kafka),options.screen].count(True)>1:
    #     logger.critical("[-]Data connot be written to Es/Kafka/Screen at the same time!")
    #     exit()
    # #子进程，处理数据到es\kafka\screen
    # elif options.es:
    #     if not options.index or not options.type:
    #         logger.critical("[-]Missing index or type name!")
    #     threadES=Process(target=processES,args=(queue,options.es,options.index,options.type))
    #     threadES.start()
    # elif options.kafka:
    #     threadKafka=Process(target=processKafka,args=(queue,options.kafka,options.topic))
    #     threadKafka.start()
    # elif options.screen:
    if options.screen:
        logger.info("[+]Out data to screen!")
        threadScreen=Process(target=processScreen,args=(queue,))
        threadScreen.start()
    elif not options.screen:
        logger.critical("[-]Missing variable:-e or -k or -s")
        exit()

    #子线程，开启并监控TCPFLOW
    tempDir=tempfile.mkdtemp()    #创建一个临时文件夹。它返回临时文件夹的绝对路径。
    logger.info("[+]TempDir:%s"%tempDir)
    threadPacp=threading.Thread(target=processPcap,args=(tempDir,tcpFlowPath,tcpflow_args))
    threadPacp.start()
    print('my_test******主进程，监控文件并生成数据')
    #主进程，监控文件并生成数据
    wm=pyinotify.WatchManager()  # 创建WatchManager对象
    wm.add_watch(tempDir,pyinotify.ALL_EVENTS)  # 添加要监控的目录，以及要监控的事件，这里ALL_EVENT表示所有事件

    eventHandler=MonitorFlow(queue)
    notifier=pyinotify.Notifier(wm,eventHandler)  # 交给Notifier进行处理
    notifier.loop()                    # 循环处理事件

    print('my_test******done')

#启动Tcpflow的进程
# tcpflow是Linux常用的命令行抓包工具
def processPcap(temDir,tcpFlowPath,tcpflow_args):
    if tcpflow_args:
        tcpflow_args=tcpflow_args.replace('"','')
        logger.info("[+]TcpFlow Command:cd %s && %s -a -e http -Ft %s"%(temDir,tcpFlowPath,tcpflow_args))
        # tcpflow_args: -i eth0 port 80   tcpFlowPath: /usr/bin/tcpflow    ??? -a -e
    output=os.popen("(cd %s && %s -a -e http -Ft %s)"%(temDir,tcpFlowPath,tcpflow_args))
#    output=os.popen("(cd %s && %s %s)"%(temDir,tcpFlowPath,tcpflow_args))
    logger.info("[+]TcpFlow UP!")
    output.read()
    logger.info("[-]Error:TcpFlow Down!")      #???

# #写入数据到ES的进程
# def processES(queue,es_host,index,type):
#     es=ES(es_host)
#     while True:
#         record=queue.get()
#         es.write_to_es(index,type,record)
# #写入数据到kafka的进程
# def processKafka(queue,kafka_host,topic):
#     kafka=Kafka(kafka_host)
#     while True:
#         record=json.dumps(queue.get())
#         kafka.Send_to_kafka(record,topic)

#输出数据到屏幕的进程
def processScreen(queue):
    while True:
	data = queue.get()
	print("my_test*************************print(queue.get())")
        print(data)
	#保存数据
        with open(out_data_path, 'a') as f:
            data_str = json.dumps(data)
            f.write(data_str + "\n")


#获取本机ip
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



#监控流文件，并提取数据
class MonitorFlow(pyinotify.ProcessEvent):  # 定制事件, 继承ProcessEvent类，自定义 process_事件名(self,event) 函数
    def __init__(self, queue,pevent=None, **kargs):
        self.queue=queue
        self.pevent = pevent
        self.my_init(**kargs)    #???
    def process_IN_CLOSE_WRITE(self,event):     # 一个打开且等待写入的文件或者目录被关闭  ???
        print("my_test*******************process_IN_CLOSE_WRITE")
	data=[]
        try:
	    print("my_test*******event.pathname:" + event.pathname + "***type***" + str(type(event.pathname)))
            file=open(event.pathname)
            firstLine=file.readline()
	    print("my_test***********************type(firstLine)")
	    print(type(firstLine))
	    print("my_test******firstLine(request_or_response):" + firstLine)
            file.close()
#	    my_ip = get_ip()
	    my_ip = target_ip
	    print("my_test*******ip:" + my_ip + "***type***" + str(type(my_ip)))
	    if my_ip not in event.pathname:
		print("my_test****** my_ip not in event.pathname")
		os.remove(event.pathname)
		return
            if firstLine[0:4] in ("GET ", "POST"):
                file = open(event.pathname)
                print("my_test_requestData_begin*****************************************")
		data = self.RequestHandler(file)
		print(data)
                print("my_test_requestData_end*******************************************")
		file.close()
            #elif firstLine[0:9]=="HTTP/1.1 " and \
            #                " Connection " not in firstLine:
            #    file = open(event.pathname)
	    #	print("my_test_responseData***********************************************")
            #    data=self.ResponseHandler(file)
	    #	print(data)
	    #	print("my_test_responseData***********************************************")
            #    file.close()
            os.remove(event.pathname)  #删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。
        except (IOError,OSError):
            pass
        if len(data)>0:
            # Get src_ip src_port dst_ip dst_port From filename
            #add to data
            filename = event.pathname.split("/")[-1]
            [flow_time, ip_port] = filename[0:54].split("T")[0:2]
            flow_time = long(flow_time)
            [src, dst] = ip_port.split("-")
            src = src.split(".")
            dst = dst.split(".")
            src_port = str(int(src[4]))
            dst_port = str(int(dst[4]))
            src_ip = "%s.%s.%s.%s" % (str(int(src[0])), str(int(src[1])), str(int(src[2])), str(int(src[3])))
            dst_ip = "%s.%s.%s.%s" % (str(int(dst[0])), str(int(dst[1])), str(int(dst[2])), str(int(dst[3])))
            for i in range(len(data)):         #???
                data[i]["src_ip"] = src_ip
                data[i]["dst_ip"] = dst_ip
                data[i]["src_port"] = src_port
                data[i]["dst_port"] = dst_port
#                data[i]["flow_time"] = flow_time
        for d in data:
            d=self.FillEmpty(d)
            self.queue.put(d)
    #http请求文件处理
    def  RequestHandler(self,file):
        data=[]
        post=False
        #Get data From File Content
        for line in file.readlines():
            print("my_test_195_for line in file.readlines():*****************")
	    print(line)    
      	    if line[0:4]=="GET ":
                d={}
                d["http_type"]="Request"
                d["method"]="GET"
                #d["uri"]=urllib.quote(line.split()[1])  #url转义
		#d["uri"]=line.split()[1]
		d["url"]=line.split()[1]
            elif line[0:5]=="POST ":
                d={}
                d["http_type"] = "Request"
                d["method"]="POST"
                #d["uri"] = urllib.quote(line.split()[1])
		#d["uri"] = line.split()[1]
		d["url"] = line.split()[1]
            elif line[0:6]=="Host: ":
                d["host"]=line[6:-2]    #??? d = {}
            elif line[0:12]=="User-Agent: ":
                d["user_agent"]=line[12:-2]    
            elif line[0:8]=="Cookie: ":
                #d["cookie"]=urllib.quote(line[8:-2])
		d["cookie"]=line[8:-2]
            elif line[0:9]=="Referer: ":
                d["referer"]=line[9:-2]
            elif line[0:16]=="Content-Length: ":
                d["content_length"]=int(line[16:-2])
            elif line[0:14]=="Content-Type: ":
                d["content_type"]=line[14:-2]
            elif line=="\r\n":      #???
                if d["method"]=="GET":
                    data.append(d)
                elif d["method"]=="POST":
                    post=True
            else:                   #???
                if post:
                    s=line.split("GET ")
                    if len(s)>1:
                        #d["data"]=urllib.quote(s[0])
			d["data"]=s[0]
                        data.append(d)
                        d={}
                        d["method"] = "GET"
                        d["http_type"] = "Request"
                        #d["uri"] = urllib.quote(s[-1].split()[0].strip())
                        #d["uri"] = s[-1].split()[0].strip()
			d["url"] = s[-1].split()[0].strip()
			post=False
                    else:
                        s=line.split("POST ")
                        if len(s) > 1:
                            #d["data"] = urllib.quote(s[0])
			    d["data"]=s[0]
                            data.append(d)
                            d = {}
                            d["method"] = "POST"
                            d["http_type"] = "Request"
                            #d["uri"] = urllib.quote(s[-1].split()[0].strip())
			    #d["uri"] = s[-1].split()[0].strip()
			    d["url"] = s[-1].split()[0].strip()
                            post = False   #???
                        else:
                            #d["data"]=urllib.quote(line[:-2])
			    d["data"]=line[:-2]
                            data.append(d)
                            post=False   #???
        return data
    def FillEmpty(self,data):
        #对数据没有的字段补空
        fields=['referer', 'http_type', 'host', 'cookie',
#               'flow_time', 'src_port', 'uri', 'src_ip',
                'src_port', 'url', 'src_ip',
	        'dst_port', 'dst_ip', 'method', 'user_agent',
#                "content_type","content_length","status","server",
                "content_type","content_length",
#		"date","data"]
		"data"]

        keys=data.keys()
        empty_field=list(set(fields)^set(keys))
        for e in empty_field:
            data[e]=""
        return data
    #响应数据文件处理
    def ResponseHandler(self,file):
        data=[]
        d={}
        response=False   #???
        while True:
            line=file.readline()
            if line[0:9]=="HTTP/1.1 ":
                if len(d)>0:
                    data.append(d)      #???
                    d={}
                    response=False
                d["http_type"]="Response"
                d["status"]=line.split()[1]
            elif line[0:8]=="Server: ":
                d["server"]=line[8:]
            elif line[0:14]=="Content-Type: ":
                d["content_type"]=line[14:]
            elif line[0:16]=="Content-Length: ":
                d["content_length"]=line[16:]
            elif line[0:6]=="Date: ":
                d["date"]=line[6:]
            elif line=="\r\n":
                if not response:
                    response=True
            elif not line:
                data.append(d)
                break
        return  data
# class ES(object):
#     def __init__(self,es_host):
#         '''init Elastisearch connection'''
#         logger.info("[+]Elasticsearch connection success!")
#         self.es_connect=Elasticsearch(hosts=es_host)
#     def write_to_es(self,index_name,type_name,record):
#         '''create a new document '''
#         try:
#             self.es_connect.index(index_name,type_name,record)
#         except TransportError:
#             logger.critical("[-]No elasticsearch Index:%s"%index_name)
# class Kafka(object):
#     def __init__(self,kafka_host):
#         self.producer = KafkaProducer(bootstrap_servers=kafka_host)
#         logger.info("[+]Kafka connection success!")
#     def Send_to_kafka(self, record,topic):
#         self.producer.send(topic,record)

if __name__=="__main__":
    main()





