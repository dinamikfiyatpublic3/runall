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

OWNER = "dinamikfiyatpublic3"  # 🔁 Bu repo sahibini kendine göre değiştir
REPO = "runall"  # 🔁 Bu scriptin çalıştığı ana repo adı
WORKFLOW_FILENAMES = [
    "run_all_kods.yml",
    "run_all_kods_all_manuel.yml",
    "run_all_kods_test.yml"
]

# ✅ Zaten çalışan workflow var mı kontrolü
def is_any_workflow_running():
    token = os.getenv('GITHUB_TOKEN_DINAMIKFIYATPUBLIC1')
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    for workflow_filename in WORKFLOW_FILENAMES:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{workflow_filename}/runs"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"⚠️ Workflow durumu kontrol edilemedi ({workflow_filename}): {response.status_code} - {response.text}")
            continue

        runs = response.json().get("workflow_runs", [])
        for run in runs:
            if run["status"] in ["in_progress", "queued"]:
                logging.warning(f"🚫 Workflow zaten çalışıyor veya kuyruğa alınmış: {workflow_filename}")
                return True

    return False

# 🚫 Workflow çalışıyorsa çık
if is_any_workflow_running():
    logging.warning("🚫 Herhangi bir workflow zaten çalışıyor, çıkılıyor...")
    sys.exit(0)

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

def trigger_group_0():
    workflows_group_0 = [
        {"workflow_owner": "dinamikfyt7", "workflow_repo": "anlik_guncel", "workflow_name": "supabase_timestamp_update.yml"}
    ]
    logging.info("Grup 0 Workflow'ları başlatılıyor...")
    for workflow in workflows_group_0:
        run_workflow(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"])

def trigger_group_1():
    workflows_group_1 = [
        {"workflow_owner": "dinamikfyt1", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt2", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt3", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt4", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt5", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt6", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt7", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_ana_api_scrape_matrix.yml"}
                
    ]
    logging.info("Grup 1 Workflow'ları başlatılıyor...")
    threads = []
    for workflow in workflows_group_1:
        thread = Thread(target=run_workflow, args=(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def trigger_group_2():
    workflows_group_2 = [
        {"workflow_owner": "dinamikfyt5", "workflow_repo": "anlik_guncel", "workflow_name": "supabase_table_yap.yml"},
        {"workflow_owner": "dinamikfyt6", "workflow_repo": "anlik_guncel", "workflow_name": "concurrent_run_api_best_sales.yml"},
        {"workflow_owner": "dinamikfyt3", "workflow_repo": "anlik_guncel", "workflow_name": "scrape_api_urunlerim_rakipli_kalan_monitor.yml"}
    ]
    logging.info("Grup 2 Workflow'ları başlatılıyor...")
    for workflow in workflows_group_2:
        run_workflow(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"])

def trigger_group_3():
    workflows_group_3 = [
        {"workflow_owner": "dinamikfyt1", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt2", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt3", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt4", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt5", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt6", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"},
        {"workflow_owner": "dinamikfyt7", "workflow_repo": "anlik_guncel", "workflow_name": "otomatik_api_scrape_matrix.yml"}
        
    ]
    logging.info("Grup 3 Workflow'ları başlatılıyor...")
    threads = []
    for workflow in workflows_group_3:
        thread = Thread(target=run_workflow, args=(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def trigger_group_4():
    workflows_group_4 = [
        {"workflow_owner": "dinamikfyt4", "workflow_repo": "anlik_guncel", "workflow_name": "supabase_run.yml"}
    ]
    logging.info("Grup 4 Workflow'ları başlatılıyor...")
    for workflow in workflows_group_4:
        run_workflow(workflow["workflow_name"], workflow["workflow_owner"], workflow["workflow_repo"])

def start_groups():
    group_0_thread = Thread(target=trigger_group_0)
    group_1_thread = Thread(target=trigger_group_1)
    group_2_thread = Thread(target=trigger_group_2)
    group_3_thread = Thread(target=trigger_group_3)
    group_4_thread = Thread(target=trigger_group_4)

    group_0_thread.start()
    group_0_thread.join() 
    group_1_thread.start()
    group_1_thread.join()  
    group_2_thread.start()
    group_2_thread.join()
    group_3_thread.start()
    group_3_thread.join()
    group_4_thread.start()
    group_4_thread.join()

if __name__ == "__main__":
    start_groups()
