import os

import oyaml as yaml

from click import UsageError

def cred_path()-> str:
    base_path = os.path.expanduser("~")
    setting_path = base_path + "/.zen/setting.yml"
    return setting_path

def cred_file_present():
    setting_path = cred_path()

    if not os.path.isfile(setting_path):
        raise UsageError("zen report data is not present please use zen create command")
    
    return setting_path
        
def cred_folder():
    base_path = os.path.expanduser("~")
    folder_path = f"{base_path}/.zen"
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    return folder_path


def pull_cred(profile):
    cred_folder()    
    
    setting_path = cred_file_present()
    with open(setting_path, "r") as f:
        data = yaml.safe_load(f)
    
    if profile not in data.keys():
        raise UsageError(f"{profile} is not present in file")
    
    publish_url = data[profile]['url']
    if publish_url[-1] != "/":
        publish_url = publish_url + "/"
    access_key = data[profile]["key"]
    secret_key = data[profile]["secret"]
    
    return access_key, secret_key, publish_url


def create(key, secret, url, profile):
    cred_folder()    
    setting_path = cred_path()

    try:
        with open(setting_path, "r") as f:
            my_dict = yaml.safe_load(f)
    except Exception as e:
        print(e)
        os.remove(setting_path)

    if not os.path.exists(setting_path):
        my_dict = {
            profile: {
                "key": key,
                "secret": secret,
                "url": url
            }
        }
    else:
        with open(setting_path, "r") as f:
            my_dict = yaml.safe_load(f)

        my_dict[profile] = {
            "key": key,
            "secret": secret,
            "url": url
        }
    with open(setting_path, "w") as f:
        yaml.safe_dump(my_dict, f)

    return "created value"


def update(key, secret, profile):
    cred_folder()    
    setting_path = cred_file_present()

    with open(setting_path, "r") as f:
        data = yaml.safe_load(f)
    
    if profile not in data.keys():
        raise UsageError(f"{profile} is not present in file")

    data[profile]['key'] = key
    data[profile]['secret'] = secret

    with open(setting_path, "w") as f:
        yaml.dump(data, f)

    return "updated value"