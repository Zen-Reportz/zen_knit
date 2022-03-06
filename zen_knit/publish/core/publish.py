import os
import shutil
import copy
import time
import webbrowser
import oyaml as yaml
import requests
from click import UsageError

from zen_knit.publish.support import cred

def publish(path, fresh, browser, profile):
    old_path = os.getcwd()
    if path != old_path:
        os.chdir(path)
    
    current = path
    files = os.listdir(current)
    present_config = any([True for file_ in files if 'config.yml' == file_])

    if not present_config:
        raise UsageError("config.yml file is not present")
  
    upload_file = {}
    for file_ in files:
        if file_ == 'config.yml':
            with open("config.yml", "r") as f:
                data = yaml.safe_load(f)
            break_list = ['title', 'type', 'language']
            for b in break_list:
                if b not in data.keys():
                    raise UsageError(f"{b.capitalize()} is not provided in config")
            if fresh:
                try:
                    del data['all_ids'][profile]
                except:
                    pass
                with open("config.yml", "w") as f:
                    yaml.dump(data, f)
            config = copy.deepcopy(data)
            
    if data.get("all_ids") is not None:
        if data["all_ids"].get(profile) is not None:
            data["id"] = data["all_ids"].get(profile)
    
    type = config.get('type')

    shutil.make_archive(".", "zip", ".")
    upload_file['zip_file'] = open(f"{path}.zip", "rb")

    access_key, secret_key , publish_url = cred.pull_cred(profile)
    data['access_key'] = access_key
    data['secret_key'] = secret_key

    print(f"publishing document at {publish_url}publish/report/")
    r = requests.post( f"{publish_url}publish/report/", files=upload_file, data=data)
    os.remove(f"{path}.zip")
    if r.status_code != 200:
        if r.status_code == 402:
            print("You have used all reports, need to updagrade Zen Reportz")
        raise UsageError(r.text)
    else:
        response = r.json()["data"]
        time.sleep(10)
        report_id = str(response["id"])
        config['all_ids'] = {
            profile: report_id
        }
        with open("config.yml".format, "w") as f:
            yaml.dump(config, f)

        if len(response["workers"])> 0 :
            workerNames = ', '.join(response["workers"])
            print(f"following worker(s) are not present, please talk your admin {workerNames}")

        if len(response["worker_groups"])> 0 :
            worker_group = ', '.join(response["worker_groups"])
            print(f"following worker group(s) are not present, please talk your admin {worker_group}")

        url_to_open = publish_url + f'report-application/{report_id}?type={type}&open=true'

        if browser:
            webbrowser.open(url_to_open)

        os.chdir(old_path)

    return "publish report"
