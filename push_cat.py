import json
import hashlib
import hmac
import requests
# endpoint = "https://dev.buzzo.ai/api/v2/elecroom/add"     #UAT
endpoint = "https://haptikapi.net/api/v2/elecroom/add"   #production
# endpoint = "https://staging.haptikapi.net/api/v2/elecroom/add" #stagging
# secret_key = "889a9749-4466-4049-911d-e4f311f2fc85"       #UAT
secret_key = "7c5ed0ca-00f0-4110-a237-b86f10a80ac7"         #production
# secret_key = "66554593-1649-47f9-9c69-ae56e7c5bdab"         #stagging
batch_size = 300
headers = {
    'X-HUB-Signature': 'secret_key',
    'Content-Type': 'application/json'
}
# Read the JSON data from the file
with open("./bencatwithrank.json", encoding="utf-8") as file:
# with open('all.json', 'r') as file:
    request_body = json.load(file)
# Split the request body into batches
batches = [request_body[i:i+batch_size] for i in range(0, len(request_body), batch_size)]
total_batches = len(batches)
record_count = 0
for index, batch in enumerate(batches, 1):
    # Convert the batch to a JSON string
    batch_json = json.dumps(batch)
    # Generate the HMAC signature using the secret key and batch JSON
    signature = hmac.new(secret_key.encode(), batch_json.encode(), hashlib.sha256).hexdigest()
    # Update the headers with the HMAC signature
    headers['X-HUB-Signature'] = signature
    # Send the POST request for the current batch
    response = requests.post(endpoint, headers=headers, json=batch)
    # Check the response status
    if response.status_code == 200:
        record_count += len(batch)
        print(f"Batch {index}/{total_batches} successfully sent. Records: {len(batch)}")
    else:
        print(f"Failed to send batch {index}/{total_batches}. Status code: {response.text}")
print(f"All batches sent. Total records sent: {record_count}")
