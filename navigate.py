# Include the Dropbox SDK
import os, dropbox, json

# Get your app key and secret from the Dropbox developer website
app_key = os.environ['APP_KEY']
app_secret = os.environ['APP_SECRET']
access_token = os.environ['ACCESS_TOKEN']

global pwd

def pj(data):
    print json.dumps(data, indent=4, separators=(',', ': '))

def delete(file):
    print 'deleting ' + file['path']
    client.file_delete(file['path'])

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
    pj(root_data)



    for file in root_data['contents']:
        if not 'magnum' in file['path']:
            continue
        pj(file)
        action = raw_input('')
        if action == 'a':
            delete(file)
        elif action == 'd':
            continue
        elif action == 'w':
            up()
        elif action == 's':
            down()
        print ''

main()