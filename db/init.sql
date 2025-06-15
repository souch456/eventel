CREATE EXTENSION IF NOT EXISTS postgis;

-- サンプルテーブル
CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  date DATE,
  address VARCHAR(255),
  location GEOGRAPHY(POINT, 4326)
);

CREATE TABLE hotels (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  address VARCHAR(255),
  location GEOGRAPHY(POINT, 4326),
  url VARCHAR(255)
);


-- ダミーイベントデータ
INSERT INTO events (name, date, address, location) VALUES
  ('隅田川花火大会', '2025-07-27', '東京都台東区花川戸1丁目1', ST_SetSRID(ST_MakePoint(139.7985, 35.7101), 4326)),
  ('東京湾大華火祭', '2025-08-12', '東京都中央区晴海5丁目', ST_SetSRID(ST_MakePoint(139.7742, 35.6496), 4326));

-- ダミーホテルデータ
INSERT INTO hotels (name, address, location, url) VALUES
  ('ホテルリバーサイド浅草', '東京都台東区駒形1-1-1', ST_SetSRID(ST_MakePoint(139.7970, 35.7085), 4326), 'https://example.com/hotel1'),
  ('ホテル東京スカイビュー', '東京都墨田区業平1-2-2', ST_SetSRID(ST_MakePoint(139.8107, 35.7100), 4326), 'https://example.com/hotel2'),
  ('晴海ホテル', '東京都中央区晴海4-7-3', ST_SetSRID(ST_MakePoint(139.7725, 35.6520), 4326), 'https://example.com/hotel3'),
  ('銀座ラグジュアリーホテル', '東京都中央区銀座7-9-10', ST_SetSRID(ST_MakePoint(139.7637, 35.6674), 4326), 'https://example.com/hotel4');