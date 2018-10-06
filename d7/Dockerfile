# ベースイメージ
FROM ubuntu

# 前提パッケージのインストール
RUN apt-get update && apt-get install -y gnupg2 curl

# Node.jsのインストール
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - 
RUN apt-get install nodejs -y 

# Node.jsのアプリのディレクトリをコンテナへコピー
ADD ./myapp/ /myapp

# 環境変数
ENV NODE_ENV development

# 公開用ポート
EXPOSE 3000

# コンテナの起動時に実行されるコマンド
CMD ["node", "/myapp/bin/www"] 

