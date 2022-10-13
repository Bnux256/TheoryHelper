FROM python:3.10-alpine
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt 
RUN pip install -U pip && pip install -r requirements.txt
ADD . .
RUN python lib/download_cache.py
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "main:app", "-b", "0.0.0.0:8000"]