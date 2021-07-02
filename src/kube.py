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

LOCAL_API = "https://192.168.49.2:8443"
LOCAL_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNyZl9Xck5pNG1MOUNtR3dvNkdQaUV0WFp6Mm5ySVViVFBPc2xuZXdJaTQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tZmxwZjYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjU4NzdkMjI0LTgzNDYtNDBmNi04OGNkLTcwYjgwNTc0ZGYxNCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.G93spJdRoUU_rKRh0-1dQBcLo01cPmgVZjoMXn_9uHAAy5kAJVfqzsxJJR0Yq1Do1EhNkEhH0Mx2XVgm6w6ZSgrYGo5RQtA_9j52tZsO_BKgUgTIdX0B9ZXpoZvei8rJ_Ox_ifGYweOuJVNAUG9zRZ26t_8um3KpCixDY2wFatkUN_o_AjUTc-24uWj9srPjEdHKf7Wop97TVf9qiu-Uq-5TWEObDyI7TIuIJUqUBFu2G4PDo4qeqQA8BLOHvWwgC9hx0FafaeDFy8ghU3FeCaIdiPj82Tgb5p9MFqRGcSsPp7dBWwnrbrGlby1MLkvYREFaIDIvZWwE7lD5H_YPKA"

def list_game_servers() -> list:
	config.load_kube_config(context="minikube")
	v1 = client.CoreV1Api()

	with client.ApiClient() as api_client:
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

def get_available_game_servers_ordered() -> list:
	game_servers = list_game_servers()
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

def list_pods_from_env():
    # Define the bearer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    token = LOCAL_TOKEN

    # Create a configuration object
    cluster_config = client.Configuration()

    # Specify the endpoint of your Kube cluster
    cluster_config.host = LOCAL_API

    # Security part.
    # In this simple example we are not going to verify the SSL certificate of
    # the remote cluster (for simplicity reason)
    cluster_config.verify_ssl = False
    # Nevertheless if you want to do it you can with these 2 parameters
    # configuration.verify_ssl=True
    # ssl_ca_cert is the filepath to the file that contains the certificate.
    # configuration.ssl_ca_cert="certificate"

    cluster_config.api_key = {"authorization": "Bearer " + token}

    # Create a ApiClient with our config
    cluster_client = client.ApiClient(cluster_config)

    # Do calls
    v1 = client.CoreV1Api(cluster_client)
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
