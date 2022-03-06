import requests

from click import UsageError

from zen_knit.publish.support import cred

def get_workers(profile):
   
    access_key, secret_key , publish_url = cred.pull_cred(profile)

    data = {}
    data['access_key'] = access_key
    data['secret_key'] = secret_key

    r = requests.post( f"{publish_url}api/external/get_worker/", data=data)
    if r.status_code != 200:
        raise UsageError(r.text)
    else:
        response = r.json()

        if response["data"] is None :
            print("no worker name present")
            return 0

        workerNames = ', '.join( d["name"] for d in response["data"])
        print(f" workers are {workerNames}")
        return 0


def get_worker_groups(profile):
    access_key, secret_key , publish_url = cred.pull_cred(profile)

    data = {}
    data['access_key'] = access_key
    data['secret_key'] = secret_key

    r = requests.post( f"{publish_url}api/external/get_worker_group/", data=data)
    if r.status_code != 200:
        raise UsageError(r.text)
    else:
        response = r.json()
        if response["data"] is None :
            print("no worker group name present")

            return 0
        workerGroupNames = ', '.join( d["name"] for d in response["data"])
        print(f" worker group are {workerGroupNames}")
        return 0
