import http.server
import http.client
import http.cookies
import webbrowser
import socketserver
import urllib
import json
#CONFIG
PORT = 8080
#DATA
DATA = []
#HANDLER
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            with open("html/index.html","rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/index":
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            with open("html/index.html","rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/form":
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            with open("html/form.html","rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/load":
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            json_data = json.dumps(DATA)
            self.wfile.write(json_data.encode('utf-8'))
        else:
            self.send_response_only(404)
    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            username = parsed_data.get('username',[''])[0]
            email = parsed_data.get('email',[''])[0]
            message = parsed_data.get('message',[''])[0]
            userIP = self.client_address
            print("Response from ",userIP," with ",email," ",username)
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            DATA.append([username,message])
            with open("html/form.html","rb") as file:
                self.wfile.write(file.read())
#MAIN
with socketserver.TCPServer(("",PORT),Handler) as httpd:
    Url = "http://localhost:"+format(PORT)
    print("Server Running at {}",Url)
    webbrowser.open(Url)
    try:
        httpd.serve_forever()
    except:
        httpd.server_close()
