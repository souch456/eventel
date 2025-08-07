<template>
  <div
    class="hotel-detail-bottomsheet"
    v-if="open"
    @click.self="$emit('close')"
  >
    <div class="drag-handle"></div>
    <HotelDetailPanel
      :hotelNo="hotelNo"
      :eventDate="eventDate"
    />
    <button class="close-btn" @click="$emit('close')">閉じる</button>
  </div>
</template>

<script setup>
import HotelDetailPanel from "./HotelDetailPanel.vue";
defineProps({
  hotelNo: Number,
  eventDate: String,
  open: Boolean
});
const emit = defineEmits(['close']);
</script>

<style scoped>
.hotel-detail-bottomsheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 36vh;
  max-height: 430px;
  min-height: 220px;
  background: #fff;
  box-shadow: 0 -2px 16px #1976d222;
  border-radius: 1.2em 1.2em 0 0;
  overflow-y: auto;
  z-index: 10;
  transition: transform 0.23s;
  padding-bottom: 2em;
}
.drag-handle {
  width: 40px;
  height: 6px;
  background: #bbb;
  border-radius: 3px;
  margin: 10px auto 10px auto;
}
.close-btn {
  position: absolute;
  right: 24px;
  bottom: 18px;
  border: none;
  background: #eee;
  color: #444;
  font-size: 1em;
  border-radius: 1em;
  padding: 0.6em 1.2em;
}
</style>
