## Overview

We implement a simple caching proof of concept. With a MongoDB database (local), we provide endpoints to get by ID or get all, both with caching.

We see that caching about halves the API response time.

## Run

To run, we use docker. Run:

```
docker-compose up --build
```

To test the API, use [the postman collection here](https://www.getpostman.com/collections/d589132028602ecac09b) with `ngrok` redirecting to your `localhost:8000`, with:

```
ngrok http 8000
```
