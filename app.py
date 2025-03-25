from flask import Flask, render_template, jsonify, send_file, request
import requests
import logging
import os
import json
from datetime import datetime
import tempfile

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cache de URLs
CACHE_FILE = 'url_cache.json'

def load_cache():
    """Carrega o cache de URLs do arquivo."""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar cache: {str(e)}")
    return {}

def save_cache(cache_data):
    """Salva o cache de URLs no arquivo."""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=4)
    except Exception as e:
        logging.error(f"Erro ao salvar cache: {str(e)}")

def clear_cache():
    """Limpa o cache de URLs."""
    try:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        return True
    except Exception as e:
        logging.error(f"Erro ao limpar cache: {str(e)}")
        return False

def read_nfe_keys(filename: str):
    """Lê as chaves de NFE do arquivo."""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def get_nfe_url(key: str):
    """Obtém a URL de download da NFE."""
    try:
        # Verifica primeiro no cache
        cache = load_cache()
        if key in cache:
            return {
                'success': True,
                'url': cache[key]['url'],
                'message': 'URL obtida do cache',
                'from_cache': True
            }

        # Se não estiver no cache, faz a requisição
        url = f"http://127.0.0.1:3002/api/nfe/interceptar-url/{key}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('success'):
            # Salva no cache
            cache[key] = {
                'url': data['url'],
                'timestamp': datetime.now().isoformat()
            }
            save_cache(cache)
            
            return {
                'success': True,
                'url': data['url'],
                'message': 'URL obtida com sucesso',
                'from_cache': False
            }
        return {
            'success': False,
            'message': data.get('message', 'Erro ao obter URL')
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }

@app.route('/')
def index():
    """Página principal com lista de NFEs."""
    keys = read_nfe_keys('nfe_keys.txt')
    cache = load_cache()
    return render_template('index.html', keys=keys, cache=cache)

@app.route('/get-url/<key>')
def get_url(key):
    """Endpoint para obter URL de download."""
    result = get_nfe_url(key)
    return jsonify(result)

@app.route('/download/<key>')
def download_nfe(key):
    """Endpoint para download direto do XML."""
    try:
        # Primeiro, obtém a URL
        result = get_nfe_url(key)
        if not result['success']:
            return jsonify({'error': result['message']}), 400

        # Configura headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Faz o download do arquivo
        response = requests.get(result['url'], headers=headers, stream=True)
        response.raise_for_status()

        # Cria um arquivo temporário para o download
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    tmp.write(chunk)
            tmp_path = tmp.name

        # Envia o arquivo para download
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=f'NFE_{key}.xml',
            mimetype='application/xml'
        )

    except Exception as e:
        logging.error(f"Erro ao fazer download da NFE {key}: {str(e)}")
        return jsonify({'error': 'Erro ao fazer download do arquivo'}), 500

@app.route('/clear-cache', methods=['POST'])
def clear_cache_endpoint():
    """Endpoint para limpar o cache."""
    try:
        if clear_cache():
            return jsonify({
                'success': True,
                'message': 'Cache limpo com sucesso'
            })
        return jsonify({
            'success': False,
            'message': 'Erro ao limpar cache'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao limpar cache: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 