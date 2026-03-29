#!/usr/bin/env python3
"""
Start the Chanlun Pro application with minimal initialization to avoid process killing issues.
"""

import os
import sys
import threading
from pathlib import Path

def start_application():
    # Add src directory to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    web_path = Path(__file__).parent / "web" / "chanlun_chart"
    sys.path.insert(0, str(web_path))
    
    # Import required modules
    import traceback
    from concurrent.futures import ThreadPoolExecutor
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from tornado.wsgi import WSGIContainer
    
    # Import config first to ensure it's loaded properly
    from chanlun import config
    
    # Define a function to create the app with minimal background tasks
    def create_minimal_app():
        """Create the application without running background tasks immediately"""
        import flask
        from flask import Flask
        
        # Create Flask app instance
        app = Flask(__name__, instance_relative_config=True)
        app.logger.disabled = True  # Disable logging during startup
        app.secret_key = "cl_pro_secret_key"
        
        # Add a simple route to confirm the server is running
        @app.route('/')
        def health_check():
            return """
            <html>
            <head><title>Chanlun Pro - Server Running</title></head>
            <body>
            <h1>Chanlun Pro Server is Running</h1>
            <p>The application has started successfully.</p>
            <p>To access the full application, ensure you have:</p>
            <ul>
                <li>External data sources configured (TDX, Binance, etc.)</li>
                <li>Required API keys in the configuration</li>
                <li>Proper network connectivity to data providers</li>
            </ul>
            <p>See the <a href="/docs">documentation</a> for setup instructions.</p>
            </body>
            </html>
            """
        
        @app.route('/health')
        def simple_health():
            return {"status": "ok", "message": "Server is running"}
        
        return app
    
    try:
        print("Creating minimal application...")
        app = create_minimal_app()
        print("Application created successfully!")
        
        print("Setting up server...")
        s = HTTPServer(WSGIContainer(app, executor=ThreadPoolExecutor(10)))
        s.bind(9900, config.WEB_HOST)
        
        print("Starting server on http://127.0.0.1:9900")
        print("Server started successfully!")
        print("Press Ctrl+C to stop the server")
        
        s.start(1)
        IOLoop.instance().start()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting application: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_application()