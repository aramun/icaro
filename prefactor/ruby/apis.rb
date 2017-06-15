require "nancy"

class Api < Nancy::Base
  use Rack::Session::Cookie, secret: ENV['SECRET_TOKEN'] # for sessions

  before do
    if request.path_info == "/" && !session[:authenticated]
      halt 401, "unauthorized"
    end
  end

  after do
    if request.path_info ~= /\.json$/
      response['Content-Type'] = 'application/json'
    else
      response['Content-Type'] = 'text/html'
    end
  end

  get "/" do
    "Hello World"
  end

  post "/login" do
    @user = User.find(params['username'])
    halt 401, "unauthorized" unless @user.authenticate(params['password'])
    session[:authenticated] = true
  end
end
