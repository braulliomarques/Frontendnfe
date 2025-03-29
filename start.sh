#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Obtém o IP da máquina local
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo -e "${GREEN}=== Sistema de Download de NFE ===${NC}"
echo -e "${BLUE}Iniciando os serviços...${NC}"

# Define as variáveis de ambiente
export API_HOST=$IP_ADDRESS
export API_PORT=3002

echo -e "${YELLOW}Configuração de rede:${NC}"
echo "API URL: http://$API_HOST:$API_PORT"
echo "Frontend URL: http://$IP_ADDRESS:5000"

# Inicia a aplicação Flask
echo -e "${BLUE}Iniciando servidor web...${NC}"
python app.py 