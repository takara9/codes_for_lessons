## Step11 ストレージ 本文に対する補足

## HelmのセットアップとIBM Cloud Block Storage プラグインのインストール

IKSマニュアルでは解りにくいとの事で「Helm」のセットアップと「IBM Cloud Block Storage プラグイン」を実行した例を書いておきます。


1. K8sクラスタにTillerをインストール

~~~
$ kubectl apply -f https://raw.githubusercontent.com/IBM-Cloud/kube-samples/master/rbac/serviceaccount-tiller.yaml
~~~

2. Helmの初期化

~~~
$ helm init --service-account tiller --upgrade
~~~

3. チャートの追加

~~~
$ helm repo add iks-charts https://icr.io/helm/iks-charts
~~~

4. ブロックストレージのプラグイン インストール

~~~
$ helm install --name blkstg iks-charts/ibmcloud-block-storage-plugin
~~~


5. ストレージクラスの確認

ブロック・ストレージ・クラスの追加に成功すれば、次のようにリストされます。

~~~
$ kubectl get sc
NAME                         PROVISIONER         AGE
default                      ibm.io/ibmc-file    2d19h
ibmc-block-bronze            ibm.io/ibmc-block   9m26s
ibmc-block-custom            ibm.io/ibmc-block   9m26s
ibmc-block-gold              ibm.io/ibmc-block   9m26s
ibmc-block-retain-bronze     ibm.io/ibmc-block   9m26s
ibmc-block-retain-custom     ibm.io/ibmc-block   9m26s
ibmc-block-retain-gold       ibm.io/ibmc-block   9m26s
ibmc-block-retain-silver     ibm.io/ibmc-block   9m26s
ibmc-block-silver            ibm.io/ibmc-block   9m26s
ibmc-file-bronze (default)   ibm.io/ibmc-file    2d19h
ibmc-file-custom             ibm.io/ibmc-file    2d19h
ibmc-file-gold               ibm.io/ibmc-file    2d19h
ibmc-file-retain-bronze      ibm.io/ibmc-file    2d19h
ibmc-file-retain-custom      ibm.io/ibmc-file    2d19h
ibmc-file-retain-gold        ibm.io/ibmc-file    2d19h
ibmc-file-retain-silver      ibm.io/ibmc-file    2d19h
ibmc-file-silver             ibm.io/ibmc-file    2d19h
~~~



## IKS ブロックストレージへのアクセスは、単一ノード or 単一ポッド か？


実行例13 のK8sクラスタのワーカーノード数は２です。そのため、ContainerCreating で待機状態なったポッドが、同一ノードのポッドか、それとも、異なるノードにスケジュールされたものか解りません。

アクセスモード RMO(ReadWriteOnce)は「単一ノードの読み出しアクセスと書き込みアクセス」を意味しており、同一ノードのスケジュールされたポッドはストレージを利用できますが、異なるノードにスケジュールされたポッドはアクセスできないことになるはずです。

その事を確かめるためのマニフェスト deploy-3pod-single-node.yml を作成しました。この中で、nodeSelector を利用して一つのノードに集中してスケジュールします。

~~~file:deploy-3pod-single-node.yml抜粋
    spec:
      nodeSelector:
        kubernetes.io/hostname: 10.193.10.44  ## <<-- 自己の環境に合わせてラベルを変更
      containers:
      - image: ubuntu
~~~


このラベルを取得するコマンドは、`kubectl get no --show-labels`です。ノード名にプライベートIPアドレスが使われていて、2ノードあることがわかります。上記のnodeSelector の設定で、ノード名 10.193.10.44 にスケジュールされます。

~~~file:実行例
bash-3.2$ kubectl get no --show-labels
NAME           STATUS   ROLES    AGE    VERSION       LABELS
10.193.10.44   Ready    <none>   110d   v1.12.6+IKS   arch=amd64,beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=u2c.2x4.encrypted,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/region=jp-tok,failure-domain.beta.kubernetes.io/zone=tok05,ibm-cloud.kubernetes.io/encrypted-docker-data=true,ibm-cloud.kubernetes.io/ha-worker=true,ibm-cloud.kubernetes.io/iaas-provider=softlayer,ibm-cloud.kubernetes.io/machine-type=u2c.2x4.encrypted,ibm-cloud.kubernetes.io/os=UBUNTU_16_64,ibm-cloud.kubernetes.io/sgx-enabled=false,ibm-cloud.kubernetes.io/worker-pool-id=d5361e9e1b0e40e099ecd7fe02a71d64-185b835,ibm-cloud.kubernetes.io/worker-version=1.12.6_1547,kubernetes.io/hostname=10.193.10.44,privateVLAN=2445839,publicVLAN=2445837
10.193.10.7    Ready    <none>   110d   v1.12.6+IKS   arch=amd64,beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=u2c.2x4.encrypted,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/region=jp-tok,failure-domain.beta.kubernetes.io/zone=tok05,ibm-cloud.kubernetes.io/encrypted-docker-data=true,ibm-cloud.kubernetes.io/ha-worker=true,ibm-cloud.kubernetes.io/iaas-provider=softlayer,ibm-cloud.kubernetes.io/machine-type=u2c.2x4.encrypted,ibm-cloud.kubernetes.io/os=UBUNTU_16_64,ibm-cloud.kubernetes.io/sgx-enabled=false,ibm-cloud.kubernetes.io/worker-pool-id=d5361e9e1b0e40e099ecd7fe02a71d64-185b835,ibm-cloud.kubernetes.io/worker-version=1.12.6_1547,kubernetes.io/hostname=10.193.10.7,privateVLAN=2445839,publicVLAN=2445837
~~~


nodeSelectorの条件を編集して、デプロイします。

~~~file:実行例：一つのノードの3ポッドをデプロイ
$ kubectl apply -f deploy-3pod-single-node.yml
deployment.apps/dep3pod-blk created
~~~


実行結果の確認です。一つのノードの場合でも、1つのポッドだけしか実行できていません。

~~~file:実行例：ポッドの実行状態の確認
$ kubectl get po --selector='app=dep3pod-blk' -o wide
NAME                         READY STATUS            AGE   IP            NODE        
dep3pod-blk-6d7f5b8c49-6d7bw 1/1   Running           3m10s 172.30.55.146 10.193.10.44
dep3pod-blk-6d7f5b8c49-8hhrk 0/1   ContainerCreating 3m10s <none>        10.193.10.44
dep3pod-blk-6d7f5b8c49-lnzht 0/1   ContainerCreating 3m10s <none>        10.193.10.44
~~~


原因を確認します。


~~~file:実行例：ポッドのエラー表示
$ kubectl describe po dep3pod-blk-6d7f5b8c49-8hhrk
<中略>
Events:
  Type     Reason       Age                  From                   Message
  ----     ------       ----                 ----                   -------
  Normal   Scheduled    8m14s                default-scheduler      Successfully assigned default/dep3pod-blk-6d7f5b8c49-8hhrk to 10.193.10.44
  Warning  FailedMount  7m49s                kubelet, 10.193.10.44  MountVolume.SetUp failed for volume "pvc-d7bef1c3-ab72-11e9-a62d-8a0381bb8d07" : mount command failed, status: Failure, reason: Error while mounting the volume &errors.errorString{s:"RWO check has failed. DevicePath /var/data/kubelet/plugins/kubernetes.io/flexvolume/ibm/ibmc-block/mounts/pvc-d7bef1c3-ab72-11e9-a62d-8a0381bb8d07 is already mounted on mountpath /var/data/kubelet/pods/0e39f8c6-ab9b-11e9-bc03-7eb7daa184af/volumes/ibm~ibmc-block/pvc-d7bef1c3-ab72-11e9-a62d-8a0381bb8d07 "}
~~~

エラーメッセージから、すでに他のポッドがマウントしているためにマウントできないことが読み取れます。

"RWO check has failed. <省略>-8a0381bb8d07 is already mounted on mountpath <省略>"



## GKE ブロックストレージへのアクセス RWO は単一ノード単位

上記のマニフェストを少し変えて、GKEでも試してみました。
GKEでは、一つのノード上で、同じブロックストレージをマウントするポッドを複数立ち上げて動作することが確認できました。

~~~
$ kubectl apply -f deploy-3pod-single-node.yml
deployment.apps/dep3pod-blk created

$ kubectl get po -o wide
NAME                           READY STATUS  AGE IP        NODE                                
dep3pod-blk-7c579947df-hrcc7   1/1   Running 84m 10.8.0.17 gke-gke-1-default-pool-4b8e4604-t0lq
dep3pod-blk-7c579947df-p72n6   1/1   Running 84m 10.8.0.18 gke-gke-1-default-pool-4b8e4604-t0lq
dep3pod-blk-7c579947df-vvb47   1/1   Running 84m 10.8.0.16 gke-gke-1-default-pool-4b8e4604-t0lq
~~~




