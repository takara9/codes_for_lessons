# minikube 利用時の問題回避方法

minikube の IPアドレスが、バージョンアップに伴って変更になっています。
これに伴いサンプルコード job-initiator.py ではminikube のIPアドレスを修正する必要があります。

以下の方法でIPアドレスを確認する事ができます。

~~~
$ minikube ip
192.168.64.2
~~~


修正箇所は、以下の部分です。

~~~
# メッセージ・ブローカーと接続
def create_queue():
    qmgr_cred= pika.PlainCredentials('guest', 'guest')
    #qmgr_host='172.16.20.11'  # for vagrant-k8s
    #qmgr_host='192.168.99.100' # for minikube old version
    qmgr_host='192.168.64.2' # for minikube latest version <<-- ここ
    qmgr_port='31672'
    qmgr_pram = pika.ConnectionParameters(
    	      host=qmgr_host,
	      port=qmgr_port,
~~~



以上、Kubernetesをお楽しみください！
