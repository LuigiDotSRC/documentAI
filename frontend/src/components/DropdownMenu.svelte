<script>
    import { onMount } from 'svelte';

    let dropdown;
    let hidden = true;
    let vector_store_data = [];
    export let target_vstore_id; 

    function toggleVisibility() {
        dropdown.classList.toggle('hidden');
        hidden = !hidden;
    }

    onMount(async () => {
        dropdown = document.getElementById('dropdown-options');
        document.getElementById('menu-button').addEventListener('click', toggleVisibility);

        // Close the dropdown when clicking outside of it
        document.addEventListener('click', clickOutsideHandler);

        await fetchVectorStores();

        return () => {
            document.removeEventListener('click', clickOutsideHandler);
        };
    });

    function clickOutsideHandler(event) {
        const dropdownClicked = dropdown.contains(event.target);
        const menuButtonClicked = document.getElementById('menu-button').contains(event.target);
        if (!dropdownClicked && !menuButtonClicked) {
            dropdown.classList.add('hidden');
            hidden = true;
        }
    }

    async function fetchVectorStores() {
        const response = await fetch('http://127.0.0.1:5000/api/vector_stores', {method: 'GET'});
        vector_store_data = await response.json();
    }

    function setTargetVectorStore(id, name) {
        if (target_vstore_id) {
            document.getElementById(`button-${target_vstore_id}`).classList.remove('bg-blue-200');
        }
        target_vstore_id = id; 
        document.getElementById(`button-${id}`).classList.add('bg-blue-200');
        document.getElementById('menu-button').textContent = name; 
    }

</script>

<div class="relative inline-block text-left mx-2">
    <div>
      <button type="button" class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" id="menu-button" aria-expanded="true" aria-haspopup="true">
        Select Vector Store
        <svg class="-mr-1 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>

    <div id="dropdown-options" class="hidden absolute pr-16 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
      <div class="py-1 pr-20" role="none">

        {#await vector_store_data}
            Loading...
        {:then data}
            {#each data as v_store}
                <button class="block px-2 py-2 text-sm text-gray-700 hover:bg-blue-100" role="menuitem" on:click={setTargetVectorStore(v_store.id, v_store.name)} id={`button-${v_store.id}`}>{v_store.name} {v_store.id}</button>
            {/each}
        {:catch error}
            Error: {error.message}
        {/await}
      </div>
    </div>
  </div>
