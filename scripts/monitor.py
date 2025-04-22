import psutil
import subprocess
import logging
import time

# Setup logging configuration
logging.basicConfig(
    filename="/home/mohammadghzawi/devops-challenge/scripts/system_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Function to log system resource usage
def log_system_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    logging.info(f"CPU Usage: {cpu_usage}% | RAM Usage: {ram_usage}% | Disk Usage: {disk_usage}%")

# Function to log container status
def log_container_status():
    try:
        containers_output = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}"],
            universal_newlines=True
        )
        containers = containers_output.strip().splitlines()
        
        logging.info(f"Running Containers: {containers}")

        for container in containers:
            status = subprocess.check_output(
                f"docker inspect --format '{{{{.State.Status}}}}' {container}",
                shell=True
            ).decode().strip()
            
            if status != 'running':
                logging.error(f"Container {container} is down. Status: {status}")
                exit(1)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking container status: {e}")
        exit(1)

def main():
    log_system_resources()
    log_container_status()

if __name__ == "__main__":
    main()

