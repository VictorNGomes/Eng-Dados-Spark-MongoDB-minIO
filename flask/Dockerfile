FROM python:3.9-slim

# Instalação das dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Criação do diretório de trabalho
WORKDIR /app

# Cópia dos arquivos de aplicação
COPY requirements.txt .
COPY app.py .
COPY templates templates/

# Instalação das dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Definição das variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar a aplicação
CMD ["flask", "run"]