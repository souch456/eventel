<template>
  <div class="event-map-layout">
  <!-- イベント選択 -->
  <EventSelector @event-selected="onSelect" />

  <!-- マップと詳細表示 -->
  <div
    class="main-content"
    :class="{ 'single': !selectedHotelNo }"
  >
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
.main-content {
  display: flex;
  flex-direction: row;
  gap: 2em;
  width: 100%;
  min-height: 600px;
  align-items: flex-start;
  transition: all 0.2s;
}

/* パネルがないときは中央寄せ＆広く */
.main-content.single {
  justify-content: center;
}

.main-content > *:first-child {
  flex: 3 1 0%;
  min-width: 400px;
  min-height: 600px;
  max-width: 1000px;
  background: none;
}

.main-content.single > *:first-child {
  flex: none;
  max-width: 680px; /* ここで大きめに中央寄せ */
  min-width: 420px;
}

.main-content > *:last-child {
  flex: 1 1 0%;
  max-width: 420px;
  min-width: 280px;
}

@media (max-width: 900px) {
  .main-content,
  .main-content.single {
    flex-direction: column;
    gap: 1.2em;
    min-height: unset;
    justify-content: flex-start;
    align-items: stretch;
  }
  .main-content > *:first-child,
  .main-content > *:last-child {
    flex: none;
    max-width: 100%;
    min-width: 0;
    min-height: 320px;
  }
  .main-content.single > *:first-child {
    max-width: 100%;
    min-width: 0;
  }
}


</style>