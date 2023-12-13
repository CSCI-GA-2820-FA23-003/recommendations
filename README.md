# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA23-003/recommendations/graph/badge.svg?token=VNH31V6V4Q)](https://codecov.io/gh/CSCI-GA-2820-FA23-003/recommendations)
[![Build Status](https://github.com/CSCI-GA-2820-FA23-003/recommendations/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-003/recommendations/actions)


## Overview

- This project involves designing, planning, building, and deploying a cloud-native microservice (Recommendation service) that is the part of an eCommerce website.
- The recommendations service is a representation of a product recommendation based on another product. In essence, it is just a relationship between two products that "go together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.). It could also recommend based on what other customers have purchased like "customers who bought item A usually buy item B". Recommendations have 3 different types: cross-sell, up-sell, and accessory.


## REST API Endpoints
All APIs have a common route prefix: http://localhost:8080/recommendations

### GET
- list_all(): Returns the list of all Recommendations.
  - It has a query capability that filters the results based on its name(recommendation_name), source product name(source_name), source product id(source_pid), and type(recommendation_type).
    ```
    GET /recommendations
    ```

- get(rec_id): Retrieves a specific Recommendation based on its ID
  - Parameter:
    - `rec_id`: int
    ```
    GET /recommendations/<id>
    ```

### POST
- post(): Creates a Recommendation
  - Parameters
    - `source_pid`: int
    - `name`: string
    - `recommendation_name`: string
    - `type`: int
    ```
    POST /recommendations
    ```

### PUT
- put(rec_id): Updates a Recommendation given its ID
  - Parameters
    - `rec_id`: int
    ```
    PUT /recommendations/<id>
    ```

- like_recommendation(rec_id): Likes a Recommendation, which increments its like count
  - Parameters
    - `rec_id`: int
    ```
    PUT /recommendations/<id>/like
    ```
    
- dislike_recommendation(rec_id): Likes a Recommendation, which increments its dislike count
  - Parameters
    - `rec_id`: int
    ```
    PUT /recommendations/<id>/dislike
    ```

### DELETE
- put(rec_id): Deletes a Recommendation given its ID
  - Parameters
    - `rec_id`: int
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
├── factories       - factory for creating test objects
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes

k8s/                  - kubernetes yaml file
├── deployment.yaml   - App deployment configuration
├── ingress.yaml      - Ingress resource setup
└── postgres.yaml     - Postgres resource setup
└── pv.yaml           - Persistent volume configuration
└── secret.yaml       - Sensitive data management
└── service.yaml      - Service exposure settings
```

## Local Kubernetes Cluster Deployment Guide

- Initialize a Kubernetes Cluster 
  - Execute the command below in your terminal to initiate a new Kubernetes cluster:  
    ```make cluster```
- Docker Image Preparation and Tag 
  - We need to build the Docker image of the project, tag it. 
  ```docker build -t recommendation:1.0 .```

    ```docker tag recommendation:1.0 cluster-registry:32000/customer:1.0```

- Add to etc/hosts 
  - Before pushing, ensure that cluster-registry:32000 is mapped to 127.0.0.1 in your /etc/hosts file.

    ```sudo bash -c "echo '127.0.0.1 cluster-registry' >> /etc/hosts"```

- Push the image to the repository 
  - After building and tagging the Docker image. Push it to your registry.

    ```docker push cluster-registry:32000/recommendation:1.0```

- Deploying on Kubernetes
  - To deploy the Postgres database as a StatefulSet along with the image we created, run the following:

    ```kubectl apply -f k8s```

- Verifying the Deployment
  - The service should be accessible at `localhost:8080`
  - For deployment health checks, use the `/health` endpoint.

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
