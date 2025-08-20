import requests
import os
import logging
import time
from urllib.parse import quote_plus
from dotenv import load_dotenv
from threading import Thread
import sys

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Owner'a göre token seçimi
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
    elif owner == "dinamikfiyatpublic3":
        return os.getenv('DINAMIKFIYATPUBLIC3')
    else:
        logging.warning(f"Bilinmeyen owner: {owner}, default token kullanılıyor.")
        return os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC')

def trigger_workflow(workflow_name, workflow_owner, workflow_repo):
    token = get_token_for_repo(workflow_owner)
    response = requests.post(
        f"https://api.github.com/repos/{workflow_owner}/{workflow_repo}/actions/workflows/{workflow_name}/dispatches",
        json={"ref": "main"},
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 204:
        logging.info(f"Workflow '{workflow_name}' başarıyla tetiklendi.")
    else:
        logging.error(f"Workflow '{workflow_name}' tetiklenemedi: {response.status_code} - {response.text}")
    return response

def check_running_workflows(workflow_owner, workflow_repo):
    token = get_token_for_repo(workflow_owner)
    response = requests.get(
        f"https://api.github.com/repos/{workflow_owner}/{workflow_repo}/actions/runs",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        logging.error(f"Çalışan workflow'lar alınamadı: {response.status_code} - {response.text}")
        return []

    runs = response.json().get("workflow_runs", [])
    return [run for run in runs if run["status"] in ["in_progress", "queued"]]

def wait_for_workflow_to_start(workflow_owner, workflow_repo):
    for _ in range(60):
        running_workflows = check_running_workflows(workflow_owner, workflow_repo)
        if running_workflows:
            logging.info("Workflow başlatıldı.")
            break
        logging.info("Workflow başlatılmadı, 2 saniye sonra tekrar kontrol ediliyor...")
        time.sleep(2)

def wait_for_workflows_to_complete(workflow_owner, workflow_repo):
    while True:
        running_workflows = check_running_workflows(workflow_owner, workflow_repo)
        if not running_workflows:
            logging.info("Tüm workflow'lar tamamlandı.")
            break
        logging.info("Bekleyen workflow'lar var, 25 saniye sonra tekrar kontrol ediliyor...")
        time.sleep(25)

def run_workflow(workflow_name, workflow_owner, workflow_repo):
    trigger_workflow(workflow_name, workflow_owner, workflow_repo)
    wait_for_workflow_to_start(workflow_owner, workflow_repo)
    wait_for_workflows_to_complete(workflow_owner, workflow_repo)

def trigger_group_3_1():
    workflows_group_3_1 = [
        {"workflow_owner": "dinamikfiyatpublic3", "workflow_repo": "anlik_guncel", "workflow_name": "supabase_update_view_yeni_table_ub.yml"}
    ]
    logging.info("Grup 3_1 Workflow'ları başlatılıyor...")
    for workflow in workflows_group_3_1:
        run_workflow(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"])
        
def trigger_group_3_2():
    workflows_group_3_2 = [
        {"workflow_owner": "dinamikfiyatpublic3", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix_ub.yml"}
        
    ]
    logging.info("Grup 3_2 Workflow'ları başlatılıyor...")
    threads = []
    for workflow in workflows_group_3_2:
        thread = Thread(target=run_workflow, args=(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def trigger_group_3_3():
    workflows_group_3_3 = [
        {"workflow_owner": "dinamikfiyatpublic3", "workflow_repo": "anlik_guncel", "workflow_name": "supabase_update_view_yeni_table_ub.yml"}
    ]
    logging.info("Grup 3_3 Workflow'ları başlatılıyor...")
    for workflow in workflows_group_3_3:
        run_workflow(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"])
        
def trigger_group_3_4():
    workflows_group_3_4 = [
        {"workflow_owner": "dinamikfiyatpublic3", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix_ub.yml"}
        
    ]
    logging.info("Grup 3_4 Workflow'ları başlatılıyor...")
    threads = []
    for workflow in workflows_group_3_4:
        thread = Thread(target=run_workflow, args=(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def trigger_group_4():
    workflows_group_4 = [
        {"workflow_owner": "dinamikfiyatpublic3", "workflow_repo": "anlik_guncel", "workflow_name": "scrape_api_markalarım_rakipli_ub.yml"}
        
    ]
    logging.info("Grup 4 Workflow'ları başlatılıyor...")
    threads = []
    for workflow in workflows_group_4:
        thread = Thread(target=run_workflow, args=(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
        

def start_groups():
    group_3_1_thread = Thread(target=trigger_group_3_1)
    group_3_2_thread = Thread(target=trigger_group_3_2)
    group_3_3_thread = Thread(target=trigger_group_3_3)
    group_3_4_thread = Thread(target=trigger_group_3_4)
    group_4_thread = Thread(target=trigger_group_4)
    
    group_3_1_thread.start()
    group_3_1_thread.join()
    group_3_2_thread.start()
    group_3_2_thread.join()
    group_3_3_thread.start()
    group_3_3_thread.join()
    group_3_4_thread.start()
    group_3_4_thread.join()
    group_4_thread.start()
    group_4_thread.join()

if __name__ == "__main__":
    start_groups()
