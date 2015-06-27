import json, os
import dropbox
from collections import deque

app_key = os.environ['APP_KEY']
app_secret = os.environ['APP_SECRET']
access_token = os.environ['ACCESS_TOKEN']

client = dropbox.client.DropboxClient(access_token)
has_kept = False

def print_json(data):
    print json.dumps(data, indent=4, separators=(',', ': '))

def keep():
    global has_kept
    has_kept = True

def delete(f):
    print 'deleting ' + f
    client.file_delete(f)

def up():
    # TODO (need to worry about pwd)
    global has_kept
    has_kept = False
    p = path.popleft()
    while files and 'fake' not in files.popleft():
        continue
    files.appendleft(p)

def down(f):
    # TODO if they emptied a folder, then put the folder back in queue
    global has_kept
    has_kept = False
    data = client.metadata(f['path'] + '/')
    path.appendleft(f)

    fake = f.copy()
    fake['fake'] = True
    files.appendleft(fake)
    files.extendleft(reversed(data['contents']))

def empty(f):
    return not client.metadata(f['path'] + '/')['contents']

def main():
    pwd = '/louise/'
    root_data = client.metadata(pwd)

    global files
    global path
    files = deque(root_data['contents'])
    path = deque()

    global has_kept
    has_kept = False

    while files:
        f = files.popleft()
        if ('fake' in f):
            if not has_kept:
                files.appendleft(path.popleft())
            continue
        else:
            print_json(f)

        action = raw_input('')
        if action == 'a':
            delete(f['path'])
        elif action == 'd':
            keep()
        elif action == 'w':
            up()
        elif action == 's' and f['is_dir'] and not empty(f):
            down(f)
        elif not action:
            return
        print ''

main()