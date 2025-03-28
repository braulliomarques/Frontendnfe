import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread
import shutil

def check_nodejs():
    """Check if Node.js is installed"""
    if shutil.which('node') is None:
        print("\nERRO: Node.js não está instalado!")
        print("\nPara instalar o Node.js:")
        print("1. Acesse https://nodejs.org/")
        print("2. Baixe a versão LTS (Long Term Support)")
        print("3. Execute o instalador e siga as instruções")
        print("4. Reinicie o computador após a instalação")
        print("\nApós instalar o Node.js, execute novamente o script.")
        sys.exit(1)

def start_api():
    """Start the Node.js API"""
    try:
        api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api')
        if not os.path.exists(api_dir):
            print("\nERRO: Pasta 'api' não encontrada!")
            print("Certifique-se de que você baixou o projeto completo.")
            print("Você pode baixar o projeto completo em:")
            print("https://github.com/braulliomarques/nfe-consulta-api/archive/refs/heads/main.zip")
            print("\nApós baixar, extraia a pasta 'api' para o diretório do projeto.")
            sys.exit(1)
            
        os.chdir(api_dir)
        print("Instalando dependências da API...")
        subprocess.run(['npm', 'install'], check=True)
        print("Iniciando a API...")
        subprocess.run(['npm', 'start'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nERRO ao iniciar a API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        sys.exit(1)

def start_flask():
    """Start the Flask application"""
    try:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(app_dir)
        print("Iniciando a interface web...")
        subprocess.run([sys.executable, 'app.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nERRO ao iniciar a interface web: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        sys.exit(1)

def main():
    print("Iniciando o sistema NFe Livre...")
    
    # Check if Node.js is installed
    check_nodejs()
    
    # Start API in a separate thread
    api_thread = Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()
    
    # Wait for API to start
    print("Aguardando a API iniciar...")
    time.sleep(5)
    
    # Start Flask app
    start_flask()

if __name__ == "__main__":
    main() 