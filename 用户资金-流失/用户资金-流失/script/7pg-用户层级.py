import requests
import os
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from platfrom_config import get_platfrom_cookies

yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
yesterday_folder = (datetime.today() - timedelta(days=1)).strftime("%m%d")

CSV_DIR = r"D:\TT用户分层"
platfrom_name = '7pg'

# === 请求 URL ===
BASE_URL = f"https://admin-sc4t56euxk6ohsc8pbuu4ls.{platfrom_name}.games/user/layers"


search_params = {
'注册当日未充值':'reg_curday_unpay',
'首充次日未登录':'first_nextday_unlogin',
'首充3日未登录':'first_3d_unlogin',
'首充7日未登录':'first_7d_unlogin',
'首充当日亏损用户':'first_curday_loss'
}


# === 会话，极大加速 ===
session = requests.Session()
session.headers.update({
    "accept": "text/html, application/xhtml+xml",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "referer": BASE_URL,
})

# === Cookie ===
cookies = get_platfrom_cookies(platfrom_name)
if not cookies:
    print(f"❌ 未获取到Cookie: {platfrom_name}")
    exit(1)

session.cookies.update(cookies)


def get_csv_file_path(platfrom_name):
    """根据平台名称生成CSV文件路径"""
    csv_path = os.path.join(CSV_DIR, yesterday_folder, platfrom_name)
    os.makedirs(csv_path, exist_ok=True)
    return os.path.join(csv_path, f"user_funds_{platfrom_name}.csv")


def csv_need_header(csv_file):
    return not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0


FIELD_MAP = {
    "UID": "UID",
    "平台名称": "平台名称",
    "用户名": "用户名",
    "手机号": "手机号",
    "注册时间": "注册时间",
    "最后登录时间": "最后登录时间"
}


# ============================================
def fetch_page(page, search_key, search_value, max_retries=10):
    params = {
        "search": {search_value: search_value},
        "day": yesterday,
        "size": 500,
        "page": page,
    }

    for attempt in range(1, max_retries + 1):
        try:
            res = session.get(
                BASE_URL,
                params=params,
                timeout=30,
                verify=False
            )

            if res.status_code != 200:
                print(f"页面{page}状态码{res.status_code}，重试{attempt}")
                time.sleep(2)
                continue

            soup = BeautifulSoup(res.text, "lxml")

            thead = soup.find("thead")
            if not thead:
                print(f"页面{page}找不到表头，重试{attempt}")
                time.sleep(1)
                continue

            raw_titles = [th.get_text(strip=True) for th in thead.find_all("th")]

            titles_page = []
            for t in raw_titles:
                titles_page.append(FIELD_MAP.get(t, t.replace(" ", "_").lower()))

            tbody = soup.find("tbody")
            if not tbody:
                print(f"页面{page}找不到表体，重试{attempt}")
                time.sleep(1)
                continue

            rows = []
            for tr in tbody.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    rows.append(cols)

            if not rows:
                print(f"页面{page}无数据行，重试{attempt}")
                time.sleep(1)
                continue

            # 页数解析
            page_info = soup.find("span", string=lambda x: x and "第" in x and "页" in x)
            if page_info:
                text = page_info.get_text(strip=True)
                part = text.split(" ")[0]
                now_page, total_pages = part.replace("第", "").replace("页", "").split("/")
                total_records = int(text.split("共")[1].replace("条记录", "").strip())
            else:
                total_pages = 1
                total_records = len(rows)

            return titles_page, rows, int(total_pages), total_records

        except Exception as e:
            print(f"页面{page}异常: {e}，重试{attempt}")
            time.sleep(2)

    print(f"页面{page}失败，跳过")
    return None, [], 1, 0


# ============================================
def fetch_and_parse_for_search(search_key, search_value):
    print(f"\n=== 开始抓取数据: {search_key} ===")
    all_rows = []
    failed_pages = []

    titles_page, rows, total_pages, total_records = fetch_page(1, search_key, search_value)

    print(f"记录 {total_records} 条，共 {total_pages} 页")

    if rows:
        all_rows.extend(rows)
    else:
        failed_pages.append(1)

    # 批量抓取所有页面
    for page in range(2, total_pages + 1):
        time.sleep(0.1)
        _, rows, _, _ = fetch_page(page, search_key, search_value)
        if rows:
            all_rows.extend(rows)
        else:
            failed_pages.append(page)
        if page % 100 == 0:
            print(f"已处理{page}页，当前数据{len(all_rows)}条")

    # 重试失败页面
    if failed_pages:
        print(f"\n重试{len(failed_pages)}个失败页面...")
        for page in failed_pages:
            time.sleep(1)
            _, rows, _, _ = fetch_page(page, search_key, search_value)
            if rows:
                all_rows.extend(rows)
                print(f"页面{page}重试成功")

    # 提取手机号
    filtered_rows = []
    phone_idx = None
    if all_rows:
        for i, col in enumerate(titles_page):
            if col == "手机号":
                phone_idx = i
        if phone_idx is None:
            print("→ 未找到 手机号 列")
            return []

        for row in all_rows:
            filtered_rows.append(row[phone_idx])

        return filtered_rows
    else:
        print("→ 无记录")
        return []

# ============================================
def main():
    out_dir = os.path.join(CSV_DIR, yesterday_folder, platfrom_name)
    os.makedirs(out_dir, exist_ok=True)

    for search_key, search_value in search_params.items():
        filtered_rows = fetch_and_parse_for_search(search_key, search_value)
        txt_file = os.path.join(out_dir, f"{search_key}.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            if filtered_rows:
                for phone in filtered_rows:
                    f.write(phone + "\n")
        print(f"→ 已写入 {txt_file}（{len(filtered_rows) if filtered_rows else 0} 条）")

    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
