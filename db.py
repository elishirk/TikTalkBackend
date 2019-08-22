from flask import abort
import json
import datetime
#from firebase_admin import credentials
from google.cloud import firestore


HAPPENINGS = firestore.Client().collection('events')

def get_events():
    print('Retrieving events from firestore')
    docs = HAPPENINGS.get()
    ret = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        ret.append(d)
    return ret

def add_happening(data, id):
    print('adding a new happening' + id + ' to firestore')
    data['date_added'] = datetime.datetime.now()
    data['likes'] = 0
    HAPPENINGS.document(id).set(data)
    return id

def like_happening(id):
    print('user liked happening' + id)
    d = _ensure_happening(id).to_dict()
    d['likes'] +=1
    HAPPENINGS.document(id).set(d)
    return d['likes']

def _ensure_happening(id):
    try:
        return HAPPENINGS.document(id).get()
    except:
        print('failed attempt to access happening ' + id)
        abort(404)
