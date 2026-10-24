
import time
import httpx

SERVER_URL = "http://127.0.0.1:8000/notifications"
POLL_INTERVAL = 3

last_seen_id = 0
request_count = 0

print("Short polling client started...")

try:
    with httpx.Client(timeout=5.0) as client:
        while True:
            request_count += 1
            print(f"\nRequest #{request_count}: Checking server...")

            try:
                response = client.get(SERVER_URL)
                response.raise_for_status()

                data = response.json()
                notifications = data["notifications"]

                new_notifications = [
                    n for n in notifications
                    if n["id"] > last_seen_id
                ]

                if new_notifications:
                    for notification in new_notifications:
                        print(
                            f"NEW: {notification['message']}"
                        )

                    last_seen_id = max(
                        n["id"] for n in new_notifications
                    )
                else:
                    print("No new notifications")

            except httpx.HTTPError as error:
                print(f"Request failed: {error}")

            time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nClient stopped")
    print(f"Total requests made: {request_count}")
