#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import sys

if len(sys.argv) == 1:
    raise Exception(f"Must provide positional argument: IP.  {sys.argv[0]} <IP>")

ip = sys.argv[1]
host = f"http://{ip}"
wait = "0"
includeMetadata = "0"
commandID = "1"
url = f"{host}:32500/player/timeline/poll?wait={wait}&includeMetadata={includeMetadata}&commandID={commandID}"

def get_playback_state():
    resp = requests.get(url)
    if resp.ok:
        content = resp.content
        root = ET.fromstring(content)

        for type_tag in root.findall('Timeline'):
            item_type = type_tag.get('itemType')
            if item_type == "music":
                state = type_tag.get('state')
                if state == "playing":
                    return "1"
        return "0"
    else:
        raise Exception(f"API call was not OK: {resp.status_code}")

def main():
    state = get_playback_state()
    print(state)

if __name__ == "__main__":
    main()
