import requests
import csv
import os
import time
from bs4 import BeautifulSoup
import datetime
from datetime import datetime,timedelta

from platfrom_config import get_platfrom_cookies

login_start_time =  (datetime.today() - timedelta(days= 7 )).strftime("%Y-%m-%d")
login_end_time =  (datetime.today() - timedelta(days= 1 )).strftime("%Y-%m-%d")
yesterday_folder = (datetime.today() - timedelta(days=1)).strftime("%m%d")

CSV_DIR = r"D:\TT用户资金数据"
platfrom_name = 'b777'

# === 请求 URL ===
BASE_URL = f"https://admin.st9gs87zt10up8185rbztdh.{platfrom_name}.games/data_report/user_funds"

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
    return os.path.join(csv_path, f"{platfrom_name}_user_funds.csv")
def csv_need_header(csv_file):
    return not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0

FIELD_MAP = {
    "用户ID": "用户ID",
    "平台名称": "平台名称",
    "手机号": "手机号",
    "总代名称": "总代名称",
    "渠道名称": "渠道名称",
    "注册时间": "注册时间",
    "注册IP": "注册IP",
    "首充次日登录时间": "首充次日登录时间",
    "最近登录时间": "最近登录时间",
    "新手剧本": "新手剧本",
    "总余额": "总余额",
    "历史赠送": "历史赠送",
    "充提差": "充提差",
    "历史充值": "历史充值",
    "今日充值": "今日充值",
    "首笔充值": "首笔充值",
    "首充金额": "首充金额",
    "首充时间": "首充时间",
    "次日充值金额": "次日充值金额",
    "3日充值金额": "3日充值金额",
    "历史充值次数": "历史充值次数",
    "累计充值天数": "累计充值天数",
    "最近充值金额": "最近充值金额",
    "最近充值时间": "最近充值时间",
    "历史提现": "历史提现",
    "今日提现": "今日提现",
    "首次提现": "首次提现",
    "首次提现时间": "首次提现时间",
    "历史提现次数": "历史提现次数",
    "最近提现金额": "最近提现金额",
    "最近提现时间": "最近提现时间",
    "历史RTP": "历史RTP",
    "总流水": "总流水",
    "总输赢": "总输赢",
    "总局数": "总局数",
}

# ============================================
def fetch_page(page, max_retries=6):

    params = {
        "login_start_time": login_start_time,
        "login_end_time": login_end_time,
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

            # 检查响应是否被截断
            if "</html>" not in res.text:
                print(f"页面{page}响应不完整(缺少</html>)，重试{attempt}")
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
                return titles_page, [], 0

            # 解析分页信息，获取实际总页数
            total_pages = 0
            page_info = soup.find("span", string=lambda x: x and "第" in x and "页" in x)
            if page_info:
                try:
                    text = page_info.get_text(strip=True)
                    part = text.split(" ")[0]
                    now_page, tp = part.replace("第", "").replace("页", "").split("/")
                    total_pages = int(tp)
                except Exception:
                    pass

            return titles_page, rows, total_pages

        except Exception as e:
            wait = min(2 * attempt, 10)
            print(f"页面{page}异常: {e}，重试{attempt}，等待{wait}s")
            time.sleep(wait)

    print(f"页面{page}连续{max_retries}次失败")
    return None, [], 0

# ============================================
def fetch_and_parse():

    print(f"\n=== 开始抓取数据 ===")

    all_rows = []
    seen_ids = set()
    titles_final = None
    page = 1
    total_pages = None

    SITE_DOWN_WAITS = [30, 60, 120, 180, 300]
    site_down_retries = 0

    while True:
        titles_page, rows, tp = fetch_page(page)

        if titles_final is None and titles_page:
            titles_final = titles_page

        if tp and tp > 0:
            total_pages = tp
            if page == 1:
                print(f"总页数: {total_pages}")

        if titles_page is None and not rows:
            if site_down_retries < len(SITE_DOWN_WAITS):
                wait = SITE_DOWN_WAITS[site_down_retries]
                site_down_retries += 1
                print(f"⚠ 页面{page}无法访问，第{site_down_retries}次等待{wait}秒后重试...")
                time.sleep(wait)
                continue
            else:
                print(f"✘ 页面{page}长时间无法访问，已等待{sum(SITE_DOWN_WAITS)}秒，数据不完整，放弃保存")
                return

        site_down_retries = 0

        if not rows:
            print(f"页面{page}无数据，抓取结束")
            break

        new_rows = []
        for row in rows:
            uid = row[0]
            if uid not in seen_ids:
                seen_ids.add(uid)
                new_rows.append(row)

        if new_rows:
            all_rows.extend(new_rows)

        if page % 50 == 0:
            print(f"已处理{page}页，当前数据{len(all_rows)}条")

        if total_pages and page >= total_pages:
            print(f"已达总页数{total_pages}，抓取结束")
            break

        if not total_pages and not rows:
            print(f"页面{page}无数据且无总页数，抓取结束")
            break

        page += 1
        time.sleep(0.1)

    # 写入 CSV
    if all_rows:
        csv_file = get_csv_file_path(platfrom_name)
        with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(titles_final)
            for row in all_rows:
                writer.writerow(row)
        print(f"→ {platfrom_name}: 写入 {len(all_rows)} 条记录 → {csv_file}")
    else:
        print("→ 无记录")

# ============================================

if __name__ == "__main__":
    fetch_and_parse()
    print("\n=== 完成 ===")