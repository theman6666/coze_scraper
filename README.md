# 🕷️ Coze QA 抓取脚本

一个基于 **Selenium** 的自动化脚本，用于从 **Coze 知识库页面** 自动登录并批量抓取问答数据，最终导出为 CSV 和 Excel 文件。

---

## 🚀 功能简介

该脚本可实现以下功能：

- 自动启动 Chrome 浏览器并登录 Coze 官网  
- 模拟人工登录（通过账号密码）  
- 自动分页滚动抓取知识库中所有「问题 - 答案」数据  
- 自动去重，防止重复抓取  
- 支持自动导出为 **CSV** 和 **Excel (.xlsx)** 文件  

---

## 🧰 环境依赖

请先确保你的环境中安装了以下组件：

| 依赖项        | 版本建议           | 说明                                                    |
| :------------ | :----------------- | :------------------------------------------------------ |
| Python        | ≥ 3.8              | 开发语言                                                |
| Chrome 浏览器 | 138.0.7204.50      | 必须与 chromedriver 匹配                                |
| chromedriver  | 与 Chrome 版本对应 | [下载地址](https://chromedriver.chromium.org/downloads) |
| Selenium      | ≥ 4.0              | 浏览器自动化                                            |
| pandas        | ≥ 1.3              | 数据导出                                                |
| python-dotenv | ≥ 0.21             | 加载 `.env` 环境变量                                    |

安装命令：

```bash
pip install selenium pandas python-dotenv
```

```
coze_scraper/
│
├── coze_scraper.py          # 主程序（即你的 Python 脚本）
├── .env                     # 存储账号密码（不会上传到 GitHub）
├── result/
│   ├── coze_qa.csv
│   └── coze_qa.xlsx
└── README.md
```

------

## 🔐 环境变量配置

在项目根目录创建 `.env` 文件，并填写你的 Coze 登录信息：

```env
USERNAME=your_username_here
PASSWORD=your_password_here
```

> ⚠️ 注意：
>
> - `.env` 文件中不要有多余的空格。
> - 请在 `.gitignore` 中添加 `.env`，防止上传到 GitHub 泄露隐私。

------

## ⚙️ 使用方法

1. **配置 ChromeDriver 路径**

   - 修改脚本中对应的路径：

     ```python
     service = Service(r'D:\\tools\\chromedriver.exe')
     ```

2. **运行脚本**

   ```bash
   python coze_scraper.py
   ```

3. **等待抓取完成**

   - 程序会自动登录、滚动并抓取所有问答数据。
   - 控制台会实时显示新增条数。

4. **查看结果**

   - 抓取结果会自动保存到 `result/` 目录下：

     ```
     coze_qa.csv
     coze_qa.xlsx
     ```

------

## 🧩 技术要点

- 使用 **Selenium WebDriverWait** + **Expected Conditions** 处理页面动态加载
- 通过 `scrollTop` 控制分页滚动
- 利用 Python 集合去重，防止重复抓取
- 多次无新增数据后自动停止（默认连续 5 次）
- 输出为两种格式（CSV、Excel）

------

## ⚠️ 注意事项

- Coze 页面结构若有变动，需调整 XPath 选择器。
- 若登录存在验证码，请先手动登录一次保持会话。
- 建议使用国内 IP 登录，避免触发安全验证。
- 抓取数据仅限于个人学习与测试用途，请勿用于商业目的。

------

## ⭐ 示例输出

```
新增数据: 如何创建知识库?... (当前总数: 1)
新增数据: 如何导入问答?... (当前总数: 2)
本屏无新数据，连续 3/5 屏无新数据。
抓取结束。共抓取 128 条数据
已保存为 coze_qa.csv 和 coze_qa.xlsx
```

