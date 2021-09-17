export default {
  api: {
    host: 'meshtastic-web',
    port: 8000,
    protocol: 'http',
    getNodesInfo: {
      path: '/api/v1/nodes/',
      interval: 30 // in seconds
    },
    getNodePath: {
      path: '/api/v1/nodes/<%= user %>/path/',
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