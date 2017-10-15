from flask import Flask
from flask import jsonify
from random import randint
import pymongo

app = Flask(__name__)
uri = 'mongodb://heroku_qg4xxhbq:2jb487u6ota241oqoh7vgpd9tj@ds119210.mlab.com:19210/heroku_qg4xxhbq'
client = pymongo.MongoClient(uri)
db = client.get_default_database()

@app.route('/')
def index():
    devices = db['devices']
    devices.insert_many(SEED_DATA)
    cursor = devices.find({'id': "31562"})
    message = ""
    for device in cursor:
        numProfiles = len(device['profiles'])
        message = f"hey, you have got {numProfiles} profiles."
    return message

@app.route('/get_device_profiles/<device_id>')
def get_device_profiles(device_id):
    devices_db = db['devices']
    devices_cursor = devices_db.find({'device_id': device_id})
    profile_ids = []
    for device in devices_cursor:
        for profile in device['profile_ids']:
            profile_ids.append(profile)
    if (len(profile_ids) > 0):
        profiles = []
        for profile_id in profile_ids:
            profiles_db = db['profiles']
            profiles_cursor = profiles_db.find({'profile_id': profile_id})
            name = "Not Set"
            for profile in profiles_cursor:
                name = profile['name']
            profile = {}
            profile['profile_id'] = profile_id
            profile['name'] = name
            profiles.append(profile)
        return jsonify(hasProfiles=True,
                        profiles=profiles)
    else:
        return jsonify(hasProfiles=False,
                        profiles=[])

@app.route('/create_device_profile/<device_id>/<name>/<color>')
def create_device_profile(device_id, name, color):
    profile_id = name.split()[0] + str(random_with_N_digits(5))
    profiles_db = db["profiles"]
    profiles_db.insert_one({'profile_id': profile_id, 'name': name, 'color': color})
    # determine whether the device already exists
    devices_db = db['devices']
    device_cursor = devices_db.find({'device_id': device_id})
    if(device_cursor.count() > 0):
        # device exists, let's recreate profile list and append to it new user
        # device = device_cursor[0]
        # profile_ids = device['profile_ids']
        # profile_ids.append(profile_id)
        devices_db.update({'device_id': device_id}, {'$push': {'profile_ids': profile_id}})
        return profile_id
    else:
        # device doesn't exist, let's start new profile list and save the new device
        profile_ids = [profile_id]
        devices_db.insert_one({'device_id': device_id, 'profile_ids': profile_ids})
        return profile_id

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

if __name__ == "__main__":
    app.run()