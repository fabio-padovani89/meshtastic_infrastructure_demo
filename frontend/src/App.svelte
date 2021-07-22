<script>
	import { onMount } from 'svelte';
	import Leaflet from 'leaflet'
	import conf from './conf';

	let map
	let mapContainer

	let nodesInfo = []
	let mapMarkers = []

	const getNodesInfo = async () => {
		const response = await fetch(conf.api.getNodesInfo.url)
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

	onMount(() => {
		map = Leaflet.map(mapContainer).setView([
			conf.map.initCoordinates.lat,
			conf.map.initCoordinates.lon
		], conf.map.initZoom)
		Leaflet.tileLayer(conf.map.tileLayer.urlTemplate, {
			maxZoom: conf.map.tileLayer.maxZoom
		}).addTo(map)

		getNodesInfo()
		setInterval(() => {
			getNodesInfo()
		}, conf.api.getNodesInfo.interval)
	})
	
</script>

<div>
	<button on:click={getNodesInfo}>
		Get Nodes info
	</button>
</div>

<div
	class="map"
	bind:this={mapContainer}
></div>

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