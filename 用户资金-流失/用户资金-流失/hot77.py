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
platfrom_name = 'hot77'

# === 请求 URL ===
BASE_URL = f"https://admin.skro1oxpzwq0hm320rb7vfm.{platfrom_name}.games/data_report/user_funds"

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

def fetch_page(page, max_retries=4):

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
                return titles_page, []

            return titles_page, rows

        except Exception as e:
            print(f"页面{page}异常: {e}，重试{attempt}")
            time.sleep(2)

    print(f"页面{page}失败，跳过")
    return None, []

# ============================================
def fetch_and_parse():

    print(f"\n=== 开始抓取数据 ===")

    all_rows = []
    seen_ids = set()
    titles_final = None
    page = 1
    page_size = None

    while True:
        titles_page, rows = fetch_page(page)

        if titles_final is None and titles_page:
            titles_final = titles_page

        if not rows:
            print(f"页面{page}无数据，抓取结束")
            break

        # 第一页确定每页条数
        if page_size is None:
            page_size = len(rows)

        # 用第一列(用户ID)去重，防止服务器返回重复数据
        new_rows = []
        for row in rows:
            uid = row[0]
            if uid not in seen_ids:
                seen_ids.add(uid)
                new_rows.append(row)

        if not new_rows:
            print(f"页面{page}全部重复，抓取结束")
            break

        all_rows.extend(new_rows)

        if page % 50 == 0:
            print(f"已处理{page}页，当前数据{len(all_rows)}条")

        # 最后一页
        if len(rows) < page_size:
            print(f"页面{page}为最后一页，抓取结束")
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