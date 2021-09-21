import conf from './conf'


const getReqData = (storage, confPath) => {
  let res = localStorage.getItem(storage)
  if (res) res = JSON.parse(res);
  if (!res) res = {};
  ['host', 'port', 'protocol'].forEach((x) => {
    console.log(x)
    if (!res[x]) res[x] = conf[confPath][x]
  })
  return res
}

const setReqData = (storage, data) => {
  localStorage.setItem(storage, JSON.stringify(data))
}

const resetReqData = (storage, confPath) => {
  localStorage.removeItem(storage)
}

const getApiReqData = () => getReqData('apiReqData', 'api')
const getMapReqData = () => getReqData('mapReqData', 'map')
const setApiReqData = (data) => setReqData('apiReqData', data)
const setMapReqData = (data) => setReqData('mapReqData', data)
const resetApiReqData = () => resetReqData('apiReqData', 'api')
const resetMapReqData = () => resetReqData('mapReqData', 'map')

export {
  getApiReqData,
  getMapReqData,
  setApiReqData,
  setMapReqData,
  resetApiReqData,
  resetMapReqData,
}