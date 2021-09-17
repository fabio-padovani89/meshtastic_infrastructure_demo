<script>
	import { onMount } from 'svelte';
	import { template } from 'lodash';
	import moment from 'moment';
	import queryString from 'query-string';
	import Leaflet from 'leaflet'
	import conf from './conf';
	import Flatpickr from './components/Flatpickr.svelte';
	import NodesTable from './components/NodesTable.svelte';
	import { Italian as flatpickrIt } from "flatpickr/dist/l10n/it"

	let map
	let mapContainer
	let mapTileLayer

	let nodesInfo = []
	let mapMarkers = []
	let mapPolyline = []
	let mapPolylineGroup = []

	let selectedNode = null

	const viewOptions = {
		NODES: 'Nodes',
		NODE_PATH: 'Node path',
	}
	let currentView = viewOptions.NODES

	const showSections = {
		connectionData: true,
		filters: true,
		nodesTable: true,
	}

	const autoRefreshData = {
		enabled: true,
		seconds: conf.api.getNodesInfo.interval,
		interval: null,
	}

	const apiReqFilters = {
		user: null,
		'dt-from': moment().subtract(7, 'd').toDate(),
		'dt-to': new Date(),
	}

	const flatpickrOptions = {
		enableTime: true,
		locale: flatpickrIt,
		minDate: new Date().fp_incr(-7),
		maxDate: new Date(),
	}

	const apiReqData = {
		host: conf.api.host,
    port: conf.api.port,
    protocol: conf.api.protocol,
	}	

	const mapReqData = {
		host: conf.map.host,
    port: conf.map.port,
    protocol: conf.map.protocol
	}

	const buildUrl = (protocol, host, port, path, filters) => {
		const qsFilters = {}
		if (filters) {
			for (const [key, value] of Object.entries(filters)) {
				if (value) {
					if (value instanceof Date) {
						qsFilters[key] = moment(value).format()
					} else {
						qsFilters[key] = value
					}
				}
			}
		}
		const qs = queryString.stringify(qsFilters);
		return `${protocol}://${host}:${port}${path}?${qs}`
	}

	const cleanMap = () => {
		if (mapMarkers.length) {
			mapMarkers.forEach((x) => {
				x.removeFrom(map)
			})
			mapMarkers = []
		}

		if (mapPolyline) {
			map.removeLayer(mapPolylineGroup)
			mapPolylineGroup = null
			mapPolyline = null
		}
	}

	const getNodesInfo = async () => {
		if (currentView !== viewOptions.NODES) return

		const url = buildUrl(
			apiReqData.protocol,
			apiReqData.host,
			apiReqData.port,
			conf.api.getNodesInfo.path,
			apiReqFilters,
		)

		const response = await fetch(url)
    nodesInfo = await response.json()

		cleanMap()
		
		if (nodesInfo) {
			let opacity = 1
			let rangeHoursDiff = null
			let momentTo = null

			if (apiReqFilters['dt-from'] && apiReqFilters['dt-to']) {
				momentTo = moment(apiReqFilters['dt-to'])
				rangeHoursDiff = Math.round(momentTo.diff(moment(apiReqFilters['dt-from']), 'hours', true))
			}

			nodesInfo.forEach(node => {
				opacity = 1
				let momentRelevationTime = (node.relevation_time) ? moment(node.relevation_time) : null

				if (momentRelevationTime && momentTo && momentRelevationTime < momentTo) {
					const nodeHoursDiff = Math.round(momentTo.diff(momentRelevationTime, 'hours', true))
					opacity = (rangeHoursDiff - nodeHoursDiff) / rangeHoursDiff
				}

				const marker = Leaflet.marker([node.position.latitude, node.position.longitude])
				marker.setOpacity(opacity);
				marker.bindPopup(
					`<pre>${JSON.stringify(node, null, 4)}</pre>`,
					{maxWidth: 500}
				).openPopup()
				mapMarkers.push(marker)
				marker.addTo(map)
			})
		}
	}

	const getNodePath = async () => {
		if (currentView !== viewOptions.NODE_PATH) return

		const url = buildUrl(
			apiReqData.protocol,
			apiReqData.host,
			apiReqData.port,
			template(conf.api.getNodePath.path)({ user: selectedNode }),
			apiReqFilters,
		)

		const response = await fetch(url)
    const latlngs = (await response.json()).map(x => [x.lat, x.lon])
		cleanMap()

		mapPolyline = Leaflet.polyline(latlngs, {color: 'red'}).addTo(map)
		mapPolylineGroup = L.layerGroup().addLayer(mapPolyline).addTo(map)

		const marker = Leaflet.marker(latlngs.at(-1))
		mapMarkers.push(marker)
		marker.addTo(map)
	}

	const initTileLayer = () => {
		if (mapTileLayer) {
			mapTileLayer.removeFrom(map)
		}

		// console.log(mapReqData)

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

	const setAutoRefresh = () => {
		clearInterval(autoRefreshData.interval)
		if (autoRefreshData.enabled) {
			autoRefreshData.interval = setInterval(() => {
			refreshData()
		}, autoRefreshData.seconds * 1000)
		}
	}

	const refreshData = (opts) => {
		switch (currentView) {
			case viewOptions.NODES:
				selectedNode = null
				getNodesInfo()
			case viewOptions.NODE_PATH:
				if (opts) selectedNode = opts
				getNodePath()
		}
	}


	const setView = (view, opts) => {
		currentView = view
		refreshData(opts)
	}

	onMount(() => {
		map = Leaflet.map(mapContainer).setView([
			conf.map.initCoordinates.lat,
			conf.map.initCoordinates.lon
		], conf.map.initZoom)

		initTileLayer()

		refreshData()

		setAutoRefresh()
	})
	
</script>

<div class="container">

	<div class="row">
		<div class="column">
			<h2>
				Current view: <strong>{currentView}</strong>
				{#if selectedNode}
				- {selectedNode}
				{/if}
				
			</h2>
			{#if currentView !== viewOptions.NODES}
			<button class="button button-inline button-small button-outline" on:click={() => { setView(viewOptions.NODES) }}>
				Switch to Nodes view
			</button>
			{/if}
		</div>
	</div>

	<div class="row">
		<div class="column">
			<div
				class="map"
				bind:this={mapContainer}
			></div>
		</div>
	</div>

	<div class="row">
		<div class="column column-20">
			<button on:click={() => refreshData()}>
				Refresh data
			</button>

			<label>
				<input type=checkbox bind:checked={autoRefreshData.enabled} on:change={() => { setAutoRefresh() }} />
				Autorefresh
			</label>

			<label>
				Seconds
				<input bind:value={autoRefreshData.seconds} type="number" on:change={() => { setAutoRefresh() }} />
			</label>
		</div>
	</div>

	<hr/>
	
	<div class="row">
		<div class="column">
			<h3>
				Connection data
			</h3>
			<button class="button button-inline button-small button-outline" on:click={() => { showSections.connectionData = !showSections.connectionData }}>
				Show / Hide
			</button>
		</div>
	</div>
	
	{#if showSections.connectionData}
	<div class="row">
		<div class="column">
			<h4>Web server</h4>
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
			
		<div class="column">
			<h4>Map server</h4>
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
	</div>
	{/if}
	
	<hr/>

	
	<div class="row">
		<div class="column">
			<h3>
				Filters
			</h3>
			<button class="button button-inline button-small button-outline" on:click={() => { showSections.filters = !showSections.filters }}>
				Show / Hide
			</button>
		</div>
	</div>

	{#if showSections.filters}
	<div class="row">
		<div class="column column-50">
			<label>
				user
				<input bind:value={apiReqFilters.user} type="text" />
			</label>

			<label for="dt-from">
				Relevation time - from
				<Flatpickr options={flatpickrOptions} bind:value={apiReqFilters['dt-from']} />
			</label>
			
			<label for="dt-to">
				Relevation time - to
				<Flatpickr options={flatpickrOptions} bind:value={apiReqFilters['dt-to']} />
			</label>
		</div>
	</div>
	{/if}
	
	<hr/>

	<div class="row">
		<div class="column">
			<h3>
				Nodes list
			</h3>
			<button class="button button-inline button-small button-outline" on:click={() => { showSections.nodesTable = !showSections.nodesTable }}>
				Show / Hide
			</button>
		</div>
	</div>

	{#if showSections.nodesTable}
	<NodesTable nodes={nodesInfo} on:show-path={x => setView(viewOptions.NODE_PATH, x.detail.user)}/>
	{/if}

</div>
