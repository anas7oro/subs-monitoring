# scheduler.py

import schedule
import time
import yaml
from concurrent.futures import ThreadPoolExecutor

from scanner import run_tools
from storage import save_subdomains
from notifier import send_notification
from targets import list_targets

def scan_and_notify(domain):
    print(f"\nMonitoring {domain}")
    subdomains = run_tools(domain)
    new_subdomains = save_subdomains(domain, subdomains)
    if new_subdomains:
        send_notification(domain, new_subdomains)
    else:
        print(f"No new subdomains found for {domain}.")

def monitor():
    domains = list_targets()
    if not domains:
        print("No domains to monitor.")
        return

    # Adjust max_workers as needed based on your VPS resources
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(scan_and_notify, domains)

def start_scheduler():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    interval = config.get('monitoring_interval', 24)

    schedule.every(interval).hours.do(monitor)
    print(f"Scheduler started. Monitoring every {interval} hours.")
    # Run an immediate scan at startup
    monitor()

    while True:
        schedule.run_pending()
        time.sleep(1)
