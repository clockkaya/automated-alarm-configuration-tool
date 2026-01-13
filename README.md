# Automated Alarm Configuration Tool
(基于 Selenium 的XX平台存量资源告警配置自动化工具)

## 📖 项目简介 (Introduction)

本项目是一个针对云网安全能力管理平台（XX平台）的自动化运维辅助工具。

**背景**：在平台迭代过程中，运营团队面临一个痛点：需要为大量存量（Legacy）虚拟机和主机资源补充告警配置。由于资源数量庞大且筛选条件复杂（涉及安全能力类型、厂商、规格等），手动在 Web 前端配置耗时且易错，而重新开发 Java 后端接口的成本过高（预估后端开发+测试需 21 人天）。

**解决方案**：采用 Python + Selenium 构建自动化脚本，模拟用户行为，通过前端 UI 批量下发告警策略。
**成果**：
- **非侵入式**：无需修改现有后端代码，零风险集成。
- **高效**：将人工重复操作转化为自动执行，大幅减少人力成本。
- **可复用**：基于 Page Object 模式封装，脚本易于维护和扩展。

## 🛠 技术栈 (Tech Stack)

* **Language**: Python 3.9+
* **Automation Framework**: Selenium WebDriver (v4.22)
* **Network Capture**: Selenium-Wire (用于 API 响应分析)
* **Design Pattern**: Page Object Model (POM)
* **Browser**: Google Chrome

## 📂 项目结构 (Structure)

```text
selenium/
├── config/             # 配置文件及环境设置
├── drivers/            # 浏览器驱动 (ChromeDriver)
├── logs/               # 运行日志
├── page_objects/       # POM 页面对象层
│   ├── maint/          # 运维门户相关页面
│   ├── operate/        # 运营门户相关页面
│   └── sama_web.py     # Base Page (封装 Driver 初始化、Cookie 注入、基础交互)
├── tests/              # 测试脚本
├── utils/              # 工具类
├── main.py             # 程序入口
└── requirements.txt    # 依赖列表
```

## 🚀 快速开始 (Getting Started)

### 1. 环境准备

确保已安装 Python 3.x 和 Google Chrome 浏览器。

Bash

```
# 克隆项目
git clone [repository-url]
cd selenium

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置说明

- **Driver**: 请确保 `drivers/` 目录下的 `chromedriver.exe` 版本与你的 Chrome 浏览器版本匹配。
- **Cookie**: 由于平台涉及 MFA 认证，本项目采用 Cookie 注入方式绕过登录。
  - 请在 `config/` 目录下创建一个名为 `maint.sama.dev.ctnisi.cn_cookies.json` 的文件（已在 `.gitignore` 中忽略）。
  - 格式参考：JSON 数组 `[{"name": "...", "value": "..."}]`。

### 3. 运行

Bash

```
python main.py
```

脚本将自动启动浏览器，导航至告警配置页面，筛选指定的存量资源，并自动填充预设的告警模板。

## 💡 核心实现亮点

1. Page Object 设计：

   将页面元素定位（Locator）与业务操作（Method）分离。例如 add_vm_alarm_tmp_with_fill_in_form 方法清晰地描述了业务流程，而底层的点击、输入逻辑被封装在 SamaWeb 基类中。

2. API 辅助定位：

   利用 selenium-wire 捕获后端接口（如 /alarm/tmp/page）的响应数据，辅助前端无法直接获取的信息校验，提高了脚本的判断准确性。

3. 稳健的交互封装：

   在 interact_with_element 中封装了显式等待（WebDriverWait），解决了页面渲染延迟导致的 ElementNotFound 异常，增强了脚本的稳定性。