import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def start_api():
    """Start the Node.js API"""
    api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api')
    os.chdir(api_dir)
    subprocess.run(['npm', 'install'])
    subprocess.run(['npm', 'start'])

def start_flask():
    """Start the Flask application"""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    subprocess.run([sys.executable, 'app.py'])

def main():
    print("Iniciando o sistema NFe Livre...")
    
    # Start API in a separate thread
    api_thread = Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()
    
    # Wait for API to start
    print("Aguardando a API iniciar...")
    time.sleep(5)
    
    # Start Flask app
    print("Iniciando a interface web...")
    start_flask()

if __name__ == "__main__":
    main() 