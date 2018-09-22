from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint
from time import sleep

uk_node = {}

def node_delete(v1,name):
    body = client.V1DeleteOptions()
    try:
        resp = v1.delete_node(name, body)
        print("delete node %s done" % name)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_node: %s\n" % e)

def node_monitor(v1):
    try:
        ret = v1.list_node(watch=False)
        for i in ret.items:
            n_name = i.metadata.name
            #print("%s" % (i.metadata.name))
            for j in i.status.conditions:
                #print("\t%s\t%s" % (j.type, j.status))
                if (j.type == "Ready" and j.status != "True"):
                    if n_name in uk_node:
                        uk_node[n_name] += 1
                    else:
                        uk_node[n_name] = 0
                    print("unknown %s  count=%d" % (n_name,uk_node[n_name]))
                    if uk_node[n_name] > 5:
                        del uk_node[n_name]
                        node_delete(v1,i.metadata.name)

                if (j.type == "Ready" and j.status == "True"):
                    if n_name in uk_node:
                        del uk_node[n_name]
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_node: %s\n" % e)

        
if __name__ == '__main__':
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    while True:
        node_monitor(v1)
        sleep(3)

