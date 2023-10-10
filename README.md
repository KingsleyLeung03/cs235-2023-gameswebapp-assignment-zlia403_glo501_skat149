# COMPSCI 235 S2 2023 Assignment Phase 2: Games WebApp
By zlia403 | glo501 | skat149

## Description

This Web application showcases the utilization of Python's Flask framework. It leverages libraries like the Jinja templating library. The design of the application incorporates architectural design patterns and principles, including Repository, Dependency Inversion, and Single Responsibility. To ensure a well-structured architecture, Flask Blueprints are employed, effectively separating various application functions. The comprehensive testing strategy encompasses both unit and end-to-end testing, facilitated by the pytest tool.

<!-- This repository contains an implementation of the domain model from Assignment 1. It contains unit tests which can be run through pytest. It also contains a simple Flask application that renders content of a Game object instance from our domain model on a blank HTML page. 

From here on you can **choose if you want to use the provided domain model or your own implementation from CodeRunner assignment 1**. The domain model implementation may have to be extended, and you may also decide to remove or modify test cases as it suits you. --> 

## Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select 'Project:cs235-2023-gameswebapp-assignment-zlia403_glo501_skat149' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *cs235-2023-gameswebapp-assignment-zlia403_glo501_skat149* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

To run the tests for the database components, these are in the folder 'tests_db', so you can call 'python -m pytest tests_db' to run them from the command line.

## Configuration

The *project directory/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
 
These settings are for the database version of the code:

* `SQLALCHEMY_DATABASE_URI`: The URI of the SQlite database, by default it will be created in the root directory of the project.
* `SQLALCHEMY_ECHO`: If this flag is set to True, SQLAlchemy will print the SQL statements it uses internally to interact with the tables.
* `REPOSITORY`: This flag allows us to easily switch between using the Memory repository or the SQLAlchemyDatabase repository.

## Data sources

The data files are modified excerpts downloaded from:

https://huggingface.co/datasets/FronkonGames/steam-games-dataset



