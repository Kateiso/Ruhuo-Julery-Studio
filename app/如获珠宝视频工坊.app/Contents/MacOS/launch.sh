#!/bin/bash
# 如获珠宝·智能视频工坊 启动脚本

# 获取 .app 所在目录（项目根目录）
APP_DIR="$(cd "$(dirname "$0")/../../../" && pwd)"

# 切换到项目目录
cd "$APP_DIR"

# 检查虚拟环境
if [ -d "$APP_DIR/venv" ]; then
    source "$APP_DIR/venv/bin/activate"
else
    echo "错误：找不到虚拟环境，请先运行 setup.sh"
    osascript -e 'display dialog "找不到虚拟环境，请先运行 setup.sh 安装依赖" buttons {"确定"} default button 1'
    exit 1
fi

# 启动 Streamlit
streamlit run gui.py --server.headless true

# 保持终端打开
exec bash
