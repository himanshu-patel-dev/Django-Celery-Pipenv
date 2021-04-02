# Django and Celery

`After cloning this project replace .env.sample file (beside settings.py) with name .env and also replce required credential with valid ones`

***

## Create Virtual env with Pipenv

### The Pipfile.lock

This file enables deterministic builds by specifying the exact requirements for reproducing an environment. It contains exact versions for packages and hashes. This is used to replicate environment in production.

### The Pipfile

Pipfile intends to replace requirements.txt. Pipenv is currently the reference implementation for using Pipfile. The syntax for the Pipfile is TOML, and the file is separated into sections. `[dev-packages]` for development-only packages, `[packages]` for minimally required packages, and `[requires]` for other requirements like a specific version of Python. This only cantains the packages not their dependencies. Like installing django will install django and it's dependencies but will list only package not its depencencies.

### requirements.txt to Pipfile

If you run `pipenv install` it should automatically detect the `requirements.txt` and convert it to a `Pipfile`, outputting something like the following.

### Commands - [Official Doc](https://docs.pipenv.org/)

- `mkdir .venv`  
  Make a `.venv` folder in project folder to that pipenv pick this folder for virtual env rather than creating one of its own in global directory,

- `pipenv shell`  
  Create the virtual env in any folder (if Pipfile is not present) or launch a virtual env (if Pipfile exists) use. Pipfile uses `toml` format.

- `pipenv --venv`  
  To know where the virtual env is located (in project folder or global folder)

- `pipenv --rm`  
  While in shell or project with Pipfile this deletes the virtual environment folder but do not deactvate the shell.

- `exit`  
  To exit the virtual env shell. `deactivate` also works same but do not use them as this do not close the subshell opened for virtual env pipenv remains in a confused state. Thus right way is to use `exit`.

- `pip freeze`  
  Gives no list as no package is installed in fresh env

- `pip list`  
  Gives a list of pip, setuptools and wheel only.

- `pip install python-decouple`  
  Install package in virtual env (while we are in venv shell) and we can check it using previous commands. But this do not create a `Pipfile.lock` neither add the installed package in `Pipfile` so may not be a preferred way.

- `pipenv install django`  
  Install the package in venv (while the shell is active). Also create a `Pipfile.lock` with package and all its dependencies listed and put the install package (django only not its dependencies) in `Pipfile's [packages]`.

- `pipenv install pytest --dev`  or `pipenv install -r dev-requirements.txt --dev`  
  To install any package for development purpose that we want to include only for developer and do not want to be install in production.

- `pipenv install --dev`  
  While replicating environment from previous `Pipfile` to install dev packages use this flag in command. Packages will be installed in `[dev-packages]`

- `pipenv run django-admin startproject newproj`  
  To run a command when virtual env of pipenv is not activated use this command to produce same result. This will run command as if we are in virtual env shell.

- We can use this method also to determin which python version and from which venv is being used for python. Also if we are not in shell then use `pipenv run python` to activate python shell.

  ```python
  >>> import sys
  >>> sys.executable
  '/home/himanshu/HP/dev/projects/Django-Celery/.venv/bin/python'
  ```

- `pipenv install -r requirements.txt`  
  To install packages from `requirements.txt` in pipenv shell or without shell.

- `pipenv uninstall <package>` or `pipenv uninstall --all`  
  To uninstall any package from environment. You can replace --all with --all-dev to just remove dev packages.

- `pipenv run <insert command here>`  
  To run a command in the virtual environment without launching a shell.

- `pipenv lock`  
  This will create/update your Pipfile.lock, which you’ll never need to edit manually. You should always use the generated file.

- `pipenv install --ignore-pipfile`  
  This tells Pipenv to ignore the Pipfile for installation and use what’s in the Pipfile.lock. Given this Pipfile.lock, Pipenv will create the exact same environment.

- `pipenv graph`  
  print out a tree-like structure showing your dependencies
  
    ```bash
    Django==3.1.7
    - asgiref [required: >=3.2.10,<4, installed: 3.3.1]
    - pytz [required: Any, installed: 2021.1]
    - sqlparse [required: >=0.2.2, installed: 0.4.1]
    python-decouple==3.4
    ```

- `pipenv graph --reverse`  
  Similar to `pipenv graph` but in reverse. To show the sub-dependencies with the parent that requires it.  

- Pipenv supports the automatic loading of environmental variables when a .env file exists in the top-level directory. That way, when you pipenv shell to open the virtual environment, it loads your environmental variables from the file. The .env file just contains key-value pairs:

    ```yaml
    DEBUG=True
    SECRET_KEY=Top-Secret-Key-Without-Quotes
    ```

- To get requirements.txt for other developer or in case team need it use below commands.

    ```bash
    # to see what will go inside requirements.txt
    pipenv lock --requirements

    # to see what will go inside requirements.txt if we lock basic as well dev packages
    pipenv lock --requirements --dev

    # to generate requirements.txt using only basic packages
    pipenv lock -r > requirements.txt

    # to generate requirements.txt using only dev packages
    pipenv lock -r --dev-only > dev-requirements.txt

    # to generate requirements.txt using all packages basic or dev
    pipenv lock -r -d > dev-requirements.txt
    ```

- If by mistake a package is install using `pip install <package>` then it's entry will not be made in Pipfile. Remove it using `pip uninstall <package>` then reinstall using pipenv. This will create entry of project in Pipfile and Piplock.

- `pipenv --python 3.9`  
  To update python version in virtual env.

- `pipenv check`  
  Python check

## Python Decouple: to store sensitive data in environment variables

- `pipenv install python-decouple`  
  Install package

- Inside settings.py  

  ```python
  from decouple import config

  SECRET_KEY = config('SECRET_KEY')
  DEBUG = config('DEBUG', default=False, cast=bool)
  EMAIL_HOST = config('EMAIL_HOST', default='localhost')
  EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
  ```

- Put your secret in a `.env` file in projects root directory or along with settings.py file as `settings.ini` file.

  ```yaml
  [settings]
  SECRET_KEY='Top-Secret-Key'
  DEBUG=True
  # commented
  ```

- If we have `pipenv` as tool to create virtual env the put `.env` file in projec's root folder or main folder of repo (along side .gitignore file). so that `pipenv` can identify the virtual env file and load those variables in environment. We can access those variables as.

  ```bash
  # enter python shell
  pipenv run python
  ```
  
  ```python
  >>> import os
  >>> os.environ['DEBUG']
  'True'
  >>> os.environ['SECRET_KEY']
  'Top-Secret-Key'
  ```

## Celery and RabbitMQ

### Concepts

- `Client (user send request) -> Django (web server) -> RabbitMQ (message broker) -> Celery (worker processes)`  
  A scheduled/event driven task which is handeled by django but django do not complete the task on it's own instead pass it on to RabbitMQ/Redis (message or event handler) which then completes the task/event as per availability or resources.

### Commands

- `pipenv install celery`  
  To install celery

- Setup RabbitMQ. Go to shell/terminal and make following commands.  
  
  ```bash
  # install the pakage
  sudo apt-get install rabbitmq-server
  # enable the process
  systemctl enable rabbitmq-server
  # start processes
  sudo systemctl start rabbitmq-server
  # check the status of service
  systemctl status rabbitmq-server
  ```

- Add a [celery.py](Celery/Celery/celery.py) file along side with manage.py.

- Setup [__init__.py](Celery/Celery/__init__.py) file of project to load celery at starup of server.

- `django-admin startapp App`  
  Create a new app in project. (`App` here) also make a new file in it named `tasks.py` and put following code in it. Also add this app to projects settings.py

  ```python
  from celery import shared_task

  @shared_task
  def add(x,y):
    return x+y
  ```

- `celery -A Celery worker -l INFO`  
  Start celery worker process. Here `Celery` is project name and `celery` is project. For this to function properly rabbitmq server should be running. See the transport layer set to `amqp://guest:**@localhost:5672//`.

  ```bash
  -------------- celery@workstation v5.0.5 (singularity)
  --- ***** ----- 
  -- ******* ---- Linux-5.8.0-48-generic-x86_64-with-glibc2.29 2021-04-01 21:33:28
  - *** --- * --- 
  - ** ---------- [config]
  - ** ---------- .> app:         Celery:0x7fc879d03610
  - ** ---------- .> transport:   amqp://guest:**@localhost:5672//
  - ** ---------- .> results:     disabled://
  - *** --- * --- .> concurrency: 4 (prefork)
  -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
  --- ***** ----- 
  -------------- [queues]
  ```

- Now go to another shell while the django server is running and open django shell and import the `tasks.py` module which we made in tha app.

  ```python
  >>> from App.tasks import add
  >>> add.apply_async((1,2), countdown=5)
  <AsyncResult: 2233792d-dd75-48e5-a8cc-7ad6f8e93964>
  ```
  
  Go to the running django server and notice the output.  
  
  ```bash
  Received task: App.tasks.add[2233792d-dd75-48e5-a8cc-7ad6f8e93964]  ETA:[2021-04-01 22:16:54.662311+00:00] 
  Task App.tasks.add[2233792d-dd75-48e5-a8cc-7ad6f8e93964] succeeded in 0.0008293840000987984s: 3
  ```

  Notice the output of function in the end of last line.

### Sending Emails using celery

- `Client -> Django -> RabbitMQ -> Celery`

  - Client (sends a request to django server)

  - Django (receive client call and validates form)

  - RabbitMQ (Handels the task of email sending given by django)

  - Celery (receive task from rabbitmq and execute)

- [forms.py](Celery/App/forms.py) - Make a form which user will fill.

- [views.py](Celery/App/views.py) - Make a view which server the request with this form and a confirmation of sent email.

- [tasks.py](Celery/App/tasks.py) - Make a task to send email. Such tasks are handeled by RabbitMQ.

- [email.py](Celery/App/email.py) - Make a module to send emails this also uses a [email_message.txt](Celery/App/templates/email_message.txt) (this file need to be in templates folder of app) file to produce email format

- Don't forget to setup setting.py file with Email settings before sending email.  

  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = config('EMAIL_HOST_USER')
  EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
  DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
  ```

- Now run the celery `celery -A Celery worker -l INFO` here make sure the rabbitMQ server is running and get connect to this shell on starting celery. Now start django server and go to `http://127.0.0.1:8000/verify/` and fill details and email will be delicered to your account. But this only deliver email to your account no validation is being done here.
