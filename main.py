from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC        # 判断某一个元素是否可以点击或者是否可见
from dotenv import dotenv_values
# 首先，要启动浏览器并登录 Coze（建议手动登录一次，保持会话）
service = Service(r'D:\\tools\\chromedriver.exe')     # 指定使用谷歌游览器驱动，记得版本要一致
driver = webdriver.Chrome(service=service)
driver.get('')   # 改成自己的游览器地址
# 加载.env文件中的环境变量
config = dotenv_values(".env")      # 从.env文件中读取环境变量
USERNAME = config['USERNAME']     # 账号
PASSWORD = config['PASSWORD']     # 密码
# 输出获得的账号密码，让用户查看
print(USERNAME)
print(PASSWORD)
wait = WebDriverWait(driver, 20)

# 1. 点击“账号登录”Tab
account_tab = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//span[contains(text(), "账号登录")]/parent::div')
))
account_tab.click()

# 2. 输入账号
identity_input = wait.until(EC.presence_of_element_located((By.ID, "Identity_input")))
identity_input.clear()
identity_input.send_keys(USERNAME)

# 3. 输入密码
password_input = wait.until(EC.presence_of_element_located((By.ID, "Password_input")))
password_input.clear()
password_input.send_keys(PASSWORD)

# 4. 点击登录按钮
login_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//button[span[text()="登录"]]')
))
login_btn.click()

# 5. 等待页面跳转或登录成功（可根据实际情况调整等待条件）
time.sleep(3)
print("开始分页式抓取数据...")
data_set = set()
max_stale_scrolls = 5  # 连续5次无新数据就停止
no_new_data_scrolls = 0

while no_new_data_scrolls < max_stale_scrolls:
    last_total = len(data_set)

    # 1. 抓取当前可见的所有行
    rows_xpath = '//div[contains(@class, "semi-table-body")]//div[@role="row" and contains(@class, "semi-table-row")]'
    try:
        visible_rows = driver.find_elements(By.XPATH, rows_xpath)
        for row_elem in visible_rows:
            try:
                # 问题
                q_elem = row_elem.find_element(
                    By.XPATH,
                    './div[@role="gridcell" and @aria-colindex="3"]//div[contains(@class, "cell-text-preview--") and contains(@class, "text-content")]'
                )
                # 答案
                a_elem = row_elem.find_element(
                    By.XPATH,
                    './div[@role="gridcell" and @aria-colindex="4"]//div[contains(@class, "cell-text-preview--") and contains(@class, "text-content")]'
                )
                q = q_elem.text.strip()
                a = a_elem.text.strip()
                if q and a and (q, a) not in data_set:
                    data_set.add((q, a))
                    print(f"新增数据: {q[:30]}... (当前总数: {len(data_set)})")
            except Exception:
                continue
    except Exception as e:
        print(f"无法找到行元素，可能页面结构已改变或加载中: {e}")

    # 2. 判断是否有新数据
    if len(data_set) == last_total:
        no_new_data_scrolls += 1
        print(f"本屏无新数据，连续 {no_new_data_scrolls}/{max_stale_scrolls} 屏无新数据。")
    else:
        no_new_data_scrolls = 0

    # 3. 滚动一屏
    driver.execute_script('''
        var tableBody = document.querySelector('.semi-table-body');
        if(tableBody){
            tableBody.scrollTop += tableBody.clientHeight;
        }
    ''')
    time.sleep(2)

print(f"抓取结束。共抓取 {len(data_set)} 条数据")
driver.quit()

# 4. 保存为Excel或CSV
data = list(data_set)
df = pd.DataFrame(data, columns=['question', 'answer'])
df.to_csv('./result/coze_qa.csv', index=False, encoding='utf-8-sig')
df.to_excel('./result/coze_qa.xlsx', index=False)
print("已保存为 coze_qa.csv 和 coze_qa.xlsx")