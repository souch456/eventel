<template>
  <div class="hotel-detail-panel">
    <div v-if="loading">読み込み中...</div>
    <template v-else>
      <h2>{{ hotel?.hotelName }}</h2>
      <div>
        <div>日付：{{ eventDate }}</div>
        <label>
          部屋数: <input type="number" min="1" max="10" v-model="roomNum" @change="fetchHotelDetail" />
        </label>
        <label>
          大人人数: <input type="number" min="1" max="10" v-model="adultNum" @change="fetchHotelDetail" />
        </label>
      </div>
      <div>
        <img :src="hotel?.hotelThumbnailUrl" style="max-width: 140px;" />
        <div>{{ hotel?.address1 }}{{ hotel?.address2 }}</div>
        <div>最安料金: {{ hotel?.hotelMinCharge ? hotel.hotelMinCharge + '円~' : '不明' }}</div>
      </div>
      <hr/>
      <div v-if="roomPlans && roomPlans.length">
        <b>空室プラン</b>
        <div v-for="plan in roomPlans" :key="plan.planId" class="plan-box">
          <div>【{{ plan.planName }}】</div>
          <div>部屋: {{ plan.roomName }}</div>
          <div>料金: {{ plan.total ? plan.total + '円' : '要確認' }}</div>
          <div>
            <a :href="plan.reserveUrl" target="_blank">予約ページ</a>
          </div>
        </div>
      </div>
      <div v-else>空室プラン情報はありません</div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { fetchVacantHotelDetail } from "../api/api.js";
const props = defineProps({
  hotelNo: Number,
  eventDate: String,
});
const hotel = ref(null);
const roomPlans = ref([]);
const roomNum = ref(1);
const adultNum = ref(1);
const loading = ref(true);

async function fetchHotelDetail() {
  loading.value = true;
  // イベント日付・翌日を使ってAPIリクエスト
  const checkinDate = props.eventDate;
  const coDate = new Date(checkinDate);
  coDate.setDate(coDate.getDate() + 1);
  const checkoutDate = coDate.toISOString().slice(0, 10);

  const resp = await fetchVacantHotelDetail({
    hotelNo: props.hotelNo,
    checkinDate,
    checkoutDate,
    adultNum: adultNum.value,
    roomNum: roomNum.value,
  });
  // 基本情報
  hotel.value = resp.hotels?.[0] || null;

  // roomInfo等を元データから取り出し
  roomPlans.value = [];
  const raw = resp.raw?.hotels?.[0]?.find(x => x.roomInfo) || {};
  if (raw.roomInfo) {
    for (const plan of raw.roomInfo) {
      const basic = plan.roomBasicInfo || {};
      const charge = plan.dailyCharge || {};
      roomPlans.value.push({
        planId: basic.planId,
        planName: basic.planName,
        roomName: basic.roomName,
        reserveUrl: basic.reserveUrl,
        total: charge.total,
      });
    }
  }
  loading.value = false;
}

// ホテル/日付/人数等が変わるたび再取得
watch(
  () => [props.hotelNo, props.eventDate, roomNum.value, adultNum.value],
  fetchHotelDetail,
  { immediate: true }
);
</script>

<style scoped>
.hotel-detail-panel {
  min-width: 320px;
  max-width: 430px;
  background: #fff;
  padding: 1.5em 1em;
  border-radius: 1.2em;
  box-shadow: 0 2px 16px #1976d211;
}
.plan-box {
  border: 1px solid #eee;
  border-radius: 0.6em;
  margin-bottom: 1em;
  padding: 0.6em;
}
</style>