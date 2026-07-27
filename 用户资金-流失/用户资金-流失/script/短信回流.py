import requests
import os
from datetime import datetime, timedelta
import platfrom_config

yesterday = (datetime.today() - timedelta(days=1)).strftime("%m%d")
yesterday_day = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
platfrom_name = ["b777", "1xspin", "brl77",  "spin77", "sp1",  "bx365", "brplay7", "gana7", "brslot", "7pg", "brspin", "brwins", "x7s"]

results = []

for platfrom_name in platfrom_name: 
    url = platfrom_config.get_platfrom_config(platfrom_name)["MESSAGE_URL"]

    cookies_dict = platfrom_config.get_platfrom_cookies(platfrom_name)

    if not cookies_dict:
        print(f"❌ 未获取到Cookie: {platfrom_name}")
        exit(1)
    csrf_token = cookies_dict.pop("csrf_token", "")
    cookie_str = "; ".join(f"{k}={v}" for k, v in cookies_dict.items())

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "cookie": cookie_str,
        "x-csrf-token": csrf_token
    }


    # 遍历 D:\TT用户分层\{yesterday}\{platfrom_name}\ 下的五个txt文件
    txt_dir = os.path.join(r"D:\TT用户分层", yesterday, platfrom_name)
    if not os.path.exists(txt_dir):
        print(f"目录不存在: {txt_dir}，跳过平台 {platfrom_name}")
        continue

    for txt_file in os.listdir(txt_dir):
        if not txt_file.endswith(".txt"):
            continue
        file_path = os.path.join(txt_dir, txt_file)
        search_key = os.path.splitext(txt_file)[0]

        with open(file_path, "r", encoding="utf-8") as f:
            phone_numbers = [line.strip() for line in f if line.strip()]

        if not phone_numbers:
            print(f"[{search_key}] 无号码，跳过")
            continue

        print(f"\n=== {platfrom_name}  {search_key} === 共 {len(phone_numbers)} 个号码")

        payload = {
            "day": yesterday_day,
            "phone_numbers": ",".join(phone_numbers)
        }
        
        for attempt in range(4):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=30)
                print("状态码:", r.status_code)

                if r.status_code !=200:
                    print(f"{search_key} 请求失败,状态码 {r.status_code}")
                    continue
    
                if r.status_code == 200:
                    data = r.json()
                    if data.get("success"):
                        d = data.get("data")
                        break
                        
            except Exception as e:
                print(f"[{search_key}] 出错:", str(e))
                continue

            if not data.get("success"):
                print(f"[{search_key}] 请求失败")
                continue

        #提取关键字段
        phone_count = d.get("total_phone_count", 0)
        recharge_user_count = d.get("recharge_user_count", 0)
        recharge_amount = d.get("recharge_amount", 0.0)
        
        results.append({
            "平台": platfrom_name,
            "流失标签": search_key,
            "号码数量": phone_count,
            "充值用户数": recharge_user_count,
            "充值金额": recharge_amount
        })

# 写入汇总文件
summary_file = os.path.join(r"D:\TT用户分层", yesterday, f"短信回流汇总_{yesterday}.csv")
with open(summary_file, "w", encoding="utf-8-sig") as f:
    f.write("平台,流失标签,号码数量,充值用户数,充值金额\n")
    for res in results:
        f.write(f"{res['平台']},{res['流失标签']},{res['号码数量']},{res['充值用户数']},{res['充值金额']}\n")
    print(f"汇总已写入: {summary_file}")