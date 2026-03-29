import pathlib
import sys

# 将项目中的 src 目录，添加到 sys.path 中
src_path = pathlib.Path(__file__).parent / "src"
sys.path.append(str(src_path))
web_server_path = pathlib.Path(__file__).parent / "web" / "chanlun_chart"
sys.path.append(str(web_server_path))

import traceback
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

import chanlun.encodefix  # Fix Windows print 乱码问题  # noqa: F401
from chanlun import config

try:
    # Temporarily patch the problematic parts before importing cl_app
    with patch('cl_app.AlertTasks.__init__', return_value=None):
        with patch('cl_app.XuanguTasks.__init__', return_value=None):
            with patch('cl_app.OtherTasks.__init__', return_value=None):
                # Now import and create the app
                from cl_app import create_app
                print("cl_app imported successfully")
                
                # We need to create instances manually since __init__ is patched
                app = create_app()
                print("App created successfully")

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

    input("出现异常，按回车键退出")

if __name__ == "__main__":
    try:
        app = create_app()
        
        s = HTTPServer(WSGIContainer(app, executor=ThreadPoolExecutor(10)))
        s.bind(9900, config.WEB_HOST)

        print("启动成功")
        print("Server running on http://127.0.0.1:9900")
        print("Press Ctrl+C to stop the server")
        s.start(1)

        # Don't auto-open browser in minimal mode
        # webbrowser.open("http://127.0.0.1:9900")
        
        IOLoop.instance().start()

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

        input("出现异常，按回车键退出")