#!/usr/bin/env python3 -u
import os, socket, mimetypes

PORT, BUF = 8080, 8192

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "?.?.?.?"

def send(sock, data): 
    sock.sendall(data.encode() if isinstance(data, str) else data)

def handle(sock):
    try:
        req = sock.recv(BUF).decode('utf-8', errors='ignore')
        parts = req.split()[1] if len(req.split()) > 1 else "/"
        url = parts
        
        if "favicon.ico" in url:
            send(sock, "HTTP/1.1 404 Not Found\r\n\r\n")
        elif url == "/":
            host = [l.split()[1] for l in req.split('\r\n') if l.startswith('Host:')]
            host = host[0] if host else f"localhost:{PORT}"
            send(sock, f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                 f"<html><body><div style='display:grid;place-content:center;height:100vh;text-align:center'>"
                 f"<h3>Select:<br><br><a href='http://{host}/home'>/home</a><br><br>"
                  f"<br><a href='http://{host}/home/th/d/rep/w/index.html'>/home/th/d/rep/w/index.html</a><br><br>"
                 f"Or from anoth PC/phone use: <br><br>http://{get_ip()}:{PORT}</h3></div></body></html>")
        elif os.path.isdir(url):
            items = ''.join(f'<li><a href="{url}/{e}">{e}</a></li>' 
                          for e in os.listdir(url) if e not in ['.', '..'])
            send(sock, f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                 f"<html><body><h3>Index of {url}</h3><ul>{items}</ul></body></html>")
        elif os.path.isfile(url):
            mime = mimetypes.guess_type(url)[0] or "text/plain"
            send(sock, f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\n\r\n")
            with open(url, 'rb') as f:
                while chunk := f.read(BUF): send(sock, chunk)
        else:
            send(sock, f"HTTP/1.1 404 Not Found\r\n\r\n{url} Not Found")
    except Exception as e: print(f"Error: {e}")
    finally: sock.close()

def main():
    print("started\n")
    import sys
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = PORT
    
    # Create stop script
    with open('stop_server.sh', 'w') as f:
        f.write(f'#!/bin/bash\nkill {os.getpid()}\n')
    os.chmod('stop_server.sh', 0o755)
    
    while port < PORT + 100:
        try:
            s.bind(('0.0.0.0', port))
            break
        except OSError:
            if port == PORT:
                print(f"Port {PORT} is in use. To release it, run:")
                print(f"  sudo lsof -ti:{PORT} | xargs kill -9")
                print(f"  OR: sudo fuser -k {PORT}/tcp")
                print(f"Then run this script again to use port {PORT}.")
                print(f"Trying next available port...\n")
            port += 1
    else:
        print(f"No available ports found between {PORT} and {PORT+99}")
        return
    s.listen(10)
    print(f"Server running at http://localhost:{port}/ and http://{get_ip()}:{port}/")
    print(f"Press Ctrl+C to stop, or run: ./stop_server.sh")
    try:
        while True: handle(s.accept()[0])
    except KeyboardInterrupt: print("\nShutdown")
    finally: s.close()

if __name__ == "__main__": main()