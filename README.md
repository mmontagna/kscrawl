# kscrawl
A kinda simple distributed python crawler.
[![Circle CI](https://circleci.com/gh/mmontagna/kscrawl.svg?style=svg)](https://circleci.com/gh/mmontagna/kscrawl)

##Environment Variables
Set REDIS_HOST to the location of your redis server.

##How to use

To print crawl state:
`python -m crawl.default.state`

To start crawler:
Run a docker image from here https://hub.docker.com/r/mmontagna/kscrawl/
or
`python -m crawl.default`

To start a crawl:
`python -m crawl.default.start --urls http://example.com --depth 1`

