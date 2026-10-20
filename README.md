# 図書館貸出管理アプリ

Flask 2.3.2 / Python 3.10 を使用した図書・利用者・貸出管理アプリです。『Flask本格入門』のルーティング・Jinja2・Blueprint・フォーム・バリデーション・ORM・認証・PRGパターンに沿う構成です。提供されたPDFは第5章途中（150ページ）までで、それ以降の構成は教科書の目次と既存コードに基づいています。

## 起動（Docker Compose）

1. `.env.example` を `.env` にコピーし、SECRET_KEY、ADMIN_PASSWORD を必ず変更する。
2. `docker compose up --build -d`
3. `http://localhost:5000/books` を開く。管理画面には環境変数の管理者アカウントでログインする。

データは `library_data` volume に永続化されます。サンプルデータが必要なときだけ SEED_DEMO_DATA=1 を指定してください。

## Docker Swarm

`LIBRARY_IMAGE` に各Swarmノードからpull可能なレジストリイメージを設定して `docker stack deploy -c docker-stack.yml library` を実行してください。ローカルイメージだけでは別ノードへの配置に失敗します。SQLiteのため単一レプリカで運用し、同一ボリュームが配置先ノードに存在することを確認してください。SECRET_KEYとADMIN_PASSWORDは環境変数に平文で渡されるため、本番ではSecretsによる管理を推奨します。

## ローカル開発

Python 3.10 の仮想環境で `pip install -r requirements.txt`、SECRET_KEYとADMIN_PASSWORDを設定し、`python init_db.py`、`flask --app app run` で起動します。
