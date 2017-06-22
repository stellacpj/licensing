#!/bin/bash
echo "This script will:
1) install all modules need to run web2py on Ubuntu 14.04
2) install web2py in /home/www-data/
3) create a self signed ssl certificate
4) setup web2py with mod_wsgi
5) overwrite /etc/apache2/sites-available/default
6) restart apache.

You may want to read this script before running it.

Press a key to continue...[ctrl+C to abort]"

read CONFIRM


# optional
# dpkg-reconfigure console-setup
# dpkg-reconfigure timezoneconf
# nano /etc/hostname
# nano /etc/network/interfaces
# nano /etc/resolv.conf
# reboot now
# ifconfig eth0

sudo apt-get update
sudo apt-get install build-essential python-dev libsqlite3-dev libreadline6-dev libgdbm-dev zlib1g-dev libbz2-dev sqlite3 zip libssl-dev

echo "installing useful packages"
echo "=========================="
sudo apt-get install python-pip
sudo pip install pyeapi
sudo pip install jsonrpc
sudo apt-get -y install git
sudo apt-get -y install wget
sudo apt-get -y install python-matplotlib
sudo apt-get -y install python-reportlab
sudo apt-get -y install mercurial
sudo apt-get -y install python-jinja2

# optional, uncomment for emacs
# apt-get -y install emacs

# optional, uncomment for backups using samba
# apt-get -y install samba
# apt-get -y install smbfs

echo "downloading, installing and starting web2py"
echo "==========================================="
cd /home
mkdir www-data
cd www-data
rm web2py_src.zip*
wget http://web2py.com/examples/static/web2py_src.zip
unzip web2py_src.zip
mv web2py/handlers/wsgihandler.py web2py/wsgihandler.py
cd /home/www-data/web2py/applications
git clone https://github.com/stellacpj/JunosPortal.git
cd /home/www-data
chown -R www-data:www-data web2py

echo "setting up apache modules"
echo "========================="
sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi
sudo a2enmod wsgi
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod headers
sudo a2enmod expires
sudo a2enmod rewrite
sudo mkdir /etc/apache2/ssl

echo "creating a self signed certificate"
echo "=================================="
sudo sh -c 'openssl genrsa 1024 >/etc/apache2/ssl/self_signed.key'
sudo chmod 400 /etc/apache2/ssl/self_signed.key
sudo sh -c 'openssl req -new -x509 -nodes -sha1 -days 365 -subj "/C=US/ST=Denial/L=Chicago/O=Dis/CN=www.example.com" -key /etc/apache2/ssl/self_signed.key > /etc/apache2/ssl/self_signed.cert'
sudo sh -c 'sudo openssl x509 -noout -fingerprint -text < /etc/apache2/ssl/self_signed.cert > /etc/apache2/ssl/self_signed.info'

echo "rewriting your apache config file to use mod_wsgi"
echo "================================================="
sudo cd /etc/apache2/sites-available 
echo '
WSGIDaemonProcess web2py user=www-data group=www-data processes=1 threads=1

<VirtualHost *:80>

  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^/?(.*) https://%{SERVER_NAME}/$1 [R,L]

  CustomLog /var/log/apache2/access.log common
  ErrorLog /var/log/apache2/error.log
</VirtualHost>

<VirtualHost *:443>
  SSLEngine on
  SSLCertificateFile /etc/apache2/ssl/self_signed.cert
  SSLCertificateKeyFile /etc/apache2/ssl/self_signed.key

  WSGIProcessGroup web2py
  WSGIScriptAlias / /home/www-data/web2py/wsgihandler.py
  WSGIPassAuthorization On

  <Directory /home/www-data/web2py>
    AllowOverride None
    Require all denied
    <Files wsgihandler.py>
      Require all granted
    </Files>
  </Directory>

  AliasMatch ^/([^/]+)/static/(?:_[\d]+.[\d]+.[\d]+/)?(.*) \
        /home/www-data/web2py/applications/$1/static/$2

  <Directory /home/www-data/web2py/applications/*/static/>
    Options -Indexes
    ExpiresActive On
    ExpiresDefault "access plus 1 hour"
    Require all granted
  </Directory>

  CustomLog /var/log/apache2/ssl-access.log common
  ErrorLog /var/log/apache2/error.log
</VirtualHost>
' > /etc/apache2/sites-available/web2py.conf   # FOR 14.04

sudo rm /etc/apache2/sites-enabled/*    # FOR 14.04
sudo a2ensite web2py                 # FOR 14.04
sudo service apache2 restart

echo "restarting apache"
echo "================"

sudo cd /home/www-data/web2py
sudo -u www-data python -c "from gluon.widget import console; console();"
sudo -u www-data python -c "from gluon.main import save_password; save_password('admin',443)"
echo "done!"
