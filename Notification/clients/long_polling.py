
import asyncio
import httpx

SERVER_URL = "http://127.0.0.1:8000/long-poll"

async def main():
    last_seen_id = 0
    request_count = 0

    async with httpx.AsyncClient(timeout=40.0) as client:
        while True:
            request_count += 1
            print(f"\nRequest #{request_count}: Waiting...")

            try:
                response = await client.get(
                    SERVER_URL,
                    params={"last_seen_id": last_seen_id}
                )

                response.raise_for_status()
                data = response.json()

                notifications = data["notifications"]

                if notifications:
                    for notification in notifications:
                        print(
                            f"NEW: {notification['message']}"
                        )

                    last_seen_id = max(
                        n["id"] for n in notifications
                    )
                else:
                    print("No new data (timeout)")

            except httpx.HTTPError as error:
                print(f"Request error: {error}")
                await asyncio.sleep(2)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient stopped")
