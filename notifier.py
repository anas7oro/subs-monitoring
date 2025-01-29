# notifier.py

import requests
import yaml

def send_notification(domain, new_subdomains):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    webhook_url = config['discord_webhook_url']
    if not webhook_url:
        print("Discord webhook URL not configured.")
        return

    if not new_subdomains:
        return  # No need to send an empty notification

    content = f"**New subdomains found for {domain}:**\n" + "\n".join(new_subdomains)
    data = {"content": content}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(webhook_url, json=data, headers=headers)
        if response.status_code == 204:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification: {response.status_code} | {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")
