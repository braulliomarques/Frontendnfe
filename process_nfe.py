import requests
import time
import logging
import os
import json
from datetime import datetime
from typing import List, Dict, Tuple
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile
import io

# Configure logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configurar logging principal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_directory, f'process_nfe_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
        logging.StreamHandler()
    ]
)

class DownloadError(Exception):
    """Classe personalizada para erros de download."""
    pass

def save_failed_keys(failed_keys: List[Dict]):
    """Salva as chaves que falharam em um arquivo JSON com detalhes do erro."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(log_directory, f'failed_keys_{timestamp}.json')
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(failed_keys, f, ensure_ascii=False, indent=4)
    
    logging.info(f"Chaves com falha foram salvas em: {filename}")

def ensure_download_directory():
    """Cria diretório de downloads se não existir."""
    download_dir = "downloads"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def validate_downloaded_file(filepath: str) -> bool:
    """Valida se o arquivo baixado está íntegro."""
    try:
        if not os.path.exists(filepath):
            return False
        
        # Verifica se o arquivo tem tamanho maior que 0
        if os.path.getsize(filepath) == 0:
            os.remove(filepath)  # Remove arquivo vazio
            return False
        
        return True
    except Exception as e:
        logging.error(f"Erro ao validar arquivo {filepath}: {str(e)}")
        return False

def download_file(url: str, key: str, download_dir: str, max_retries: int = 3) -> Tuple[bool, str]:
    """Faz download do arquivo e retorna tupla (sucesso, mensagem)."""
    retry_count = 0
    error_message = ""
    
    while retry_count < max_retries:
        try:
            session = requests.Session()
            
            # Configura headers para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Primeira requisição para obter o arquivo
            response = session.get(url, stream=True, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Determina a extensão do arquivo
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' in content_type:
                extension = '.pdf'
            elif 'xml' in content_type:
                extension = '.xml'
            else:
                extension = '.txt'
            
            # Cria nome do arquivo
            filename = os.path.join(download_dir, f"NFE_{key}{extension}")
            
            # Download do arquivo em chunks
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Valida o arquivo baixado
            if validate_downloaded_file(filename):
                logging.info(f"Download concluído com sucesso: {filename}")
                return True, "Download realizado com sucesso"
            else:
                error_message = "Arquivo baixado está corrompido ou vazio"
                raise DownloadError(error_message)
            
        except requests.Timeout:
            error_message = "Timeout durante o download"
            logging.warning(f"Tentativa {retry_count + 1}/{max_retries}: {error_message}")
        
        except requests.RequestException as e:
            error_message = f"Erro na requisição HTTP: {str(e)}"
            logging.warning(f"Tentativa {retry_count + 1}/{max_retries}: {error_message}")
        
        except DownloadError as e:
            error_message = str(e)
            logging.warning(f"Tentativa {retry_count + 1}/{max_retries}: {error_message}")
        
        except Exception as e:
            error_message = f"Erro inesperado: {str(e)}"
            logging.warning(f"Tentativa {retry_count + 1}/{max_retries}: {error_message}")
        
        retry_count += 1
        if retry_count < max_retries:
            time.sleep(5)  # Espera 5 segundos entre tentativas
    
    return False, error_message

def read_nfe_keys(filename: str) -> List[str]:
    """Lê as chaves de NFE do arquivo."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_single_key(key: str, download_dir: str, max_retries: int = 5, retry_delay: int = 3) -> Tuple[bool, Dict]:
    """Processa uma única chave NFE e retorna tupla (sucesso, detalhes)."""
    # Usa o hostname atual para permitir acesso de qualquer IP local
    api_host = os.environ.get('API_HOST', '127.0.0.1')
    api_port = os.environ.get('API_PORT', '3002')
    url = f"http://{api_host}:{api_port}/api/nfe/interceptar-url/{key}"
    
    attempts = 0
    details = {
        "chave": key,
        "tentativas_api": 0,
        "tentativas_download": 0,
        "erro": None,
        "timestamp": datetime.now().isoformat()
    }

    while attempts < max_retries:
        try:
            response = requests.get(url)
            data = response.json()
            details["tentativas_api"] += 1

            if data.get('success'):
                download_url = data.get('url')
                logging.info(f"URL obtida para chave {key}: {download_url}")
                
                # Tenta fazer o download
                success, message = download_file(download_url, key, download_dir)
                details["tentativas_download"] += 1
                
                if success:
                    return True, details
                else:
                    details["erro"] = f"Falha no download: {message}"
            else:
                details["erro"] = f"API retornou falha: {data.get('message', 'Sem mensagem')}"
            
            logging.warning(f"Tentativa {attempts + 1}/{max_retries} falhou para chave {key}")
            
            attempts += 1
            if attempts < max_retries:
                time.sleep(retry_delay)
        
        except requests.RequestException as e:
            details["erro"] = f"Erro na requisição: {str(e)}"
            logging.error(f"Erro de requisição para chave {key}: {str(e)}")
            attempts += 1
            if attempts < max_retries:
                time.sleep(retry_delay)
        
        except Exception as e:
            details["erro"] = f"Erro inesperado: {str(e)}"
            logging.error(f"Erro inesperado para chave {key}: {str(e)}")
            attempts += 1
            if attempts < max_retries:
                time.sleep(retry_delay)
    
    logging.error(f"Falha ao processar chave {key} após {max_retries} tentativas")
    return False, details

def main():
    input_file = "nfe_keys.txt"
    failed_keys = []
    
    try:
        download_dir = ensure_download_directory()
        keys = read_nfe_keys(input_file)
        logging.info(f"Encontradas {len(keys)} chaves para processar")

        successful_keys = 0
        failed_keys_count = 0

        for key in keys:
            success, details = process_single_key(key, download_dir)
            if success:
                successful_keys += 1
            else:
                failed_keys_count += 1
                failed_keys.append(details)

        # Salva informações sobre falhas
        if failed_keys:
            save_failed_keys(failed_keys)

        # Log dos resultados finais
        logging.info("Processamento concluído!")
        logging.info(f"Downloads com sucesso: {successful_keys}")
        logging.info(f"Downloads com falha: {failed_keys_count}")

    except Exception as e:
        logging.error(f"Erro no processo principal: {str(e)}")

if __name__ == "__main__":
    main() 