from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 设置ChromeDriver路径
chrome_driver_path = r"D:\anaconda3\Scripts\chromedriver.exe"

# 初始化Service对象
service = Service(executable_path=chrome_driver_path)

# 创建ChromeOptions对象，如果有特殊配置可以在这里设置
options = Options()

# 初始化webdriver实例
driver = webdriver.Chrome(service=service, options=options)

try:
    # 打开指定的网址
    driver.get("https://www.example.com")
    
    # 使用新的find_element方法，通过By.ID定位元素
    search_box = driver.find_element(By.ID, "search_box")
    
    # 输入文本
    search_box.send_keys("Selenium Tutorial")
    
    # 模拟按下回车键进行搜索
    search_box.send_keys(Keys.RETURN)
    
    # 等待页面加载完成，这里使用隐式等待
    driver.implicitly_wait(5)
    
    # 打印当前页面的标题
    print("Page Title:", driver.title)
    
finally:
    # 完成后关闭浏览器窗口
    driver.quit()
