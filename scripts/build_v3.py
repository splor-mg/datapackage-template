import yaml
import copy
from rich import print_json

def normalize_package(descriptor):
    result = copy.deepcopy(descriptor)

    for resource in result['resources']:
        # map of old names to new names for lookups
        mapping = {}
        
        # update fields
        for field in resource['schema']['fields']:
            # if title exists, switch title and name
            if 'title' in field:
                field['name'], field['title'] = field['title'], field['name']
                mapping[field['title']] = field['name']

            # keep only the specified properties
            for key in list(field.keys()):
                if key not in ['name', 'title', 'description', 'constraints', 'notes', 'example']:
                    del field[key]
                    
        # update primary keys if necessary
        if 'primaryKey' in resource['schema']:
            for i, key in enumerate(resource['schema']['primaryKey']):
                if key in mapping:
                    resource['schema']['primaryKey'][i] = mapping[key]

        # update foreign keys if necessary
        if 'foreignKeys' in resource['schema']:
            for fk in resource['schema']['foreignKeys']:
                for i, field in enumerate(fk['fields']):
                    if field in mapping:
                        fk['fields'][i] = mapping[field]

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