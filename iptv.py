import http.server
import socketserver
import os

PORT = 8080

m3u_path = input("📂 Enter FULL path to your .m3u file:\n").strip()

if not os.path.isfile(m3u_path):
    print(f"❌ ERROR: File does not exist: {m3u_path}")
    exit(1)
else:
    print(f"✅ Found: {m3u_path}")

file_name = os.path.basename(m3u_path)
directory = os.path.dirname(m3u_path)

os.chdir(directory)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/playlist.m3u':
            self.path = '/' + file_name
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("\n🚀 IPTV .m3u Server Running!")
    print(f"🔗 Local: http://localhost:{PORT}/playlist.m3u")
    print("\n🌍 For global, use: `ngrok http {PORT}`")
    print("\nPress CTRL+C to stop.")
    httpd.serve_forever()
