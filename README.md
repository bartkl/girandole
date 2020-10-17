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


### Setup and configuration
Now that all the necessary installations have been done, we need to configure the environment, tools and application.

There's a few aspects to this.

#### Beets and whatlastgenre
You need to supply configuration for Beets and whatlastgenre. You can use your existing configs, or create dedicated new ones, but in both cases you have to make sure they will be available within the application.

* If running locally, make sure Girandole, Beets and whatlastgenre are installed and configured in the same (virtual or not) environment.
* When running in Docker, make sure you mount or copy all necessary configuration files.
	- For Beets, you'll need the config file and library database. Those need to be present in the `$BEETSDIR` on the container.
	- For whatlastgenre, there's the `.whatlastgenre` config dir in your home directory. This needs to be present at `/root/.whatlastgenre` in the container. Also, make sure the `whatlastgenre` package is in your `$PYTHONPATH` so it is discovered. See the `Dockerfile` earlier for an example.

#### Girandole environment
There are two environment variables with which you can control Girandole's behavior:

* `$GIRANDOLE_CONFIG_DIR`: If defined, this should point to the directory where `config.ini` can be found. It defaults to `/etc/girandole`.
* `$GIRANDOLE_MUSIC_DIR`: This should be set if you wish to rebase the paths in the Beets database for I/O operations. This is useful when you are running Girandole in a Docker container, and the path to the music files is different from that on the host computer.

If running in a Docker container, make sure these environment variables are passed in the container. I recommend defining a `docker-compose.yaml` file in which you set the `environment`.

#### Girandole config
Finally, there's the application config: `config.ini`. Currently, the only two sections and settings can most easily be demonstrated by example:

```ini
[girandole: albums]
paths in response = yes

[beets]
windows paths = no
```

* `paths in response`: This determines the inclusion of exclusion of the `path` of the albums in the API `Album` responses. By default this is disabled, since some people experience heavy performance issues with this enabled.
* `windows paths`: If the paths in the Beets config and library are Windows paths, set this to `yes`. This is especially important if you run in a Docker container on a Windows host, and you have to rebase the library paths so Girandole can access the files.

#### Example `docker-compose.yaml`
This is the `docker-compose.yaml` I use on my Raspberry Pi:

```yaml
version: '3'
services:
  girandole:
    build:
      context: .
      dockerfile: Dockerfile.py37.armv7  # See `Dockerfile` earlier.
    ports:
      - ${GIRANDOLE_PORT}:8080
    volumes:
      - ./girandole:/opt/girandole  # Remove in production.
      - ${GIRANDOLE_MUSIC_DIR}:${GIRANDOLE_MUSIC_DIR}
      - ${GIRANDOLE_CONFIG_DIR}/config.ini:/etc/girandole/config.ini
      - ${GIRANDOLE_BEETS_DB}:/etc/beets/library.db
      - ${GIRANDOLE_BEETS_CONFIG}:/etc/beets/config.yaml
      - ${GIRANDOLE_WLG_DIR}:/root/.whatlastgenre
    environment:
      - GIRANDOLE_CONFIG_DIR:${GIRANDOLE_CONFIG_DIR}
    entrypoint: uvicorn --host 0.0.0.0 --port 8080 girandole.main:app --reload
```

The variables used here are defined in the accompanying `.env` file:

```
GIRANDOLE_PORT=8080
GIRANDOLE_MUSIC_DIR=/media/droppie/libraries/music
GIRANDOLE_BEETS_DB=/media/droppie/libraries/music/.meta/beets/library.db
GIRANDOLE_BEETS_CONFIG=/media/droppie/libraries/music/.meta/beets/config.yaml
GIRANDOLE_WLG_DIR=/home/bart/.whatlastgenre
GIRANDOLE_CONFIG_DIR=/home/bart/.dotfiles/local/oblomov/conf/girandole
```

### Running the server

#### Local
As can be seen in the example `docker-compose.yaml` earlier, the way to serve the app using `uvicorn` is:
```
$ uvicorn --host 0.0.0.0 --port 8080 girandole.main:app --reload
```

#### Running the docker container
Start the Docker container including the mounts and environment:

```
$ docker-compose up
```

If you've changed something about the Docker configuration files, you should restart the container. If you've changed the `Dockerfile` contents in a way that requires rebuilding, you can call:
```
$ docker-compose up --build
```