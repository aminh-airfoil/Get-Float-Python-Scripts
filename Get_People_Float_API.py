import requests
import os

# Load secrets from environment
float_api_token = os.getenv("FLOAT_API_TOKEN")
float_url = "https://api.float.com/v3/people"
n8n_people_webhook_url = os.getenv("N8N_PEOPLE_WEBHOOK_URL")

# Auth headers
headers = {
    "Authorization": f"Bearer {float_api_token}",
    "Accept": "application/json"
}

# Pagination loop
all_people = []
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

    all_people.extend(data)
    page += 1

# Send to n8n webhook
response = requests.post(n8n_people_webhook_url, json=all_people)

# Confirm POST status
if response.status_code == 200:
    print(f"✅ {len(all_people)} people sent to n8n successfully!")
else:
    print(f"❌ Failed to send data to n8n. Status code: {response.status_code}")
    print(response.text)
