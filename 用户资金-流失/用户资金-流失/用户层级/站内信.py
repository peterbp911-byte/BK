import requests
import csv
import os
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import platfrom_config
from platfrom_config import get_platfrom_config, get_platfrom_cookies

CSV_DIR = "D:/TT站内信兑换码"
platfrom_names = ['7ss','vana7','7luck','brlucky','7xx','7aa','novo7', 'b7', 'sp7', 'b777', '1xspin', 'brl77', 'spin77', 'sp1', 'bx365', 'brplay7', 'gana7','brslot', '7pg', 'brspin', 'brwins', 'x7s']

FIELD_MAP = {
    "ID": "ID",
    "标题": "标题",
    "类型": "类型",
    "发送者": "发送者",
    "全局消息": "全局消息",
    "发送统计": ["总计", "已读", "未读"],
    "创建时间": "创建时间",
    "操作": "操作"
}

# ========== 日期范围配置 ==========
START_DATE = datetime(2026, 4, 15)
END_DATE = datetime(2026, 4, 28)

# 分页参数名（根据实际网站修改，如 'page', 'p', 'offset'）
PAGE_PARAM = "page"


def parse_date(date_str):
    """将页面上的日期字符串转为 datetime 对象"""
    # 常见格式：2026-04-15 或 2026/04/15 或 15/04/2026 等
    # 这里尝试几种常见格式
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%Y年%m月%d日"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except:
            continue
    # 如果包含时间，比如 "2026-04-15 10:30:00"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except:
            continue
    return None


def fetch_page(platform_name, session, base_url, page, max_retries=10):
    """抓取指定页码，返回 (表头列表, 数据行列表)"""
    params = {
        "search": "",
        "message_type": "",
        "sender_id": "",
        "is_global": "",
        "size": 50,
        "commit": "搜索",
        PAGE_PARAM: page  # 添加分页参数
    }

    for attempt in range(1, max_retries + 1):
        try:
            res = session.get(base_url, params=params, timeout=30, verify=False)
            if res.status_code != 200:
                print(f"  页 {page} 状态码 {res.status_code}，重试 {attempt}")
                time.sleep(2)
                continue

            soup = BeautifulSoup(res.text, "lxml")
            thead = soup.find("thead")
            if not thead:
                print(f"  页 {page} 无表头，重试 {attempt}")
                time.sleep(1)
                continue

            raw_titles = [th.get_text(strip=True) for th in thead.find_all("th")]
            # 映射表头
            titles_page = []
            for t in raw_titles:
                mapped = FIELD_MAP.get(t, t.replace(" ", "_").lower())
                if isinstance(mapped, list):
                    titles_page.extend(mapped)
                else:
                    titles_page.append(mapped)

            tbody = soup.find("tbody")
            if not tbody:
                print(f"  页 {page} 无表体，重试 {attempt}")
                time.sleep(1)
                continue

            rows = []
            for tr in tbody.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    new_cols = []
                    for idx, col in enumerate(cols):
                        if raw_titles[idx] == "发送统计":
                            m = re.search(r"总计[:：]\s*(\d+).*?已读[:：]\s*(\d+).*?未读[:：]\s*(\d+)", col)
                            if m:
                                new_cols.extend([m.group(1), m.group(2), m.group(3)])
                            else:
                                new_cols.extend(["", "", ""])
                        else:
                            new_cols.append(col)
                    rows.append(new_cols)

            if not rows:
                # 没有数据行，说明没数据了
                return titles_page, []

            return titles_page, rows

        except Exception as e:
            print(f"  页 {page} 异常: {e}，重试 {attempt}")
            time.sleep(2)

    print(f"  页 {page} 失败，跳过")
    return None, []


def main():
    out_dir = os.path.join(CSV_DIR)
    os.makedirs(out_dir, exist_ok=True)

    # 每个平台单独输出一个 CSV 文件（也可改成合并，看个人需求）
    for platform_name in platfrom_names:
        print(f"\n=== 处理平台: {platform_name} ===")

        base_url = platfrom_config.get_platfrom_config(platform_name)["ZN_URL"]

        session = requests.Session()
        session.headers.update({
            "accept": "text/html, application/xhtml+xml",
            "accept-language": "zh-CN,zh;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "referer": base_url,
        })

        cookies = get_platfrom_cookies(platform_name)
        if not cookies:
            print(f"❌ 未获取到 Cookie: {platform_name}")
            continue
        session.cookies.update(cookies)

        # 分页抓取
        all_filtered_rows = []
        titles = None
        page = 1
        stop_flag = False

        while not stop_flag:
            print(f"  抓取第 {page} 页...")
            title_row, rows = fetch_page(platform_name, session, base_url, page)

            if not rows:
                print(f"  第 {page} 页无数据，停止翻页")
                break

            if titles is None and title_row:
                titles = title_row
                # 增加 platform_name 列
                titles.insert(0, "platform_name")
                # 找到“创建时间”列的索引
                try:
                    date_idx = titles.index("创建时间")
                except ValueError:
                    print("⚠️ 表头没有‘创建时间’列，无法按日期过滤，停止")
                    break

            # 确保 rows 的长度和 titles 对得上（多了 platform_name 列，rows 中还没有）
            # 为每行前面插入 platform_name
            for row in rows:
                full_row = [platform_name] + row
                # 提取创建时间（注意 +1 因为插入了 platform_name）
                date_str_raw = full_row[date_idx + 1]  # +1 是因为前面插了一列
                row_date = parse_date(date_str_raw)

                if row_date is None:
                    # 无法解析日期，跳过该行
                    continue

                # 判断是否在目标范围内
                if START_DATE <= row_date <= END_DATE:
                    all_filtered_rows.append(full_row)
                elif row_date < START_DATE:
                    # 由于站内信通常是按创建时间倒序排列（最新的在前）
                    # 一旦遇到早于 START_DATE 的数据，说明后续页更早，可以停止翻页
                    print(f"  发现日期 {date_str_raw} < {START_DATE.strftime('%Y-%m-%d')}，停止翻页")
                    stop_flag = True
                    break

            # 如果没有停止，继续下一页
            if not stop_flag:
                page += 1
                time.sleep(1)  # 礼貌间隔

        # 写入 CSV（只保留过滤后的数据）
        if titles and all_filtered_rows:
            csv_file = os.path.join(out_dir,
                                    f"{platform_name}_站内信_{START_DATE.strftime('%Y%m%d')}_至_{END_DATE.strftime('%Y%m%d')}.csv")
            with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(titles)
                writer.writerows(all_filtered_rows)
            print(f"  已写入 {len(all_filtered_rows)} 条数据到: {csv_file}")
        else:
            print(f"  未找到 {START_DATE.strftime('%Y-%m-%d')} 至 {END_DATE.strftime('%Y-%m-%d')} 范围内的数据")

    print("\n=== 全部完成 ===")


if __name__ == "__main__":
    main()