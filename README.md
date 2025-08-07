# Eventel(イベント連携型ホテル検索サービス)


## セットアップ


```bash
git clone <このリポジトリ>
cd eventel/frontend
npm create vue@latest .
cd ..
docker compose up
```

立ち上がったら
フロント: http://localhost:5173/
バックエンド: http://localhost:8000/docs

で確認可能

デプロイ方法
```bash
npm run build
firebase deploy --only hosting
```