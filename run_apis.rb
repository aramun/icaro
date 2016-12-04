require 'timeout'
require 'socket'

api_environ = ARGV[0]+"_API"
apis = ENV[api_environ].split(";")

def is_port_open?(ip, port)
    begin
        Timeout::timeout(1) do
            begin
                s = TCPSocket.new(ip, port)
                s.close
                return true
            rescue Errno::ECONNREFUSED, Errno::EHOSTUNREACH
                return false 
            end
        end
    rescue Timeout::Error
    end
    return false
end
def executeApi(api,port)        
    cmd = "uwsgi --socket 127.0.0.1:"+port.to_s+" --protocol=http --wsgi-file api/"+api+".py --callable api" 
    fork{
        exec(cmd)
    }
end


i = 0
port = ""
apis.each do |api|        
    begin
        port = ("800"+i.to_s).to_i
        i+=1    
    end while is_port_open?("127.0.0.1", port)
    executeApi(api, port)     
end    
