# 一键打开论文阅读器

直接展示已有的 `reader/preview/` 静态快照，需要 Python 3.8+，无需构建或安装依赖。

- Linux / macOS：在项目根目录执行 `./start.sh`。
- Windows：双击项目根目录的 `start.bat`。已有系统 Python 即可，不需要安装本项目的 Linux Conda 环境。

启动后打印本机地址并自动打开浏览器。保持终端打开，按 `Ctrl+C` 停止服务。默认端口 8000，已被占用时自动选择空闲端口；只监听 `127.0.0.1`。

可从任意工作目录调用；路径包含空格时请加引号。

可用 `./start.sh --no-browser --port 8080` 或 `start.bat --no-browser --port 8080` 禁用自动打开浏览器并指定端口。`--port 0` 自动分配端口；显式指定已占用的端口会报错退出。优先使用项目内 Python，随后尝试系统 Python；Windows 失败时窗口会暂停显示错误。
