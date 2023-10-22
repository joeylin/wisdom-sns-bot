#!/bin/bash

# 获取脚本的目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 命令参数：start, stop, restart
cmd=$1

start_server() {
    echo "启动 server.py ..."
    nohup python "$DIR"/main.py >> "$DIR"/server.log 2>&1 &
    echo $! > "$DIR"/server.pid
}

stop_server() {
    echo "停止 server.py ..."
    if [ -f "$DIR"/server.pid ]; then
        # shellcheck disable=SC2046
        kill -9 $(cat "$DIR"/server.pid)
        rm "$DIR"/server.pid
    else
        echo "没有找到 server.pid 文件，无法停止进程。"
    fi
}

case $cmd in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        echo "重新启动 server.py ..."
        stop_server
        sleep 2
        start_server
        ;;
    *)
        echo "未知命令 $cmd"
        echo "可用命令参数：start, stop, restart"
        ;;
esac