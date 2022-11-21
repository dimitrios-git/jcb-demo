# JCB Demo
## The task
Deploy a Python/Flask application on Docker and use Ansible to manage the
configuration. The app shall be modified to accept the sample size as a
variable and that variable should be set using Ansible.

## Notes on my implementation
I used Docker and docker compose to create a couple of containers. The first
one is running an Nginx websever, with a custom configuration to serve the app's
output at `/data`.

A second container contains the Python app, which is altered to use the Gunicorn
server instead of the development server. Additionally, the app's code is
altered to read the `$SAMPLE_SIZE` environmental variable and plot the graph based
on that value.

While trying to go from `docker compose` to `ansible-playbook`, I decided to go step by
step. Ansible is able to not only control Docker, but also build containers.
Therefore, it makes sense to get rid of `docker compose` at first and in the
next step get rid of `Dockerfile`s as well.

Using the `Dockerfile`s the images for the two containers are created:
```
docker build -t jcb_demo-app app/
docker build -t jcb_demo-nginx nginx/
```

For the configuration to work we need both containers to be in the same network,
usually `docker compose` takes care of that, but without it I shall create it
manually:

```
docker network create jcb_demo-network
```

Now that the network is created, I can use it to start the app container first,
since the second one depends on it.

```
docker run -d -p 8000:80 -e SAMPLE_SIZE=1000 --network jcb_demo-network
--net-alias=app --name jcb_demo-app_cotainer jcb_demo-app
```
| parameter     | explanation
|:------------- | :---
| `-d`          | Runs the container detached aka in the background
| `-p 8000:80`  | Forwards port 8000 of the container to port 80 of the localhost
| `-e`          | Set environment variable
| `--network`   | Add the container to a network
| `--net-alias` | Set the hostname of the container
| `name`        | Set the name of the container

The app container is now up and running, so let's start the Nginx container, too:
```
docker run -d -p 80:80 --network jcb_demo-network --name
jcb_demo-nginx_container jcb_demo-nginx
```
The setup should be ready now.

Another thing to take into account is that without `docker compose`, stopping
and removing the containers and the network will not be automated. Instead, I
must do it manually:
```
docker stop jcb_demo-nginx
docker stop jcb_demo-app
docker rm jcb_demo-nginx
docker rm jcb_demo-app
docker network rm jcb_demo network
```
With the docker commands laid down, I will now try to use Ansible to:
- [x] Start the configuration, [`ansible-run.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-run.yml)
- [x] Stop and clean, [`ansible-compose-down.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-compose-down.yml)
- [x] Build images, so that we can get rid of the `Dockerfile`s, too. [`ansible-build-app.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-build-app.yml) [`ansible-build-nginx.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-build-nginx.yml)

With all the pieces in place, I tried to replicate the functionality of `docker
compose`, and I created the
[`ansible-compose-up.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-compose-up.yml)
and [`ansible-compose-down.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-compose-down.yml). The [`ansible-compose-down.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-compose-down.yml) 
cleans up the system by stopping the two containers and removing them along with the
network. The [`ansible-compose-up.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-compose-up.yml) consists of three separate ansible playbooks:
1. [`ansible-build-app.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-build-app.yml) which builds the app image,
2. [`ansible-build-nginx.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-build-nginx.yml) which builds the nginx image,
3. [`ansible-build-nginx.yml`](https://github.com/dscharalampidis/jcb-demo/blob/main/ansible-build-nginx.yml) which starts the containers.

All ansible playbooks can be run separately as stand-alone playbooks. It must be
noted that they lack error handling, and therefore, running them twice will
produce errors, but I believe that error handling is out of the scope of this
project.



 
