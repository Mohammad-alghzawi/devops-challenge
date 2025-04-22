#!/bin/bash

echo "🔐 Starting server hardening..."

# Step 1: Disable root SSH login
echo "🚫 Disabling root SSH login..."
sudo sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Step 2: Change SSH port
NEW_PORT=2000
echo "📡 Changing SSH port to $NEW_PORT..."
sudo sed -i "s/^#Port 22/Port $NEW_PORT/" /etc/ssh/sshd_config
sudo sed -i "s/^Port 22/Port $NEW_PORT/" /etc/ssh/sshd_config

# Allow new port through UFW firewall
echo "🔓 Allowing port $NEW_PORT through UFW..."
sudo ufw allow ${NEW_PORT}/tcp

# Step 3: Install and configure Fail2Ban
echo "🛡️ Installing Fail2Ban..."
sudo apt update
sudo apt install fail2ban -y

echo "⚙️ Configuring Fail2Ban for SSH..."
sudo bash -c "cat > /etc/fail2ban/jail.local" <<EOF
[sshd]
enabled = true
port = $NEW_PORT
logpath = %(sshd_log)s
backend = systemd
maxretry = 3
findtime = 10m
bantime = 1h
EOF

sudo systemctl restart fail2ban

# Restart SSH to apply changes
echo "🔁 Restarting SSH..."
sudo systemctl restart sshd

echo "✅ Hardening script completed!"

