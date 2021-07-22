export default {
  api: {
    getNodesInfo: {
      url: 'http://meshtastic-web:8000/nodes/',
      interval: 5000
    }
  },
  map: {
    initCoordinates: {
      lat: 45.494643,
	    lon: 10.938749
    },
    initZoom: 10,
    tileLayer: {
      urlTemplate: 'http://meshtastic-maps:8080/styles/basic-preview/{z}/{x}/{y}.png',
      maxZoom: 22
    }
  }
}