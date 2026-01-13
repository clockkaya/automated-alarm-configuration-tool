import json
import time
import yaml
import logging
import os
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

class SamaWeb:
    def __init__(self, portal="operate"):
        self.logger = logging.getLogger(__name__)
        # 获取当前文件所在的目录 (page_objects)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._load_config(portal)
        self._initialize_driver(portal)

    def _load_config(self, portal):
        """加载配置文件"""
        config_path = os.path.join(self.base_dir, 'config', 'config.yml')
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            self.env = config["env"]
            # 拼接 cookie 文件路径
            self.cookie_file_path = os.path.join(self.base_dir, 'config', f"{portal}.sama.{self.env}.ctnisi.cn_cookies.json")
        except FileNotFoundError:
            self.logger.error(f"配置文件未找到: {config_path}")
            raise

    def _initialize_driver(self, portal):
        """初始化WebDriver并加载cookies"""
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        # 如果是演示项目，可以考虑开启 headless 模式，或者保留界面以便面试展示
        # options.add_argument('--headless') 
        
        seleniumwire_options = {'disable_encoding': True}

        self.driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)
        self.base_url = f"https://{portal}.sama.{self.env}.ctnisi.cn:30443/#"
        redirect_address = "/resource/poolManage"
        
        try:
            self.driver.get(self.base_url + redirect_address)
            self.driver.maximize_window()
            self.load_and_add_cookies()
        except Exception as e:
            self.logger.error(f"初始化 Driver 失败: {e}")
            self.driver.quit()

    def load_and_add_cookies(self):
        """从指定路径加载cookies并添加到浏览器会话中"""
        if not os.path.exists(self.cookie_file_path):
            self.logger.warning(f"Cookie 文件未找到: {self.cookie_file_path}，将跳过 Cookie 加载。")
            return

        try:
            with open(self.cookie_file_path, 'r', encoding='utf-8') as file:
                cookies_list = json.load(file)

            for cookie in cookies_list:
                cookie.pop('expirationDate', None)
                cookie.pop('sameSite', None)
                self.driver.add_cookie(cookie)
            
            # 加载完 Cookie 后刷新页面以生效
            self.driver.refresh()
            time.sleep(2)
        except Exception as e:
            self.logger.error(f"加载 Cookies 失败: {e}")

    def request(self, parent_page, sleep_seconds=2):
        """发送请求至指定URL"""
        self.driver.get(self.base_url + parent_page)
        time.sleep(sleep_seconds)

    def find_and_process_request(self, target_api):
        """遍历网络请求，寻找匹配特定URL模式的请求并处理响应体"""
        # 注意：selenium-wire 会捕获所有请求，长时间运行可能占用内存，生产环境需注意
        for request in self.driver.requests:
            if target_api in request.url and request.response:
                # print(f"找到匹配的请求: {request.url}") # 调试时可开启
                try:
                    # 处理可能的编码问题
                    body = request.response.body
                    # 尝试解码，如果失败可能需要根据 Content-Encoding 处理
                    try:
                        response_body = body.decode('utf-8')
                    except UnicodeDecodeError:
                        # 如果是压缩数据，可能需要解压，这里简单处理
                        return None
                        
                    return json.loads(response_body)
                except (json.JSONDecodeError) as e:
                    self.logger.error(f"解析响应 JSON 失败: {e}")

        self.logger.info("未找到匹配的请求或请求无响应体")
        return None

    def _wait_and_find_element(self, by, locator, timeout):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            return element
        except TimeoutException:
            self.logger.error(f"等待元素出现超时: {locator}")
            return None
        except Exception as e:
            self.logger.error(f"查找元素发生未知错误: {e}")
            return None

    def interact_with_element(self, by, locator, action, input=None, description='', timeout=10):
        element = self._wait_and_find_element(by, locator, timeout)
        if not element:
            return None

        actions = {
            'click': lambda: (element.click(), self.logger.info(f"点击按钮：【{description}】")),
            'send_keys': lambda: (element.clear(), element.send_keys(input), self.logger.info(f"键入文本：【{description}：{input}】")),
            'select': lambda: (Select(element).select_by_visible_text(description), None),
        }

        action_func = actions.get(action)
        if action_func:
            try:
                action_func()
                return description
            except Exception as e:
                self.logger.error(f"执行操作 '{action}' 失败: {e}")
        else:
            self.logger.warning(f"对于【{description}】，不支持操作'{action}'！")
        return None

    def scroll(self):
        try:
            action_chains = ActionChains(self.driver)
            action_chains.scroll_by_amount(0, 1000).perform()
        except Exception as e:
             self.logger.error(f"滚动屏幕失败: {e}")