# Usar uma imagem base Python com pacotes comuns pré-instalados
FROM python:3.10-slim

# Instalar dependências
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o código da runtime
COPY runtime.py /app/runtime.py

# Diretório temporário para código do usuário
RUN mkdir -p /tmp/function_code

# Definir diretório de trabalho
WORKDIR /app

# Comando padrão
CMD ["python", "runtime.py"]