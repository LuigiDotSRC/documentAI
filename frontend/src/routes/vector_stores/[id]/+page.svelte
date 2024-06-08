<script>
    import Navbar from '../../../components/navbar.svelte';
    import { onMount } from 'svelte';

    import { page } from '$app/stores';
    const id = $page.params.id;

    let name = '';
    let files = []; 

    onMount(async () => {
        await fetchVectorStoreData(); 
    });

    async function fetchVectorStoreData() {
        const response = await fetch(`http://127.0.0.1:5000/api/vector_stores?id=${id}`);
        const response_json = await response.json();
        name = response_json.name;
        files = response_json.files;  
    }
</script>

<main>
    <Navbar />
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">{id}</h3>
        <h1 class="text-4xl">
            {#await name}
                Loading...
            {:then}
                {name}
            {:catch error}
                Error: {error.message}
            {/await}
        </h1>
    </div>

    {#await name}
        Loading...
    {:then}
        {#each files as file}
            <p>{file}</p>
        {/each}
    {:catch error}
        Error: {error.message}
    {/await}
    
</main>

