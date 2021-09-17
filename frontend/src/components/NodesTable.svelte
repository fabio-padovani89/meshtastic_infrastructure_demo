<script>
  import { createEventDispatcher } from 'svelte'

  export let nodes

  const dispatch = createEventDispatcher()

  const showPath = (user) => {
		dispatch('show-path', { user })
	}


</script>

<div class="row">
  <div class="column">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>RELEVATION TIME</th>
          <th>LAT</th>
          <th>LON</th>
          <th>BATTERY LEVEL</th>
          <th>ACTIONS</th>
        </tr>
      </thead>
    
      <tbody>
        {#if nodes}
          {#each nodes as node}
            <tr>
              <td>{node._id}</td>
              <td>{node.relevation_time}</td>
              <td>{node.position.latitude}</td>
              <td>{node.position.longitude}</td>
              <td>{node.batteryLevel}</td>
              <td>
                <button class="button button-small" on:click={showPath(node._id)}>Show path</button>
              </td>
            </tr>
          {/each}
        {:else}
          <tr>
            <td colspan="5">No data available</td>
          </tr>
        {/if}
      </tbody>
    </table>
  </div>
</div>
