from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/events")
def get_events():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM events"))
        events = [dict(row._mapping) for row in result]
    return {"events": events}

@app.get("/events/{event_id}/hotels")
def get_hotels(event_id: int):
    with engine.connect() as conn:
        # 経度(lon)と緯度(lat)を直接SELECT
        event_row = conn.execute(text(
            "SELECT *, ST_X(location::geometry) as lon, ST_Y(location::geometry) as lat FROM events WHERE id=:id"
        ), {"id": event_id}).first()
        if not event_row:
            return {"hotels": []}
        event = event_row._mapping
        sql = """
            SELECT *, ST_X(location::geometry) as lon, ST_Y(location::geometry) as lat FROM hotels
            WHERE ST_DWithin(
              location,
              ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
              1000
            )
        """
        hotels = conn.execute(
            text(sql),
            {"lon": event["lon"], "lat": event["lat"]}
        )
        hotels = [dict(row._mapping) for row in hotels]
    return {"hotels": hotels}