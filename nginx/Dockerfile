FROM nginx:alpine

ARG DEBUG
# If DEBUG is set (EVEN TO NULLSTRING),
# FILENAME become == dev otherwise nullstring
ARG FILENAME=${DEBUG:+dev}
# If FILENAME is nullstring, set it to prod or untouch
ARG FILENAME=${FILENAME:-prod}

#RUN echo ${FILENAME}

# adding configuration files
RUN rm -rf /etc/nginx/conf.d/*
COPY conf/${FILENAME}.conf /etc/nginx/conf.d/default.conf

EXPOSE 80