import time
import hashlib
import requests

API_URL = "http://localhost:3000/device/real/query"
TOKEN = "interview_token_123"
MAX_BATCH_SIZE = 10
RATE_LIMIT_SECONDS = 1
TOTAL_DEVICES = 500
MAX_RETRIES = 3


def generate_serial_numbers():
    return [f"SN-{str(i).zfill(3)}" for i in range(TOTAL_DEVICES)]


def generate_signature(url, token, timestamp):
    raw_string = f"{url}{token}{timestamp}"
    return hashlib.md5(raw_string.encode()).hexdigest()


def batch_serials(serials, batch_size):
    for i in range(0, len(serials), batch_size):
        yield serials[i:i + batch_size]


def send_request(batch):
    timestamp = str(int(time.time()))
    signature = generate_signature("/device/real/query", TOKEN, timestamp)

    headers = {
        "Authorization": TOKEN,
        "Timestamp": timestamp,
        "Signature": signature,
        "Content-Type": "application/json"
    }

    payload = {
        "sn_list": batch
    }


    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"📤 Sending request (attempt {attempt})...")
            response = requests.post(API_URL, json=payload, headers=headers)

            print(f"📡 Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✅ Batch success\n")
                return response.json()

            elif response.status_code == 429:
                print("⚠️ Rate limit hit. Retrying after 1 second...\n")
                time.sleep(RATE_LIMIT_SECONDS)

            else:
                print(f"❌ Error Response: {response.text}\n")

        except requests.exceptions.RequestException as e:
            print(f"🌐 Network error: {e}\n")

        time.sleep(RATE_LIMIT_SECONDS)

    print("❌ Failed after max retries\n")
    return None


def main():
    print("🚀 Client started\n")

    serials = generate_serial_numbers()
    batches = list(batch_serials(serials, MAX_BATCH_SIZE))

    all_results = []

    print(f"📦 Total devices: {TOTAL_DEVICES}")
    print(f"📨 Total batches: {len(batches)}\n")

    for idx, batch in enumerate(batches, start=1):
        print(f"➡️ Sending batch {idx}/{len(batches)}: {batch}")
        result = send_request(batch)

        if result is not None:
            all_results.append(result)

        time.sleep(RATE_LIMIT_SECONDS)

    print("🎉 All requests completed")
    print(f"📊 Total successful responses: {len(all_results)}")


if __name__ == "__main__":
    main()
