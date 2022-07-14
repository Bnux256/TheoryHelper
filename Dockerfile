FROM python:3.10-alpine
WORKDIR /usr/src/app
ADD . .
RUN pip install -U pip && pip install -r requirments.txt
EXPOSE 5001:8000
CMD ["gunicorn", "-w", "4", "main:app", "-b", "0.0.0.0:8000"]