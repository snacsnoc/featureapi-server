# feature on off server

turn features on or off remotely


Run
```bash
./manage.py runserver
```

# Display
Send POST to `/api/v1/gs` (get script)
feature_hash = script to display


# Fetching new changes

* worker to fetch new changes on schedule
* github action pings API to tell to refresh code in cache
   * authentication