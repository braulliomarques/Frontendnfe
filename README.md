# NFe Livre - Sistema de Download de Notas Fiscais Eletrônicas

Um sistema gratuito e de código aberto para contadores e escritórios contábeis baixarem Notas Fiscais Eletrônicas (NF-e) utilizando os webservices da Receita Federal.

---

## 🌟 Por que usar o NFe Livre?

- **100% Gratuito**: Economize com licenças de sistemas caros
- **Seguro**: Código aberto e verificável, sem compartilhamento de dados sensíveis
- **Rápido**: Processe múltiplas NF-e simultaneamente
- **Flexível**: Organize notas por CNPJ, filtre e gerencie facilmente
- **Personalizável**: Adapte o código às necessidades do seu escritório

---

## 📋 Requisitos

- Python 3.8 ou superior
- Certificado Digital A1 válido (e-CNPJ ou e-CPF)
- Acesso à internet
- Git
- Node.js (versão LTS)

---

## 🚀 Instalação

### Alternativa 1: Clonar o repositório via Git

```bash
git clone https://github.com/braulliomarques/nfe-livre.git
cd nfe-livre
```

### Alternativa 2: Baixar o ZIP do Projeto

[Download .zip do repositório](https://github.com/braulliomarques/nfe-livre/archive/refs/heads/main.zip)

Depois de baixar, extraia o conteúdo e abra a pasta extraída no terminal para continuar com a instalação.

---

### Para usuários de Linux e macOS

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

Acesse no navegador: http://localhost:5000

---

### Para usuários de Windows

#### 1. Instalando Python

1. Baixe em: https://www.python.org/downloads/release/python-3120/  
2. Antes de clicar em "Install Now", marque: ✅ **Add Python to PATH**
3. Após instalar, abra o terminal e execute:

```bash
python.exe -m pip install --upgrade pip
```

#### 2. Instalando Git

1. Baixe em: https://git-scm.com/download/win  
2. Escolha 32-bit ou 64-bit conforme seu sistema  
3. Siga a instalação padrão

Abra o PowerShell como **administrador** e execute:

```powershell
Set-ExecutionPolicy RemoteSigned
```

#### 3. Instalando Node.js

1. Baixe em: https://nodejs.org/  
2. Escolha a versão LTS (Long Term Support)  
3. Instale normalmente

Verifique a instalação com:

```bash
node --version
npm --version
```

#### 4. Configurando o Projeto

```bash
# Clone o repositório (caso ainda não tenha feito)
git clone https://github.com/braulliomarques/nfe-livre.git
cd nfe-livre

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

Acesse no navegador: http://localhost:5000
