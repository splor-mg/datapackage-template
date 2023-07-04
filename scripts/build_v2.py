from frictionless import Package
from rich import print_json

package = Package('datapackage.yaml')

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
        "schema": {"fields": [
            {
             'name': field.title if field.title else field.name,
             'type': field.type
            } for field in package.get_resource(resource_name).schema.fields
        ]}
        } for resource_name in package.resource_names
    ]
}

print_json(data = output_descriptor)

Package.from_descriptor(output_descriptor).to_json('data.json')
