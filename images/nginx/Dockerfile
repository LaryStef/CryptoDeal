FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./html/MobileDevice.html /usr/share/nginx/html/MobileDevice.html
COPY ./html/500.html /usr/share/nginx/html/500.html
COPY ./fullchain.pem /etc/nginx/fullchain.pem
COPY ./privkey.pem /etc/nginx/privkey.pem
