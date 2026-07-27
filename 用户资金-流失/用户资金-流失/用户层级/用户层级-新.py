import requests
from requests.adapters import HTTPAdapter
import ssl
import csv
import os
import time
from bs4 import BeautifulSoup
import datetime
from datetime import datetime, timedelta
from platfrom_config import get_platfrom_cookies        
import platfrom_config


class TLSAdapter(HTTPAdapter):
    """强制 TLS 1.3 优先，兼容 Cloudflare"""
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.maximum_version = ssl.TLSVersion.TLSv1_3
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

CSV_DIR = r"D:\TT用户分层"
platfrom_names = ['7ss','vana7','7luck','brlucky','7xx','7aa','novo7','b7','sp7','b777','1xspin','brl77','spin77','sp1','bx365','brplay7','gana7','brslot','7pg','brspin','brwins','x7s']

search_params = {
'注册当日未充值':'reg_curday_unpay',
'首充次日未登录':'first_nextday_unlogin',
'首充3日未登录':'first_3d_unlogin',
'首充7日未登录':'first_7d_unlogin',
'首充当日亏损用户':'first_curday_loss'
}

FIELD_MAP = {
    "UID": "UID",
    "平台名称": "平台名称",
    "用户名": "用户名",
    "手机号": "手机号",
    "注册时间": "注册时间",
    "最后登录时间": "最后登录时间"
}


# ============================================
def fetch_page(session, base_url, page, search_key, search_value, yesterday, max_retries=10):
    params = {
        "search": {search_value: search_value},
        "day": yesterday,
        "size": 500,
        "page": page,
    }

    for attempt in range(1, max_retries + 1):
        try:
            res = session.get(
                base_url,
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
def fetch_and_parse_for_search(session, base_url, search_key, search_value, yesterday):
    print(f"\n=== 开始抓取数据: {search_key} ===")
    all_rows = []
    failed_pages = []

    titles_page, rows, total_pages, total_records = fetch_page(session, base_url, 1, search_key, search_value, yesterday)

    print(f"记录 {total_records} 条，共 {total_pages} 页")

    if rows:
        all_rows.extend(rows)
    else:
        failed_pages.append(1)

    # 批量抓取所有页面
    for page in range(2, total_pages + 1):
        time.sleep(0.1)
        _, rows, _, _ = fetch_page(session, base_url, page, search_key, search_value, yesterday)
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
            _, rows, _, _ = fetch_page(session, base_url, page, search_key, search_value, yesterday)
            if rows:
                all_rows.extend(rows)
                print(f"页面{page}重试成功")

    # 提取手机号和平台名
    filtered_rows = []
    phone_idx = None
    plat_idx = None
    if all_rows:
        for i, col in enumerate(titles_page):
            if col == "手机号":
                phone_idx = i
            if col == "平台名称":
                plat_idx = i
        if phone_idx is None:
            print("→ 未找到 手机号 列")
            return []

        for row in all_rows:
            phone = row[phone_idx]
            plat = row[plat_idx] if plat_idx is not None and len(row) > plat_idx and row[plat_idx] else None
            filtered_rows.append((phone, plat))

        return filtered_rows
    else:
        print("→ 无记录")
        return []


# ============================================
def main():
    for day in range(1,2):
        yesterday = (datetime.today() - timedelta(days=day)).strftime("%Y-%m-%d")
        yesterday_folder = (datetime.today() - timedelta(days=day)).strftime("%m%d")

        print(f"\n{'='*60}")
        print(f"  日期: {yesterday} (文件夹: {yesterday_folder})")
        print(f"{'='*60}")

        for platfrom_name in platfrom_names:
            print(f"\n>>> 平台: {platfrom_name}")

            BASE_URL = platfrom_config.get_platfrom_config(platfrom_name)["LE_URL"]

            # === 会话 ===
            session = requests.Session()
            session.mount("https://", TLSAdapter())
            session.headers.update({
                "accept": "text/html, application/xhtml+xml",
                "accept-language": "zh-CN,zh;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "referer": BASE_URL,
            })

            # === Cookie ===
            cookies = get_platfrom_cookies(platfrom_name)
            if not cookies:
                print(f"❌ 未获取到Cookie: {platfrom_name}，跳过")
                continue

            session.cookies.update(cookies)

            out_dir = os.path.join(CSV_DIR, yesterday_folder, platfrom_name)
            os.makedirs(out_dir, exist_ok=True)

            for search_key, search_value in search_params.items():
                filtered_rows = fetch_and_parse_for_search(session, BASE_URL, search_key, search_value, yesterday)
                # 按平台名分组保存
                plat_dict = {}
                for phone, plat in filtered_rows:
                    plat_key = plat if plat else platfrom_name if platfrom_name else "主站"
                    plat_dict.setdefault(plat_key, []).append(phone)
                for plat_key, phones in plat_dict.items():
                    txt_file = os.path.join(out_dir, f"{search_key}_{plat_key}.txt")
                    with open(txt_file, "w", encoding="utf-8") as f:
                        for phone in phones:
                            f.write(phone + "\n")
                    print(f"→ 已写入 {txt_file}（{len(phones)} 条）")

            print(f"\n=== {platfrom_name} {yesterday} 完成 ===")

    print("\n=== 全部完成 ===")

if __name__ == "__main__":
    main()
