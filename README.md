# 演習用のサンプルコード

このリポジトリは、[15Stepで習得 Dockerから入るKubernetes コンテナ開発からK8s本番運用まで (StepUp!選書)](https://amzn.to/2mgCRya)に掲載した演習用のサンプルコードです。

## 本書の章立てとの対応づけ

ディレクトリのStep番号で対応づけています。内容によってコマンドだけで完結するのでサンプルコードのないStepもあります。

### 2章 コンテナ開発を習得する5ステップ
* Step01 コンテナ最初の一歩 (サンプルコードなし）
* Step02 コンテナの操作 (サンプルコードなし）
* Step03 コンテナ開発
* Step04 コンテナとネットワーク
* Step05 コンテナAPI

### 3章 K8s実践活用のための10ステップ
* Step06 Kubernetes最初の一歩 (サンプルコードなし）
* Step07 マニフェストとポッド
* Step08 デプロイメント
* Step09 サービス
* Step10 ジョブとクーロンジョブ
* Step11 ストレージ
* Step12 ステートフルセット
* Step13 イングレス
* Step14 オートスケール
* Step15 クラスタの仮想化


## 実行環境

IKSやGKEといったパブリッククラウドの環境でも動作します。また、読者自身のパソコン環境にVirtualBox と Vagrant で仮想環境をセットアップすれば、自分だけの学習環境も構築できます。

* Minikube https://github.com/takara9/vagrant-minikube 
* オリジナルのKubernetesクラスタ https://github.com/takara9/vagrant-kubernetes

Kubernetes環境と組み合わせて利用できる永続ストレージです。

* NFSサーバー 一般的NFSサーバーをコンテナからマウントする環境 https://github.com/takara9/vagrant-nfs
* GlusterFSサーバー + Heketi の動的プロビジョニング環境 https://github.com/takara9/vagrant-glusterfs


どうぞ、Docker や Kubernetes をお楽しみください。





