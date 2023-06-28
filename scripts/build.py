from pathlib import Path
from frictionless import Package, Schema, transform, steps
from datetime import datetime
import typer

def main(descriptor: str, output_path: Path):
    package = Package(descriptor)
    package.custom['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    for resource in package.resources:
        schema = Schema.describe(resource.path)
        resource.schema = schema
        resource.infer(stats=True)

        resource = transform(resource, 
                             steps=[
                                 steps.resource_update(name = resource.name, 
                                                       descriptor = {'path': f'{resource.name}.csv'})
                             ])

    package.to_json(Path(output_path, 'datapackage.json'))
    
if __name__ == '__main__':
    typer.run(main)