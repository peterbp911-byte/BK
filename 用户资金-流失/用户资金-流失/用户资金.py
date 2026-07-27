#爬取日用户资金
from concurrent import futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
from datetime import timedelta, datetime
from concurrent.futures import ThreadPoolExecutor,as_completed
from platfrom_config import get_platfrom_config, PLATFROM_CONFIGS


today = datetime.today().strftime("%Y%m%d")
yesterday = (datetime.today()-timedelta(days=1)).strftime("%m%d")
day_num = (datetime.today() - timedelta(days=3)).strftime("%m%d")

login_start_time =  (datetime.today() - timedelta(days= 7 )).strftime("%Y-%m-%d")
login_end_time =  (datetime.today() - timedelta(days= 1 )).strftime("%Y-%m-%d")

input_path = "C:/Users/wsmian/Downloads"
csv_dir = "D:/TT用户资金数据"
driver_path = ChromeDriverManager().install()  # 只下载一次

def create_driver():
    options = Options()
    options.add_argument("--start-maximized")  #最大化窗口
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless") #无界面模式
    return webdriver.Chrome(service=Service(driver_path), options=options)


#登录
def login(driver, url, username, password):
    """登录函数"""
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    # 等待用户名输入框出现并填充
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "email_address")))
    username_field.send_keys(username)

    # 填充密码
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    # 点击登录按钮
    login_button = driver.find_element(By.NAME, "button")
    login_button.click()

    # 等待登录成功（URL 跳转离开登录页）
    wait.until(EC.url_changes(url))

def ck(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    button = driver.find_element(By.XPATH, '//button[@onclick="user_fund_export_modal.showModal()"]')
    button.click()
    print("成功点击按钮")
    time.sleep(2)
    login_start_date = driver.find_element(By.XPATH, '//label[text()="登录开始日期"]/following-sibling::input')
    login_start_date.clear()  # 先清空
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",login_start_date, login_start_time)
    time.sleep(1)
    login_end_date = driver.find_element(By.XPATH, '//label[text()="登录结束日期"]/following-sibling::input')
    login_end_date.clear()
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",login_end_date, login_end_time)
    time.sleep(1)
    sub_botton = driver.find_element(By.XPATH, '//*[@id="submit_btn"]')
    sub_botton.click()
    time.sleep(2)

def download(driver, yesterday, url):
    driver.get(url)
    wait = WebDriverWait(driver, 40)
    date_xpath = f"//td[contains(@class, 'whitespace-nowrap') and contains(text(), '资金汇总导出_{today}')]"
    date_cell = wait.until(EC.presence_of_element_located((By.XPATH,date_xpath)))
    time.sleep(420)
    for _ in range(12):
        try:
            row = date_cell.find_element(By.XPATH,"./ancestor::tr")
            download_links = row.find_elements(By.XPATH, ".//a[contains(text(),'下载')]")
            if download_links:
                break
        except:
            pass
        driver.refresh()
        time.sleep(10)
        date_cell = wait.until(EC.presence_of_element_located((By.XPATH, date_xpath)))
    else:   
        raise Exception("未找到下载链接")
    for link in download_links:
        link.click()
        time.sleep(5)
    time.sleep(40)

def process_platform(platform_name, config):
    driver = create_driver()
    try:
        print(f"正在处理平台:{platform_name}")
        login(driver, config['LOGIN_PAGE_URL'], config['USERNAME'], config['PASSWORD'])
        ck(driver, config['FU_URL'])
        download(driver, today, config['TASKS_URL'])
        print(f'{platform_name}_资金汇总导出 已下载')
    except Exception as e:
        print(f"{platform_name} ，跳过。错误:{e}")
    finally:
        driver.quit()

def move():
    all_files = [f for f in os.listdir(input_path) if f.endswith('.csv') and 'user_fund_export' in f]
    for f in all_files:

        platfrom_name = f.split('_')[0]
        n_filename = f"{platfrom_name}_user_funds.csv"
        move_path = os.path.join(csv_dir, yesterday, platfrom_name)
        os.makedirs(move_path, exist_ok=True)

        shutil.move(os.path.join(input_path,f),os.path.join(move_path,n_filename))
    print('done')

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=len(PLATFROM_CONFIGS)) as executor:
            futures = {
                executor.submit(process_platform, name, config): name
                for name, config in PLATFROM_CONFIGS.items()
            }
            for future in as_completed(futures):
                future.result()
    move()

