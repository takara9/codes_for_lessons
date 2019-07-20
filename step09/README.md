# Step09 サービスの本文に記述できなかった補足です。


## ExtenalName 外部DNS名のアドレス解決の例

v1.13以降では、extenalNameにIPアドレスを記述できますが、DNS名の文字列として扱われます。
そのため、マニフェストに、DNS名を書いてアクセスする必要があります。


実行例 svc-ext-dns.yml

~~~
$ kubectl apply -f svc-ext-dns.yml
service/yahoo created

$ kubectl get svc
NAME         TYPE           CLUSTER-IP   EXTERNAL-IP       PORT(S)   AGE
kubernetes   ClusterIP      10.96.0.1    <none>            443/TCP   5d2h
yahoo        ExternalName   <none>       www.yahoo.co.jp   <none>    15s

$ kubectl run -it bustbox --restart=Never --rm --image=busybox sh
If you don't see a command prompt, try pressing enter.
/ # ping yahoo
PING yahoo (183.79.217.124): 56 data bytes
64 bytes from 183.79.217.124: seq=0 ttl=61 time=16.367 ms
64 bytes from 183.79.217.124: seq=1 ttl=61 time=16.493 ms
64 bytes from 183.79.217.124: seq=2 ttl=61 time=16.939 ms
64 bytes from 183.79.217.124: seq=3 ttl=61 time=16.449 ms
^C
--- yahoo ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 16.367/16.562/16.939 ms
~~~



## ヘッドレスにIPアドレスをハードコードする例 

ヘッドレスサービスとエンドポイントを svc-headless.yml で作成します。
ポイントは、Endpoint のマニフェストを作成して、その中にIPアドレスを
ハードコードすること、オブジェクト名は、サービスとエンドポイントで
一致していることです。


実行例 svc-headless.yml

~~~
$ kubectl apply -f svc-headless.yml
endpoints/server1 created
service/server1 created

$ kubectl get svc
NAME         TYPE           CLUSTER-IP   EXTERNAL-IP       PORT(S)   AGE
server1      ClusterIP      None         <none>            <none>    7s

$ kubectl get ep
NAME         ENDPOINTS             AGE
server1      192.168.1.16          13s

$ kubectl run -it busybox --restart=Never --rm --image=busybox sh
If you don't see a command prompt, try pressing enter.
/ # ping server1
PING server1 (192.168.1.16): 56 data bytes
64 bytes from 192.168.1.16: seq=0 ttl=61 time=0.754 ms
64 bytes from 192.168.1.16: seq=1 ttl=61 time=0.905 ms
64 bytes from 192.168.1.16: seq=2 ttl=61 time=0.585 ms
^C
--- server1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.585/0.748/0.905 ms~
~~~

上記の例では、本件に関係ないものサービスは省略しています。

