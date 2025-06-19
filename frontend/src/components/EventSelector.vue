<template>
  <div class="selector-card">
    <label for="evsel">イベント選択：</label>
    <select v-model="selectedId" @change="onChange" id="evsel">
      <option v-for="ev in events" :key="ev.id" :value="ev.id">{{ ev.name }}</option>
    </select>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { fetchEvents } from "../api/api.js";
const emit = defineEmits(["event-selected"]);
const events = ref([]);
const selectedId = ref(null);

onMounted(async () => {
  events.value = await fetchEvents();
  if (events.value.length) {
    selectedId.value = events.value[0].id;
    emit("event-selected", selectedId.value);
  }
});
function onChange() {
  emit("event-selected", selectedId.value);
}
</script>
<style scoped>
.selector-card {
  background: #fff;
  padding: 1em 1.2em;
  border-radius: 1em;
  box-shadow: 0 2px 12px #0001;
  margin-bottom: 0.5em;
  display: flex;
  align-items: center;
  gap: 1em;
}
select {
  font-size: 1.1em;
  border: 1px solid #bbb;
  border-radius: 0.6em;
  padding: 0.3em 1em;
  background: #f6f8fa;
  outline: none;
}
</style>
