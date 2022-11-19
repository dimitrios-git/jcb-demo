# JCB Demo
## The task
Deploy a Python/Flask application on Docker and use Ansible to manage the
configuration. The app shall be modified to accept the sample size as a
variable and that variable should be set using Ansible.

## Notes on my implementation
I used to Docker and docker compose to create a couple of containers. The first
one is running an Nginx websever, with a custom configuration to serve the app's
output at `/data`.
A second container contains the Python app, which is altered to use the Gunicorn
server instead of the development server. Additionally, the app's code is
altered to read the $SAMPLE_SIZE environmental variable and plot the graph based
on the value.

Next steps:
Convert this to Ansible.
