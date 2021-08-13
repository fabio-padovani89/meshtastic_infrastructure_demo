<script>
	import { onMount } from 'svelte';
	import Leaflet from 'leaflet'
	import conf from './conf';

	let map
	let mapContainer
	let mapTileLayer

	let nodesInfo = []
	let mapMarkers = []

	const apiReqData = {
		host: conf.api.host,
    port: conf.api.port,
    protocol: conf.api.protocol
	}

	const mapReqData = {
		host: conf.map.host,
    port: conf.map.port,
    protocol: conf.map.protocol
	}

	const buildUrl = (protocol, host, port, path) => {
		return `${protocol}://${host}:${port}${path}`
	}

	const getNodesInfo = async () => {
		const response = await fetch(
			buildUrl(
				apiReqData.protocol,
				apiReqData.host,
				apiReqData.port,
				conf.api.getNodesInfo.path,
			)
		)
    nodesInfo = await response.json()

		mapMarkers.forEach((x) => {
			x.removeFrom(map)
		})
		mapMarkers = []
		
		nodesInfo.forEach(node => {
			const marker = Leaflet.marker([node.position.latitude, node.position.longitude])
			marker.bindPopup(JSON.stringify(node)).openPopup()
			mapMarkers.push(marker)
			marker.addTo(map)
		})
	}

	const initTileLayer = () => {
		if (mapTileLayer) {
			mapTileLayer.removeFrom(map)
		}

		console.log(mapReqData)

		mapTileLayer = Leaflet.tileLayer(
			buildUrl(
				mapReqData.protocol,
				mapReqData.host,
				mapReqData.port,
				conf.map.tileLayer.path,
			),
			{
				maxZoom: conf.map.tileLayer.maxZoom
			}
		)

		mapTileLayer.addTo(map)
	}

	onMount(() => {
		map = Leaflet.map(mapContainer).setView([
			conf.map.initCoordinates.lat,
			conf.map.initCoordinates.lon
		], conf.map.initZoom)

		initTileLayer()

		getNodesInfo()
		setInterval(() => {
			getNodesInfo()
		}, conf.api.getNodesInfo.interval)
	})
	
</script>

<div
	class="map"
	bind:this={mapContainer}
></div>

<div>
	<h3>Web server connection data</h3>

	<label>
		protocol
		<select bind:value={apiReqData.protocol}>
			<option value="http">http</option>
			<option value="https">https</option>
		</select>
	</label>

	<label>
		host
		<input bind:value={apiReqData.host} />
	</label>

	<label>
		port
		<input bind:value={apiReqData.port} type="number" />
	</label>
</div>

<div>
	<h3>Map server connection data</h3>

	<label>
		protocol
		<select bind:value={mapReqData.protocol} on:blur={initTileLayer}>
			<option value="http">http</option>
			<option value="https">https</option>
		</select>
	</label>

	<label>
		host
		<input bind:value={mapReqData.host} on:change={initTileLayer} />
	</label>

	<label>
		port
		<input bind:value={mapReqData.port} type="number" on:change={initTileLayer} />
	</label>
</div>

<div>
	<button on:click={getNodesInfo}>
		Get Nodes info
	</button>
</div>

<ul>
	{#each nodesInfo as node, i}
		<li>
			{JSON.stringify(node)}
		</li>
	{/each}
</ul>

<style>
	.map {
		width: 100%;
		height: 70vh;
	}
</style>