FROM bartkl/uvicorn-fastapi:python3.7

ENV PYTHONPATH "${PYTHONPATH}:/opt/whatlastgenre:/opt/girandole"
ENV BEETSDIR "/media/droppie/libraries/music/.config/beets"

COPY ./requirements.txt /etc/girandole-requirements.txt
RUN pip install -r /etc/girandole-requirements.txt

RUN git clone \
        --single-branch \
        --branch feature/api-friendly \
         https://github.com/bartkl/whatlastgenre.git \
         /opt/whatlastgenre

COPY ./app /opt/girandole/girandole/app
COPY ./config.yaml /etc/girandole/

WORKDIR /
