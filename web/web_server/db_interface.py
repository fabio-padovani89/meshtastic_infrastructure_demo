import atexit

from datetime import datetime
from os import environ

import pymongo


# MongoDB
MONGO_DATA = {
    'url': environ.get('MONGO_URL'),
    'database': environ.get('MONGO_DATABASE'),
    'collection': environ.get('MONGO_COLLECTION'),
    'username': environ.get('MONGO_USERNAME'),
    'password': environ.get('MONGO_PASSWORD'),
    'nodes_expire_seconds': int(environ.get('MONGO_NODES_EXPIRE_SECONDS'))
}
MONGO_CLIENT = pymongo.MongoClient(
    MONGO_DATA['url'],
    username=MONGO_DATA['username'],
    password=MONGO_DATA['password']
)

MONGO_DB = MONGO_CLIENT[MONGO_DATA['database']]
MONGO_COLLECTION = MONGO_DB[MONGO_DATA['collection']]
MONGO_COLLECTION.create_index(
    'relevation_time',
    name='expire_index',
    expireAfterSeconds=MONGO_DATA['nodes_expire_seconds']
)


def store_nodes_info(data):
    if data:
        for x in data:
            x['relevation_time'] = datetime.fromtimestamp(x['relevation_time'])
        
        MONGO_COLLECTION.insert_many(data)

def get_nodes_info(user=None, dt_from=None, dt_to=None):
    pipeline = []

    if user is not None:
        pipeline.append({
            '$match': {
                'user.longName': user
            }
        })

    if dt_from is not None:
        pipeline.append({
            '$match': {
                'relevation_time': {
                    "$gte" : dt_from
                }
            }
        })

    if dt_to is not None:
        pipeline.append({
            '$match': {
                'relevation_time': {
                    "$lte" : dt_to
                }
            }
        })

    pipeline += [
        {
            '$sort': {
                'user.longName': 1,
                'relevation_time': -1,
                
            }
        },
        { 
            '$group': {
                '_id' : '$user.longName',
                'time': {'$first': '$time'},
                'user': {'$first': '$user'},
                'position': {'$first': '$position'},
                'batteryLevel': {'$first': '$batteryLevel'},
                'snr': {'$first': '$snr'},
                'relevation_time': {'$first': '$relevation_time'},
            }
        }
    ]

    res = list(MONGO_COLLECTION.aggregate(pipeline))

    for x in res:
        x['relevation_time'] = x['relevation_time'].isoformat()

        if x.get('position') and x.get('position', {}).get('time'):
            x['position']['time'] = datetime.fromtimestamp(x['position']['time']).isoformat()
        
    return res

def exit_procedure():
    MONGO_CLIENT.close()


atexit.register(exit_procedure)
