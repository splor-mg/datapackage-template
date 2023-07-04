import yaml
import copy
from rich import print_json

def normalize_package(descriptor):
    result = copy.deepcopy(descriptor)
    result['profile'] = 'tabular-data-package'
    for resource in result['resources']:
        
        # keep only the specified properties
        for key in list(resource.keys()):
            if key not in ['name', 'title', 'description', 'schema']:
                del resource[key]
        
        resource['path'] = f'data/{resource["name"]}.csv'
        resource['format'] = 'csv'
        resource['encoding'] = 'utf-8'
        resource['profile'] = 'tabular-data-resource'
        
        # map of old names to new names for lookups
        field_mapping = {}
        
        schema = resource['schema']

        # update fields
        for field in schema['fields']:
            # if title exists, switch title and name
            if 'title' in field:
                field['name'], field['title'] = field['title'], field['name']
                field_mapping[field['title']] = field['name']

            # keep only the specified properties
            for key in list(field.keys()):
                if key not in ['name', 'title', 'description', 'constraints', 'notes', 'example']:
                    del field[key]
                    
        # update primary keys if necessary
        if 'primaryKey' in schema:
            for i, key in enumerate(schema['primaryKey']):
                if key in field_mapping:
                    schema['primaryKey'][i] = field_mapping[key]

        # update foreign keys if necessary
        if 'foreignKeys' in schema:
            for fk in schema['foreignKeys']:
                for i, field in enumerate(fk['fields']):
                    if field in field_mapping:
                        fk['fields'][i] = field_mapping[field]

                # Fetch the resource specified in fk['reference']['resource']
                ref_resource = next((r for r in descriptor['resources'] if r['name'] == fk['reference']['resource']), None)
                if ref_resource is not None:
                    # Generate a map for this resource
                    ref_mapping = {f['name']: f['title'] for f in ref_resource['schema']['fields'] if 'title' in f}
                    for i, field in enumerate(fk['reference']['fields']):
                        if field in ref_mapping:
                            fk['reference']['fields'][i] = ref_mapping[field]

    return result



with open('data.yaml', 'r') as file:
    data = yaml.safe_load(file)

result = normalize_package(data)
print_json(data = result)