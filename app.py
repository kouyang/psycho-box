from flask import Flask
from flask import render_template
from flask import jsonify
import json, os
import dropbox
from collections import deque

app = Flask(__name__)

app_key = os.environ['APP_KEY']
app_secret = os.environ['APP_SECRET']
access_token = os.environ['ACCESS_TOKEN']

client = dropbox.client.DropboxClient(access_token)
has_kept = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/swipe')
def swipe():
    return render_template('swipe.html')

@app.route('/begin')
def begin():
    pwd = '/'
    root_data = client.metadata(pwd)

    global files
    files = deque(root_data['contents'])
    global path
    path = deque()

    global has_kept
    has_kept = False

    global f
    f = files.popleft()
    if ('fake' in f):
        global f
        f = path.popleft()
    return jsonify(f)

@app.route('/delete')
def delete():
    client.file_delete(f['path'])

    global f
    f = files.popleft()
    if ('fake' in f):
        global f
        f = path.popleft()
    return jsonify(f)

@app.route('/keep')
def keep():
    global has_kept
    has_kept = True

    global f
    global files
    f = files.popleft()
    if ('fake' in f):
        global f
        f = path.popleft()
    return jsonify(f)

@app.route('/up')
def up():
    global has_kept
    has_kept = False

    if not path:
        files.appendleft(f)
        return
    p = path.popleft()
    while files and 'fake' not in files.popleft():
        continue
    files.appendleft(p)

    global f
    f = files.popleft()
    if ('fake' in f):
        global f
        f = path.popleft()
    return jsonify(f)

@app.route('/down')
def down():
    global has_kept
    has_kept = False
    data = client.metadata(f['path'] + '/')
    path.appendleft(f)

    fake = f.copy()
    fake['fake'] = True
    files.appendleft(fake)
    files.extendleft(reversed(data['contents']))

    global f
    f = files.popleft()
    if ('fake' in f):
        global f
        f = path.popleft()
    return jsonify(f)

if __name__ == '__main__':
    app.run(debug=True)
