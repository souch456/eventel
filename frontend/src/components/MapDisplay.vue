<script setup>
import { ref, watch } from "vue";
import { nextTick } from "vue";
import { fetchEventDetail, fetchHotels, fetchVacantStatus } from "../api/api.js";
const props = defineProps({ eventId: Number });
const eventDetail = ref(null);
const hotels = ref([]);
const openEventInfo = ref(true);
const eventIcon = "https://maps.google.com/mapfiles/ms/icons/orange-dot.png";
const vacantIcon = "https://maps.google.com/mapfiles/ms/icons/red-dot.png";
const defaultIcon = "https://maps.google.com/mapfiles/ms/icons/blue-dot.png";
const openHotelIndex = ref(null);
const loadingVacant = ref(false);

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
  emit('hotel-selected', hotelNo);
}

watch(
  () => props.eventId,
  async (newVal) => {
    if (!newVal) return;
    eventDetail.value = await fetchEventDetail(newVal);

    hotels.value = (await fetchHotels(newVal)).map(hotel => ({
      ...hotel,
      isVacant: null // 初期状態
    }));
    openHotelIndex.value = null;

    // 空室判定前にローディングON
    loadingVacant.value = true;

    const checkinDate = eventDetail.value?.date;
    const checkoutDate = (() => {
      const d = new Date(checkinDate);
      d.setDate(d.getDate() + 1);
      return d.toISOString().slice(0,10);
    })();
    const hotelNos = hotels.value.map(h => String(h.hotelNo));

    fetchVacantStatus({ hotelNos, checkinDate, checkoutDate }).then(vacantList => {
      const vacantMap = Object.fromEntries(vacantList.map(x => [String(x.hotelNo), x.isVacant]));
      hotels.value = hotels.value.map(hotel => ({
        ...hotel,
        isVacant: vacantMap[String(hotel.hotelNo)] ?? false
      }));
      // 空室判定後にローディングOFF
      loadingVacant.value = false;
    }).catch(() => {
      loadingVacant.value = false;
    });
  },
  { immediate: true }
);
</script>

<template>
  <div v-if="eventDetail" class="map-container">
    <!-- ローディングアイコン -->
    <div v-if="loadingVacant" class="vacant-loading">
      <span class="loader"></span> 空室判定中...
    </div>
    <GMapMap
      :center="{ lat: eventDetail.lat, lng: eventDetail.lon }"
      :zoom="14"
      style="width: 100%; height: 520px; border-radius: 1em; box-shadow: 0 4px 24px #1976d211;"
    >
      <!-- イベントピン -->
      <GMapMarker
        :position="{ lat: eventDetail.lat, lng: eventDetail.lon }"
        :clickable="true"
        :draggable="false"
        :icon="eventIcon"
        @click="onEventMarkerClick"
      >
        <GMapInfoWindow :opened="openEventInfo" @closeclick="openEventInfo = false">
          <div>
            <strong>{{ eventDetail.name }}</strong><br/>
            {{ eventDetail.address }}
          </div>
        </GMapInfoWindow>
      </GMapMarker>

      <!-- ホテルピン -->
      <GMapMarker
        v-for="(hotel, idx) in hotels"
        :key="hotel.hotelNo"
        :position="{ lat: Number(hotel.latitude), lng: Number(hotel.longitude) }"
        :icon="hotel.isVacant === true ? vacantIcon : defaultIcon"
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
      <!-- 判例（凡例）エリア -->
      <div class="legend">
        <div><img :src="vacantIcon" width="20" style="vertical-align:middle;"> 空室あり</div>
        <div><img :src="defaultIcon" width="20" style="vertical-align:middle;"> 空室なし/未判定</div>
        <div><img :src="eventIcon" width="20" style="vertical-align:middle;"> イベント会場</div>
      </div>
    </GMapMap>
  </div>
  <!-- <div style="background:#fff;margin:1em;padding:1em;">
    <div v-for="hotel in hotels" :key="hotel.hotelNo">
      {{ hotel.hotelNo }}: {{ hotel.hotelName }} | isVacant: {{ hotel.isVacant }}
    </div>
  </div> -->
</template>

<style scoped>
.map-container {
  width: 100%;
  margin: 0 auto;
  margin-bottom: 2em;
  min-height: 520px;
}

.vacant-loading {
  position: absolute;
  top: 18px;
  right: 36px;
  z-index: 10;
  background: rgba(255,255,255,0.97);
  border-radius: 1.5em;
  box-shadow: 0 2px 8px #1976d221;
  padding: 0.7em 1.3em;
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1em;
}

/* アニメーション付アイコン */
.loader {
  border: 2px solid #1976d2;
  border-top: 2px solid #ccc;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  margin-right: 8px;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
</style>
