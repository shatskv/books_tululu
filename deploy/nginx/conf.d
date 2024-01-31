upstream book-library {
    server web:8000;
}

server {

    listen 443 ssl;

    listen 80;
    
    server_name books-library.ru;
    
    ssl_certificate /etc/nginx/ssl/domain.ca-bundle;
    ssl_certificate_key /etc/nginx/ssl/books-library.key;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    keepalive_timeout 70;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_stapling on;

    if ($scheme = http) {
    return 301 https://$server_name$request_uri;
    }
    
    resolver 8.8.8.8;

    location / {

        proxy_pass http://book-library;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /static/ {
        alias /app/static;
    }
    location /media/ {
    alias /app/media;
    }
}