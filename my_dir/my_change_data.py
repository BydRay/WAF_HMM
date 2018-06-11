#coding=utf-8
#import json
#with open("/my_source_data.json", "a")as f:
#    my_dict = {'content_length': 363, 'status': '', 'src_port': '5533', 'uri': '/online/setpoint', 'http_type': 'Request', 'server': '', 'src_ip': '10.108.39.194', 'host': 'task.browser.360.cn', 'referer': '', 'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE', 'content_type': 'application/x-www-form-urlencoded', 'dst_ip': '123.125.54.231', 'date': '', 'cookie': '__huid=11g3AIgZDC6qlrRA1gcHTxvitMSbtANbGA8GKc7nr5mDM=; __guid=132730903.2093671922316579000.1516245069310.37; __DC_gid=59612149.90150474.1516245354712.1516245354712.1; __gid=54771369.901120895.1520252993163.1520253002716.2; Q=u%3D360H3003731637%26n%3D%26le%3DAmp1BGH4AmpkWGDjpKRhL29g%26m%3D%26qid%3D3003731637%26im%3D1_t011655040b3ed000bf%26src%3D360se%26t%3D1; T=s%3D327f27f22a7d3473c0e8f236a139cc4c%26t%3D1516245626%26lm%3D%26lf%3D1%26sk%3Dbbc80f0a3526e86910f54b556054f408%26mt%3D1516245626%26rc%3D3%26v%3D2.0%26a%3D1', 'dst_port': '80', 'data': 'stamp=1524015665&qt=Q%3Du%3D360H3003731637%26n%3D%26le%3DAmp1BGH4AmpkWGDjpKRhL29g%26m%3D%26qid%3D3003731637%26im%3D1_t011655040b3ed000bf%26src%3D360se%26t%3D1%0D%0AT%3Ds%3D327f27f22a7d3473c0e8f236a139cc4c%26t%3D1516245626%26lm%3D%26lf%3D1%26sk%3Dbbc80f0a3526e86910f54b556054f408%26mt%3D1516245626%26rc%3D3%26v%3D2.0%26a%3D1&verify=b292f5613ece004212afe3487e888c', 'method': 'POST', 'flow_time': 1524014779L}
#    json.dump(my_dict, f)




import json
with open("/lua_out_dir/data.json", "w")as f:
	my_dict = {'content_length': 363, 'status': '', 'src_port': '5533', 'uri': '/online/select*/etpoint', 'http_type': 'Request', 'server': '', 'src_ip': '10.108.39.194', 'host': 'task.browser.360.cn', 'referer': '', 'user_agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE', 'content_type': 'application/x-www-form-urlencoded', 'dst_ip': '123.125.54.231', 'date': '', 'cookie': '__huid=11g3AIgZDC6qlrRA1gcHTxvitMSbtANbGA8GKc7nr5mDM=; __guid=132730903.2093671922316579000.1516245069310.37; __DC_gid=59612149.90150474.1516245354712.1516245354712.1; __gid=54771369.901120895.1520252993163.1520253002716.2; Q=u%3D360H3003731637%26n%3D%26le%3DAmp1BGH4AmpkWGDjpKRhL29g%26m%3D%26qid%3D3003731637%26im%3D1_t011655040b3ed000bf%26src%3D360se%26t%3D1; T=s%3D327f27f22a7d3473c0e8f236a139cc4c%26t%3D1516245626%26lm%3D%26lf%3D1%26sk%3Dbbc80f0a3526e86910f54b556054f408%26mt%3D1516245626%26rc%3D3%26v%3D2.0%26a%3D1', 'dst_port': '80', 'data': 'stamp=1524015665&qt=Q%3Du%3D360H3003731637%26n%3D%26le%3DAmp1BGH4AmpkWGDjpKRhL29g%26m%3D%26qid%3D3003731637%26im%3D1_t011655040b3ed000bf%26src%3D360se%26t%3D1%0D%0AT%3Ds%3D327f27f22a7d3473c0e8f236a139cc4c%26t%3D1516245626%26lm%3D%26lf%3D1%26sk%3Dbbc80f0a3526e86910f54b556054f408%26mt%3D1516245626%26rc%3D3%26v%3D2.0%26a%3D1&verify=b292f5613ece004212afe3487e888c', 'method': 'POST', 'flow_time': 1524014779L}
	json.dump(my_dict, f)
	






