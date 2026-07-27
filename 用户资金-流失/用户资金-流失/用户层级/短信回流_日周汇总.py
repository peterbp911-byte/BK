import requests
import json
import os
from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import platfrom_config

# 定义两周的日期范围
week1_dates = []  #
week2_dates = []  #

for day_offset in range(1):
    d1 = date(2026, 4, 28) + timedelta(days=day_offset)
    d1_folder = d1.strftime("%m%d")
    d1_api = (d1 + timedelta(days=1)).strftime("%Y-%m-%d")  # 第二天
    week1_dates.append({
        "folder": d1_folder,
        "api_day": d1_api,
    })
    d2 = date(2026, 5, 5) + timedelta(days=day_offset)
    d2_folder = d2.strftime("%m%d")
    d2_api = (d2 + timedelta(days=1)).strftime("%Y-%m-%d")  # 第二天
    week2_dates.append({
        "folder": d2_folder,
        "api_day": d2_api,
    })

weeks = [
    {"name": "第一周(4.29-5.05)", "dates": week1_dates, "label": "0429-0505"},
    {"name": "第二周(5.06-5.12)", "dates": week2_dates, "label": "0506-0512"},
]

platfrom_names = ['7ss','vana7','7luck','brlucky','7xx','7aa','novo7','b7','sp7','b777','1xspin','brl77','spin77','sp1','bx365','brplay7','gana7','brslot','7pg','brspin','brwins','x7s']

results_lock = threading.Lock()


def process_platform_day(platfrom_name, day_info, week_name):
    """处理单个平台单天的所有txt文件，返回结果列表"""
    folder_name = day_info["folder"]
    api_day = day_info["api_day"]
    day_results = []

    url = platfrom_config.get_platfrom_config(platfrom_name)["MESSAGE_URL"]
    cookies_dict = dict(platfrom_config.get_platfrom_cookies(platfrom_name))  # 拷贝，避免并发修改

    if not cookies_dict:
        print(f"❌ 未获取到Cookie: {platfrom_name}")
        return day_results
    csrf_token = cookies_dict.pop("csrf_token", "")
    cookie_str = "; ".join(f"{k}={v}" for k, v in cookies_dict.items())

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "cookie": cookie_str,
        "x-csrf-token": csrf_token
    }

    txt_dir = os.path.join(r"D:\TT用户分层", folder_name, platfrom_name)
    if not os.path.exists(txt_dir):
        return day_results

    for txt_file in os.listdir(txt_dir):
        if not txt_file.endswith(".txt"):
            continue
        file_path = os.path.join(txt_dir, txt_file)
        search_key = os.path.splitext(txt_file)[0]

        with open(file_path, "r", encoding="utf-8") as f:
            phone_numbers = [line.strip() for line in f if line.strip()]

        if not phone_numbers:
            continue

        print(f"--- {platfrom_name} | {folder_name} | {search_key} --- 共 {len(phone_numbers)} 个号码")

        payload = {
            "day": api_day,
            "phone_numbers": ",".join(phone_numbers)
        }

        d = None
        for attempt in range(4):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=30)
                if r.status_code != 200:
                    print(f"[{platfrom_name}|{folder_name}|{search_key}] 状态码 {r.status_code}，重试{attempt+1}")
                    continue
                data = r.json()
                if data.get("success"):
                    d = data.get("data")
                    break
                else:
                    print(f"[{platfrom_name}|{folder_name}|{search_key}] 请求未成功，重试{attempt+1}")
                    continue
            except Exception as e:
                print(f"[{platfrom_name}|{folder_name}|{search_key}] 出错: {e}，重试{attempt+1}")
                continue

        if d is None:
            print(f"[{platfrom_name}|{folder_name}|{search_key}] 多次重试后仍失败，跳过")
            continue

        phone_count = int(d.get("total_phone_count", 0))
        recharge_user_count = int(d.get("recharge_user_count", 0))
        recharge_amount = float(d.get("recharge_amount", 0))

        day_results.append({
            "周": week_name,
            "日期": api_day,
            "平台": platfrom_name,
            "流失标签": search_key,
            "号码数量": phone_count,
            "充值用户数": recharge_user_count,
            "充值金额": recharge_amount
        })

    return day_results


def process_platform_week(platfrom_name, week_dates, week_name):
    """处理单个平台一整周的数据（按天顺序执行，避免同平台并发冲突）"""
    all_results = []
    for day_info in week_dates:
        day_results = process_platform_day(platfrom_name, day_info, week_name)
        all_results.extend(day_results)
    return all_results


results = []  # 每日明细

for week in weeks:
    week_name = week["name"]
    week_label = week["label"]
    summary = {}

    print(f"\n{'#'*60}")
    print(f"  {week_name}")
    print(f"{'#'*60}")

    # 按平台并发，每个平台内按天顺序执行（避免同平台并发冲突）
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(process_platform_week, plat, week["dates"], week_name): plat
            for plat in platfrom_names
        }
        for future in as_completed(futures):
            plat = futures[future]
            try:
                plat_results = future.result()
                for item in plat_results:
                    results.append(item)
                    key = (item["平台"], item["流失标签"])
                    if key not in summary:
                        summary[key] = {"号码数量": 0, "充值用户数": 0, "充值金额": 0.0}
                    summary[key]["号码数量"] += item["号码数量"]
                    summary[key]["充值用户数"] += item["充值用户数"]
                    summary[key]["充值金额"] += item["充值金额"]
                print(f"✅ {plat} {week_name} 完成，{len(plat_results)} 条记录")
            except Exception as e:
                print(f"[{plat}] 任务异常: {e}")

    # 写入本周汇总
    summary_file = os.path.join(r"D:\TT用户分层", f"短信回流_{week_label}_周汇总.csv")
    with open(summary_file, "w", encoding="utf-8-sig") as f:
        f.write(f"平台,流失标签,号码数量(总计),充值用户数(总计),充值金额(总计)\n")
        total_phone = 0
        total_recharge_user = 0
        total_recharge_amount = 0.0
        for (plat, tag), vals in sorted(summary.items()):
            f.write(f"{plat},{tag},{vals['号码数量']},{vals['充值用户数']},{vals['充值金额']}\n")
            total_phone += vals["号码数量"]
            total_recharge_user += vals["充值用户数"]
            total_recharge_amount += vals["充值金额"]
        f.write(f"合计,全部,{total_phone},{total_recharge_user},{total_recharge_amount}\n")
    print(f"\n{week_name} 汇总已写入: {summary_file}")

# 写入全部明细
detail_file = os.path.join(r"D:\TT用户分层", f"短信回流_两周明细_0428-0512.csv")
with open(detail_file, "w", encoding="utf-8-sig") as f:
    f.write("周,日期,平台,流失标签,号码数量,充值用户数,充值金额\n")
    for res in results:
        f.write(f"{res['周']},{res['日期']},{res['平台']},{res['流失标签']},{res['号码数量']},{res['充值用户数']},{res['充值金额']}\n")
print(f"\n每日明细已写入: {detail_file}")
print("\n=== 全部完成 ===")
