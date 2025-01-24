import os
import time
import redis
import json
import importlib.util
from zipfile import ZipFile
from types import SimpleNamespace

# Função para carregar código de um ZIP
def load_function_from_zip(zip_path, entry_function):
    temp_dir = "/tmp/function_code"
    os.makedirs(temp_dir, exist_ok=True)

    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Localize o arquivo Python principal
    main_file = os.path.join(temp_dir, "__main__.py")
    spec = importlib.util.spec_from_file_location("module", main_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Obter a função de entrada
    return getattr(module, entry_function)

# Configurações
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_input_key = os.getenv("REDIS_INPUT_KEY", "default_input_key")
redis_output_key = os.getenv("REDIS_OUTPUT_KEY", "default_output_key")
monitoring_period = int(os.getenv("REDIS_MONITORING_PERIOD", 5))
zip_file_path = os.getenv("ZIP_FILE_PATH", "")
entry_function_name = os.getenv("ENTRY_FUNCTION", "handler")

# Inicializar Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Carregar a função
#function_handler = load_function_from_zip(zip_file_path, entry_function_name)

# Estado da execução
last_seen_data = None
context = SimpleNamespace(env={})

# Loop principal
while True:
    print("ok1")
    try:
        # Obter dados do Redis
        data = redis_client.get(redis_input_key)
        if data and data != last_seen_data:
            input_data = json.loads(data)
            last_seen_data = data

            print("ok2")

            # Chamar a função do usuário
            #result = function_handler(input_data, context)

            # Salvar resultado no Redis
            #redis_client.set(redis_output_key, json.dumps(result))
        
        time.sleep(monitoring_period)
    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(monitoring_period)
