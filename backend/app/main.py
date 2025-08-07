from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from datetime import timedelta, datetime
from fastapi import Body
from fastapi.responses import JSONResponse

load_dotenv()

# 許可するオリジンのリスト
origins = [
    "http://localhost:5173",   # Vite(前端)のURL
    # 本番の場合は↓を追加
    "https://eventel-a6e78.web.app",
    "https://192.168.0.119:5173"
    # "https://your-production-url.com",
]

# DATABASE_URL = os.environ['DATABASE_URL']
# engine = create_engine(DATABASE_URL)

DATABASE_URL = "sqlite:///./test.db"  # SQLite用
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

RAKUTEN_APP_ID = os.getenv("APP_ID")
RAKUTEN_AFFILIATE_ID = os.getenv("affiliateId")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # 上記リストにあるオリジンだけ許可
    allow_credentials=True,
    allow_methods=["*"],                  # 全てのHTTPメソッドを許可
    allow_headers=["*"],                  # 全てのHTTPヘッダーを許可
)

@app.get("/events")
def get_events():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM events"))
        events = [dict(row._mapping) for row in result]
    return {"events": events}

@app.get("/events/{event_id}")
def get_event(event_id: int):
    with engine.connect() as conn:
        # row = conn.execute(text("""
        #     SELECT id, name, date, address,
        #            ST_X(location::geometry) as lon,
        #            ST_Y(location::geometry) as lat
        #     FROM events
        #     WHERE id=:id
        # """), {"id": event_id}).first()
        row = conn.execute(text("""
            SELECT id, name, date, address, lat, lon
            FROM events
            WHERE id=:id
        """), {"id": event_id}).first()
        if not row:
            return {"event": None}
        d = dict(row._mapping)
        # locationカラムは返さず、lat/lonとして返す
        return {"event": {
            "id": d["id"],
            "name": d["name"],
            "date": d["date"],
            "address": d["address"],
            "lat": d["lat"],
            "lon": d["lon"],
        }}

@app.get("/events/{event_id}/hotels")
def get_hotels(event_id: int):
    with engine.connect() as conn:
        # DBからイベントの緯度・経度を取得
        # event_row = conn.execute(text(
        #     "SELECT ST_X(location::geometry) as lon, ST_Y(location::geometry) as lat FROM events WHERE id=:id"
        # ), {"id": event_id}).first()
        event_row = conn.execute(text(
            "SELECT lon, lat FROM events WHERE id=:id"
        ), {"id": event_id}).first()
        if not event_row:
            return {"hotels": []}
        event = event_row._mapping
        lon = event["lon"]
        lat = event["lat"]

    # 楽天APIのリクエストURLを生成
    url = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426"
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "format": "json",
        "datumType": 1,            # 世界測地系、単位は度
        "latitude": lat,
        "longitude": lon,
        "searchRadius": 2,         # 1km圏内
        "hits": 20,                # 最大10件だけ取得
        "formatVersion": 2,        # レスポンスを配列で
        "responseType": "middle",  # 中くらいの情報量
    }
    # API呼び出し
    resp = requests.get(url, params=params)
    data = resp.json()

    # ホテル情報を整形して返す（必要なら抜粋/整形）
    hotels = []
    for hotel_info in data.get("hotels", []):
        # もしhotel_infoがlist型なら中身を取得
        if isinstance(hotel_info, list):
            hotel_info = hotel_info[0]
        basic = hotel_info.get("hotelBasicInfo", {})
        hotels.append({
            "hotelNo": basic.get("hotelNo"),
            "hotelName": basic.get("hotelName"),
            "hotelInformationUrl": basic.get("hotelInformationUrl"),
            "hotelMinCharge": basic.get("hotelMinCharge"),
            "latitude": basic.get("latitude"),
            "longitude": basic.get("longitude"),
            "address1": basic.get("address1"),
            "address2": basic.get("address2"),
            "hotelThumbnailUrl": basic.get("hotelThumbnailUrl"),
            "reviewAverage": basic.get("reviewAverage"),
            "reviewCount": basic.get("reviewCount"),
        })
    return {"hotels": hotels}

@app.get("/vacant-hotels")
def search_vacant_hotels(
    hotelNo: int = Query(..., description="楽天トラベルのホテルID"),
    checkinDate: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}", description="チェックイン日 (YYYY-MM-DD)"),
    checkoutDate: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}", description="チェックアウト日 (YYYY-MM-DD)"),
    adultNum: int = Query(1, ge=1, le=99, description="大人の人数"),
    roomNum: int = Query(1, ge=1, le=10, description="部屋数"),
):
    url = "https://app.rakuten.co.jp/services/api/Travel/VacantHotelSearch/20170426"
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "format": "json",
        "hotelNo": hotelNo,
        "checkinDate": checkinDate,
        "checkoutDate": checkoutDate,
        "adultNum": adultNum,
        "roomNum": roomNum,
        "datumType": 1,
        "formatVersion": 2,
        "responseType": "middle",
        "hits": 10
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    
    hotels = []
    for hotel_info in data.get("hotels", []):
        if isinstance(hotel_info, list):
            hotel_info = hotel_info[0]
        basic = hotel_info.get("hotelBasicInfo", {})
        hotels.append({
            "hotelNo": basic.get("hotelNo"),
            "hotelName": basic.get("hotelName"),
            "hotelInformationUrl": basic.get("hotelInformationUrl"),
            "hotelMinCharge": basic.get("hotelMinCharge"),
            "latitude": basic.get("latitude"),
            "longitude": basic.get("longitude"),
            "address1": basic.get("address1"),
            "address2": basic.get("address2"),
            "hotelThumbnailUrl": basic.get("hotelThumbnailUrl"),
            "reviewAverage": basic.get("reviewAverage"),
            "reviewCount": basic.get("reviewCount"),
            "planListUrl": basic.get("planListUrl"),
            "access": basic.get("access"),
        })
    return {
        "hotels": hotels,
        "raw": data  # 必要に応じてレスポンス本体も返却
    }

@app.post("/vacant-status")
def vacant_status(
    req: dict = Body(...)
):
    """
    req = {
        "hotelNos": [111, 222, ...],
        "checkinDate": "2025-08-10",
        "checkoutDate": "2025-08-11",
        "adultNum": 1,
        "roomNum": 1
    }
    """
    # print(req)
    hotelNos = req.get("hotelNos", [])
    checkinDate = req.get("checkinDate")
    checkoutDate = req.get("checkoutDate")
    adultNum = req.get("adultNum", 1)
    roomNum = req.get("roomNum", 1)
    result = []

    url = "https://app.rakuten.co.jp/services/api/Travel/VacantHotelSearch/20170426"

    for hotelNo in hotelNos:
        params = {
            "applicationId": RAKUTEN_APP_ID,
            "affiliateId": RAKUTEN_AFFILIATE_ID,
            "format": "json",
            "hotelNo": hotelNo,
            "checkinDate": checkinDate,
            "checkoutDate": checkoutDate,
            "adultNum": adultNum,
            "roomNum": roomNum,
            "datumType": 1,
            "formatVersion": 2,
            "hits": 1
        }
        try:
            resp = requests.get(url, params=params, timeout=4)
            data = resp.json()
            is_vacant = bool(data.get("hotels"))
        except Exception as e:
            is_vacant = False  # 取得失敗時は空きなし扱い
        result.append({"hotelNo": hotelNo, "isVacant": is_vacant})
    # print(result)
    return JSONResponse({"results": result})