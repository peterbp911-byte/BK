from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import glob
from datetime import timedelta, datetime
from platfrom_config import get_platfrom_config, PLATFROM_CONFIGS

today = datetime.today().strftime('%Y-%m-%d')
tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

start_time = today + "T06:00"
end_time = tomorrow + "T09:00"
print("开始时间:", start_time)

# 配置 Chrome 浏览器选项
options = Options()
options.add_argument("--start-maximized")  # 最大化窗口，便于调试
options.add_argument("--headless")  # 无界面模式（生产环境启用）

driver = webdriver.Chrome(
    service=Service("C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/session/chromedriver.exe"),
    options=options
)

def login(url, username, password):
    """登录函数"""
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    # 等待用户名输入框出现并填充
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "email_address")))
    username_field.send_keys(username)

    # 填充密码
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    # 点击登录按钮（假设是 submit 类型，根据源码调整 selector）
    login_button = driver.find_element(By.NAME, "button")
    login_button.click()

    # 等待登录成功（URL 跳转离开登录页）
    wait.until(EC.url_changes(url))

def create_redemption_code(platform_name, use_scope, code_name, start_time, end_time, supply_count, generate_count, bet_multiple, amount):
    """自动化创建兑换码函数"""
    # 导航到兑换码创建页面
    redemption_url = get_platfrom_config(platform_name)["REDEMPTION_URL"]
    driver.get(redemption_url)  # 请替换为实际 URL

    wait = WebDriverWait(driver, 20)

    # 定义使用范围（select 下拉）
    use_scope_select = wait.until(EC.presence_of_element_located((By.ID, "redemption_code_use_scope")))
    use_scope_select.send_keys(use_scope)  # e.g., "历史有充值用户" 或 value "recharge"

    # 兑换码名称
    name_field = driver.find_element(By.NAME, "redemption_code[name]")
    name_field.send_keys(code_name)

    # 开始时间（datetime-local，使用 JS 设置以避免 UI 问题）
    start_input = driver.find_element(By.NAME, "redemption_code[start_time]")
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));", start_input, start_time)

    # 结束时间
    end_input = driver.find_element(By.NAME, "redemption_code[end_time]")
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));", end_input, end_time)

    # 供应数量
    supply_field = driver.find_element(By.NAME, "redemption_code[supply_count]")
    supply_field.clear()
    supply_field.send_keys(supply_count)

    # 生成数量
    generate_field = driver.find_element(By.NAME, "redemption_code[generate_count]")
    generate_field.clear()
    generate_field.send_keys(generate_count)

    # 打码倍数
    bet_multiple_field = driver.find_element(By.NAME, "redemption_code[play_ratio]")
    bet_multiple_field.clear()
    bet_multiple_field.send_keys(bet_multiple)

    # 兑换金额
    amount_field = driver.find_element(By.NAME, "redemption_code[amount]")
    amount_field.clear()
    amount_field.send_keys(amount)

    # 点击创建按钮（使用 JS 点击避免被遮挡）
    create_button = driver.find_element(By.NAME, "commit")
    driver.execute_script("arguments[0].scrollIntoView(true);", create_button)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", create_button)

    # 等待创建成功（检查成功提示或新页面元素）
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='兑换码创建成功']")))
        print(f"创建成功, 兑换金额: {amount}")
    except:
        print("创建失败，检查页面")

# 遍历所有平台
amount = [3, 5, 8, 10, 15, 20]

for platform_name, config in PLATFROM_CONFIGS.items():
    if platform_name  not in ['7ss','vana7','7luck','brlucky','7xx','7aa','brl77','novo7','sp7','b7']:
        print(f"\n===== 正在处理平台: {platform_name} =====")
        try:
            login(config["LOGIN_PAGE_URL"], config["USERNAME"], config["PASSWORD"])

            for a in amount:
                create_redemption_code(
                    platform_name=platform_name,
                    use_scope="历史有充值用户",
                    code_name="累充分层",
                    start_time=start_time,
                    end_time=end_time,
                    supply_count="5000",
                    generate_count="1",
                    bet_multiple="8",
                    amount=str(a)
                )
        except Exception as e:
            print(f"平台 {platform_name} 处理失败,跳过需要手动。错误:{e}")


# 关闭浏览器
time.sleep(5)
driver.quit()