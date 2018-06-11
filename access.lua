require 'init'
require 'lib'

function waf_main()
    
--    ngx.print("ngx.print  function waf_main()  </br>")
    if white_ip_check() then
--	ngx.print("white_ip_check() then  </br>")
    elseif black_ip_check() then
--	ngx.print("black_ip_check() then  </br>")
    elseif cc_attack_check() then
--        ngx.print("elseif cc_attack_check() then  </br>")
    elseif AI_check() then
--        ngx.print("elseif AI_check() then  </br>")

--    ngx.print("return  </br>")
    else
        ngx.print("clear  log   <br/>")
        log_record('clear',ngx.var_request_uri,"_","_")
        return 
    end
end

local a = waf_main()

--ngx.print(type(a).."<br/>")
ngx.print("waf_main()  done </br>")
