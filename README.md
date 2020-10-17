# Girandole

Girandole is an HTTP REST API on top of Beets. Its goal is to provide a more feature-rich alternative to the native [Web plugin](https://beets.readthedocs.io/en/stable/plugins/web.html). We also like to think the code is more maintaible thanks to using FastAPI and Pydantic.

Much of the initial modeling was done by peeking at the source code of the Beets Web plugin, but over time the implementations have diverged increasingly. Therefore, the extent of their interchangeability cannot be guaranteed.

## Motivation
The immediate motivation for this project was to have a HTTP interface to the Beets library that supports more than just reading from it. This is where the native Web plugin is too limited, so we decided to create something new altogether.

Having such an API has allowed as to create [Red Candle](https://github.com/gmvoliveira/red-candle), a web app which enables us to manage our Beets library.

## Features
Currently, among other things, the following features are supported:

- Reading album data from the library.
- Updating genres for albums, with the option to write these modifications to file tags as well.
- Genre suggestions for albums.
- Serve album art.

## Installation and configuration
Whatever way you choose to install, the setup is basically as follows.

### Dependencies
The immediate dependencies of Girandole itself are:
- _Python_ (≥ 3.7)
- _FastAPI_ (0.54.1)
- _uvicorn_ (0.11.3) (optional, but we use `unicorn` to serve the app)

Furthermore Girandole is dependent on some tools:
- _Beets_ (1.4.9).
Girandole will use Beets's API for library access and reading configuration settings.
- _whatlastgenre_ (My [API friendly fork](https://github.com/bartkl/whatlastgenre/tree/feature/api-friendly)).
Whatlastgenre is a tool that tries to find genres for your albums. This is what Girandole uses for its genre suggestions. We have forked the tool to make it suited for our purposes.


### Local installation
Simply install the aforementioned dependencies. It is recommended to use a virtual environment.

In a Python 3.7 environment, you can simply do:
```sh
$ pip install fastapi uvicorn beets
```

Installing the whatlastgenre fork is a bit more cumbersome for now. You have to obtain the code from Git and place the files some place which is discoverable by the used Python interpreter. Later you'll see how we'll make this package discoverable by using `$PYTHONPATH`.

For example:
```sh
$ git clone \
      --single-branch \
      --branch feature/api-friendly \
      https://github.com/bartkl/whatlastgenre.git \
      /opt/whatlastgenre
```

This will clone the code to `/opt/whatlastgenre`.

When done, please proceed to the _Configuration_ section.

### Installing using Docker container
You can automate the installation described above in a `Dockerfile`.

* If you're on an `amd64` CPU architecture (which is very likely), you can base your Dockerfile on one of the [uvicorn-gunicorn-fastapi](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi/) images.
* If you're on an `amdv7` CPU architecture, such as a Raspberry Pi, you can use [my simple image](https://hub.docker.com/repository/docker/bartkl/uvicorn-fastapi/).
* Otherwise, you'll have to manage the installations of FastAPI and Uvicorn in your own Dockerfile, extending one of the official [Python images](https://hub.docker.com/_/python) for instance.

### Example Dockerfile
My own `Dockerfile`, the one I use on my Raspberry Pi, looks as follows:

```
FROM bartkl/uvicorn-fastapi:python3.7

ENV PYTHONPATH "${PYTHONPATH}:/opt/whatlastgenre:/opt"
ENV BEETSDIR "/etc/beets"

COPY ./requirements.txt /etc/girandole-requirements.txt
RUN pip install -r /etc/girandole-requirements.txt

RUN git clone \
        --single-branch \
        --branch feature/api-friendly \
        https://github.com/bartkl/whatlastgenre.git \
        /opt/whatlastgenre

COPY ./girandole /opt/girandole

WORKDIR /
```

As you can see, it is pretty straight-forward. Note that the installation of Beets is concealed in the `requirements.txt` file.
The defined environment variables `PYTHONPATH` and `BEETSDIR` will be explained in the _Configuration_ section.


### Setup and Configuration
...
