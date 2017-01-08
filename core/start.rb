require 'timeout'
require 'socket'
require 'json'

obj = ARGV[0]
port = ARGV[1]
project = ARGV[2]
type = ARGV[3]
command = ARGV[4]

def killProcess(pid)
    begin  
    Process.kill("HUP", pid)  
    raise 'I can t kill process ' + pid.to_s
  rescue
    puts 'Process ' + pid.to_s + ' handled'  
  end 
end

def track(obj, pid, project, type)
    process_track = File.expand_path(File.dirname(__FILE__)) + "/" + project + '_' + type + '.icaro'
    api_obj = {
                :name => obj,
                :pid => pid
            }
    content = File.read(process_track)
    open(process_track, 'w') { |f|
        content = JSON.parse(content).push(api_obj)
        f.puts content.to_json
    }
end

def closeApi(obj, project, type)
    process_track = File.expand_path(File.dirname(__FILE__)) + "/" + project + '_'+ type +'.icaro'
    if not File.exists? (process_track)
        open(process_track, 'w') { |f|
            f.puts "[]"
        }
    else
        objs = JSON.parse(File.read(process_track))
        objs.each do |api_obj|
            if obj == api_obj["name"]
                killProcess(api_obj["pid"])
                objs.delete_at(objs.index(api_obj))
            end
        end
        open(process_track, 'w') { |f|
            f.puts objs.to_json
        }
    end
end

def executeApi(obj, port, project, type)
    cmd = "uwsgi --enable-threads --socket 127.0.0.1:" + port.to_s + " --protocol=http --wsgi-file " + type + "/" + obj + ".py --callable api" 
    fork{
        track(obj, Process.pid, project, type)
        exec(cmd)
    }
end


closeApi(obj, project, type)
if command != "terminate"
    executeApi(obj, port, project, type)
end
