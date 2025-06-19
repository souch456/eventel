<template>
  <div id="app">
    <header>
      <h1>イベントホテル検索マップ</h1>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', 'Arial', sans-serif;
  background: #f6f8fa;
}
header {
  background: linear-gradient(90deg, #2196f3 0%, #1976d2 100%);
  color: #fff;
  padding: 1.2em 0;
  text-align: center;
  box-shadow: 0 2px 10px #0002;
}
main {
  padding: 2em 0.5em 0 0.5em;
  max-width: 1400px;
  margin: 0 auto;
}
</style>