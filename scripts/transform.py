from frictionless import Package, Resource, Dialect
import petl as etl
import logging
import typer

logger = logging.getLogger(__name__)

def transform(resource_name, descriptor):
    package = Package(descriptor)
    resource = package.get_resource(resource_name)
    logger.info(f'Transforming resource {resource.name}')
    source = Resource(resource.sources[0])
    table = source.to_petl()
    field_names = {field.title: field.name for field in resource.schema.fields}
    table = etl.rename(table, field_names)
    etl.tocsv(table, resource.path, encoding='utf-8')

def main(resource_name: str, descriptor: str = 'datapackage.yaml'):
    transform(resource_name, descriptor)

if __name__ == '__main__':
    typer.run(main)
