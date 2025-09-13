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

**I am not going to cover the docker install:**

Follow the instructions for your specific distro or environment

**Build image -run from project directory, where Dockerfile is:**

docker build -t flask-docker-demo .

**Build image from specific Dockerfile:**

docker build -t img -f other.Dockerfile .

**Run docker file in detached mode:**

docker rund -d flask-docker-demo

**Slightly enhanced command:**

docker run -d --name flask-1 -p 5000:5000 flask-docker-demo

**Full Command:**

docker run -d --name flask-1 -p 5000:5000 -v $(pwd)/instance:/app/instance -v $(pwd)/logs:/logs flask-docker-demo

**Extra parameters for added functionality:**

-p 5000:5000   *expose the correct port, the former reroutes port 5000, 5001:5000 == 127.0.0.1:5001*
-v $(pwd)/instance:/app/instance  *persist the db*
-v $(pwd)/logs:/app/logs  *persist the logs*
--name flask-demo   *rename, goes right before the img name, at end*

*This is just an example, I wont touch these today*
--cpus="0.5"  *limit cpu to 1/2*
--memory="256m"   *limit memory to 256mb*

**Example of running a second identical container (to first)- note the port, naming convention:**

docker run -d --name flask-demo-2 flask-docker-demo

**Verify the image is running:**

docker ps

**If it is not on the list, run this:**

docker ps -a

**Stop a container:**

docker stop container id/name

**Remove a stopped container:**

docker rm container id/name

**Remover all stopped containers:**

docker container prune

**Remover everything**

docker system prune -a

**Other useful commands:**

**Docker Login**

docker login -u username

**Prepare img for upload**

docker tag img username/desired_img_name/ver *like 0.0.1*

**Push to docker hub**

docker push username/desired_img_name/ver *matches ver above*

**Access a bash console from the image**

docker exec --interactive --tty d90d

**Loop to remove all docker images, modular**

docker ps -aq | xargs docker rmi server_name *run other commands replacing post xargs*

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

**A venv with all the requirements need to be present in the project directory with the output from all freeze commands in requirements.txt and installed in the venv using the pip install <package> command.**



