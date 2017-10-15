from flask import Flask
from flask import jsonify
from random import randint
import pymongo
from datetime import date, datetime, timedelta

app = Flask(__name__)
uri = 'mongodb://heroku_qg4xxhbq:2jb487u6ota241oqoh7vgpd9tj@ds119210.mlab.com:19210/heroku_qg4xxhbq'
client = pymongo.MongoClient(uri)
db = client.get_default_database()

@app.route('/')
def index():
    convert_frequency_and_time_to_date(datetime(2017, 10, 3), 4, "8:00")
    return "Hi! Welcome to PillPal!"

@app.route('/get_device_profiles/<device_id>')
def get_device_profiles(device_id):
    devices_db = db['devices']
    devices_cursor = devices_db.find({'device_id': device_id})
    profile_ids = []
    for device in devices_cursor:
        for profile_id in device['profile_ids']:
            profile_ids.append(profile_id)
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
        return jsonify(profiles=profiles)
    else:
        return jsonify(profiles=[])

@app.route('/create_device_profile/<device_id>/<name>/<color>')
def create_device_profile(device_id, name, color):
    profile_id = name.split()[0] + str(random_with_N_digits(5))
    profiles_db = db["profiles"]
    profiles_db.insert_one({'profile_id': profile_id, 'name': name, 'color': color, 'prescription_ids': []})
    # determine whether the device already exists
    devices_db = db['devices']
    device_cursor = devices_db.find({'device_id': device_id})
    if (device_cursor.count() > 0):
        # device exists, let's recreate profile list and append to it new user
        devices_db.update({'device_id': device_id}, {'$push': {'profile_ids': profile_id}})
        return jsonify(profile_id=profile_id)
    else:
        # device doesn't exist, let's start new profile list and save the new device
        profile_ids = [profile_id]
        devices_db.insert_one({'device_id': device_id, 'profile_ids': profile_ids})
        return jsonify(profile_id=profile_id)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@app.route('/get_next_prescription/<device_id>')
def get_next_prescription(device_id):
    devices_db = db['devices']
    devices_cursor = devices_db.find({'device_id': device_id})
    profile_ids = []
    for device in devices_cursor:
        for profile_id in device['profile_ids']:
            profile_ids.append(profile_id)
        if (len(profile_ids) > 0):
            for profile_id in profile_ids:
                profiles_db = db["profiles"]
                profile_cursor = profiles_db.find({'profile_id': profile_id})
                if (profile_cursor.count() > 0):
                    # profile exists, which is normal. Let's get the prescriptions
                    profile = profile_cursor[0]
                    prescription_ids = profile['prescription_ids']
                    if (len(prescription_ids) > 0):
                        # figure out next prescription and send it back
                        prescriptions = []
                        prescriptions_db = db['prescriptions']
                        for prescription_id in prescription_ids:
                            prescription_cursor = prescriptions_db.find({'prescription_id': prescription_id})
                            if (prescription_cursor.count() > 0):
                                prescriptions.append(prescription_cursor[0])
                        
                        prescridoses_dates = []
                        # given each prescription, we'll need to get doses
                        for prescription in prescriptions:
                            prescridoses_dates.append(convert_frequency_and_time_to_date(prescription['start_date'], prescription['frequency'], prescription['time']))

                        # sort
                        prescridoses_dates.sort()
                        return jsonify(error=False, next_prescription=prescridoses_dates[0])

                    else:
                        # no prescriptions to deal with
                        return jsonify(error=False, next_prescription="")
                else:
                    # well shit, so the profile doesn't exist
                    return jsonify(error=True, next_prescription="")

def convert_frequency_and_time_to_date(start_date, frequency, time):
    time_bits = time.split(":")
    hour = int(time_bits[0]) - 1
    minute = int(time_bits[1]) - 1
    if (minute < 0):
        minute = 0
    start_date = datetime(start_date.year, start_date.month, start_date.day, hour, minute)
    while (start_date < datetime.now()):
        start_date = start_date + timedelta(days=frequency)
    return start_date

if __name__ == "__main__":
    app.run()