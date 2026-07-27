import requests
import csv
import os
import time
from bs4 import BeautifulSoup
import datetime
from datetime import datetime, timedelta
import platfrom_config
from platfrom_config import get_platfrom_config,get_platfrom_cookies


CSV_DIR = "D:/TT站内信兑换码"
platfrom_names = ['7ss','vana7','7luck','brlucky','7xx','7aa','novo7','b7','sp7','b777','1xspin','brl77','spin77','sp1','bx365','brplay7','gana7','brslot','7pg','brspin','brwins','x7s']

FIELD_MAP = {
    "ID": "ID",
    "名称": "名称",
    "领取链接": "领取链接",
    "兑换金额": "兑换金额",
    "打码倍数": "打码倍数",
    "供应数量": "供应数量",  
    "已领钱数量": "已领钱数量",
    "有效期": "有效期",
    "状态":"状态",
    "创建人":"创建人",
    "操作":"操作"
}

# ============================================
def fetch_page(platfrom_name, session, BASE_URL, page, max_retries=10):
    params = {
        "page": page,
        "size": 50
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
                titles_page = raw_titles

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

                return titles_page, rows

            except Exception as e:
                print(f"页面{page}异常: {e}，重试{attempt}")
                time.sleep(2)

                print(f"页面{page}失败，跳过")
                return None, []


# ============================================
def main():
    out_dir = os.path.join(CSV_DIR)
    os.makedirs(out_dir, exist_ok=True)
    csv_file = os.path.join(out_dir, f"兑换码.csv")
    
    for platfrom_name in platfrom_names:
  
        print(f"\n=== 处理平台: {platfrom_name} ===")
        
        BASE_URL = platfrom_config.get_platfrom_config(platfrom_name)["DH_URL"]

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

        for page in range(1, 5):  
            titles, rows = fetch_page(platfrom_name, session, BASE_URL, page)

            # 直接写入所有平台数据
            with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                # 只在文件为空时写表头
                if f.tell() == 0 and titles:
                    writer.writerow(["platfrom_name"] + titles)
                for row in rows:
                    writer.writerow([platfrom_name] + row)
            print(f"→ 已写入 {csv_file}（{len(rows)} 条）")
        print("\n=== 完成 ===")

if __name__ == "__main__":
    main()

