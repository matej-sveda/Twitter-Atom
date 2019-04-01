# Twitter - Atom feed generator

Project contains API application, which communicate with Twitter API and generates an Atom feed, contained of 30 most recent tweets and its answers on user dashboard.

## Getting Started

### Prerequisites

Project was build and tested on Ubuntu 16.04 with Python 3.5.2, using following modules:

- flask 1.0.2
- tweepy 3.7.0
- werkzeug 0.15.1

### Installing

Install all missing modules using pip:
```
pip install flask
pip install tweepy
pip install werkzeug
```

## How to use
API requires argument user, which needs to be a valid twitter username. API send a request to 3rd Twitter API and returns an Atom feed of user's dashboard.

- input example

```
GET http://localhost:5000/dashboard.xml?user=TalkPython	

```

## Authors

* **Matej Sveda** - [matej-sveda](https://github.com/matej-sveda)
