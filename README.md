# feature on off server

Turn Javascript features on or off remotely. 

Code from version control is stored in a caching server and served on request. When code is updated from version control, the code cache gets updated. This allows you to embed version-controlled code snippets anywhere.
A Javascript client fetches the code and executes it.

Sample Javascript client:
```javascript
class HttpController {
    constructor() {
        this.myHeaders = new Headers();
        this.myHeaders.append("User-Agent", navigator.userAgent);
        this.myHeaders.append("Referer", window.location.href);
        this.myHeaders.append("Accept-Language", navigator.language);

        this.requestOptions = {
            method: 'GET',
            headers: this.myHeaders,
            redirect: 'follow'
        };
    }

    async get(url) {
        try {
            const response = await fetch(url, this.requestOptions);
            const result = await response.text();
            return result;
        } catch (error) {
            console.log('error', error);
        }
    }
}

class FeatureApi {
    constructor(hash, backupFile) {
        this.hash = hash;
        this.backupFile = backupFile;
        this.httpController = new HttpController();

    }
    async display() {
        try {
            const result = await this.httpController.get(`http://127.0.0.1:8000/api/v1/gs?feature_hash=${this.hash}`);
            const parsedResult = JSON.parse(result);
            if (parsedResult.message) {
                var code = parsedResult.message;
                var func = new Function(code);
                func();
            }
        } catch (error) {
            console.log('error', error);
            // fetch from the backup file
            this.fetchBackup();
        }
    }


    fetchBackup() {
        fetch(this.backupFile)
            .then(response => response.text())
            .then(code => eval(code))
            .catch(error => console.error('Error fetching backup code: ', error));
    }
}

// Client code
const featureApi = new FeatureApi("c26257b3-059b-46db-9f1f-e5f754263e8b", "http://website.cdn.com/myfile.js");
featureApi.display();
```


# How it works
[![Feature-On-Off-1.png](https://i.postimg.cc/hvMNdwXb/Feature-On-Off-1.png)](https://postimg.cc/MfMsk9bv)

## Django 4.1

Run
```bash
./manage.py runserver
```

# Display
Send POST to `/api/v1/gs` (get script)

`feature_hash` = script to display


# Fetching new changes (in-progress)

* worker to fetch new changes on schedule
* github webhook listener
* github action pings API to tell to refresh code in cache




Resources:
  https://github.com/jazzband/django-redis#infinite-timeout