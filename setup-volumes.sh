#!/bin/bash

# Criar o volume se não existir
docker volume create frontapi_app_data

# Criar um container temporário para copiar os arquivos
docker run --rm -v frontapi_app_data:/app -v $(pwd):/source alpine cp -r /source/* /app/

# Criar os outros volumes necessários
docker volume create frontapi_letsencrypt_data
docker volume create frontapi_traefik_data
docker volume create frontapi_nfe_keys_data
docker volume create frontapi_url_cache_data

# Criar arquivo acme.json com as permissões corretas
docker run --rm -v frontapi_letsencrypt_data:/letsencrypt alpine touch /letsencrypt/acme.json
docker run --rm -v frontapi_letsencrypt_data:/letsencrypt alpine chmod 600 /letsencrypt/acme.json

echo "Volumes configurados com sucesso!" 