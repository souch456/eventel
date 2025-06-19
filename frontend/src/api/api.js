import axios from "axios";
const BASE_URL = "http://localhost:8000"; // FastAPIサーバーURL

export async function fetchEvents() {
  const res = await axios.get(`${BASE_URL}/events`);
  return res.data.events;
}

export async function fetchEventDetail(eventId) {
  const res = await axios.get(`${BASE_URL}/events/${eventId}`);
  return res.data.event;
}

export async function fetchHotels(eventId) {
  const res = await axios.get(`${BASE_URL}/events/${eventId}/hotels`);
  return res.data.hotels;
}

export async function fetchVacantHotelDetail({ hotelNo, checkinDate, checkoutDate, adultNum, roomNum }) {
  const params = new URLSearchParams({
    hotelNo,
    checkinDate,
    checkoutDate,
    adultNum,
    roomNum,
  });
  const resp = await fetch(`${BASE_URL}/vacant-hotels?${params.toString()}`);
  return await resp.json();
}
