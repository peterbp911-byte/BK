import requests
import platfrom_config
from platfrom_config import get_platfrom_cookies
import get_cookies
import time
import json
import psycopg2
from psycopg2 import sql
from typing import List, Optional

def build_day_range(days_ago: int):
    day = time.localtime(time.time() - days_ago * 24 * 3600)
    start_ms = int(time.mktime((day.tm_year, day.tm_mon, day.tm_mday, 0, 0, 0, 0, 0, -1)) * 1000)
    end_ms = int(time.mktime((day.tm_year, day.tm_mon, day.tm_mday, 23, 59, 59, 0, 0, -1)) * 1000)
    return start_ms, end_ms


# 唯一建约束，按目标表名或报表类型配置
TABLE_CONFLICT_COLUMNS = {
    "A8_opration_data": ["statisDate"],
    "M9_opration_data": ["statisDate"], 
    "T1_opration_data": ["statisDate"],
    "A8_deposit_member_record": ["orderNo"],
    "M9_deposit_member_record": ["orderNo"],
    "T1_deposit_member_record": ["orderNo"],
    "A8_game_statistics_report":["reportDate"],
    "M9_game_statistics_report":["reportDate"], 
    "T1_game_statistics_report":["reportDate"],
    "A8_platfrom_daily_revenue":["reportDate"],
    "M9_platfrom_daily_revenue":["reportDate"],
    "T1_platfrom_daily_revenue":["reportDate"]
}

# URL key -> table suffix mapping
URL_TABLE_MAP = {
    "opr_url": "opration_data",
    "game_url": "game_statistics_report",
    "dRe_url": "deposit_member_record",
    "kpi_url": "platfrom_daily_revenue",
}


def get_conflict_columns(table_name: str) -> List[str]:
    return TABLE_CONFLICT_COLUMNS.get(table_name, [])


def get_tenant_sys(plat: str) -> str:
    return f"{plat.lower()}sport"

def upload_to_db(
    plat: str,
    url_or_table: str,
    result_list,
    conflict_cols: Optional[List[str]] = None,
):
    """Upload items to PostgreSQL table. `url_or_table` may be a URL key (e.g. 'game_url') or a table name."""
    # determine target table name from url_or_table
    if url_or_table in URL_TABLE_MAP:
        suffix = URL_TABLE_MAP[url_or_table]
        table_name = f"{plat}_{suffix}"
    elif url_or_table.endswith("_url"):
        suffix = url_or_table.replace("_url", "")
        table_name = f"{plat}_{suffix}_data"
    else:
        table_name = url_or_table
    if result_list is None:
        print(f"❌ {plat} 没有要上传的数据")
        return False

    if not isinstance(result_list, list):
        result_list = [result_list]

    if not result_list:
        print(f"❌ {plat} 结果列表为空，不执行插入")
        return False

    if conflict_cols is None:
        conflict_cols = get_conflict_columns(table_name)

    conn_params = {
        "host": "localhost",
        "port": 5432,
        "dbname": "postgres",
        "user": "postgres",
        "password": "147258",
    }

    table_identifier = sql.Identifier(table_name)
    columns = list(result_list[0].keys())
    columns_sql = sql.SQL(', ').join(sql.Identifier(col) for col in columns)
    values_sql = sql.SQL(', ').join(sql.Placeholder() for _ in columns)


    if conflict_cols:
        valid_conflict_cols = [col for col in conflict_cols if col in columns]
        if valid_conflict_cols:
            conflict_sql = sql.SQL(', ').join(sql.Identifier(col) for col in valid_conflict_cols)

            insert_sql = sql.SQL(
                "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO NOTHING"
            ).format(table_identifier, columns_sql, values_sql, conflict_sql)

        else:
            print(f"⚠️ {plat} 冲突列 {conflict_cols} 未全部在结果列中找到，改为无冲突插入")
            insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(table_identifier, columns_sql, values_sql)
    else:
        insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(table_identifier, columns_sql, values_sql)


    try:
        inserted_count = 0
        skipped_count = 0
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                for item in result_list:
                    values = [item.get(col) for col in columns]
                    try:
                        cur.execute(insert_sql, values)
                        rc = getattr(cur, 'rowcount', 0) or 0
                        if isinstance(rc, int) and rc > 0:
                            inserted_count += rc
                    except psycopg2.errors.UniqueViolation:
                        skipped_count += 1
                        conn.rollback()
                        # 重置游标状态后继续下一条
                        cur = conn.cursor()
                    except Exception as exc:
                        print(f"❌ {plat} 插入单行失败: {exc}")
                        conn.rollback()
                        continue

        if conflict_cols:
            print(f"✅ {plat} 实际插入 {inserted_count} / {len(result_list)} 条到 {table_name}，跳过 {skipped_count} 重复项，冲突列: {conflict_cols}")
        else:
            print(f"✅ {plat} 实际插入 {inserted_count} / {len(result_list)} 条到 {table_name}，跳过 {skipped_count} 重复项")
        return True
    except Exception as exc:
        print(f"❌ {plat} 上传数据库失败: {exc}")
        return False


def calw(plat, url_key: str, startTime, endTime):
    """Fetch report for given url_key from platfrom_config and return result list."""
    print(f"正在处理平台: {plat} {url_key}")
    config = platfrom_config.get_platfrom_config(plat)
    if not config:
        print(f"❌ 未找到平台配置: {plat}")
        return None

    URL = config.get(url_key)
    if not URL:
        print(f"❌ {plat} 未配置 {url_key}")
        return None

    cookies_data = get_platfrom_cookies(plat)
    if not cookies_data or not isinstance(cookies_data, dict):
        print(f"❌ {plat} 未能读取 cookies 数据，请检查 session/cookies_{plat}.json 是否存在")
        return None

    cookies_dict = cookies_data.get("cookies") or {}
    sakura_value = cookies_data.get("sakura") or cookies_dict.get("TokenKey")
    token_header_name = cookies_data.get("sakura_header_name") or cookies_dict.get("TokenHeaderKey") or "sakura"
    cookie_header = "; ".join(f"{name}={value}" for name, value in cookies_dict.items())

    if not sakura_value:
        print(f"⚠️ {plat} 未找到 sakura token，cookies keys={list(cookies_dict.keys())}")

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN",
        "agentflag": "0",
        "content-type": "application/json",
        "cookie": cookie_header,
        "origin": "https://admin-tenant.t1game888.com",
        "referer": "https://admin-tenant.t1game888.com/agentManagementNews/depositQuota",
        "tenantsys": get_tenant_sys(plat),
        "udid": "1683281bb5fec480e3ed98ed3347af89",
        "user-agent": "Mozilla/5.0",
        "usertype": "2",
        "x-language": "CN",
    }
    if sakura_value:
        headers[token_header_name] = sakura_value
        print(f"{plat} 使用 header {token_header_name}={sakura_value[:50]}...")

    collected = []
    page = 1
    while page <= 100:

        payload = {
            "startTime": startTime,
            "endTime": endTime,
            "pageNum": page,
            "pageSize": 1000,
        }

        try:
            response = requests.post(URL, headers=headers, json=payload, timeout=20)
        except Exception as e:
            print(f"❌ {plat} 请求异常: {e}")
            return None

        if response.status_code == 200:
            try:
                resp_json = response.json()
            except Exception:
                print(f"❌ {plat} {url_key} 返回无法解析为 JSON")
                return None

            data = resp_json.get("data")

            if isinstance(data, dict) and "list" in data:
                result_list = data["list"]
            elif isinstance(data, list):
                result_list = data
            elif resp_json.get("rows"):
                result_list = resp_json.get("rows")
            else:
                result_list = None

            if not result_list:
                if page == 1:
                    print(f"❌ {plat} {url_key} 未获取到数据或列表为空")
                    return None
                break

            collected.extend(result_list)
            print(f"{plat} {url_key} 第 {page} 页抓取 {len(result_list)} 条")

            if len(result_list) < 1000:
                break
            page += 1
            continue

        if response.status_code == 401 or (response.status_code == 200 and response.json().get("code") == 401):
            print(f"❌ {plat} {url_key} 请求未授权, Cookie 过期或无效")
            if get_cookies.main(plat):
                cookies_data = get_platfrom_cookies(plat)
                if cookies_data and isinstance(cookies_data, dict):
                    cookies_dict = cookies_data.get("cookies") or {}
                    sakura_value = cookies_data.get("sakura") or cookies_dict.get("TokenKey")
                    token_header_name = cookies_data.get("sakura_header_name") or cookies_dict.get("TokenHeaderKey") or "sakura"
                    cookie_header = "; ".join(f"{name}={value}" for name, value in cookies_dict.items())
                    headers["cookie"] = cookie_header
                    if sakura_value:
                        headers[token_header_name] = sakura_value
                    print(f"已刷新 {plat} {url_key} 请求头, header={token_header_name}, cookie_keys={list(cookies_dict.keys())}")
                    print(f"刷新后 token header: {token_header_name}={sakura_value[:50]}...")
                    time.sleep(1)
                    continue
                print(f"❌ {plat} 刷新后仍未读取到 cookies 数据")
                return None
            print(f"❌ {plat} 刷新 Cookie 失败")
            return None

        print(f"❌ {plat} {url_key} 请求失败，状态码: {response.status_code}")
        return None

    if not collected:
        print(f"❌ {plat} {url_key} 未获取到任何数据")
        return None

    print(f"{plat} {url_key} 共抓取 {len(collected)} 条，页数 {page if page <= 20 else 20}")
    return collected



def main(plat: str, startTime: int, endTime: int):
    # iterate over the four report endpoints and upload each
    keys = [ "dRe_url"]
    for key in keys:
        try:
            result_list = calw(plat, key, startTime, endTime)
            if result_list:
                upload_to_db(plat, key, result_list)
        except Exception as e:
            print(f"❌ {plat} 处理 {key} 时出错: {e}")


if __name__ == "__main__":
    platfrom_name =  ['A8','M9','T1']

    for days_ago in range(26, 0, -1):
        startTime, endTime = build_day_range(days_ago)
        print(f"days_ago={days_ago}, startTime={startTime}, endTime={endTime}")
        for plat in platfrom_name:
            main(plat, startTime, endTime)
    

