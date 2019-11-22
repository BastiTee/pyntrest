FROM nginx:1.17.6-alpine

# Install base python environment
RUN apk upgrade --update
RUN apk add \
python3 py3-pip vim curl git zlib-dev gcc python3-dev jpeg-dev musl-dev su-exec

# Install pyntrest requirements
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Prepare folders
RUN mkdir -p /usr/share/pyntrest
COPY manage.py /usr/share/pyntrest/manage.py
COPY pyntrest /usr/share/pyntrest/pyntrest
COPY pyntrest_project /usr/share/pyntrest/pyntrest_project
COPY sample_images /usr/share/pyntrest/sample_images

# Configure entrypoint
# COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# RUN chmod +x /usr/local/bin/entrypoint.sh

# COPY nginx.conf /etc/nginx/nginx.conf

# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
