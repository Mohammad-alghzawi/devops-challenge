import psutil
import subprocess
import logging
import time

# Setup logging configuration
logging.basicConfig(filename="/home/mohammadghzawi/devops-challenge/scripts/system_monitor.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# Function to log system resource usage
def log_system_resources():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # RAM usage
    ram = psutil.virtual_memory()
    ram_usage = ram.percent

    # Disk usage
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    # Log the system resource usage
    logging.info(f"CPU Usage: {cpu_usage}% | RAM Usage: {ram_usage}% | Disk Usage: {disk_usage}%")

# Function to log container status
def log_container_status():
    try:
        # Run docker ps to check the status of containers
        containers = subprocess.check_output(["docker", "ps", "--format", "'{{.Names}}'"], universal_newlines=True)
        containers = containers.strip().splitlines()

        # Log the container status
        logging.info(f"Running Containers: {containers}")
        
        # Check if any container is down
        for container in containers:
            status = subprocess.check_output(f"docker inspect --format '{{{{.State.Status}}}}' {container}", shell=True)
            status = status.strip()
            if status != 'running':
                logging.error(f"Container {container} is down. Status: {status}")
                exit(1)  # Exit with error if a container is down

    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking container status: {e}")
        exit(1)  # Exit with error in case of a failure

def main():
    log_system_resources()
    log_container_status()

# Run the script
if __name__ == "__main__":
    main()
