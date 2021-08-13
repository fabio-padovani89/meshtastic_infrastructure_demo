export default {
  api: {
    host: 'meshtastic-web',
    port: 8000,
    protocol: 'http',
    getNodesInfo: {
      path: '/nodes/',
      interval: 5000
    }
  },
  map: {
    host: 'meshtastic-maps',
    port: 8080,
    protocol: 'http',
    initCoordinates: {
      lat: 45.494643,
	    lon: 10.938749
    },
    initZoom: 10,
    tileLayer: {
      path: '/styles/basic-preview/{z}/{x}/{y}.png',
      maxZoom: 22
    }
  }
}