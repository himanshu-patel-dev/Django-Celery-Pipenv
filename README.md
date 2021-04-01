# Django and Celery

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

## Python Decouple: to store sensitive data in environment variables
