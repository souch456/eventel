<template>
  <div class="selector-card">
    <label for="prefsel">都道府県：</label>
    <select v-model="selectedPref" @change="onPrefChange" id="prefsel">
      <option v-for="pref in prefectures" :key="pref" :value="pref">{{ pref }}</option>
    </select>
    <label for="evsel">イベント選択：</label>
    <select v-model="selectedId" @change="onChange" id="evsel">
      <option v-for="ev in filteredEvents" :key="ev.id" :value="ev.id">
        {{ ev.name }}（{{ ev.date }}）
      </option>
    </select>
    <div class="selector-desc">以下に会場から3km圏内のホテルを表示しています</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { fetchEvents } from "../api/api.js";
const emit = defineEmits(["event-selected"]);

const events = ref([]);
const selectedId = ref(null);
const selectedPref = ref("");
const prefectures = ref([]);

// 今日以前を除外
function filterFutureEvents(rawEvents) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return rawEvents.filter(ev => {
    const evDate = new Date(ev.date);
    evDate.setHours(0, 0, 0, 0);
    return evDate >= today;
  });
}

onMounted(async () => {
  const raw = await fetchEvents();
  events.value = filterFutureEvents(raw);

  // 都道府県一覧を抽出して昇順ソート
  const uniquePrefs = Array.from(
    new Set(events.value.map(ev => ev.prefecture))
  ).sort();
  prefectures.value = uniquePrefs;
  selectedPref.value = uniquePrefs[0] || "";

  // イベント初期化
  if (filteredEvents.value.length) {
    selectedId.value = filteredEvents.value[0].id;
    emit("event-selected", selectedId.value);
  }
});

// 都道府県でフィルタ
const filteredEvents = computed(() =>
  events.value.filter(ev => ev.prefecture === selectedPref.value)
);

// 都道府県選択時
function onPrefChange() {
  if (filteredEvents.value.length) {
    selectedId.value = filteredEvents.value[0].id;
    emit("event-selected", selectedId.value);
  } else {
    selectedId.value = null;
  }
}

watch(selectedPref, onPrefChange);

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
.selector-desc {
  font-size: 0.95em;
  color: #666;
  margin-bottom: 0.5em;
}
@media (max-width: 900px) {
  .selector-card {
    flex-direction: column;    /* 縦並びに */
    align-items: flex-start;   /* 左寄せに */
    gap: 0.5em;                /* 間隔を少し狭く */
    width: 100vw;              /* 横幅いっぱいに */
    box-sizing: border-box;    /* 余白バグ対策 */
    padding-left: 0.8em;
    padding-right: 0.8em;
  }
  .selector-desc {
    margin-bottom: 0.3em;
    font-size: 0.95em;
  }
  select {
    width: 100%;
    min-width: 0;
    font-size: 1.08em;
  }
}
</style>
