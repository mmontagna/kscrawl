FROM continuumio/miniconda

RUN conda install numpy scikit-learn
RUN pip install redis beautifulsoup4 urlnorm chardet boto3 nltk coverage mock attrdict

COPY . /app

WORKDIR /app

