--WAF Action
require 'config'
require 'lib'

--args
local rulematch = ngx.re.find

--allow white ip
function white_ip_check()
     if config_white_ip_check == "on" then
        local IP_WHITE_RULE = get_rule('whiteip.rule')
        local WHITE_IP = get_client_ip()
        if IP_WHITE_RULE ~= nil then
            for _,rule in pairs(IP_WHITE_RULE) do     --标准库提供了集中迭代器，包括迭代文件每行的(io.lines)，迭代table元素的(pairs)
                if rule ~= "" and rulematch(WHITE_IP,rule,"jo") then    --返回的是匹配的字串的起始位置索引和结束位置索引，如果没有匹配成功，那么将会返回两个nil，如果匹配出错，还会返回错误信息到err中。
                    log_record('White_IP',ngx.var_request_uri,"_","_")    --Lua认为false和nil为假，true和非nil为真。要注意的是Lua中 0 为 true：  
                    --ngx.print("function white_ip_check()  done  <br/>")
		    return true                           
                end
            end
        end
    end
end

--deny black ip
function black_ip_check()
     if config_black_ip_check == "on" then
        local IP_BLACK_RULE = get_rule('blackip.rule')
        local BLACK_IP = get_client_ip()
        if IP_BLACK_RULE ~= nil then
            for _,rule in pairs(IP_BLACK_RULE) do
                if rule ~= "" and rulematch(BLACK_IP,rule,"jo") then
                    log_record('BlackList_IP',ngx.var_request_uri,"_","_")
                    if config_waf_enable == "on" then
--			ngx.print("waf_output() begin <br/>")
                        waf_output()
--			ngx.print("waf_output() done <br/>")
                        return true
                    end
                end
            end
        end
    end
end


--deny cc attack
function cc_attack_check()
    if config_cc_check == "on" then
        local ATTACK_URI=ngx.var.uri
        local CC_TOKEN = get_client_ip()..ATTACK_URI
        local limit = ngx.shared.limit
        CCcount=tonumber(string.match(config_cc_rate,'(.*)/'))
        CCseconds=tonumber(string.match(config_cc_rate,'/(.*)'))
        local req,_ = limit:get(CC_TOKEN)
        if req then
            if req + 1 > CCcount then
                log_record('CC_Attack',ngx.var.request_uri,"-","-")
                if config_waf_enable == "on" then
                    ngx.exit(403)
                end
            else
                limit:incr(CC_TOKEN,1)
            end
        else
            limit:set(CC_TOKEN,1,CCseconds)
        end
    end
    return false
end



function AI_check()
    --提取数据
--    ngx.print("function AI_check()  begin  <br/>")
    local t_content_length=ngx.req.get_headers()['content-length']
--    ngx.print("my_test***************t_content_length <br/>")
--    ngx.print(t_content_length)
    local t_src_port = ngx.var.remote_port
    local t_uri =  ngx.var.uri
    local t_src_ip = ngx.var.remote_addr 
    local t_host =  ngx.var.host
    local t_referer = ngx.var.http_referer
    local t_user_agent = ngx.var.http_user_agent
    local t_content_type = ngx.var.content_type       
    local t_dst_ip = ngx.var.server_addr   
    local t_cookie = ngx.var.http_cookie
    local t_dst_port = ngx.var.server_port
    local t_data = ""
    if "POST" == request_method then
        ngx.req.read_body()
        t_data = ngx.req.get_body_data()
    end
    local t_method = ngx.var.request_method

    
    if t_content_length == nil then t_content_length = '' end
    if t_src_port == nil then t_src_port = '' end
    if t_uri == nil then t_uri = '' end
    if t_src_ip == nil then t_src_ip = '' end   
    if t_host == nil then t_host = '' end 
    if t_referer == nil then t_referer = '' end
    if t_user_agent == nil then t_user_agent = '' end
    if t_content_type == nil then t_content_type = '' end
    if t_dst_ip == nil then t_dst_ip = '' end
    if t_cookie == nil then t_cookie = '' end
    if t_dst_port == nil then t_dst_port = '' end
    if t_method == nil then t_method = '' end
    if t_data == nil then t_data = '' end

    local t_data_id = tostring(ngx.now())

    local cjson = require "cjson"
    local io = require 'io'
    local data_obj = {
	data_id = t_data_id,

	http_type = "Request",
	content_length = t_content_length,
	src_port = t_src_port,
	url = t_uri,
	src_ip = t_src_ip,
	host = t_host,
	referer = t_referer,
	user_agent = t_user_agent,
	content_type = t_content_type,
	dst_ip = t_dst_ip,
	cookie = t_cookie,
	dst_port = t_dst_port,
	data = t_data,
	method = t_method,
    }
    local data_json = cjson.encode(data_obj)
    local data_path = config_lua_out_dir..'/'..'data.json'
--    ngx.print(data_path.."<br/>")
    local file = io.open(data_path, "a")
    if file == nil then
--	ngx.print("if file == nil then  <br/>")
        return
    end
    file:write(data_json.."\n")
    file:flush()
    file:close()

--os模块执行检测
--    local ex_out1 = os.execute("cd /usr/local/openresty/nginx/conf/waf/my_dir")
--    local ex_out2 = os.execute("python my_detection.py -i "..t_data_id)
--    ngx.print("my_test*******os.execute done <br/>")
--    ngx.print(ex_out1.." <br/>"..ex_out2.." <br/>")
--    ngx.print(ex_out2.." <br/>")
    ngx.print(t_data_id.." <br/>")
    local cmd = "python /usr/local/openresty/nginx/conf/waf/my_dir/my_detection.py -i "..t_data_id
    local f_t = io.popen(cmd)
--    ngx.print(f_t)
    ngx.print(f_t:read("*a").."<br/>")
    ngx.print("*************f_t done  <br/>")


--从detection_out_data_path读取结果   "/my_detection_out_data.json"
    local check_flag 
    local file = io.open(detection_out_data_path ,"r"); 
    local abnormal_info = {} 
    for line in file:lines() do  
        local data = cjson.decode(line) 
	ngx.print(data.data_id)    --拿不到本次的，只拿到上一次的
	ngx.print("<br/>")
	if data.data_id == t_data_id and data.data_type == "parameter_abnormal"then
	    check_flag = "parameter_abnormal"
            
--          data["p_name"] = model_d["p_name"]
--          data["p_type"] = model_d["p_type"]
--          data["p_profile"] = profile
--          data["score"] = score
--          准备保存相关数据到日志中
            
            if data.p_name == nil then data.p_name = '' end            
            if data.p_type == nil then data.p_type = '' end
            if data.p_profile == nil then data.p_profile = '' end
            if data.score == nil then data.score = '' end

            abnormal_info["p_name"] = data.p_name
            abnormal_info["p_type"] = data.p_type
            abnormal_info["p_profile"] = tostring(data.p_profile)
            abnormal_info["score"] = tostring(data.score)

	elseif data.data_id == t_data_id and data.data_type == "parameter_normal"then     
            check_flag = "parameter_normal"
        elseif data.data_id == t_data_id and data.data_type == "model_not_exist"then 
            check_flag = "model_not_exist"
	end  
    end  
    file:close()
    
    ngx.print(check_flag)
    ngx.print("********check_flag   <br/>")
    

    if check_flag == "parameter_abnormal" then
	log_record('AI_check_parameter_abnormal',ngx.var_request_uri,abnormal_info,"_")
            if config_waf_enable == "on" then
                ngx.print("waf_output() begin <br/>")
                waf_output()
                ngx.print("waf_output() done <br/>")
                return true
            end
    elseif check_flag == "model_not_exist" then
        log_record('AI_check_model_not_exist',ngx.var_request_uri,"_","_")
        if config_waf_enable == "on" then
            ngx.print("waf_output() begin <br/>")
            waf_output()
            ngx.print("waf_output() done <br/>")
            return true
        end

    else
        ngx.print("function AI_check()  done  </br>")
        return false    --表明没问题
    end
   
end







