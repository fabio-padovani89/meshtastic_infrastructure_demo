export default {
  api: {
    getNodesInfo: {
      // url: 'http://localhost:8000/nodes/',
      url: 'http://192.168.2.15:8000/nodes/',
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
      // urlTemplate: 'http://localhost:8080/styles/basic-preview/{z}/{x}/{y}.png',
      urlTemplate: 'http://192.168.2.15:8080/styles/basic-preview/{z}/{x}/{y}.png',
      maxZoom: 22
    }
  }
}