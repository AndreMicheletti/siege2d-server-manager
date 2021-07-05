import os
from kubernetes import client, config
from kubernetes.client import ApiException
from pprint import pprint

#######################################
## How to get credentials for K8S API
# https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/
#######################################
## Agones CRD API Reference.
# https://agones.dev/site/docs/reference/agones_crd_api_reference/
#######################################

CLUSTER_HOST = os.getenv("CLUSTER_HOST")
CLUSTER_TOKEN = os.getenv("CLUSTER_TOKEN")

def get_available_game_servers_ordered() -> list:
  api_client = get_client_from_token()
  game_servers = list_game_servers(api_client)
  if game_servers:
    available = [
      {
        **gs["status"],
        "port": gs["status"]["ports"][0]["port"]
      } for gs in game_servers["items"] if gs["status"]["state"] == "Ready"
    ]
    pprint(available)
    return list(sorted(available, key=lambda x: x["port"]))
  else:
    return []

def list_game_servers(api_client: client.ApiClient) -> list:
    # Create an instance of the API class
    api_instance = client.CustomObjectsApi(api_client)
    group = "agones.dev"
    version = "v1"
    plural = "gameservers"
    name = "gameservers.agones.dev"

    try:
      return api_instance.list_cluster_custom_object(group, version, plural, watch=False)			
    except ApiException as e:
      print("Exception when calling CustomObjectsApi->list_cluster_custom_object: %s\n" % e)
      return None

def get_client_from_config():
  config.load_kube_config(context="minikube")
  return client.ApiClient()

def get_client_from_token():
    token = CLUSTER_TOKEN
    cluster_config = client.Configuration()
    cluster_config.host = CLUSTER_HOST
    cluster_config.verify_ssl = False
    cluster_config.api_key = {"authorization": "Bearer " + token}
    return client.ApiClient(cluster_config)
