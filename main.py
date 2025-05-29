import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Tạo thư mục nếu chưa có
os.makedirs("asks", exist_ok=True)
os.makedirs("replies", exist_ok=True)

# Đọc dữ liệu JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Hàm tải file
def download_audio(task):
    url, save_path = task
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        return f"✅ Tải xong: {save_path}"
    except Exception as e:
        return f"❌ Lỗi tải {url}: {e}"

# Tạo danh sách các nhiệm vụ tải
tasks = []

for item in data:
    ask_id = item["_id"]

    # Thêm nhiệm vụ tải cho câu hỏi
    ask_audio_url = item["ask"]["audio"]["url"]
    ask_save_path = os.path.join("ask", f"{ask_id}.mp3")
    tasks.append((ask_audio_url, ask_save_path))

    # Thêm nhiệm vụ tải cho các câu trả lời
    for reply in item["replies"]:
        reply_id = reply["_id"]
        reply_audio_url = reply["audio"]["url"]
        reply_save_path = os.path.join("replies", f"{ask_id}_{reply_id}.mp3")
        tasks.append((reply_audio_url, reply_save_path))

# Dùng ThreadPoolExecutor để tải đa luồng
MAX_THREADS = 10  # Có thể điều chỉnh tùy tốc độ mạng
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    future_to_task = {executor.submit(download_audio, task): task for task in tasks}
    for future in as_completed(future_to_task):
        print(future.result())

