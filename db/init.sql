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
  ('東京競馬場花火 2025', '2025-07-02', '東京都府中市日吉町１−１', ST_SetSRID(ST_MakePoint(139.4859855390394, 35.662631851104464), 4326)),
  ('第59回 葛飾納涼花火大会', '2025-07-22', '東京都葛飾区柴又７丁目', ST_SetSRID(ST_MakePoint(139.881399, 35.761287), 4326)),
  ('第48回 隅田川花火大会', '2025-07-26', '東京都台東区今戸１丁目１−１０', ST_SetSRID(ST_MakePoint(139.805884, 35.717591), 4326)),
  ('八王子花火大会', '2025-07-26', '東京都八王子市台町２丁目２', ST_SetSRID(ST_MakePoint(139.322779, 35.651149), 4326)),
  ('立川まつり 国営昭和記念公園花火大会', '2025-07-26', '東京都立川市緑町３１７３', ST_SetSRID(ST_MakePoint(139.39357735269218, 35.711951989443), 4326)),
  ('御蔵島花火大会', '2025-07-31', '東京都御蔵島村', ST_SetSRID(ST_MakePoint(139.589021, 33.897265), 4326)),
  ('第66回 いたばし花火大会', '2025-08-02', '東京都板橋区新河岸１丁目２５−１', ST_SetSRID(ST_MakePoint(139.665259, 35.798901), 4326)),
  ('第50回 江戸川区花火大会', '2025-08-02', '東京都江戸川区上篠崎１丁目', ST_SetSRID(ST_MakePoint(139.90312315195996, 35.718163236507884), 4326)),
  ('第32回 神津島 渚の花火大会', '2025-08-04', '東京都神津島村', ST_SetSRID(ST_MakePoint(139.1294354953103, 34.20969126635294), 4326)),
  ('奥多摩納涼花火大会', '2025-08-09', '東京都西多摩郡奥多摩町氷川', ST_SetSRID(ST_MakePoint(139.09666749330896, 35.80924415850971), 4326)),
  ('第24回 八丈島納涼花火大会', '2025-08-11', '東京都八丈町三根４１８４−１', ST_SetSRID(ST_MakePoint(139.81817538329537, 33.12273654235142), 4326)),
  ('神宮外苑花火大会', '2025-08-16', '東京都新宿区霞ヶ丘町１−１', ST_SetSRID(ST_MakePoint(139.7176951916521, 35.678735127489055), 4326)),
  ('第53回 昭島市民くじら祭 夢花火', '2025-08-23', '東京都昭島市東町５丁目１２', ST_SetSRID(ST_MakePoint(139.38703441647374, 35.70317905432196), 4326)),
  ('第40回 調布花火', '2025-09-20', '東京都調布市多摩川７丁目３８−１', ST_SetSRID(ST_MakePoint(139.5447581654588, 35.6405513418958), 4326)),
  ('第47回 世田谷区たまがわ花火大会', '2025-10-04', '東京都世田谷区鎌田１丁目１', ST_SetSRID(ST_MakePoint(139.620875, 35.613323), 4326));

-- ダミーホテルデータ
INSERT INTO hotels (name, address, location, url) VALUES
  ('ホテルリバーサイド浅草', '東京都台東区駒形1-1-1', ST_SetSRID(ST_MakePoint(139.7970, 35.7085), 4326), 'https://example.com/hotel1'),
  ('ホテル東京スカイビュー', '東京都墨田区業平1-2-2', ST_SetSRID(ST_MakePoint(139.8107, 35.7100), 4326), 'https://example.com/hotel2'),
  ('晴海ホテル', '東京都中央区晴海4-7-3', ST_SetSRID(ST_MakePoint(139.7725, 35.6520), 4326), 'https://example.com/hotel3'),
  ('銀座ラグジュアリーホテル', '東京都中央区銀座7-9-10', ST_SetSRID(ST_MakePoint(139.7637, 35.6674), 4326), 'https://example.com/hotel4');