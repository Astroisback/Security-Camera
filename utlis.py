import psutil

def get_system_info():
    # Get system information using psutil
    cpu_percent = psutil.cpu_percent(interval=1)
    mem_info = psutil.virtual_memory()
    total_memory = round(mem_info.total / (1024**3), 2)  # Convert to GB
    used_memory = round(mem_info.used / (1024**3), 2)    # Convert to GB

    return {
        "cpu_percent": cpu_percent,
        "total_memory": total_memory,
        "used_memory": used_memory
    }
system_info = get_system_info()
