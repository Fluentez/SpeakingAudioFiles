import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

# Đọc dữ liệu JSON từ file
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tạo thư mục lưu
ask_dir = "asks"
reply_dir = "replies"
os.makedirs(ask_dir, exist_ok=True)
os.makedirs(reply_dir, exist_ok=True)

# Danh sách công việc để tải
download_jobs = []

# Tạo danh sách job download cho asks và replies
for i, item in enumerate(data, start=1):
    ask_url = item.get("ask", {}).get("audio", {}).get("url")
    if ask_url:
        ask_filename = os.path.join(ask_dir, f"ask-{i}.mp3")
        download_jobs.append((ask_url, ask_filename))

    for j, reply in enumerate(item.get("replies", []), start=1):
        reply_url = reply.get("audio", {}).get("url")
        if reply_url:
            reply_filename = os.path.join(reply_dir, f"ask-{i}-reply-{j}.mp3")
            download_jobs.append((reply_url, reply_filename))

# Hàm tải file
def download_audio(url, filename):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Tải xong: {filename}")
    except Exception as e:
        print(f"❌ Lỗi khi tải {filename} từ {url}: {e}")

# Tải đa luồng
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(lambda job: download_audio(*job), download_jobs)

