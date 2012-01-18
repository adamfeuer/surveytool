<VirtualHost *:9000>
   ServerAdmin webmaster@localhost
   ServerName research-staging.liveingreatness.com

   # Tell Apache this is a HTTPS request without actually using HTTPS on the localhost
   SetEnvIf X-Forwarded-Protocol "^https$" HTTPS=on
    
   WSGIDaemonProcess domain-staging display-name=surveytool-staging-%{GROUP} maximum-requests=10000
   WSGIProcessGroup domain-staging
   WSGIScriptAlias / /opt/webapps/research-staging.liveingreatness.com/apache/django.wsgi-staging

   <Directory /opt/webapps/research-staging.liveingreatness.com/apache>
      Order deny,allow
      Allow from all
   </Directory>

   # static files
   Alias /robots.txt /opt/webapps/research-staging.liveingreatness.com/surveytool/static/robots.txt 
   Alias /favicon.ico /opt/webapps/research-staging.liveingreatness.com/surveytool/static/favicon.ico
   Alias /media/admin/ /opt/webapps/research-staging.liveingreatness.com/surveytool/static/admin/
   Alias /media/ /opt/webapps/research-staging.liveingreatness.com/surveytool/media/

   <Directory /opt/webapps/research-staging.liveingreatness.com/surveytool/media>
      Order deny,allow
      Allow from all
   </Directory>

   <Directory /opt/webapps/research-staging.liveingreatness.com/surveytool/static>
      Order deny,allow
      Allow from all
   </Directory>

   ErrorLog /var/log/apache2/research-staging.liveingreatness.com-error.log
   CustomLog /var/log/apache2/research-staging.liveingreatness.com-access.log combined
    
</VirtualHost>
