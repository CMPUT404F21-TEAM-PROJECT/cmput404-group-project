<h1>Deployment Guide</h1>

<h2>Starting Project on the Virtual Machines using Docker</h2>

After pulling the latest version of our code, navigate to the deploy folder and make sure that you have docker installed on the virtual machine. \
If docker is not installed, you may need to run \
<b>sudo snap install docker</b> \
Now you will have to build the Docker images using the Dockerfiles and this can be done via \
<b>docker-compose build</b> \
If you get a permission denied error, you will need to either re-run the command using sudo or add the current user to the docker group with
```
sudo addgroup --system docker
sudo adduser $USER docker
// Restart the VM and you should now be able to run docker commands without sudo
```
To run the project: \
<b>docker-compose up</b> \
within the deploy directory to start the project locally on your machine. \
Default Access Ports: \
<b>Front End:</b> Port 80 or just <b>localhost</b> \
<b>Server:</b> Port 8000 or <b>localhost:8000</b>
