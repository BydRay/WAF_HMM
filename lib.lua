--waf core lib
require 'config'

--Get the client IP
function get_client_ip()
    CLIENT_IP = ngx.req.get_headers()["X_real_ip"]
    if CLIENT_IP == nil then
        CLIENT_IP = ngx.req.get_headers()["X_Forwarded_For"]
    end
    if CLIENT_IP == nil then
        CLIENT_IP  = ngx.var.remote_addr
    end
    if CLIENT_IP == nil then
        CLIENT_IP  = "unknown"
    end
    return CLIENT_IP
end

--Get WAF rule
function get_rule(rulefilename)
    local io = require 'io'
    local RULE_PATH = config_rule_dir
    local RULE_FILE = io.open(RULE_PATH..'/'..rulefilename,"r")  --??
    if RULE_FILE == nil then
        return
    end
    RULE_TABLE = {}
    for line in RULE_FILE:lines() do
        table.insert(RULE_TABLE,line)
    end
    RULE_FILE:close()
    return(RULE_TABLE)
end

--WAF log record for json,(use logstash codec => json)
function log_record(method,url,abnormal_info,ruletag)
    ngx.print(method)
    local cjson = require("cjson")
    local io = require 'io'
    local LOG_PATH = config_log_dir
    local LOCAL_TIME = ngx.localtime()

    local t_content_length=ngx.req.get_headers()['content-length']
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

--    ngx.print(abnormal_info)
    local log_json_obj
    if abnormal_info == "_" then
        log_json_obj = {
            local_time = LOCAL_TIME,
            attack_method = method,

            abnormal_name = "",
            abnormal_tpye = "",
            abnormal_profile = "",
            abnormal_score = "",
            
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
    else
        log_json_obj = {
            local_time = LOCAL_TIME,
            attack_method = method,

            abnormal_name = abnormal_info["p_name"],
            abnormal_tpye = abnormal_info["p_type"],
            abnormal_profile = abnormal_info["p_profile"],
            abnormal_score = abnormal_info["score"],
            
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

    end

--处理 \/
--    for k,v in pairs(log_json_obj) do
--        ngx.print(k)
--        ngx.print(v)     --没有出现\/
--        log_json_obj[k] = string.gsub(v, "\\/", "/") 
--    end 

--    ngx.print("my_test************url***"..log_json_obj.url)
    local LOG_LINE = cjson.encode(log_json_obj)
--    ngx.print("my_test************cjson后的内容***"..LOG_LINE)

--处理 \/
    LOG_LINE = string.gsub(LOG_LINE, "\\/", "/")

    local LOG_NAME = LOG_PATH..'/'..ngx.today().."_waf.log"
    ngx.print(LOG_NAME)
    local file = io.open(LOG_NAME,"a")
    if file == nil then
        ngx.print("if file == nil then  <br/>")       
        return
    end
    file:write(LOG_LINE.."\n")
    file:flush()
    file:close()
end

--WAF return
function waf_output()
    if config_waf_output == "redirect" then
        ngx.redirect(config_waf_redirect_url, 301)
    else
        ngx.header.content_type = "text/html"
        ngx.status = ngx.HTTP_FORBIDDEN
        ngx.say(config_output_html)
        ngx.exit(ngx.status)
    end
end

