FROM nginx

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY /client/static /app/static

COPY /client/nginx.conf /etc/nginx/nginx.conf

COPY /client/templates/index.html /app/static/index.html
RUN chown -R www-data:www-data /app


