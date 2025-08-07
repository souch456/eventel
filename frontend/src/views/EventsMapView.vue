<template>
  <div class="eventel-main">
    <header>
      <h1>Eventel - イベント連動型ホテル検索</h1>
    </header>
    <div class="selector-header">
      <EventSelector @event-selected="onSelect" />
    </div>
    <div
      class="map-main-layout"
      :class="{ mobile: isMobile }"
    >
      <MapDisplay
        :eventId="selectedEventId"
        @hotel-selected="onHotelSelect"
        class="gmap-mobile-fixed"
      />
      <HotelDetailBottomSheet
        v-if="isMobile && selectedHotelNo"
        :hotelNo="selectedHotelNo"
        :eventDate="eventDetail?.date"
        :open="!!selectedHotelNo"
        @close="selectedHotelNo = null"
      />
      <HotelDetailPanel
        v-if="!isMobile && selectedHotelNo"
        :hotelNo="selectedHotelNo"
        :eventDate="eventDetail?.date"
      />
    </div>
    <footer>
      &copy; 2025 Eventel. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import EventSelector from "../components/EventSelector.vue";
import MapDisplay from "../components/MapDisplay.vue";
import HotelDetailPanel from "../components/HotelDetailPanel.vue";
import HotelDetailBottomSheet from "../components/HotelDetailBottomSheet.vue";
import { fetchEventDetail } from "../api/api.js";

const selectedEventId = ref(null);
const selectedHotelNo = ref(null);
const eventDetail = ref(null);

// デバイス幅でスマホ判定
const isMobile = ref(false);
function handleResize() {
  isMobile.value = window.innerWidth < 900;
}
onMounted(() => {
  handleResize();
  window.addEventListener("resize", handleResize);
});
watch(selectedEventId, async (id) => {
  if (!id) return;
  eventDetail.value = await fetchEventDetail(id);
  selectedHotelNo.value = null;
});
function onSelect(id) {
  selectedEventId.value = id;
}
function onHotelSelect(hotelNo) {
  selectedHotelNo.value = hotelNo;
}
</script>

<style scoped>
header {
  background: linear-gradient(90deg, #2196f3 0%, #1976d2 100%);
  color: #fff;
  padding: 1.2em 0;
  text-align: center;
  box-shadow: 0 2px 10px #0002;
  width: 100vw;
}
header h1 {
  font-size: 1.28em;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
  overflow-x: auto;
  text-overflow: ellipsis;
  letter-spacing: 0.04em;
}
.eventel-main {
  min-height: 100vh;
  width: 100vw;
  background: #f6f8fa;
  overflow-x: hidden;
}
.selector-header {
  background: #fff;
  padding: 0.5em 1em;
  border-bottom: 1px solid #e3e9f0;
}
.map-main-layout {
  display: flex;
  flex-direction: row;
  height: calc(100vh - 56px - 56px); /* ヘッダー＋セレクタ高さ(仮) */
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}
.gmap-mobile-fixed {
  flex: 3 1 0%;
  min-width: 350px;
  min-height: 420px;
  max-width: 1000px;
  height: 100%;
}
.map-main-layout.mobile {
  flex-direction: column;
  height: calc(100vh - 56px - 56px);
}
footer {
  width: 100vw;
  background: #e3e9f0;
  color: #555;
  text-align: center;
  padding: 0.6em 0;
  font-size: 0.93em;
  border-top: 1px solid #d4dae2;
  position: relative;
  bottom: 0;
}
@media (max-width: 900px) {
  .eventel-main {
    width: 100vw;
    min-width: 0;
    box-sizing: border-box;
    overflow-x: hidden;
  }
  .map-main-layout {
    display: flex;
    flex-direction: column;
    width: 100vw;
    max-width: 100vw;
    min-width: 0;
    height: auto;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
  }
  .gmap-mobile-fixed {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 0 !important;
    height: 350px !important;      /* ここは必要に応じて auto, min/max-height にしてもOK */
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    border-radius: 0 !important;
  }
  .selector-header, .selector-card {
    width: 100vw;
    max-width: 100vw;
    min-width: 0;
    box-sizing: border-box;
    margin: 0;
    padding-left: 0.5em;
    padding-right: 0.5em;
  }
  header h1 {
    font-size: 1.05em;
    padding: 0 0.5em;
  }
  footer {
    font-size: 0.85em;
    padding: 0.5em 0;
  }
}
</style>