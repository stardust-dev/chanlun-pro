import pathlib
import sys

# 将项目中的 src 目录，添加到 sys.path 中
src_path = pathlib.Path(__file__).parent.parent / ".." / "src"
sys.path.append(str(src_path))
web_server_path = pathlib.Path(__file__).parent
sys.path.append(str(web_server_path))

import traceback
import webbrowser
from concurrent.futures import ThreadPoolExecutor

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

import chanlun.encodefix  # Fix Windows print 乱码问题  # noqa: F401
from chanlun import config

try:
    # Import the create_app function without triggering background tasks
    # We'll need to patch the problematic parts
    
    # Temporarily modify the cl_app module to prevent immediate execution of tasks
    import cl_app
    original_create_app = cl_app.create_app
    
    def patched_create_app(test_config=None):
        # Temporarily override problematic initialization
        # Store original classes
        original_alert_run = getattr(cl_app.AlertTasks, 'run', None)
        
        # Patch the run method to do nothing during app creation
        if original_alert_run:
            def dummy_run(self):
                print("Background tasks disabled for minimal startup")
                return True
            cl_app.AlertTasks.run = dummy_run
        
        # Create the app
        app = original_create_app(test_config)
        
        # Restore original method if it existed
        if original_alert_run:
            cl_app.AlertTasks.run = original_alert_run
            
        return app
    
    # Replace the function
    cl_app.create_app = patched_create_app
    
    app = create_app = patched_create_app

except Exception as e:
    print(e)
    traceback.print_exc()

    input("出现异常，按回车键退出")

if __name__ == "__main__":
    try:
        app_instance = app()
        
        s = HTTPServer(WSGIContainer(app_instance, executor=ThreadPoolExecutor(10)))
        s.bind(9900, config.WEB_HOST)

        print("启动成功")
        s.start(1)

        print("Server running on http://127.0.0.1:9900")
        print("Press Ctrl+C to stop the server")
        
        # Don't auto-open browser in minimal mode
        # webbrowser.open("http://127.0.0.1:9900")
        
        IOLoop.instance().start()

    except Exception as e:
        print(e)
        traceback.print_exc()

        input("出现异常，按回车键退出")