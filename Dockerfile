FROM python:3.9
COPY main.py ./
COPY requirements ./
RUN pip install -r requirements
CMD ["python3", "main.py"]
