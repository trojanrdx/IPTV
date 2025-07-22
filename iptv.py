import os
import socket
from flask import Flask, Response, abort
from pyngrok import ngrok, conf
from threading import Thread

app = Flask(__name__)

# === SET YOUR NGROK AUTHTOKEN HERE ===
NGROK_AUTHTOKEN = "30CtJdnEsiqHdY09PdvHaRZtmBr_89iYY9EkVFT7WwitbPNCD"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"
    return local_ip

def ask_for_file():
    while True:
        path = input("📂 Enter FULL path to your .m3u file:\n").strip()
        if os.path.isfile(path):
            print(f"✅ Found: {path}")
            return path
        else:
            print(f"❌ File not found! Try again.\n")

M3U_FILE_PATH = ask_for_file()

@app.route('/playlist.m3u')
def serve_m3u():
    """Serve raw M3U"""
    try:
        with open(M3U_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, mimetype='audio/x-mpegurl')
    except Exception as e:
        print(f"❌ ERROR reading file: {e}")
        abort(500)

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    LOCAL_IP = get_local_ip()

    # Configure ngrok with your token automatically
    conf.get_default().auth_token = NGROK_AUTHTOKEN

    print("\n🚀 IPTV Playlist Server starting...")
    print(f"📂 Serving: {M3U_FILE_PATH}")
    print(f"🔗 Local:   http://localhost:{PORT}/playlist.m3u")
    print(f"🔗 LAN:     http://{LOCAL_IP}:{PORT}/playlist.m3u")

    # Start Flask in background
    def run_flask():
        app.run(host=HOST, port=PORT)

    Thread(target=run_flask, daemon=True).start()

    # Start ngrok tunnel
    print("\n🌍 Starting ngrok tunnel automatically...")
    public_url = ngrok.connect(PORT, "http")
    print(f"✅ Public ngrok link: {public_url}/playlist.m3u")
    print("\n💡 Share this link worldwide. CTRL+C to stop.\n")

    input("Press ENTER to stop server...\n")
