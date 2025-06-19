<script setup>
import { ref, watch } from "vue";
import { nextTick } from "vue";
import { fetchEventDetail, fetchHotels } from "../api/api.js";
const props = defineProps({ eventId: Number });
const eventDetail = ref(null);
const hotels = ref([]);
const openEventInfo = ref(true);
// どのホテルのInfoWindowを開くか
const openHotelIndex = ref(null);

const emit = defineEmits(['hotel-selected']);

function onMarkerClick(idx) {
  if (openHotelIndex.value === idx) {
    openHotelIndex.value = null;
    nextTick(() => {
      openHotelIndex.value = idx;
    });
  } else {
    openHotelIndex.value = idx;
  }
}

function onEventMarkerClick() {
  if (openEventInfo.value) {
    openEventInfo.value = false;
    nextTick(() => {
      openEventInfo.value = true;
    });
  } else {
    openEventInfo.value = true;
  }
}

function onHotelMarkerClick(idx, hotelNo) {
  openHotelIndex.value = idx;
  // 必要に応じてemit
  // $emitが未定義の場合は defineEmits で定義
  emit('hotel-selected', hotelNo);
}

watch(
  () => props.eventId,
  async (newVal) => {
    if (!newVal) return;
    eventDetail.value = await fetchEventDetail(newVal);
    hotels.value = await fetchHotels(newVal);
    openHotelIndex.value = null; // イベント変更時は閉じる
  },
  { immediate: true }
);
</script>

<template>
  <div v-if="eventDetail" class="map-container">
    <GMapMap
      :center="{ lat: eventDetail.lat, lng: eventDetail.lon }"
      :zoom="14"
      style="width: 100%; height: 520px; border-radius: 1em; box-shadow: 0 4px 24px #1976d211;"
    >
      <!-- イベントピン（常時表示） -->
      <GMapMarker
        :position="{ lat: eventDetail.lat, lng: eventDetail.lon }"
        :clickable="true"
        :draggable="false"
        label="E"
        @click="onEventMarkerClick"
      >
        <GMapInfoWindow :opened="openEventInfo" @closeclick="openEventInfo = false">
          <div>
            <strong>{{ eventDetail.name }}</strong><br/>
            {{ eventDetail.address }}
          </div>
        </GMapInfoWindow>
      </GMapMarker>

      <!-- ホテルピン（クリック時のみInfoWindowを表示） -->
      <GMapMarker
        v-for="(hotel, idx) in hotels"
        :key="hotel.hotelNo"
        :position="{ lat: Number(hotel.latitude), lng: Number(hotel.longitude) }"
        :clickable="true"
        @click="onHotelMarkerClick(idx, hotel.hotelNo)"
      >
        <GMapInfoWindow :opened="openHotelIndex === idx" @closeclick="openHotelIndex = null">
          <div style="min-width:150px;">
            <b>{{ hotel.hotelName }}</b><br>
            <a :href="hotel.hotelInformationUrl" target="_blank">詳細</a><br>
            料金: {{ hotel.hotelMinCharge ? hotel.hotelMinCharge + '円~' : '不明' }}
          </div>
        </GMapInfoWindow>
      </GMapMarker>
    </GMapMap>
  </div>
</template>

<style scoped>
.map-container {
  width: 100%;
  margin: 0 auto;
  margin-bottom: 2em;
  min-height: 520px;
}
</style>
