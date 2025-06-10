import requests
import os
from datetime import datetime, timezone
import logging
from dotenv import load_dotenv
import sys

# Ortam değişkenlerini yükle
load_dotenv()
logging.basicConfig(level=logging.INFO)


def get_run_duration(run):
    start_str = run.get("run_started_at")
    if not start_str:
        return "Workflow not started yet - Duration unknown"
    start_time = datetime.fromisoformat(start_str.rstrip("Z")).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    raw_duration = now - start_time
    total_seconds = int(raw_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}"


def get_token_for_repo(owner):
    tokens = {
        "dinamikfyt1": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC1'),
        "dinamikfyt2": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC2'),
        "dinamikfyt3": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC3'),
        "dinamikfyt4": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC4'),
        "dinamikfyt5": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC5'),
        "dinamikfyt6": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC6'),
        "dinamikfyt7": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC7'),
        "dinamikfiyatpublic3": os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC3_PUBLIC')
    }
    token = tokens.get(owner)
    if not token:
        logging.warning(f"Bilinmeyen owner: {owner}, default token kullanılıyor.")
        token = os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC1')
    return token


def check_running_workflows(workflow_owner, workflow_repo):
    token = get_token_for_repo(workflow_owner)
    url = f"https://api.github.com/repos/{workflow_owner}/{workflow_repo}/actions/runs"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        logging.error(f"Çalışan workflow'lar alınamadı: {response.status_code} - {response.text}")
        sys.exit()

    runs = response.json().get("workflow_runs", [])
    found_active = False

    for run in runs:
        if run["status"] in ["in_progress", "queued"]:
            if not found_active:
                print("Workflow owner:    Workflow name:     Duration:")
            print(f"{workflow_owner:<18} {run['name']:<18} {get_run_duration(run)}")
            found_active = True

    return found_active

def check_all_accounts(accounts_to_check, repo_to_check):
    found_active = False
    for account in accounts_to_check:
        if check_running_workflows(account, repo_to_check):
            found_active = True
    if not found_active:
        print("No active workflows found in any of the repos for any of the accounts.")
    return found_active


# === Ana yapılandırma ===
sub_workflow_owners = ["dinamikfyt1", "dinamikfyt2", "dinamikfyt3", "dinamikfyt4", "dinamikfyt5", "dinamikfyt6", "dinamikfyt7"]
sub_workflow_repo = "anlik_guncel"
main_workflow_owner = "dinamikfiyatpublic3"
main_workflow_repo = "runall"


# === Kontroller başlıyor ===
if check_running_workflows(main_workflow_owner, main_workflow_repo):
    print("Main workflow (runall) şu anda çalışıyor.")
    check_all_accounts(sub_workflow_owners, sub_workflow_repo)
else:
    if not check_all_accounts(sub_workflow_owners, sub_workflow_repo):
        sys.exit()  # Hiçbir aktif işlem yok, çıkıyoruz.
