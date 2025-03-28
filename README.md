 # NFe Livre - Sistema de Download de Notas Fiscais Eletrônicas

Um sistema gratuito e de código aberto para contadores e escritórios contábeis baixarem Notas Fiscais Eletrônicas (NF-e) utilizando os webservices da Receita Federal.

## 🌟 Por que usar o NFe Livre?

- **100% Gratuito**: Economize com licenças de sistemas caros
- **Seguro**: Código aberto e verificável, sem compartilhamento de dados sensíveis
- **Rápido**: Processe múltiplas NF-e simultaneamente
- **Flexível**: Organize notas por CNPJ, filtre e gerencie facilmente
- **Personalizável**: Adapte o código às necessidades do seu escritório

## 📋 Requisitos

- Python 3.8 ou superior
- Certificado Digital A1 válido (e-CNPJ ou e-CPF)
- Acesso à internet

## 🚀 Instalação

### Para usuários de Linux e macOS

```bash
# Clone o repositório
git clone https://github.com/braulliomarques/Frontendnfe


# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
flask run --host=0.0.0.0 --port=5000
```

### Para usuários de Windows

#### Instalando Python

1. Faça download em https://www.python.org/downloads/release/python-3120/
2. Antes de clicar em "Install Now", marque essa caixinha: ✅ Add Python to PATH
   Isso é super importante — é o que faz o comando python e pip funcionarem no terminal.
3. Após instalar, crie uma pasta para o projeto, abra-o como terminal, e execute:
   ```
   python.exe -m pip install --upgrade pip
   ```

#### Instalando Git

1. Baixe o Git em https://git-scm.com/download/win
2. Escolha uma das opções: 32-bit Git for Windows Setup ou 64-bit Git for Windows Setup.
3. Instale seguindo as opções padrão
4. Abra PowerShell como administrador e execute o comando:
   ```
   Set-ExecutionPolicy RemoteSigned
   ```

#### Configurando o projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/nfe-livre.git
cd nfe-livre

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
ou python3 app.py
```

Após iniciar, acesse a aplicação em seu navegador: http://localhost:5000

## 📱 Como usar

1. **Página Inicial**: Contém informações sobre o sistema e seus benefícios
 Acessível pela URL http://localhost:5000

3. **Adicionar chaves NFe**: Insira manualmente ou cole múltiplas chaves
4. **Agrupar por CNPJ**: O sistema organiza automaticamente as notas pelo CNPJ do emitente
5. **Baixar XMLs**: Processe individualmente ou baixe todos os XMLs de uma vez

## ⚠️ Atenção ao Certificado Digital

Para baixar XMLs de NFe de **diferentes clientes**, você precisa **fechar a página** e abri-la novamente para permitir a seleção do certificado digital correspondente. Certifique-se de que os certificados digitais de todos os seus clientes estejam instalados no computador.

## 🛠️ Configuração Avançada

### Ajustando a quantidade de processamentos simultâneos

Você pode configurar o número de chaves processadas simultaneamente (de 5 a 30) dependendo do seu computador e conexão.

