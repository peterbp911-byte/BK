# -*- coding: utf-8 -*-
import time
import datetime
import subprocess
import sys
import logging
import os
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# # Telegram 配置
# TELEGRAM_BOT_TOKEN = '8506427222:AAEtbfZGLROhS8scb2ISPJhxRKHm-lqwgOg'
# TELEGRAM_CHAT_ID = '5228899812'

# 设置日志记录
def setup_logger():
    logger = logging.getLogger("scheduler")
    logger.setLevel(logging.INFO)

    # 日志文件放脚本同目录下的 logs 文件夹
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "任务日志.log")

    # 文件 handler
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
PYTHON_EXECUTABLE = sys.executable

# 11个脚本任务
SCRIPTS = [
   # {"name": "1xspin", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/登录.py", "time": (11,5)},
   #  {"name": "novo7", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/novo7.py", "time": (11,30)},
   #  {"name": "sp7", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/sp7.py", "time": (11,30)},
   #  {"name": "b7", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/b7.py", "time": (11,30)},
   #  {"name": "1xspin", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/1xspin.py", "time": (11,30)},
   #  {"name": "sp1", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/sp1.py", "time": (11,30)},
    {"name": "b777", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/b777.py", "time": (11,30)},
   #  {"name": "brplay7", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/brplay7.py", "time": (11,30)},
   #  {"name": "spin77", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/spin77.py", "time": (11,30)},
   #  {"name": "brl77", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/brl77.py", "time": (11,30)},
    {"name": "bx365", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/bx365.py", "time": (11,30)},
    {"name": "gana7", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/gana7.py", "time": (11,30)},
    {"name": "brslot", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/brslot.py", "time": (11,30)},
    {"name": "7pg", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/7pg.py", "time": (11,30)},
    {"name": "brspin", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/brspin.py", "time": (11,30)},
    {"name": "brwins", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/brwins.py", "time": (11,30)},
    {"name": "x7s", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/x7s.py", "time": (11,30)},
    {"name": "用户资金", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/用户资金.py", "time": (12,5)},
    {"name": "清洗", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/清洗.py", "time": (14,1)},
    {"name": "每日兑换码", "script": "C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/每日兑换码.py", "time": (14,1)},
]

# def send_telegram_message(message):
#     """发送消息到 Telegram"""
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": message,
#         "parse_mode": "HTML"
#     }
#     try:
#         response = requests.post(url, json=payload, timeout=10)
#         response.raise_for_status()
#         logger.info("✅ Telegram 消息发送成功")
#     except Exception as e:
#         logger.error(f"❌ Telegram 发送失败: {e}")

def execute_script(script_name, script_path):
    """执行单个脚本"""
    logger.info(f"开始执行: {script_name}")
    start_time = datetime.datetime.now()
    
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [PYTHON_EXECUTABLE, script_path],
            capture_output=True,
            text=True,
            timeout=7200,  # 改为 3+ 小时
            encoding='utf-8',
            env=env
        )
        
        duration = (datetime.datetime.now() - start_time).total_seconds()
        
        if result.returncode == 0:
            logger.info(f"✅ {script_name} 完成 - 耗时 {duration:.0f} 秒")
            return {"name": script_name, "status": "✅ 成功", "duration": duration, "returncode": 0}
        else:
            logger.error(f"❌ {script_name} 失败 - 退出码: {result.returncode}")
            if result.stderr:
                logger.error(f"错误信息: {result.stderr[:500]}")
            return {"name": script_name, "status": "❌ 失败", "duration": duration, "returncode": result.returncode}
    
    except subprocess.TimeoutExpired:
        logger.error(f"⏱ {script_name} 超时 (2小时)")
        return {"name": script_name, "status": "⏱ 超时", "duration": 21600, "returncode": -1}
    except Exception as e:
        logger.error(f"❌ {script_name} 异常: {str(e)}")
        return {"name": script_name, "status": "❌ 异常", "duration": 0, "returncode": -1}

def execute_batch_by_time(task_time, scripts_to_run):
    """按时间执行一批脚本（并行执行）"""
    logger.info(f"=== 开始执行时间 {task_time[0]:02d}:{task_time[1]:02d} 的脚本 ===")
    logger.info(f"共 {len(scripts_to_run)} 个脚本，并行执行")
    batch_start = datetime.datetime.now()
    results = []
    
    # 并行执行脚本
    with ThreadPoolExecutor(max_workers=len(scripts_to_run)) as executor:
        futures = {
            executor.submit(execute_script, script_info["name"], script_info["script"]): script_info 
            for script_info in scripts_to_run
        }
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            logger.info(f"脚本完成: {result['name']} - {result['status']}")
    
    batch_duration = (datetime.datetime.now() - batch_start).total_seconds()
    logger.info(f"批次耗时: {batch_duration:.0f} 秒")
    return results, batch_duration

def format_report(all_results, batch_times):
    """格式化报告"""
    report = "📊 <b>用户资金流失数据爬取任务</b>\n\n"
    
    success_count = sum(1 for r in all_results if r["status"] == "✅ 成功")
    total_count = len(all_results)
    total_duration = sum(r["duration"] for r in all_results)
    
    report += f"<b>执行统计:</b>\n"
    report += f"✅ 成功: {success_count}/{total_count}\n"
    report += f"⏱ 总耗时: {total_duration:.0f} 秒 (~{total_duration/60:.1f} 分钟)\n\n"
    
    report += "<b>详细结果:</b>\n"
    for result in all_results:
        report += f"{result['status']} {result['name']:<15} ({result['duration']:.0f}s)\n"
    
    report += f"\n⏰ 执行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return report

def wait_for_tasks():
    """主循环：等待并执行任务"""
    logger.info("✅ 任务调度器启动")
    executed_today = False

    while True:
        now = datetime.datetime.now()
        current_time = (now.hour, now.minute)
        current_date = now.date()

        # 计划时间（小时, 分钟）
        time_a = (11,5)
        time_b = (14,15)

        # 重置日期标记
        if not hasattr(wait_for_tasks, 'last_date') or wait_for_tasks.last_date != current_date:
            executed_today = False
            wait_for_tasks.last_date = current_date

        # 执行任务
        if not executed_today and (current_time == time_a or current_time == time_b):
            logger.info(f"检测到任务执行时间: {current_time[0]:02d}:{current_time[1]:02d}")
            
            all_results = []
            batch_times = []
            
            # time_a 的脚本
            scripts_a = [s for s in SCRIPTS if s["time"] == time_a]
            if scripts_a and current_time == time_a:
                logger.info(f"执行 time_a ({time_a[0]:02d}:{time_a[1]:02d}) 的 {len(scripts_a)} 个脚本")
                results, duration = execute_batch_by_time(time_a, scripts_a)
                all_results.extend(results)
                batch_times.append(duration)
            
            # time_b 的脚本
            scripts_b = [s for s in SCRIPTS if s["time"] == time_b]
            if scripts_b and current_time == time_b:
                logger.info(f"执行 time_b ({time_b[0]:02d}:{time_b[1]:02d}) 的 {len(scripts_b)} 个脚本")
                results, duration = execute_batch_by_time(time_b, scripts_b)
                all_results.extend(results)
                batch_times.append(duration)
            
            # 生成报告并发送
            if all_results:
                report = format_report(all_results, batch_times)
                logger.info("\n" + report)
                # send_telegram_message(report)
                executed_today = True
        
        time.sleep(60)  # 每 60 秒检查一次

if __name__ == "__main__":
    try:
        wait_for_tasks()
    except KeyboardInterrupt:
        logger.info("📛 程序已手动停止")
    except Exception as e:
        logger.error(f"❌ 程序异常: {str(e)}", exc_info=True)
        # send_telegram_message(f"❌ <b>任务调度器异常</b>\n错误: {str(e)}")
    finally:
        logging.shutdown()
