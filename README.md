# Check out my Persistent DB Docker Flask Application

**Information:**

Don't look to much into the functionality of the application.
It's simple Flask Server making use of Python, SQLite, and SQLAlchemy.
Its single page validates and registers users and posts the information
To the other side of page. However, slightly modified these pages could
be useful in a login and registration system.

The main purpose of this simple application is to display how to write,
build and setup docker containers. This displays the db is persistant across
multiple containers, even when they are closed or disposed of.

A good activity would be to build a container, make a change to the Users table,
open up a second container and verify the changes persist across images. Then you
can stop or delete both containers. From there create a new one or start and old
back up and check out the table!! Very cool!

## Debian-based Linux Distros

**I am not going to cover the docker install**

**Build image -run from project directory, where Dockerfile is:**

docker build -t flask-docker-demo .

**Run docker image w/ persistent db mapping, and exposing of port:**

docker run -d -p 5000:5000 -v $(pwd)/instance:/app/instance --name flask-demo flask-docker-demo

**Run docker image with /persistant db mapping, and exposing of port, a control group:**

docker run -d -p 5000:5000 -v $(pwd)/instance:/app/instance
--name flask-demo-limited --cpus="0.5" --memory="256m" flask-docker-demo

**Example of running a second identical container (to first)- note the port, naming convention:**

docker run -d -p 5001:5000 -v $(pwd)/instance:/app/instance --name flask-demo-2 flask-docker-demo

**Verify the image is running:**

docker ps

**If it is not on the list, run this:**

docker ps -a

**Stop a container:**

docker stop container id

**Remove a stopped container:**

docker rm container id

**Remover all stopped containers:**

docker container prune

**Other useful commands:**

**Print out required modules:**

pip freeze

**Python virtual environment info:**

Super useful for isolating dependencies when building a container and managing Python modules in general. Highly recommended! When you create a virtual environment in your project directory and activate it, any pip packages you install will only be available to that specific environment — they won’t affect other projects or the system Python.

You can test this by running pip freeze before activating the environment, then activating your venv and running pip freeze again. You should see that the installed packages are isolated. It helps if you already have some pip packages installed before you try this, so you can clearly see the difference.

**Create a virtual environment:**

python3 -m venv venv
source venv/bin/activate
deactivate - (when not using)

**Note:**

**A venv with all the requirements need**

**to be present in the project directory**

**with the output from all freeze commands**

**in requirements.txt and installed in the**

**venv using the pip install <package> command.**



