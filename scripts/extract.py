from frictionless import Package, Resource
import requests
from bs4 import BeautifulSoup
import csv
import logging
import typer

logger = logging.getLogger(__name__)

def extract(resource_name, descriptor):
    package = Package(descriptor)
    resource = package.get_resource(resource_name)

    with Resource(resource.sources[0]) as source:
        logger.info('Geração de Arquivos Texto...')
        res = requests.get(source.custom['link']) # Resource is stripping url property
        logger.info('Fim geração de Arquivos Texto...')
        res.raise_for_status()
        if 'gerado com sucesso!' not in res.text:
            raise Exception
        
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()
        logger.info(text)

        with open(resource.path, 'w', newline='') as fs:
            writer = csv.writer(fs)
            writer.writerow(resource.schema.field_names)
            for row in source.row_stream:
                writer.writerow(row.to_list())

def main(resource_name: str, descriptor: str = 'datapackage.yaml'):
    extract(resource_name, descriptor)

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
    logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
    typer.run(main)