import requests
import os
from datetime import datetime, timezone

import logging
import time
from urllib.parse import quote_plus
from dotenv import load_dotenv
from threading import Thread
import sys

load_dotenv()
logging.basicConfig(level=logging.INFO)


def get_run_duration(run):
    start_str = run.get("run_started_at")
    if not start_str:
        return ("Workflow not started yet - Duration unknown")
    start_time = datetime.fromisoformat(start_str.rstrip("Z")).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    raw_duration = now - start_time
    total_seconds = int(raw_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return(f"Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")


def get_token_for_repo(owner):
    if owner == "dinamikfyt1":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC1')
    elif owner == "dinamikfyt2":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC2')
    elif owner == "dinamikfyt3":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC3')
    elif owner == "dinamikfyt4":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC4')
    elif owner == "dinamikfyt5":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC5')
    elif owner == "dinamikfyt6":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC6')
    elif owner == "dinamikfyt7":
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC7')
    else:
        logging.warning(f"Bilinmeyen owner: {owner}, default token kullanılıyor.")
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC')

def check_running_workflows(workflow_owner, workflow_repo): #Eğer aktif workflow varsa True dönüyor (Sonra işimize yarayacak)
    token = get_token_for_repo(workflow_owner)
    response = requests.get(
        f"https://api.github.com/repos/{workflow_owner}/{workflow_repo}/actions/runs",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        print(f"Çalışan workflow'lar alınamadı: {response.status_code} - {response.text}")
        sys.exit()

    runs = response.json().get("workflow_runs", [])
    if runs:
        print("Workflow owner:    Workflow name:     Duration:")
        for run in runs:
            if run["status"] in ["in_progress", "queued"]:
                print(f"{workflow_owner}, {run['name']}, {get_run_duration(run)}")
        return True
            
    else:
        return False

def check_all_accounts(accounts_to_check): #get all the repos for all users and control it one by one
    found_active = False
    for account in accounts_to_check:
        token = get_token_for_repo(account)
        possible_repos = requests.get(f"https://api.github.com/users/{account}/repos",
        headers={"Authorization": f"Bearer {token}"}).json() 
        for repo in possible_repos:
            if check_running_workflows(account,repo["name"]):
                found_active = True
    if not found_active:
        print("No active workflows found in any of the repos for any of the accounts")
    return found_active

                
sub_workflow_owners = ["dinamikfyt1","dinamikfyt2","dinamikfyt3","dinamikfyt4","dinamikfyt5","dinamikfyt6","dinamikfyt7"]
main_workflow_owner = "dinamikfiyatpublic3" #TODO Verify public account name
main_workflow_repo = "runall"




if check_running_workflows(main_workflow_owner,main_workflow_repo):
    print("run_all_kods dosyası şu an işlemde")
    check_all_accounts(sub_workflow_owners)
else:
    if not check_all_accounts(sub_workflow_owners):
        sys.exit()
