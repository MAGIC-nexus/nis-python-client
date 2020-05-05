# cd <this Dockerfile directory>
# docker build -t magic-jupyter .
# Test run:
# docker run -it --rm -p 8000:8000 -v /home/myuser/docker/jupyterhub:/home magic-jupyter
# Open browser: "http://localhost:8000"
#
# At Magic Server:
# docker create --network=magic-net --name magic-jupyterhub
#    -v /srv/docker/magic/data/jupyter:/home
#    magic-jupyter
# docker start magic-jupyterhub
#
FROM debian:10.3

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Update and install Debian packages
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 libspatialindex-dev \
    git mercurial subversion

# Install CONDA
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
#    wget --quiet https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh -O ~/anaconda.sh && \
#    wget --quiet https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh -O ~/anaconda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

# "init" for Docker containers
RUN apt-get install -y curl grep sed dpkg vim && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

RUN conda install -c conda-forge mpld3 && \
#    conda install -c conda-forge jupyterlab==0.35.2 && \
    conda install -c r r-irkernel && \
    conda install -c r r-essentials && \
    conda install -c r rpy2

RUN pip install --upgrade pip && \
#    pip install jupyterlab && \
    pip install npm webdavclient && \
    jupyter serverextension enable --py jupyterlab

RUN conda install -c plotly plotly && \
#    conda install -c conda-forge jupyterhub && \
    conda update jupyter_core jupyter_client

RUN apt-get install -y software-properties-common gnupg

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs && \
#    jupyter labextension install @jupyterlab/hub-extension && \
    pip install mapboxgl fiona folium geocoder geopandas geopy googlemaps pyproj pysal rtree shapely telluric


# For dashboards, each kernel should run: jupyter nbextension enable jupyter_dashboards --py --sys-prefix
#RUN conda install -c r rpy2

RUN pip install jupyter_dashboards && jupyter dashboards quick-setup --sys-prefix && \
    pip install ipywidgets && \
    jupyter nbextension enable --py --sys-prefix widgetsnbextension && \
#    jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38 && \
#    pip install ipysankeywidget && jupyter nbextension enable --py --sys-prefix ipysankeywidget && \
    pip install ipyleaflet && jupyter labextension install jupyter-leaflet && \
#    jupyter labextension install @jupyterlab/geojson-extension && \  ## INCOMPATIBLE WITH JUPYTERLAB_PYVIZ
    jupyter labextension install @jupyterlab/plotly-extension

RUN conda install -c bokeh bokeh && \
    jupyter labextension install jupyterlab_bokeh && \
    conda install -c conda-forge holoviews && \
    jupyter labextension install @pyviz/jupyterlab_pyviz && \
    pip install py_d3 altair vega_datasets && \
    pip install bqplot && jupyter labextension install bqplot && \
    jupyter labextension install cy-jupyterlab && \
    pip install ipysigma && \
    jupyter nbextension enable --py --sys-prefix ipysigma && \
    jupyter labextension install ipysigma

RUN conda install -c conda-forge cartopy
RUN pip install pivottablejs

RUN pip install ipylab && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager ipylab
#RUN conda install -c conda-forge ipylab

RUN pip install nexinfosys-client

ADD users.csv /root/users.csv
ADD create_users.py /root/create_users.py
ADD init_script.sh /root/init_script.sh
ADD jupyterhub_config.py /root/jupyterhub_config.py
RUN ["chmod", "+x", "/root/init_script.sh"]

ENTRYPOINT [ "/usr/bin/tini", "--" ]
#CMD [ "/bin/bash" ]
EXPOSE 8000
CMD ["/root/init_script.sh"]
#CMD ["jupyter", "notebook", "--port=8000", "--no-browser", "--allow-root", "--ip=0.0.0.0"]
