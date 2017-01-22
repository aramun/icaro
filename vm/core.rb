require 'timeout'
require 'socket'
require 'json'

command = ARGV[0]
obj = ARGV[1]

def killProcess(pid)
    begin
    Process.kill("HUP", pid)  
    raise 'I can t kill process ' + pid.to_s
  rescue
    puts 'Process ' + pid.to_s + ' handled'
  end
end

def track(obj, type, pid)
    process_track = "tracker/"+ type + "/" + obj + '.icaro'
    api_obj = {
                :pid => pid
            }
    content = File.read(process_track)
    open(process_track, 'w') { |f|
        content = JSON.parse(content).push(api_obj)
        f.puts content.to_json
    }
end

def closeApi(obj, type, pid)
    process_track = "tracker/"+ type + "/" + obj + '.icaro'
    if not File.exists? (process_track)
        open(process_track, 'w') { |f|
            f.puts "[]"
        }
    else
        killProcess(JSON.parse(File.read(process_track))["pid"])
        open(process_track, 'w') { |f|
            f.puts "[]"
        }
    end
end

def executeApi(obj, port, type)
    cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + port.to_s + " --wsgi-file " + type + "/" + obj + ".py --callable api" 
    fork{
        track(obj, Process.pid, type)
        exec(cmd)
    }
end

if command == "run"
    executeApi(obj["name"], obj["port"], obj["type"])
end

if command == "terminate"
    closeApi(obj, project, type)
end
