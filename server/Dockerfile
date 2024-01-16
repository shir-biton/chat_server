FROM python:3.12
WORKDIR /code
COPY ./requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/server/requirements.txt
COPY . ./server
WORKDIR ./server/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]