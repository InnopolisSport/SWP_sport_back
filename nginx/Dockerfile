FROM nginx:alpine

# adding configuration files
RUN rm -rf /etc/nginx/conf.d/*
COPY conf/* /etc/nginx/conf.d/

EXPOSE 80