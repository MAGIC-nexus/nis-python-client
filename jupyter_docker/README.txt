Extracted from the Dockerfile:

Build image:

cd <this Dockerfile directory>
docker build -t magic-jupyter .

Test run:

docker run -it --rm -p 8000:8000 -v /home/myuser/docker/jupyterhub:/home magic-jupyter
Open browser: "http://localhost:8000"

At Magic Server:

docker create --network=magic-net --name magic-jupyterhub -v /srv/docker/magic/data/jupyter:/home magic-jupyter
docker start magic-jupyterhub
