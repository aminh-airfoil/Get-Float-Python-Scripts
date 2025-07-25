import requests
import os

# Load secrets from environment
float_api_token = os.getenv("FLOAT_API_TOKEN")
n8n_publicholidays_webhook_url = os.getenv("N8N_PUBLICHOLIDAYS_WEBHOOK_URL")
float_url = "https://api.float.com/v3/public-holidays"

# Auth headers
headers = {
    "Authorization": f"Bearer {float_api_token}",
    "Accept": "application/json"
}

# Pagination loop
all_holidays = []
page = 1
while True:
    paged_url = f"{float_url}?page={page}&per_page=50"
    response = requests.get(paged_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error fetching data: {response.status_code}")
        break

    data = response.json()
    if not data:
        break

    all_holidays.extend(data)
    page += 1

# Send to n8n webhook
webhook_response = requests.post(n8n_publicholidays_webhook_url, json=all_holidays)

# Confirm POST status
if webhook_response.status_code == 200:
    print(f"✅ {len(all_holidays)} public holidays sent to n8n successfully!")
else:
    print(f"❌ Failed to send data to n8n. Status code: {webhook_response.status_code}")
    print(webhook_response.text)
