from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from time import sleep
from picamera import PiCamera

class statusHandler(BaseHTTPRequestHandler) :
    def do_GET(self) :
        if self.path != '/web/snapshot.jpg' :
            self.send_error(404, "File not found.")
            return

        with PiCamera() as camera :
            camera.resolution = (1280, 720)
            camera.start_preview()
            # Camera warm-up time
            sleep(2)
            camera.capture('status.jpg')

        self.send_response(200)
        self.send_header('Content-type', "image/jpg")
        self.end_headers()
        with open('./status.jpg', 'rb') as photo :
            self.wfile.write(photo.read())


if __name__ == '__main__':
    # Start a simple server, and loop forever
    # from BaseHTTPServer import HTTPServer
    with open('IP.txt', 'r', encoding='utf8') as IP :
        host = IP.readline().strip()
        server = HTTPServer((host, 8081), statusHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()