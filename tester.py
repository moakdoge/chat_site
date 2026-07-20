import requests

BASE_URL = "http://127.0.0.1:8000"


def main():
    # Login
    login_response = requests.post(
        f"{BASE_URL}/api/login/moakdoge",
        json={
            "username": "moakdoge",
            "password": "1234"
        }
    )

    print("Login status:", login_response.status_code)
    print(login_response.text)

    login_data = login_response.json()

    if not login_data.get("success"):
        print("Login failed")
        return

    token = login_data["session_token"]
    user_id = login_data["id"]

    print("Logged in as:", user_id)

    # Send message
    channel = 1  # change this to a real channel

    send_response = requests.post(
        f"{BASE_URL}/channels/{channel}/send",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "content": "Hello from the test CLI!",
            "author": user_id
        }
    )

    print("Send status:", send_response.status_code)
    print(send_response.text)


if __name__ == "__main__":
    main()