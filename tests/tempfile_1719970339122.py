from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 不直接指定executable_path，假设ChromeDriver已加入系统PATH或通过其他方式配置好
driver = webdriver.Chrome()

try:
    # 打开百度首页
    driver.get("https://www.baidu.com")
    
    # 显式等待搜索框出现，最多等待10秒
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kw"))
    )
    
    # 在搜索框中输入关键词
    search_box.send_keys("Selenium教程")
    
    # 模拟按下回车键进行搜索
    search_box.send_keys(Keys.RETURN)
    
    # 简单等待页面加载，这里使用隐式等待5秒
    driver.implicitly_wait(5)
    
    # 打印当前页面的标题，验证是否跳转到了搜索结果页
    print("Page Title:", driver.title)
    
finally:
    # 关闭浏览器窗口
    driver.quit()
