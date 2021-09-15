FROM python:3.6
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /expense_api
WORKDIR /expense_api
COPY requirements.txt /expense_api/
RUN pip install -r requirements.txt
COPY . /expense_api/