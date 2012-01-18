<VirtualHost *:9000>
   ServerAdmin webmaster@localhost
   ServerName research.liveingreatness.com

   # Tell Apache this is a HTTPS request without actually using HTTPS on the localhost
   SetEnvIf X-Forwarded-Protocol "^https$" HTTPS=on
    
   WSGIDaemonProcess domain-prod display-name=surveytool-prod-%{GROUP} maximum-requests=10000
   WSGIProcessGroup domain-prod
   WSGIScriptAlias / /opt/webapps/research.liveingreatness.com/apache/django.wsgi-prod

   <Directory /opt/webapps/research.liveingreatness.com/apache>
      Order deny,allow
      Allow from all
   </Directory>

   # static files
   Alias /robots.txt /opt/webapps/research.liveingreatness.com/surveytool/static/robots.txt 
   Alias /favicon.ico /opt/webapps/research.liveingreatness.com/surveytool/static/favicon.ico
   Alias /media/admin/ /opt/webapps/research.liveingreatness.com/surveytool/static/admin/
   Alias /media/ /opt/webapps/research.liveingreatness.com/surveytool/media/

   <Directory /opt/webapps/research.liveingreatness.com/surveytool/media>
      Order deny,allow
      Allow from all
   </Directory>

   <Directory /opt/webapps/research.liveingreatness.com/surveytool/static>
      Order deny,allow
      Allow from all
   </Directory>

   ErrorLog /var/log/apache2/research.liveingreatness.com-error.log
   CustomLog /var/log/apache2/research.liveingreatness.com-access.log combined
    
</VirtualHost>
