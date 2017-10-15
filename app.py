from flask import Flask
import pymongo

app = Flask(__name__)
uri = 'mongodb://heroku_qg4xxhbq:2jb487u6ota241oqoh7vgpd9tj@ds119210.mlab.com:19210/heroku_qg4xxhbq'


SEED_DATA = [
    {
        'id': 'ABCDE',
        'profiles': []
    },
    {
        'id': '31562',
        'profiles': [ "binit1", "max2", "emma3"]
    },
    {
        'id': 'WELCO',
        'profiles': [ "RANDO", "MIDIZED"]
    }
]

@app.route('/')
def index():
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    devices = db['devices']
    devices.insert_many(SEED_DATA)
    cursor = devices.find({'id': "31562"})
    message = ""
    for device in cursor:
        numProfiles = len(device['profiles'])
        message = f"hey, you have got {numProfiles} profiles."
    return message

if __name__ == "__main__":
    app.run()