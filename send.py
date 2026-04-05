import requests
import time
import json
import os

# 🔐 TOKEN (shu yerga o'zingni tokeningni qo'y)
BOT_TOKEN = "8362796729:AAHdJ8FUSmck819NFiAuQhGSWy1INwM9boE"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

CHATS_FILE = "chats.json"


# =========================
# 📂 CHATLARNI SAQLASH
# =========================

def load_chats():
    if not os.path.exists(CHATS_FILE):
        return []
    with open(CHATS_FILE, "r") as f:
        return json.load(f)


def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f)


def add_chat(chat_id):
    chats = load_chats()
    if chat_id not in chats:
        chats.append(chat_id)
        save_chats(chats)
        print(f"New chat saved: {chat_id}")


# =========================
# 📤 SEND MESSAGE
# =========================

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, data=data)


# =========================
# 🖼 SEND PHOTO
# =========================

def send_photo(chat_id, photo_file_id, caption=""):
    url = f"{API_URL}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo_file_id,
        "caption": caption
    }
    requests.post(url, data=data)


# =========================
# 🚀 HAMMAGA YUBORISH
# =========================

def broadcast_text(text):
    chats = load_chats()
    for chat_id in chats:
        send_message(chat_id, text)
        time.sleep(1)


def broadcast_photo(caption, file_id):
    chats = load_chats()
    for chat_id in chats:
        send_photo(chat_id, file_id, caption)
        time.sleep(1)


# =========================
# 🔄 UPDATES OQISH
# =========================

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {}
    if offset:
        params["offset"] = offset
    return requests.get(url, params=params).json()


# =========================
# 🤖 MAIN LOOP
# =========================

def main():
    print("Bot started...")

    last_update_id = 0

    while True:
        updates = get_updates(last_update_id + 1)

        if updates.get("ok"):
            for update in updates["result"]:
                last_update_id = update["update_id"]

                if "message" not in update:
                    continue

                msg = update["message"]

                chat_id = msg["chat"]["id"]

                # 🧠 CHAT SAQLASH
                add_chat(chat_id)

                text = msg.get("text")
                caption = msg.get("caption")

                content = text if text else caption

                # =========================
                # 📌 /post COMMAND
                # =========================
                if content and content.startswith("/post"):
                    content = content.replace("/post", "", 1).strip()

                    # 📷 RASM BO'LSA
                    if "photo" in msg:
                        file_id = msg["photo"][-1]["file_id"]
                        broadcast_photo(content, file_id)
                        print("PHOTO SENT")

                    # 📝 TEXT BO'LSA
                    else:
                        broadcast_text(content)
                        print("TEXT SENT")

        time.sleep(2)


# =========================
# ▶️ RUN
# =========================

if __name__ == "__main__":
    main()
