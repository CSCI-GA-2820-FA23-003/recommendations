# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA23-003/recommendations/graph/badge.svg?token=VNH31V6V4Q)](https://codecov.io/gh/CSCI-GA-2820-FA23-003/recommendations)
[![Build Status](https://github.com/CSCI-GA-2820-FA23-003/recommendations/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-003/recommendations/actions)

<!-- This is a skeleton you can use to start your projects -->

## Overview

This project is the a microserivce recommendation service. 
- `/service` folder contains the `models.py` file for the model and a `routes.py` file for APIs. 
- `/tests` folder has test case starter code for testing the model and the service separately.

## APIs
### GET
- Getting the list of all recommendations
- Getting the list of a specific recommendation with given ID
- Paramseters:
  - `id`: int
```
GET /recommendations
GET /recommendations/<id>
```
### POST
- Create a Recommendation
- Parameters
  - `source_pid`: int
  - `name`: string
  - `recommendation_pid`: int
  - `recommendation_name`: string
  - `type`: int
```
POST /recommendations
```
### PUT
- Update a Recommendation with given ID
- Parameters
  - `id`: int
```
PUT /recommendations/<id>
```
### DELETE
- Delete a Recommendation with given ID
- Parameters
  - `id`: int
```
DELETE /recommendations/<id>
```


<!-- This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from. -->

<!-- ## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository. -->

<!-- ## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
``` -->

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
