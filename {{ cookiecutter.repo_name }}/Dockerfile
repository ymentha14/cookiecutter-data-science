FROM python:3.6.9
COPY ./ ./app
WORKDIR ./app

RUN apt-get update && \
    apt-get -y install curl && \
    apt-get -y install nodejs && \
    apt-get -y install make

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager

CMD [ "/bin/bash" ]

