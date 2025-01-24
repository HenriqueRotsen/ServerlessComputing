from mymodule import handler
import os

def main(): 
    # Redis connection
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    input_key = os.getenv("REDIS_INPUT_KEY", "metrics")
    output_key = os.getenv("REDIS_OUTPUT_KEY", "results")
    monitor_period = int(os.getenv("REDIS_MONITOR_PERIOD", 5))
    entry_function_name = os.getenv("ENTRY_FUNCTION", "handler")

if __name__ == "__main__":
    main()