FROM continuumio/miniconda

RUN pip install redis BeautifulSoup urlnorm chardet

COPY . /app

WORKDIR /app

