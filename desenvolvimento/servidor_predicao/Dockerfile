FROM python:3.6

# Configure environment
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

COPY app /app
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
