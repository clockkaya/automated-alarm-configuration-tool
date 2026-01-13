# 导入selenium的webdriver模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 设置ChromeDriver的路径，确保与你的环境匹配
chrome_driver_path = r"D:\anaconda3\Scripts\chromedriver.exe"

# 初始化webdriver实例，这里以Chrome为例
driver = webdriver.Chrome()

try:
    # 打开指定的网址
    driver.get("https://www.example.com")
    
    # 查找页面上的一个元素，比如搜索框，这里假设它有一个id为"search_box"
    search_box = driver.find_element_by_id("search_box")
    
    # 在找到的元素中输入文本
    search_box.send_keys("Selenium Tutorial")
    
    # 模拟按下回车键进行搜索
    search_box.send_keys(Keys.RETURN)
    
    # 等待页面加载完成，这里简单等待5秒作为示例
    driver.implicitly_wait(5)
    
    # 打印当前页面的标题
    print("Page Title:", driver.title)
    
    # 可以添加更多操作，比如截图、点击链接等
    
except Exception as e:
    # 打印异常信息
    print("An error occurred:", e)

finally:
    # 完成后关闭浏览器窗口
    driver.quit()
