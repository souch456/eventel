# Eventel（イベント連携型ホテル検索サービス）

イベント会場周辺のホテルをマップ上で探せるフルスタックアプリケーションです。  
PostGIS で管理するイベントデータを FastAPI から提供し、Vue 3（Vite）製のフロントエンドで地図表示や空室検索を行います。

## 主な機能
- イベント一覧と会場位置の表示
- イベント周辺ホテルのマップ表示（Google Maps）
- 楽天トラベル API を用いた空室状況と料金プランの取得
- 空間検索に対応した PostgreSQL + PostGIS 構成

## 技術スタック
- Frontend: Vue 3, Vite, @fawmi/vue-google-maps, Axios
- Backend: FastAPI, SQLAlchemy, Requests
- Database: PostgreSQL 16 + PostGIS 3
- Infrastructure: Docker Compose

## リポジトリ構成
```
.
├── backend/          # FastAPI アプリケーション
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── db/               # 初期データ投入用 SQL（PostGIS 拡張を含む）
├── frontend/         # Vue 3 + Vite フロントエンド
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## 前提条件
- Docker / Docker Compose（推奨）
- 楽天トラベル API 用アプリケーション ID
- Google Maps JavaScript API キー
- （オプション）ローカル開発で Docker を使わない場合は Node.js 20 / Python 3.11

## 環境変数の設定
公開前に全てのシークレットを `.env` に移してください。サンプルは各ディレクトリの `.env.example` を参照します。

### backend/app/.env
| 変数名 | 説明 |
| --- | --- |
| `APP_ID` | 楽天アプリケーション ID（必須） |
| `affiliateId` | 楽天アフィリエイト ID（必要な場合のみ） |
| `DATABASE_URL` | SQLAlchemy 形式の接続文字列。Docker Compose 使用時は自動設定されるため省略可 |

### frontend/.env
| 変数名 | 説明 | 例 |
| --- | --- | --- |
| `VITE_GOOGLE_MAPS_API_KEY` | Google Maps JavaScript API キー | `VITE_GOOGLE_MAPS_API_KEY=xxxx` |
| `VITE_API_BASE_URL` | バックエンドの URL | `VITE_API_BASE_URL=http://localhost:8000` |

## クイックスタート（Docker Compose）
```bash
git clone <this-repository-url>
cd eventel

cp backend/app/.env.example backend/app/.env
cp frontend/.env.example frontend/.env
# ↑ 各ファイルを編集して API キーを設定

docker compose up --build
```

- Frontend: http://localhost:5173  
- Backend (OpenAPI docs): http://localhost:8000/docs  
- PostgreSQL: localhost:5432（ユーザー `eventuser` / パスワード `eventpass`）

初回起動時に `db/init.sql` が自動実行され、ダミーのイベント・ホテルデータが投入されます。

## 開発モードで個別起動する場合
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 主要な API エンドポイント
- `GET /events` : 登録済みイベント一覧
- `GET /events/{event_id}` : イベント詳細（地理座標含む）
- `GET /events/{event_id}/hotels` : 指定イベント周辺のホテル一覧
- `GET /events/{event_id}/vacant-hotels` : 空室状況付きホテル一覧（人数・部屋数などのクエリあり）
- `GET /vacant-hotels` : ホテル ID を指定した空室検索

Swagger UI（/docs）からパラメータを試しながら確認できます。

## データベース
- PostgreSQL + PostGIS 拡張を使用しています。
- `db/init.sql` でサンプルのイベント／ホテルデータと空間カラム（GEOGRAPHY）が作成されます。
- 追加データを投入する際は SRID 4326（WGS84 度単位）で位置情報を登録してください。

## テスト・整合性
- 現時点で自動テストは用意されていません。機能追加時には FastAPI のエンドポイントテストやフロントエンドのユニットテストの追加を推奨します。
- 楽天 API / Google Maps API キーの利用制限と課金設定には十分注意してください。

