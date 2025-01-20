from typing import Any, Dict
from datetime import datetime, timedelta


def handler(input: Dict[str, Any], context: Any) -> Dict[str, Any]:
    # Extracting metrics from the input
    timestamp = input.get("timestamp")
    net_bytes_sent = input.get("net_io_counters_eth0-bytes_sent", 0)
    net_bytes_recv = input.get("net_io_counters_eth0-bytes_recv", 0)
    memory_cached = input.get("virtual_memory-cached", 0)
    memory_buffers = input.get("virtual_memory-buffers", 0)
    memory_total = input.get("virtual_memory-total", 1)  # Avoid division by zero

    # Parse the current timestamp
    current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    # Calculate percentage of network egress
    percent_network_egress = (
        (net_bytes_sent / (net_bytes_sent + net_bytes_recv)) * 100
        if (net_bytes_sent + net_bytes_recv) > 0
        else 0
    )

    # Calculate percentage of memory caching content
    percent_memory_caching = ((memory_cached + memory_buffers) / memory_total) * 100

    # Initialize environment storage if not present
    if not hasattr(context, "env") or not context.env:
        context.env = {}

    # Calculate moving average CPU utilization
    moving_avg_cpu = {}
    for key, value in input.items():
        if key.startswith("cpu_percent-"):
            cpu_id = key.split("-")[1]

            # Retrieve the historical data for the CPU
            history_key = f"history_cpu{cpu_id}_60sec"
            history = context.env.get(history_key, [])

            # Append the new data point with the current timestamp
            history.append((current_time, value))

            # Filter the history to keep only the last 60 seconds
            one_minute_ago = current_time - timedelta(seconds=60)
            history = [entry for entry in history if entry[0] >= one_minute_ago]

            # Store the updated history in the context
            context.env[history_key] = history

            # Calculate the moving average
            if history:
                avg_value = sum(value for _, value in history) / len(history)
            else:
                avg_value = 0.0

            moving_avg_cpu[f"avg_util_cpu{cpu_id}_60sec"] = avg_value
    
    

    # Prepare the output
    output = {
        "timestamp": timestamp,
        "percent_network_egress": percent_network_egress,
        "percent_memory_caching": percent_memory_caching,
        **moving_avg_cpu,
    }

    # print("INPUT\n-----------------------------------")
    # print(input)
    # print("==========================================")
    # print("OUTPUT\n-----------------------------------")
    # print(output)
    # print("Context\n-----------------------------------")
    # print(context.env)

    return output
