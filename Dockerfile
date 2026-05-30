# 1. Usa uma imagem oficial do Python super leve baseada em Linux
FROM python:3.12-slim

# 2. Define variáveis de ambiente para o Python não travar logs na tela
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define a pasta dentro do container onde o projeto vai morar
WORKDIR /app

# 4. Instala dependências do sistema necessárias para compilar o PostgreSQL (libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia o requirements.txt e instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copia todo o restante do código do projeto para dentro do container
COPY . /app/

# 7. Expõe a porta que o Django usa
EXPOSE 8000