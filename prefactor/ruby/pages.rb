require "nancy"

class Page < Nancy::Base
  use Rack::Session::Cookie, secret: ENV['SECRET_TOKEN']
  include Nancy::Render

  before do
    if request.path_info == "/protected" && !session[:authenticated]
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
    @message = "Hello world"
    render("views/hello.erb")
  end

  get "/users/:id.json" do
    @user = User.find(params['id'])
    halt 404 unless @user
    UserSerializer.new(@user).to_json
  end
end

