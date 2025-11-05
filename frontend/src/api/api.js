import axios from "axios";

const DEFAULT_API_BASE_URL = "http://localhost:8000";
const BASE_URL = import.meta.env?.VITE_API_BASE_URL || DEFAULT_API_BASE_URL;

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
