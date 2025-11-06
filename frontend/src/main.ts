import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueGoogleMaps from '@fawmi/vue-google-maps'

const app = createApp(App)

app.use(router)

const googleMapsApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY

if (googleMapsApiKey) {
  app.use(VueGoogleMaps, {
    load: { key: googleMapsApiKey }
  })
} else {
  console.warn('[Eventel] VITE_GOOGLE_MAPS_API_KEY is not set. Google Maps will not be initialised.')
  const MissingKeyStub = {
    template: `<div style="padding:1.5rem;border:1px solid #ccc;border-radius:0.75rem;background:#fffbe6;color:#8a6d3b;">
      Google Maps API key is not configured. Set VITE_GOOGLE_MAPS_API_KEY in your .env file to display the map.
    </div>`
  }
  app.component('GMapMap', MissingKeyStub)
  app.component('GMapMarker', { template: '<span />' })
  app.component('GMapInfoWindow', { template: '<span><slot /></span>' })
}

app.mount('#app')
