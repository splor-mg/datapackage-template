FROM rocker/r-ver:4.2.3

WORKDIR /project

RUN /rocker_scripts/install_python.sh

COPY requirements.txt .
COPY DESCRIPTION .

RUN python -m pip install -r requirements.txt
RUN Rscript -e "install.packages('renv')" && Rscript -e 'renv::install()'
