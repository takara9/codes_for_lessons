# Ingress コントローラー+ Keepalived の動作確認補足


ここではマスターノードからkubectl を実行して動作を確認する例を提示します。

~~~
vagrant@master:~$ git clone https://github.com/takara9/codes_for_lessons
~~~


## Ingress Controller + Keepalived のマニフェスト適用

~~~
vagrant@master:~/codes_for_lessons/step13$ kubectl apply -f ingress-keepalived/
namespace/tkr-system created
configmap/nginx-configuration created
configmap/tcp-services created
configmap/udp-services created
deployment.apps/nginx-ingress-controller created
service/nginx-ingress-svc created
deployment.extensions/default-http-backend created
service/default-http-backend created
serviceaccount/nginx-ingress-serviceaccount created
clusterrolebinding.rbac.authorization.k8s.io/nginx-ingress-clusterrole-nisa-binding created
configmap/vip-configmap created
daemonset.extensions/kube-keepalived-vip created
serviceaccount/kube-keepalived-vip created
clusterrole.rbac.authorization.k8s.io/kube-keepalived-vip created
clusterrolebinding.rbac.authorization.k8s.io/kube-keepalived-vip created
~~~

## 起動までの待ち状態と起動完了状態

~~~
vagrant@master:~/codes_for_lessons/step13$ kubectl get pod -n tkr-system -w
NAME                                        READY   STATUS              RESTARTS   AGE
default-http-backend-675897b6d8-kpl4v       0/1     ContainerCreating   0          13s
kube-keepalived-vip-cdm9g                   0/1     ContainerCreating   0          12s
kube-keepalived-vip-hxr4v                   0/1     ContainerCreating   0          12s
nginx-ingress-controller-797f965f47-lhwnl   0/1     ContainerCreating   0          13s
kube-keepalived-vip-cdm9g                   1/1     Running             0          13s
kube-keepalived-vip-cdm9g                   0/1     Completed           0          20s
kube-keepalived-vip-cdm9g                   1/1     Running             1          22s
nginx-ingress-controller-797f965f47-lhwnl   1/1     Running             0          29s
kube-keepalived-vip-cdm9g                   0/1     Completed           1          28s
default-http-backend-675897b6d8-kpl4v       1/1     Running             0          32s
kube-keepalived-vip-hxr4v                   1/1     Running             0          41s
kube-keepalived-vip-cdm9g                   0/1     CrashLoopBackOff    1          43s
kube-keepalived-vip-cdm9g                   1/1     Running             2          44s
^C

vagrant@master:~/codes_for_lessons/step13$ kubectl get pod -n tkr-system 
NAME                                        READY   STATUS    RESTARTS   AGE
default-http-backend-675897b6d8-kpl4v       1/1     Running   0          15m
kube-keepalived-vip-cdm9g                   1/1     Running   2          15m
kube-keepalived-vip-hxr4v                   1/1     Running   0          15m
nginx-ingress-controller-797f965f47-lhwnl   1/1     Running   0          15m
~~~

## Ingressを利用したアプリケーションの起動

~~~
vagrant@master:~/codes_for_lessons/step13$ kubectl apply -f test-apl/
deployment.apps/hello-world-deployment created
service/hello-world-svc created
ingress.extensions/hello-world-ingress created
~~~

## アプリケーションの動作確認

~~~
vagrant@master:~/codes_for_lessons/step13$ kubectl get ing
NAME                  HOSTS            ADDRESS   PORTS   AGE
hello-world-ingress   abc.sample.com             80      4s

vagrant@master:~/codes_for_lessons/step13$ kubectl get pod
NAME                                    READY   STATUS              RESTARTS   AGE
hello-world-deployment-88fd567c-h497j   0/1     ContainerCreating   0          8s
hello-world-deployment-88fd567c-kd455   0/1     ContainerCreating   0          8s
hello-world-deployment-88fd567c-mwg2b   0/1     ContainerCreating   0          8s
hello-world-deployment-88fd567c-s74rz   0/1     ContainerCreating   0          8s
hello-world-deployment-88fd567c-x9ttx   0/1     ContainerCreating   0          8s

vagrant@master:~/codes_for_lessons/step13$ kubectl get pod
NAME                                    READY   STATUS    RESTARTS   AGE
hello-world-deployment-88fd567c-h497j   1/1     Running   0          66s
hello-world-deployment-88fd567c-kd455   1/1     Running   0          66s
hello-world-deployment-88fd567c-mwg2b   1/1     Running   0          66s
hello-world-deployment-88fd567c-s74rz   1/1     Running   0          66s
hello-world-deployment-88fd567c-x9ttx   1/1     Running   0          66s
~~~


## curlコマンドによるアクセステスト

DNSやhostsに登録する事なく、curlのヘッダーにドメイン名を設定する事で、Ingress の判定をパスする事ができる。

~~~
vagrant@master:~$ curl --header "Host: abc.sample.com" http://172.16.20.99/
<html><head><title>HTTP Hello World</title></head><body><h1>Hello from hello-world-deployment-88fd567c-h497j</h1></body></html
~~~


## 注意

このマニフェストは、K8s 1.14 を確認していますが、将来のバージョンで動作する保証はありません。