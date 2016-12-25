require 'timeout'
require 'socket'

api = ARGV[0]
port = ARGV[1]

def executeApi(api,port)    
    cmd = "uwsgi --socket 127.0.0.1:" + port.to_s + " --protocol=http --wsgi-file api/" + api + ".py --callable api" 
    fork{
        exec(cmd)
    }
end

executeApi(api, port)
