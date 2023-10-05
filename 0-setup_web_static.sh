#!/usr/bin/env bash
#Bash script that sets up your web servers for the deployment of web_statici

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i " /location \/hbnb_static {/ a\\
        alias /data/web_static/current/;
" $config_file

# Restart Nginx
sudo service nginx restart

exit 0
