import http.server
import socketserver
import os

# === CONFIG ===
PORT = 8080

m3u_path = input("📂 Enter FULL path to your .m3u file:\n").strip()

if not os.path.isfile(m3u_path):
    print(f"❌ ERROR: File does not exist: {m3u_path}")
    exit(1)
else:
    print(f"✅ Found: {m3u_path}")

# Get file name only
file_name = os.path.basename(m3u_path)
directory = os.path.dirname(m3u_path)

# Change working dir to where the file is
os.chdir(directory)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/playlist.m3u':
            self.path = '/' + file_name
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Start server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("\n🚀 Serving IPTV .m3u file!")
    print(f"🔗 Local:  http://localhost:{PORT}/playlist.m3u")
    print(f"🔗 LAN:    http://<YOUR_LOCAL_IP>:{PORT}/playlist.m3u")
    print(f"\n🌍 Use with ngrok: `ngrok http {PORT}`")
    print("\nPress CTRL+C to stop server.\n")

    httpd.serve_forever()
