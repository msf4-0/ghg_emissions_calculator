#!/usr/bin/env python3
"""
AWS Application entry point for Elastic Beanstalk
"""
import subprocess
import sys
import os

def application(environ, start_response):
    """WSGI application entry point"""
    # This is a workaround for Streamlit on Elastic Beanstalk
    # Start Streamlit in the background
    if not os.path.exists('/tmp/streamlit.pid'):
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'main_app.py',
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true'
        ])
        with open('/tmp/streamlit.pid', 'w') as f:
            f.write(str(process.pid))
    
    # Simple WSGI response
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    
    return [b'''
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=http://localhost:8501">
    </head>
    <body>
        <p>Redirecting to GHG Emissions Calculator...</p>
        <p>If not redirected, <a href="http://localhost:8501">click here</a></p>
    </body>
    </html>
    ''']

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    httpd.serve_forever()
