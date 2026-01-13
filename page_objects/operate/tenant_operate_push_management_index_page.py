from page_objects.sama_web import SamaWeb


class PushManage(SamaWeb):
    def __init__(self):
        super().__init__(portal="operate")
        self.request("/tenant-operate/push-Management/index")

    def tmp_page_test(self):
        response_body = self.find_and_process_request(target_api="/notice/receiver/page")
        print(f"响应体内容: {response_body}")


if __name__ == "__main__":
    alarmConfigPage = PushManage()
    alarmConfigPage.tmp_page_test()
