import requests
import os

# Load secrets from environment
float_api_token = os.getenv("FLOAT_API_TOKEN")
n8n_allocation_webhook_url = os.getenv("N8N_ALLOCATION_WEBHOOK_URL")
float_url = "https://api.float.com/v3/tasks?page=1&per_page=50"

# Auth headers
headers = {
    "Authorization": f"Bearer {float_api_token}",
    "Accept": "application/json"
}

# Single page fetch (no loop for now)
response = requests.get(float_url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error fetching data: {response.status_code}")
    exit()

data = response.json()

# Send to n8n webhook
webhook_response = requests.post(n8n_allocation_webhook_url, json=data)

# Confirm POST status
if webhook_response.status_code == 200:
    print(f"✅ {len(data)} allocations live data sent to n8n successfully!")
else:
    print(f"❌ Failed to send data to n8n. Status code: {webhook_response.status_code}")
    print(webhook_response.text)
