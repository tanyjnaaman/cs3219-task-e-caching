FROM python:3.8
WORKDIR /usr/
COPY . /usr/
RUN pip install -r /usr/requirements.txt
CMD python -m src.main