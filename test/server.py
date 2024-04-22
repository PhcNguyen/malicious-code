import json
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

class MyJSONHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')


        if self.path == '/json' and self.command == 'POST':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            
            try:
                json_data = json.loads(post_data)
                response_data = {'message': 'Received POST data successfully', 'data': json_data}
            except json.JSONDecodeError:
                response_data = {'error': 'Invalid JSON format'}

            
            response_json = json.dumps(response_data)
            self.wfile.write(response_json.encode())
        else:
            
            self.send_error(404, "Not Found")


class HttpServer:
    def __init__(self, port=8000, directory='.'):
        self.port = port
        self.directory = directory

    def start(self):
        try:
            Handler = MyJSONHTTPRequestHandler
            Handler.directory = self.directory

            with TCPServer(("", self.port), Handler) as httpd:
                print(f"Server started at port {self.port}")
                httpd.serve_forever()

        except KeyboardInterrupt:
            print("Server stopped.")

# Sử dụng:
if __name__ == "__main__":
    server = HttpServer(port=8000)
    server.start()

