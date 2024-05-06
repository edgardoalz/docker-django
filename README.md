# Finance API

## Setup

We use python 3.12 and recommend to use pyenv to manage you're python versions.
Here's how to install it with Hombrew.

`brew update`

`brew install pyenv`

## Local Development

To set the minimum env config copy the example file

`cp example.env .env`

We require you to setup MySQL. The project includes a docker-compose file which
should work with the example configs without extra work.

`docker-compose up -d`
