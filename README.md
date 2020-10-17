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
- _uvicorn_ (0.11.3) (probably optional if you serve the app differently)

Furthermore Girandole is dependent on some tools:
- _Beets_ (1.4.9)
Girandole will use Beets's API for library access and reading configuration settings.
- _whatlastgenre_ (My [API friendly fork](https://github.com/bartkl/whatlastgenre/tree/feature/api-friendly).)
Whatlastgenre is a tool that tries to find genres for your albums. This is what Girandole uses for its genre suggestions. We have forked the tool to make it suited for our purposes.


### Local installation
_Warning_: this guide is not tested properly. I haven't done the installation locally yet, so please know that no guarantees can be made to its completeness and validity.

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


### Configuration
Of course, the configuration of these tools has to be in order as well. It's up to you if you want to use dedicated config files for Girandole, or have Girandole use the configs already in use by yourself. How to set this up will become more concrete further on.

Finally, the environment needs to provide the necessary variables for Girandole to run properly. This too will be discussed in more detail later.
