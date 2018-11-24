# OpenCon application

This application has been designed to support the application process for [OpenCon 2018](http://www.opencon2018.org), the conference and community empowering the next generation to advance open access, open education and open data. It collects  applications to attend the conference and facilitates a multi-step community rating process.

In addition to [OpenCon 2018](https://github.com/sparcopen/opencon-2018-app-code), we have also published the code for [OpenCon 2015](https://github.com/sparcopen/opencon-2015-app-code), [OpenCon 2016](https://github.com/sparcopen/opencon-2016-app-code) and [OpenCon 2017](https://github.com/sparcopen/opencon-2017-app-code).

## Installation

This application is using `docker-compose`. The examples below are for the development version of the app using the development version: `dev.yml`.

Follow the steps `Getting your computer ready`, `Setting up the application` and `Creating users` from the README in [Connect OER](https://github.com/sparcopen/connect-oer-code), they are identical. Once your computer is ready, run the development server:

`docker-compose -f dev.yml up`

After this, you can open your web browser and navigate to `http://localhost:9121`. To access the administrative area, go to `http://localhost:9121/admin`.

It is also necessary to create `.env` file in the root of the project containing the project settings, e.g.:

```
DEFAULT_FROM_EMAIL=noreply@opencon2018.org
DEFAULT_REPLYTO_EMAIL=opencon@sparcopen.org
EMAIL_HOST_USER=exampleuser
EMAIL_HOST_PASSWORD=examplepassword
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
DOWNLOAD_SECRET=somerandomstring
```

## Working with the app

Prospective OpenCon attendees submit applications which are then passed through several rounds of ratings, named `Round 0` (simple Yes/No rating), `Round 1` (done by the OpenCon alumni) and `Round 2` (carried out by the Organizing Committee).

If the app is updated as the rating process is in progress (e.g. when `opencon/application/models.py` file is changed, `opencon/application/constants.py` is changed or rating logic is updated), it is necessary to recalculate the values already stored in the database using `docker-compose -f dev.yml run django python manage.py recalculate_ratings`.
