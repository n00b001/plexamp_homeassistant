#!/usr/bin/env python3
import sys
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
except:
    install("requests")
    import requests

if len(sys.argv) == 1:
    raise Exception(f"Must provide positional argument: IP.  {sys.argv[0]} <IP>")

ip = sys.argv[1]
host = f"http://{ip}"
url = f"{host}:32500/player/playback/pause"

def pause_plexamp():
    resp = requests.get(url)
    if resp.ok:
        content = resp.content
        return content
    else:
        raise Exception(f"API call was not OK: {resp.status_code}")

def main():
    pause_plexamp()

if __name__ == "__main__":
    main()
