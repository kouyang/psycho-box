import json, os
import dropbox
from collections import deque

app_key = os.environ['APP_KEY']
app_secret = os.environ['APP_SECRET']
access_token = os.environ['ACCESS_TOKEN']

client = dropbox.client.DropboxClient(access_token)


def print_json(data):
    print json.dumps(data, indent=4, separators=(',', ': '))

def delete(f):
    print 'deleting ' + f
    client.file_delete(f)

def up():
    # TODO (need to worry about pwd)
    return

def down(path):
    data = client.metadata(path)
    files.extendleft(data['contents'])

def main():
    pwd = '/'
    root_data = client.metadata(pwd)

    global files
    files = deque(root_data['contents'])

    while files:
        f = files.popleft()
        print_json(f)
        action = raw_input('')
        if action == 'a':
            delete(f['path'])
        elif action == 'd':
            continue
        elif action == 'w':
            up()
        elif action == 's' and f['is_dir']:
            down(f['path'] + '/')
        elif not action:
            return
        print ''

main()