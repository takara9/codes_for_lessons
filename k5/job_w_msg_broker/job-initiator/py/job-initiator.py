#!/usr/bin/env python
# -*- coding:utf-8 -*-

#from os import path
import yaml
import pika
from kubernetes import client, config

OBJECT_NAME = "pngen"
qname = 'taskqueue'

# メッセージ・ブローカーと接続
def create_queue():
    qmgr_cred= pika.PlainCredentials('guest', 'guest')
    #qmgr_host='172.16.20.11'  # for vagrant-k8s
    qmgr_host='192.168.99.100' # for minikube
    qmgr_port='31672'
    qmgr_pram = pika.ConnectionParameters(
    	      host=qmgr_host,
	      port=qmgr_port,
	      credentials=qmgr_cred)
    conn = pika.BlockingConnection(qmgr_pram)
    chnl = conn.channel()
    chnl.queue_declare(queue=qname)
    return chnl

# ジョブのマニフェスト作成
def create_job_manifest(n_job, n_node):
    container = client.V1Container(
        name="pn-generator",
        image="maho/pn_generator:0.7",
        env=[
            client.V1EnvVar(name="BROKER_URL",value="amqp://guest:guest@taskqueue:5672"),
            client.V1EnvVar(name="QUEUE",value="taskqueue")
        ]
    )
    template = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(containers=[container],
                              restart_policy="Never"                              
        ))
    spec = client.V1JobSpec(
        backoff_limit=4,
        template=template,
        completions=n_job,
        parallelism=n_node)
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=OBJECT_NAME),
        spec=spec)
    return job


if __name__ == '__main__':

    # 素数計算の分割パラメータ
    job_parms = [[1,1000],[1001,2000],[2001,2000],[3001,4000]]
    jobs  = len(job_parms)
    nodes = 2

    # キューへの書き込み
    queue = create_queue()
    for param_n in job_parms:
        param = str(param_n).replace('[','').replace(']','')
        queue.basic_publish(exchange='',routing_key=qname,body=param)

    # kubectlの.kubeを読んでk8sマスタへ、ジョブ・リクエストを送信
    config.load_kube_config()
    client.BatchV1Api().create_namespaced_job(
        body=create_job_manifest(jobs,nodes),namespace="default")
