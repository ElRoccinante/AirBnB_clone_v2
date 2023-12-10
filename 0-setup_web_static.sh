#!/usr/bin/env bash
# install the configuration and setup the env for deply the code
if !command nginx -v &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

sudo sh -c "echo 'Hello world!'>/data/web_static/releases/test/index.html"

source="/data/web_static/releases/test/"
target="/data/web_static/current"

if [ -h $target ]; then
    rm $target
fi
sudo ln -s $source $target

sudo chown -R ubuntu:ubuntu /data/
sudo chgrp -R ubuntu /data/

path="/etc/nginx/sites-available/default"
content="\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "/^\tserver_name _;/a\\$content" $path

sudo service nginx restart
