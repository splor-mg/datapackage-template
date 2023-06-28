from frictionless import Package, Pipeline, steps, transform
import petl as etl
import csv
import logging
import typer
from pathlib import Path
import csv

logger = logging.getLogger(__name__)

def transform_resource(resource_name: str, descriptor: str = 'datapackage.yaml'):
    logger.info(f'Transforming resource {resource_name}')
    package = Package(descriptor)
    resource = package.get_resource(resource_name)
    target = transform(resource, steps=[steps.table_normalize()])
    table = target.to_petl()
    for field in resource.schema.fields:
        if field.title:
            table = etl.rename(table, field.name, field.title)
    etl.tocsv(table, Path(f'build/{resource_name}.csv'), encoding='utf-8')

if __name__ == '__main__':
    typer.run(transform_resource)
