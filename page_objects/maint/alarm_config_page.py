import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.sama_web import SamaWeb
from config.logging_config import main


class AlarmConfigPage(SamaWeb):
    def __init__(self):
        super().__init__(portal="maint")
        self.request("/alarm/config")

    def query_child_api(self):
        data = self.find_and_process_request(target_api="/alarm/tmp/page")
        print(f"响应体内容: {data}")

        # 遍历每一项并提取'templateName'
        unique_text_list = [row['templateName'] for row in data['rows']]
        print(unique_text_list)

    def click_detail(self, index=1):
        css_selector = f".el-table__fixed-right .el-table__row:nth-child({index}) .el-button:nth-child(1) > span"
        self.interact_with_element(By.CSS_SELECTOR, css_selector, "click", description="详情")
        time.sleep(2)
        self.interact_with_element(By.CSS_SELECTOR, ".el-dialog__wrapper:nth-child(5) .el-dialog__close", "click", description="关闭详情")

    def add_vm_alarm_tmp_with_fill_in_form(self, confirm=False):
        # 新增告警配置
        self.interact_with_element(By.CSS_SELECTOR, ".filter-item > span", "click", description="新增告警配置")

        # 基础配置
        current_time = datetime.now()
        formatted_time = current_time.strftime('%m%d%H%M%S')
        self.interact_with_element(By.CSS_SELECTOR, ".el-form-item__content:nth-child(2) > .el-input > .el-input__inner", "send_keys",
                                   input="selenium-"+formatted_time, description="告警名称")
        self.interact_with_element(By.CSS_SELECTOR, ".el-form > .el-row .el-select .el-input__inner", "click", description="选择告警类型")
        self.ul_li_select("/html/body/div[3]/div[1]/div[1]/ul/li", "虚拟机")
        self.interact_with_element(By.CSS_SELECTOR, ".el-form-item__content .el-switch__core", "click", description="取消启动")

        # 资源配置
        # pool_tree = self.find_and_process_request(target_api="/account/area/poolTree")
        # print(f"响应体内容: {pool_tree}")
        # target_area = self._find_organizations(pool_tree, '西藏')
        # target_pool = self._find_organizations(pool_tree, '拉萨天翼云')
        # print(target_area, target_pool)
        self.interact_with_element(By.CSS_SELECTOR, ".el-row > .el-form-item:nth-child(1) .el-select .el-input__inner", "click",
                                   description="所属区域")
        self.ul_li_select("/html/body/div[4]/div[1]/div[1]/ul/li", "西藏")
        self.interact_with_element(By.CSS_SELECTOR, "div > .el-row > .el-form-item:nth-child(2) .el-select__caret", "click", description="所属资源池")
        self.ul_li_select("/html/body/div[5]/div[1]/div[1]/ul/li", "拉萨天翼云")
        self.interact_with_element(By.CSS_SELECTOR, ".select-input-con span", "click", description="选择资源")
        self.interact_with_element(By.XPATH, "/html/body/div[6]/div/div[2]/div/div[1]/div[2]/form/div/div/div/div[2]/input", "click", description="部署主机")
        # self.interact_with_element(By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul/label/span[1]/span", "click", description="全选")
        self.ul_li_select("/html/body/div[7]/div[1]/div[1]/ul/li", "37")
        self.interact_with_element(By.XPATH, "/html/body/div[6]/div/div[2]/div/div[1]/div[2]/form/button", "click", description="查询")
        self.tr_td_select_with_paging("/html/body/div[6]/div/div[2]/div/div[1]/div[3]/div[3]/table/tbody/tr",
                                    ".btn-next:nth-child(4)",
                                    "kafka",
                                    "/td[1]/div/label/span/span")
        self.interact_with_element(By.CSS_SELECTOR, ".middle-card > div:nth-child(1) > .el-button", "click", description="选中")
        # 重选
        # self.interact_with_element(By.XPATH, "/html/body/div[6]/div/div[2]/div/div[1]/div[2]/form/div/div/div/div[2]/span/span/i", "click",
        #                            description="重选部署主机")
        # self.ul_li_select("/html/body/div[7]/div[1]/div[1]/ul/li", "37")
        # self.ul_li_select("/html/body/div[7]/div[1]/div[1]/ul/li", "38")
        # self.interact_with_element(By.XPATH, "/html/body/div[6]/div/div[2]/div/div[1]/div[2]/form/button", "click", description="查询")
        self.interact_with_element(By.XPATH, "/html/body/div[6]/div/div[3]/div/button[2]", "click", description="确定")
        self.scroll()

        # 条件配置
        self.interact_with_element(By.XPATH, "//div[@id='app']/div/div/section/div[2]/div[2]/div[4]/div/div[2]/div/form/div[6]/div[3]/button/span", "click", description="选择告警模板")
        time.sleep(1)
        self.interact_with_element(By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__header > button", "click", description="关闭告警模板窗口")
        self.interact_with_element(By.XPATH, "(//input[@type='text'])[12]", "click", description="告警条件")
        self.ul_li_select("/html/body/div[6]/div[1]/div[1]/ul/li", "CPU")
        self.interact_with_element(By.XPATH, "(//input[@type='text'])[13]", "send_keys", input="30", description="持续")
        self.interact_with_element(By.CSS_SELECTOR, ".time .el-input__inner", "click", description="时间单位")
        self.ul_li_select("/html/body/div[7]/div[1]/div[1]/ul/li", "m")
        self.interact_with_element(By.XPATH, "(//input[@type='text'])[16]", "send_keys", input="80", description="阈值")
        self.interact_with_element(By.XPATH, "(//input[@type='text'])[17]", "click", description="告警条件")
        self.ul_li_select("/html/body/div[8]/div[1]/div[1]/ul/li", "高")

        # 通知配置

        # 保存配置
        if confirm:
            self.interact_with_element(By.XPATH, "//div[@id='app']/div/div/section/div[2]/div[2]/div[4]/div/div[2]/div/div/button/span", "click", description="保存配置")
            # TODO:确认成功
        else:
            time.sleep(2)
            self.interact_with_element(By.XPATH, "//*[@id='app']/div/div/section/div[2]/div[2]/div[4]/div/div[1]/button", "click", description="取消保存")

    def ul_li_select(self, li_xpath, target_keyword):
        wait = WebDriverWait(self.driver, 10)
        li_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, li_xpath)))
        for index, li in enumerate(li_elements):
            if target_keyword in li.text:
                self.interact_with_element(By.XPATH, f"{li_xpath}[{index + 1}]", "click", description=f"{li.text}")

    def tr_td_select(self, tr_xpath, target_text, td_location):
        wait = WebDriverWait(self.driver, 10)
        tr_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, tr_xpath)))
        for index, td in enumerate(tr_elements):
            if target_text in td.text:
                self.interact_with_element(By.XPATH, f"{tr_xpath}[{index + 1}]{td_location}", "click", description=f"{td.text}".replace("\n", " "))

    def tr_td_select_with_paging(self, tr_xpath, next_page_selector, target_text, td_location):
        wait = WebDriverWait(self.driver, 10)
        while True:
            tr_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, tr_xpath)))
            for index, td in enumerate(tr_elements):
                if target_text in td.text:
                    self.interact_with_element(By.XPATH, f"{tr_xpath}[{index + 1}]{td_location}", "click", description=f"{td.text}".replace("\n", " "))
                    return
            try:
                self.interact_with_element(By.CSS_SELECTOR, next_page_selector, "click", description="下一页")
            except Exception:
                print("已到达最后一页，未找到目标文本")
                break

    def _find_organizations(self, data, keyword):
        results = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'orgName' and keyword in value:
                    results.append(value)
                elif isinstance(value, (dict, list)):
                    results.extend(self._find_organizations(value, keyword))
        elif isinstance(data, list):
            for item in data:
                results.extend(self._find_organizations(item, keyword))
        return results


if __name__ == "__main__":
    main()
    alarmConfigPage = AlarmConfigPage()
    # alarmConfigPage.query_child_api()
    # alarmConfigPage.click_detail(2)
    alarmConfigPage.add_vm_alarm_tmp_with_fill_in_form()
    time.sleep(10)
