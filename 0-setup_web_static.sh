#!/usr/bin/env bash
# Install Nginx if not already installed

if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary folders if not exists
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create fake HTML file
sudo sh -c 'echo "Hello World!" > /data/web_static/releases/test/index.html'

# Create or recreate symbolic link
sudo rm -r /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/
sudo chgrp -R ubuntu /data/

# Update Nginx configuration
nginx_conf="/etc/nginx/sites-available/default"
nginx_alias="\n\tlocation /hbnb_static/ { \n\t\talias /data/web_static/current/;\n\t }"
sudo sed -i "/^\tserver_name _;/i\\$nginx_alias" $nginx_conf
# Restart Nginx
sudo service nginx restart
