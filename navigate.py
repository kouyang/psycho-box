import json, os
import dropbox
from collections import deque

app_key = os.environ['APP_KEY']
app_secret = os.environ['APP_SECRET']
access_token = os.environ['ACCESS_TOKEN']

global pwd

def print_json(data):
    print json.dumps(data, indent=4, separators=(',', ': '))

def delete(f):
    print 'deleting ' + f['path']
    client.file_delete(f['path'])

def up():
    # TODO
    return

def down():
    # TODO
    return

def main():
    global client
    client = dropbox.client.DropboxClient(access_token)
    pwd = '/'
    root_data = client.metadata(pwd)

    files = deque(root_data['contents'])

    while files:
        f = files.popleft()
        print_json(f)
        action = raw_input('')
        if action == 'a':
            delete(f)
        elif action == 'd':
            continue
        elif action == 'w':
            up()
        elif action == 's':
            down()
        elif not action:
            return
        print ''

main()