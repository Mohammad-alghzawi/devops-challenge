#!/bin/bash

# Log file path
LOG_FILE="monitor.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] Monitoring system..." >> $LOG_FILE

# --- System Resource Usage ---
echo "--- System Resource Usage ---" >> $LOG_FILE
echo "CPU usage:" >> $LOG_FILE
top -bn1 | grep "Cpu(s)" >> $LOG_FILE

echo "RAM usage:" >> $LOG_FILE
free -h >> $LOG_FILE

echo "Disk usage:" >> $LOG_FILE
df -h >> $LOG_FILE

# --- Docker Container Status ---
echo "--- Docker Container Status ---" >> $LOG_FILE
docker ps >> $LOG_FILE

# Replace this with your actual container name
CONTAINER_NAME="devops-challenge-web-1"  # Update this with your container name
RUNNING=$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME 2>/dev/null)

if [ "$RUNNING" != "true" ]; then
  echo "[$TIMESTAMP] ERROR: Container $CONTAINER_NAME is not running." >> $LOG_FILE
  echo "[✖] Container down. Exiting..."  # This will show on the console
  exit 1
else
  echo "[$TIMESTAMP] Container $CONTAINER_NAME is running." >> $LOG_FILE
  echo "[✔] Container running."  # This will show on the console
fi

echo "[✔] Monitoring complete." >> $LOG_FILE
