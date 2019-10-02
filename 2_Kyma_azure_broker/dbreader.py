#!/usr/bin/env python
import base64
import os
import ssl
import sys
import urllib3
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
from kubernetes import client, config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def base64_decode_dict(data):
    for k, v in data.items():
        data[k] = base64.b64decode(v).decode("utf-8")
    return data

def get_binding_secret(namespace, binding_secret_name):
    config.load_kube_config(os.environ['KUBECONFIG'])
    v1 = client.CoreV1Api()
    #  in case of self-signed
    v1.api_client.rest_client.pool_manager.connection_pool_kw['cert_reqs'] = ssl.CERT_NONE
    secrets = v1.list_namespaced_secret(namespace, watch=False)
    for item in secrets.items:
        if item.metadata.name == binding_secret_name:
            return base64_decode_dict(item.data)


namespace = sys.argv[1]
binding_secret_name = sys.argv[2]
binding_secret = get_binding_secret(namespace, binding_secret_name)


dbclient = cosmos_client.CosmosClient(url_connection=binding_secret['documentdb_host_endpoint'], auth={
                                    'masterKey': binding_secret['documentdb_master_key']})

database_link = 'dbs/' + binding_secret['databaseName']
db = dbclient.ReadDatabase(database_link)
print('Database with id \'{0}\' found'.format(binding_secret['databaseName']))


# Create container options
options = {
    'offerThroughput': 400
}

container_definition = {
    'id': "Demo"
}

# Create a container
try:
    container = dbclient.CreateContainer(db['_self'], container_definition, options)
    print('Container {0} created'.format(container_definition['id']))
    collection_link = database_link + '/colls/' + container_definition['id']
    dbclient.CreateItem(collection_link, { "id": "update", "time": "Not updated" })
    print('Initial item created')
except errors.HTTPFailure as e:
    if e.status_code == 409:
        print('A collection with id \'{0}\' already exists'.format(container_definition['id']))
        container_link = database_link + '/colls/{0}'.format(container_definition['id'])
        container = dbclient.ReadContainer(container_link)
    else:
        raise


# # Query update
query = {'query': 'SELECT * FROM u'}
options = {}
options['maxItemCount'] = 1

result_iterable = dbclient.QueryItems(container['_self'], query, options)
for item in iter(result_iterable):
    print(item['time'])
