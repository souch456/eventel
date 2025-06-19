<template>
  <div class="event-map-layout">
    <!-- イベント選択 -->
    <EventSelector @event-selected="onSelect" />

    <!-- マップと詳細表示を横並びで -->
    <div class="main-content">
      <MapDisplay
        :eventId="selectedEventId"
        @hotel-selected="onHotelSelect"
      />
      <HotelDetailPanel
        v-if="selectedHotelNo"
        :hotelNo="selectedHotelNo"
        :eventDate="eventDetail?.date"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import EventSelector from "../components/EventSelector.vue";
import MapDisplay from "../components/MapDisplay.vue";
import HotelDetailPanel from "../components/HotelDetailPanel.vue";
import { fetchEventDetail } from "../api/api.js";

const selectedEventId = ref(null);
const selectedHotelNo = ref(null);
const eventDetail = ref(null);

function onSelect(id) {
  selectedEventId.value = id;
}

function onHotelSelect(hotelNo) {
  selectedHotelNo.value = hotelNo;
}

// イベント選択で詳細も再取得
watch(selectedEventId, async (id) => {
  if (!id) return;
  eventDetail.value = await fetchEventDetail(id);
});
</script>
<style scoped>
.event-map-layout {
  display: flex;
  flex-direction: column;
  gap: 1.5em;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2vw;
}

.main-content {
  display: flex;
  flex-direction: row;
  gap: 2em;
  width: 100%;
  min-height: 600px;
  align-items: flex-start;
}

.main-content > *:first-child {
  /* マップエリアは幅大きめ・高さ十分に */
  flex: 3 1 0%;
  min-width: 400px;
  min-height: 600px;
  max-width: 1000px;
  /* 必要ならカード背景は外す */
  background: none;
}

.main-content > *:last-child {
  /* 詳細パネルは狭め */
  flex: 1 1 0%;
  max-width: 420px;
  min-width: 280px;
}

/* EventSelectorも幅いっぱいにせず中央上部に */
.event-map-layout > *:first-child {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 1em;
}

/* モバイルは縦並び */
@media (max-width: 900px) {
  .main-content {
    flex-direction: column;
    gap: 1.2em;
    min-height: unset;
  }
  .main-content > *:first-child,
  .main-content > *:last-child {
    flex: none;
    max-width: 100%;
    min-width: 0;
    min-height: 320px;
  }
}

</style>