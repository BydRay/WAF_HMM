--WAF config file,enable = "on",disable = "off"

--waf status
config_waf_enable = "on"

--log dir
config_log_dir = "/usr/local/openresty/nginx/conf/waf/waf_logs"

--lua out data dir
config_lua_out_dir = "/lua_out_dir"

--detection out path
detection_out_data_path = "/my_detection_out_data.json"

--rule setting
config_rule_dir = "/usr/local/openresty/nginx/conf/waf/rule-config"

--enable/disable white ip
config_white_ip_check = "on"

--enable/disable block ip
config_black_ip_check = "on"

--enable/disable cc filtering
config_cc_check = "on"

--cc rate the xxx of xxx seconds
config_cc_rate = "10/60"

--config waf output redirect/html
config_waf_output = "html"

--if config_waf_output ,setting url
config_waf_redirect_url = "https://www.baidu.com"
config_output_html=[[
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="zh-cn" />
<title>my_waf</title>
</head>
<body>
<h1>WAF响应，如有疑问，请联系开发人员</h1>
</body>
</html>
]]

