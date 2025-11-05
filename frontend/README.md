# Eventel Frontend

Eventel のフロントエンドは Vue 3 + Vite で構築されており、イベント会場と周辺ホテルを Google Maps で表示する SPA です。

## 必要要件
- Node.js 20 以上
- npm 10 以上
- Google Maps JavaScript API キー
- バックエンド API（FastAPI）が起動済みであること

## 環境変数
`.env.example` をベースに `.env` を作成してください。

| 変数名 | 説明 | 例 |
| --- | --- | --- |
| `VITE_GOOGLE_MAPS_API_KEY` | Google Maps JavaScript API キー | `VITE_GOOGLE_MAPS_API_KEY=xxxx` |
| `VITE_API_BASE_URL` | FastAPI サーバーのベース URL | `VITE_API_BASE_URL=http://localhost:8000` |

Google Cloud Console で Maps JavaScript API を有効化し、課金設定済みのプロジェクトで API キーを発行してください。キーが未設定の場合はアプリ内で警告が表示され、地図は読み込まれません。

## セットアップ
```bash
npm install
```

## 開発サーバーの起動
```bash
npm run dev
```
- Vite の開発サーバーが http://localhost:5173 で立ち上がります。
- `.env` を変更した場合はサーバーを再起動してください。

## ビルド
```bash
npm run build
```
成果物は `dist/` に出力されます。ビルドのみ実行したい場合は `npm run build-only` を使用します。

## 型チェック
```bash
npm run type-check
```

## 主な依存ライブラリ
- `vue` / `vue-router` : SPA 構築
- `@fawmi/vue-google-maps` : Google Maps 表示
- `axios` : バックエンド API 呼び出し

## API ベース URL の変更
`src/api/api.js` では `VITE_API_BASE_URL` を参照しています。Docker Compose など別ドメインで公開する場合は `.env` を更新し再起動してください。
