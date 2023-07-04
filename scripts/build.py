from pathlib import Path
from frictionless import Package, Schema, transform, steps
from datetime import datetime
import json
import typer

def main(output_path: Path, descriptor: str = 'datapackage.yaml'):
    package = Package(descriptor)
    
    output_descriptor = {
        "profile": "tabular-data-package",
        "name": package.name,
        "resources": [
            {
            "profile": "tabular-data-resource",
            "name": resource_name,
            "path": f'data/{resource_name}.csv',
            "format": "csv",
            "encoding": "utf-8",
            "schema": {"fields": []}
            } for resource_name in package.resource_names
        ]
    }
    
    output = Package.from_descriptor(output_descriptor)
    output.custom['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    for resource in output.resources:
        schema = Schema.describe(resource.path)
        resource.schema = schema
        resource.infer(stats=True)

        resource = transform(resource, 
                             steps=[
                                 steps.resource_update(name = resource.name, 
                                                       descriptor = {'path': f'{resource.name}.csv'})
                             ])

    output.to_json(Path(output_path, 'datapackage.json'))
    
if __name__ == '__main__':
    typer.run(main)