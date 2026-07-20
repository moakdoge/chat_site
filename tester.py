import requests
import curses

BASE_URL = "http://127.0.0.1:8000"


class ChatTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.token = None
        self.user_id = None
        self.channel_id = None
        self.messages = []

        curses.curs_set(1)
        self.stdscr.clear()

    def login(self):
        username = "moakdoge"
        password = "1234"

        r = requests.post(
            f"{BASE_URL}/api/login/{username}",
            json={
                "username": username,
                "password": password
            }
        )

        data = r.json()

        if not data.get("success"):
            raise Exception("Login failed")

        self.token = data["session_token"]
        self.user_id = data["id"]

    def create_channel(self):
        r = requests.post(
            f"{BASE_URL}/channels/new",
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            json={
                "name": "tui_channel",
                "description": "Created from TUI"
            }
        )

        data = r.json()
        self.channel_id = data["id"]

    def send_message(self, content):
        r = requests.post(
            f"{BASE_URL}/channels/{self.channel_id}/send",
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            json={
                "content": content,
                "author": self.user_id
            }
        )

        return r.ok

    def draw(self):
        self.stdscr.clear()

        height, width = self.stdscr.getmaxyx()

        self.stdscr.addstr(
            0,
            0,
            f"Channel: {self.channel_id} | User: {self.user_id}"
        )

        y = 2
        for msg in self.messages[-(height - 5):]:
            self.stdscr.addstr(y, 0, msg[:width - 1])
            y += 1

        self.stdscr.addstr(
            height - 2,
            0,
            "> "
        )

        self.stdscr.refresh()

    def run(self):
        self.login()
        self.create_channel()

        while True:
            self.draw()

            height, width = self.stdscr.getmaxyx()

            self.stdscr.move(height - 2, 2)
            self.stdscr.clrtoeol()

            msg = self.stdscr.getstr(
                height - 2,
                2
            ).decode()

            if msg == "/quit":
                break

            if not msg.strip():
                continue

            success = self.send_message(msg)

            if success:
                self.messages.append(
                    f"You: {msg}"
                )
            else:
                self.messages.append(
                    "Failed to send message"
                )


def main(stdscr):
    app = ChatTUI(stdscr)

    try:
        app.run()
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(
            0,
            0,
            f"Error: {e}"
        )
        stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)