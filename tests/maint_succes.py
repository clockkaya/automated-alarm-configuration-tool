import time

from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')

# 假设cookies是从某个地方（比如插件导出的.txt文件）读取到的字符串，格式类似于[{name, value, domain, path}]
with open('../config/maint.sama.dev.ctnisi.cn_cookies.json', 'r') as file:
    cookies_json = file.read()

# 将JSON字符串转换为Python字典列表
cookies_list = json.loads(cookies_json)

# 初始化WebDriver
driver = webdriver.Chrome(options=options)

# 访问目标网站
driver.get("https://maint.sama.dev.ctnisi.cn:30443/#/resource/poolManage")

# 添加Cookies到当前会话
for cookie in cookies_list:
    # 移除可能不被Selenium接受的字段
    if 'expirationDate' in cookie:
        del cookie['expirationDate']
    if 'sameSite' in cookie:
        del cookie['sameSite']
    driver.add_cookie(cookie)

# 刷新页面或直接导航到需要的页面
driver.refresh()  # 或者使用driver.get("<specific_page_url>")导航到特定页面
time.sleep(10)