# coding: UTF-8
#
# 状態不明ノードをクラスタから削除する
#
import signal, os, sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from time import sleep

uk_node = {}  # KEYは状態不明になったノード名、値は不明状態カウント数

## 停止要求シグナル処理
def handler(signum, frame):
    sys.exit(0)

## ノード削除 関数
def node_delete(v1,name):
    body = client.V1DeleteOptions()
    try:
        resp = v1.delete_node(name, body)
        print("delete node %s done" % name)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_node: %s\n" % e)

## ノード監視 関数
def node_monitor(v1):
    try:
        ret = v1.list_node(watch=False)
        for i in ret.items:
            n_name = i.metadata.name
            #print("%s" % (i.metadata.name)) #デバック用
            for j in i.status.conditions:
                #print("\t%s\t%s" % (j.type, j.status)) #デバック用
                if (j.type == "Ready" and j.status != "True"):
                    if n_name in uk_node:
                        uk_node[n_name] += 1
                    else:
                        uk_node[n_name] = 0
                    print("unknown %s  count=%d" % (n_name,uk_node[n_name]))
                    # カウンタが3回超えるとノードを削除
                    if uk_node[n_name] > 3:
                        del uk_node[n_name]
                        node_delete(v1,i.metadata.name)
                # 1回でも状態が戻るとカウンタリセット
                if (j.type == "Ready" and j.status == "True"):
                    if n_name in uk_node:
                        del uk_node[n_name]
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_node: %s\n" % e)

## メイン        
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handler) # シグナル処理
    config.load_incluster_config()         # 認証情報の取得
    v1 = client.CoreV1Api()                # インスタンス化
    # 監視ループ 
    while True:
        node_monitor(v1)
        sleep(5) # 監視の間隔時間

