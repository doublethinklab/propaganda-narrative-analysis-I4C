# Propaganda Narrative Analysis

## Overview

We analyze tweets from the PRC embassy in the Philippines between 
1st January 2020 to 30th June 2021 for propaganda narratives.

We offer some high level computational perspectives on the data to try and 
identify what is being talked about and how it is being talked about.

## Getting Started

To run the app:

```
./build_dev.sh
./build_postgres.sh
docker volume create dtl-pna
# if you are on linux or max
./run_app.sh
# if you are on windows
./run_app_windows.sh
```

Then browse to `localhost:5000` and you can interact with the web page.
