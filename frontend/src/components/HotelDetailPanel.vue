<template>
  <div class="hotel-detail-panel">
    <div v-if="loading">読み込み中...</div>
    <template v-else>
      <h2>{{ hotel?.hotelName }}</h2>
      <div>
        <div>日付：{{ eventDate }}</div>
        <div class="counter-row">
          <span>部屋数:</span>
          <button class="counter-btn" @click="changeRoomNum(-1)" :disabled="roomNum <= 1">−</button>
          <span class="counter-value">{{ roomNum }}</span>
          <button class="counter-btn" @click="changeRoomNum(1)" :disabled="roomNum >= 10">＋</button>
        </div>
        <div class="counter-row">
          <span>大人人数:</span>
          <button class="counter-btn" @click="changeAdultNum(-1)" :disabled="adultNum <= 1">−</button>
          <span class="counter-value">{{ adultNum }}</span>
          <button class="counter-btn" @click="changeAdultNum(1)" :disabled="adultNum >= 10">＋</button>
        </div>
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
import { ref, watch } from "vue";
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

function changeRoomNum(delta) {
  const newVal = roomNum.value + delta;
  if (newVal >= 1 && newVal <= 10) roomNum.value = newVal;
}
function changeAdultNum(delta) {
  const newVal = adultNum.value + delta;
  if (newVal >= 1 && newVal <= 10) adultNum.value = newVal;
}

async function fetchHotelDetail() {
  loading.value = true;
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
  // console.log(resp);
  hotel.value = resp.hotels?.[0] || null;

  roomPlans.value = [];
  const raw = resp.raw?.hotels?.[0]?.find(x => x.roomInfo) || {};
  if (raw.roomInfo) {
    // roomInfoは {roomBasicInfo: ...}, {dailyCharge: ...}, ... のような配列
    for (let i = 0; i < raw.roomInfo.length; i++) {
      const plan = raw.roomInfo[i];
      // roomBasicInfoがあったら次のdailyChargeとセットで
      if (plan.roomBasicInfo) {
        const basic = plan.roomBasicInfo;
        // 次の要素にdailyChargeがあれば取得、なければnull
        const chargeObj = raw.roomInfo[i + 1] && raw.roomInfo[i + 1].dailyCharge ? raw.roomInfo[i + 1] : {};
        const charge = chargeObj.dailyCharge || {};
        roomPlans.value.push({
          planId: basic.planId,
          planName: basic.planName,
          roomName: basic.roomName,
          reserveUrl: basic.reserveUrl,
          total: charge.total,
        });
      }
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

.counter-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.6em;
  gap: 0.5em;
}
.counter-btn {
  font-size: 1.2em;
  background: #e3e6ee;
  border: none;
  border-radius: 0.5em;
  width: 2.2em;
  height: 2.2em;
  cursor: pointer;
  transition: background 0.15s;
  user-select: none;
}
.counter-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.counter-value {
  display: inline-block;
  width: 2em;
  text-align: center;
  font-size: 1.1em;
}
</style>