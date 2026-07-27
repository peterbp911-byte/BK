#登录获取cookies和saukral
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import shutil
from platfrom_config import get_platfrom_config
import pyotp
from seleniumwire import webdriver


COOKIES_DIR = "C:/Users/Richa/Desktop/A8现有报表/session"

def login_and_save_profile(platfrom_name):
    """登录指定平台并保存cookies"""
    config = get_platfrom_config(platfrom_name)
    if not config:
        print(f"❌ 未找到平台配置: {platfrom_name}")
        return False
    
    login_url = config.get('LOGIN_PAGE_URL')
    username = config.get('USERNAME')
    password = config.get('PASSWORD')
    verify_key = config.get('google_key')     #or config.get('haiyue_key')  
    verify_code = pyotp.TOTP(verify_key).now()
    print(f"验证码: {verify_code} (基于密钥: {verify_key})")

    if not username or not password:
        print(f"❌ 平台 {platfrom_name} 缺少配置")
        return False
    
    print(f"\n开始登录: {platfrom_name}")
    
    # 确保 cookies 文件夹存在
    if not os.path.exists(COOKIES_DIR):
        os.makedirs(COOKIES_DIR)

    options = Options()
    #options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as exc:
        print(f"❌ Chrome 启动失败: {exc}")
        return False

    try:
        print(f"浏览器已启动，正在打开: {login_url}")
        driver.get(login_url)
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)


        verify_xpath = '//*[@id="app"]/div/form/div/div[4]/div/div[2]/input'
        verify_input = driver.find_element(By.XPATH, verify_xpath)
        verify_input.send_keys(verify_code)

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login-btn.el-button--primary"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.5)
        try:
            button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", button)

        # if url_contains("dashboard") not in driver.current_url:
        
        
        if platfrom_name == "T1":
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, "bullshit__return-home").click()
            expected_fragment = "welcome"
        else:
            expected_fragment = "dashboard"

        WebDriverWait(driver, 15).until(
            EC.url_contains(expected_fragment)
        )
        
        print(f"✅ {platfrom_name} 登录成功")

        cookies = driver.get_cookies()
        print(f"获取到的cookies: {cookies}")
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        sakura_header_name = None
        sakura_value = None
        for request in getattr(driver, 'requests', []):
            for header_candidate in ("Sakura-Token", "sakura"):
                if header_candidate in request.headers:
                    sakura_header_name = header_candidate
                    sakura_value = request.headers.get(header_candidate)
                    print("找到 Sakura Header:", header_candidate)
                    print(request.headers)
                    print("sakura 值:", sakura_value)
                    break
            if sakura_value:
                break

        cookies_file = os.path.join(COOKIES_DIR, f"cookies_{platfrom_name}.json")
        save_data = {
            "cookies": cookies_dict,
            "sakura": sakura_value,
            "sakura_header_name": sakura_header_name,
        }
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

        time.sleep(3)
        return True

    except Exception as e:
        print(f"❌ {platfrom_name} 登录失败: {e}")
        return False

    finally:
        driver.quit()


def main(platfrom:str):
    if platfrom is None:
        print("❌ 请指定 platfrom 参数，例如 'A8'、'T1' 或 'M9'")
        return False

    success = login_and_save_profile(platfrom)
    if success:
        return True

    time.sleep(2)
    for attempt in range(3):
        success = login_and_save_profile(platfrom)
        if success:
            return True
        time.sleep(2)

    return False

if __name__ == "__main__":
    platfrom = None
    #main(platfrom)  # 可以替换为 "A8" 或 "T1" 来测试其他平台
    main('A8')
