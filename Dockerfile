FROM python:3
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3","seetree.py"]
