import os
import sys
# 将当前目录添加到系统路径，确保能找到 page_objects
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from page_objects.maint.alarm_config_page import AlarmConfigPage
from config.logging_config import main as init_logging

def run_automation():
    """
    自动化任务入口
    """
    print("=== 开始执行存量资源告警配置自动化任务 ===")
    
    # 1. 初始化日志配置
    try:
        init_logging()
    except Exception as e:
        print(f"日志初始化失败，继续执行: {e}")

    # 2. 初始化页面对象 (会自动启动浏览器并登录)
    try:
        alarm_page = AlarmConfigPage()
        
        # 3. 执行业务逻辑
        # add_vm_alarm_tmp_with_fill_in_form 方法包含了核心的自动化流程
        # confirm=False 表示演示模式，不点击最终的保存按钮，防止弄脏数据
        alarm_page.add_vm_alarm_tmp_with_fill_in_form(confirm=False)
        
        print("=== 任务执行完成 ===")
        
        # 保持浏览器开启一小段时间以便观察
        import time
        time.sleep(5)
        
    except Exception as e:
        print(f"自动化任务执行过程中发生错误: {e}")

if __name__ == '__main__':
    run_automation()