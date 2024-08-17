
# Vanna Enterprise: 内网数据库与大模型联动框架

![Vanna Logo](./vanna.png)

Vanna Enterprise 是一个基于 Vanna 框架的扩展项目，旨在解决企业内网环境下共用数据库与大模型联动的问题。通过 Vanna Enterprise，企业用户可以轻松地在内部网络中进行数据库连接、预训练、文档训练、SQL 训练和推理，并提供一个用户友好的 Web 界面进行交互。
./welcome.png
目前仅支持zhipuAI的调用实例，后续将会逐步同步原vanna框架主流LLM的集成

## 特性

- **多数据库支持**：支持 MySQL、SQLite 和 Snowflake 数据库。
- **内网部署**：专为企业内网环境设计，确保数据安全。
- **预训练**：自动获取数据库元数据并进行预训练。
- **文档训练**：从文档文件中读取内容并进行训练。
- **SQL 训练**：从 SQL 列表中进行训练。
- **SQL 问题训练**：从 Excel 文件中读取问题和对应的 SQL 语句进行训练。
- **推理**：根据问题生成 SQL 查询。
- **Web 界面**：提供一个用户友好的 Web 界面，方便用户进行交互和监控。

## 安装

### 环境要求

- Python 3.7+
- MySQL/SQLite/Snowflake 数据库
- Vanna 框架

### 依赖安装

1. 克隆项目仓库：
   ```bash
   git clone https://github.com/jiangchengchengark/vanna-Enterprise.git
   cd vanna-enterprise
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   在项目根目录下找到 `.env` 文件，并添加以下内容：
   ```
   API_KEY=your_api_key_here
   LOCAL_ADRESS=your_local_adress_here
   ```

## 使用

### 启动 Web 服务器

1. 启动应用：
   ```bash
   python app.py
   ```

2. 打开浏览器，访问 `http://your_local_adress:port`，其中 `port` 是应用启动时分配的端口，默认5000。

3. 注意，如果重启python进程，需要删除生成的pre-train.log日志文件再运行

### 前端界面操作

1. **欢迎页面**：访问应用的欢迎页面，选择数据库类型。
2. **数据库连接**：填写数据库连接信息，包括主机、数据库名称、用户名和密码等。
3. **生成实例**：点击生成实例按钮，系统将自动连接数据库并启动预训练。
4. **查看实例**：在实例查看页面，可以进行推理、查看预训练日志等操作。

./config1.png

### 预训练

预训练将在生成实例时自动进行，用户可以在实例查看页面查看预训练日志。

./pre_train.png

### 文档训练

在实例查看页面，上传文档文件（支持 `.docx` 格式），系统将自动进行文档训练。

### SQL 训练

在实例查看页面，输入 SQL 语句列表，系统将自动进行 SQL 训练。

### SQL 问题训练

在实例查看页面，上传 Excel 文件（包含问题和对应的 SQL 语句），系统将自动进行 SQL 问题训练。

### 推理

在实例查看页面，输入问题，系统将生成对应的 SQL 查询并返回结果。
./get_answer.png

## 服务器部署

为了确保服务器稳定运行，建议在生产环境中使用专业的 Web 服务器，如 Gunicorn 或 uWSGI，并配合 Nginx 进行反向代理。

### 使用 Gunicorn

1. 安装 Gunicorn：
   ```bash
   pip install gunicorn
   ```

2. 使用 Gunicorn 启动应用：
   ```bash
   gunicorn --bind 0.0.0.0:8000 app:app
   ```

### 使用 uWSGI

1. 安装 uWSGI：
   ```bash
   pip install uwsgi
   ```

2. 使用 uWSGI 启动应用：
   ```bash
   uwsgi --http :8000 --wsgi-file app.py --callable app
   ```

### 配置 Nginx

1. 安装 Nginx：
   ```bash
   sudo apt-get install nginx
   ```

2. 配置 Nginx 反向代理：
   在 `/etc/nginx/sites-available/` 目录下创建一个配置文件，例如 `vanna-enterprise`，并添加以下内容：
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_ip;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. 启用配置并重启 Nginx：
   ```bash
   sudo ln -s /etc/nginx/sites-available/vanna-enterprise /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 贡献

我们欢迎任何形式的贡献，包括但不限于：

- 提交问题和建议
- 改进文档
- 提交代码改进

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多信息。

## 许可证

本项目基于 MIT 许可证开源，详情请参见 [LICENSE](LICENSE) 文件。

## 联系

如有关于本项目的任何问题或建议，请通过 [email](mailto:3306065226@qq.com) 或 [GitHub Issues](https://github.com/jiangchengchengark/Vanna-Enterprise/issues) 联系我们。

---

感谢您使用 Vanna Enterprise！我们希望这个项目能帮助您在内网环境下更高效地进行数据库与大模型的联动。
