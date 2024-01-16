FROM python:3.12
WORKDIR /code
COPY ./requirements.txt ./client/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/client/requirements.txt
COPY . ./client
WORKDIR ./client/
CMD ["python", "-u", "main.py"]