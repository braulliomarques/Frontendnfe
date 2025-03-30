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
PROCESSING_CACHE_FILE = 'processing_cache.json'

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

def load_processing_cache():
    """Carrega o cache de chaves em processamento."""
    try:
        if os.path.exists(PROCESSING_CACHE_FILE):
            with open(PROCESSING_CACHE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar cache de processamento: {str(e)}")
    return {}

def save_processing_cache(cache_data):
    """Salva o cache de chaves em processamento."""
    try:
        with open(PROCESSING_CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=4)
    except Exception as e:
        logging.error(f"Erro ao salvar cache de processamento: {str(e)}")

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
    """Página principal - landing page."""
    return render_template('landing.html')

@app.route('/consulta')
def consulta():
    """Página de consulta com lista de NFEs."""
    keys = read_nfe_keys('nfe_keys.txt')
    cache = load_cache()
    processing_cache = load_processing_cache()
    return render_template('index.html', keys=keys, cache=cache, processing=processing_cache)

@app.route('/landing')
def landing():
    """Rota alternativa para landing - redireciona para a página principal."""
    return render_template('landing.html')

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

@app.route('/save-key', methods=['POST'])
def save_key():
    """Endpoint para salvar chave NFe no arquivo."""
    try:
        data = request.json
        key = data.get('key')
        
        if not key:
            return jsonify({'success': False, 'message': 'Chave NFe não fornecida'}), 400
        
        # Valida a chave (deve ter 44 dígitos numéricos)
        if not (key.isdigit() and len(key) == 44):
            return jsonify({'success': False, 'message': 'Formato de chave inválido. Deve ter 44 dígitos numéricos'}), 400
        
        # Lê as chaves existentes
        existing_keys = read_nfe_keys('nfe_keys.txt')
        
        # Verifica se a chave já existe
        if key in existing_keys:
            return jsonify({'success': True, 'message': 'Chave já existe', 'already_exists': True})
        
        # Adiciona a chave ao arquivo
        with open('nfe_keys.txt', 'a') as file:
            file.write(f"\n{key}")
        
        return jsonify({'success': True, 'message': 'Chave adicionada com sucesso'})
    
    except Exception as e:
        logging.error(f"Erro ao salvar chave: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro ao salvar chave: {str(e)}'}), 500

@app.route('/save-multiple-keys', methods=['POST'])
def save_multiple_keys():
    """Endpoint para salvar múltiplas chaves NFe no arquivo."""
    try:
        data = request.json
        keys = data.get('keys', [])
        
        if not keys:
            return jsonify({'success': False, 'message': 'Nenhuma chave NFe fornecida'}), 400
        
        # Lê as chaves existentes
        existing_keys = read_nfe_keys('nfe_keys.txt')
        
        added_keys = []
        invalid_keys = []
        existing_count = 0
        
        for key in keys:
            key = key.strip()
            
            # Pula chaves vazias
            if not key:
                continue
            
            # Valida a chave (deve ter 44 dígitos numéricos)
            if not (key.isdigit() and len(key) == 44):
                invalid_keys.append(key)
                continue
            
            # Verifica se a chave já existe
            if key in existing_keys:
                existing_count += 1
                continue
            
            # Adiciona à lista de chaves a serem salvas
            added_keys.append(key)
            existing_keys.append(key)
        
        # Se há chaves válidas para adicionar
        if added_keys:
            with open('nfe_keys.txt', 'a') as file:
                for key in added_keys:
                    file.write(f"\n{key}")
        
        # Prepara a resposta
        result = {
            'success': True,
            'message': f'{len(added_keys)} chaves adicionadas com sucesso.',
            'added_count': len(added_keys),
            'invalid_count': len(invalid_keys),
            'existing_count': existing_count,
            'invalid_keys': invalid_keys[:10]  # Limita para não sobrecarregar a resposta
        }
        
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"Erro ao salvar múltiplas chaves: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro ao salvar chaves: {str(e)}'}), 500

@app.route('/delete-key', methods=['POST'])
def delete_key():
    """Endpoint para remover uma chave NFe do arquivo."""
    try:
        data = request.json
        key = data.get('key')
        
        if not key:
            return jsonify({'success': False, 'message': 'Chave NFe não fornecida'}), 400
        
        # Lê as chaves existentes
        existing_keys = read_nfe_keys('nfe_keys.txt')
        
        # Verifica se a chave existe
        if key not in existing_keys:
            return jsonify({'success': False, 'message': 'Chave NFe não encontrada'}), 404
        
        # Remove a chave da lista
        existing_keys.remove(key)
        
        # Reescreve o arquivo sem a chave removida
        with open('nfe_keys.txt', 'w') as file:
            file.write('\n'.join(existing_keys))
        
        # Limpa o cache para a chave removida
        cache = load_cache()
        if key in cache:
            del cache[key]
            save_cache(cache)
        
        return jsonify({'success': True, 'message': 'Chave NFe removida com sucesso'})
    
    except Exception as e:
        logging.error(f"Erro ao remover chave: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro ao remover chave: {str(e)}'}), 500

@app.route('/delete-all-keys', methods=['POST'])
def delete_all_keys():
    """Endpoint para remover todas as chaves NFe do arquivo."""
    try:
        # Lê as chaves existentes para contagem
        existing_keys = read_nfe_keys('nfe_keys.txt')
        num_keys = len(existing_keys)
        
        # Cria um arquivo vazio para limpar todas as chaves
        with open('nfe_keys.txt', 'w') as file:
            file.write('')
        
        # Limpa todo o cache
        clear_cache()
        
        return jsonify({
            'success': True, 
            'message': f'Todas as chaves foram removidas com sucesso ({num_keys} chaves)',
            'count': num_keys
        })
    
    except Exception as e:
        logging.error(f"Erro ao remover todas as chaves: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro ao remover todas as chaves: {str(e)}'}), 500

@app.route('/set-processing-status', methods=['POST'])
def set_processing_status():
    """Endpoint para definir o status de processamento de uma chave."""
    try:
        data = request.json
        key = data.get('key')
        status = data.get('status')  # 'processing', 'retry', 'done', 'error'
        message = data.get('message', '')
        
        if not key or not status:
            return jsonify({'success': False, 'message': 'Chave ou status não fornecidos'}), 400
        
        # Carrega o cache existente
        processing_cache = load_processing_cache()
        
        # Status 'done' remove do cache de processamento
        # Status 'error' ou 'retry' mantém no cache, apenas atualiza o status
        if status == 'done':
            if key in processing_cache:
                del processing_cache[key]
        else:
            # Status 'processing', 'retry' ou 'error' adiciona/atualiza o cache
            processing_cache[key] = {
                'status': status,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
        
        # Salva o cache atualizado
        save_processing_cache(processing_cache)
        
        return jsonify({
            'success': True,
            'message': 'Status de processamento atualizado'
        })
        
    except Exception as e:
        logging.error(f"Erro ao atualizar status de processamento: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500

@app.route('/get-processing-status', methods=['GET'])
def get_processing_status():
    """Endpoint para obter o status de processamento de todas as chaves."""
    try:
        processing_cache = load_processing_cache()
        return jsonify({
            'success': True,
            'processing': processing_cache
        })
    except Exception as e:
        logging.error(f"Erro ao obter status de processamento: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500

@app.route('/get-url-cache', methods=['GET'])
def get_url_cache():
    """Endpoint para obter o cache de URLs."""
    try:
        cache = load_cache()
        return jsonify({
            'success': True,
            'cache': cache
        })
    except Exception as e:
        logging.error(f"Erro ao obter cache de URLs: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500

@app.route('/clear-processing-cache', methods=['POST'])
def clear_processing_cache_endpoint():
    """Endpoint para limpar o cache de processamento."""
    try:
        # Limpar o cache de processamento
        processing_cache = {}
        save_processing_cache(processing_cache)
        
        return jsonify({
            'success': True,
            'message': 'Cache de processamento limpo com sucesso'
        })
    except Exception as e:
        logging.error(f"Erro ao limpar cache de processamento: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erro ao limpar cache de processamento: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000) 