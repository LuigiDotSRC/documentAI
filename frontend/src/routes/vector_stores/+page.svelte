<script>
    import Navbar from "../../components/Navbar.svelte";
    import VectorStoreCard from "../../components/VectorStoreCard.svelte";
    import {onMount} from 'svelte';
    import toast, { Toaster } from 'svelte-french-toast';

    let vector_store_data = [];
    let vstore_name = ''; 

    onMount(async () => {
        await fetchVectorStores(); 
    });

    async function create_vector_store() {
        await fetch(`http://127.0.0.1:5000/api/vector_stores/?name=${vstore_name}`, {
            method: 'POST', 
        }).then(async function(response) {
            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.message;
                toast.error(`Error: ${errorMessage}`);
            } else {
                toast.success("Successfully created vector store!");
            }
        });
        vstore_name = '';
        await fetchVectorStores();
    }

    async function fetchVectorStores() {
        const response = await fetch('http://127.0.0.1:5000/api/vector_stores', {method: 'GET'});
        vector_store_data = await response.json();
    }

    async function remove_vector_store(vstore_id) {
        toast('Working...', {
	        icon: '⏳',
        });
        await fetch(`http://127.0.0.1:5000/api/vector_stores/?id=${vstore_id}`, {
            method: 'DELETE', 
            headers: {
                'content-type': 'application/json'
            }
        }).then(async function(response) {
            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.message;
                toast.error(`Error: ${errorMessage}`);
            } else {
                toast.success("Successfully deleted vector store!");
            }
        });
        await fetchVectorStores();
    }
</script>

<Toaster />

<main class="bg-neutral-700">
    <Navbar />
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">Upload Files</h3>
        <h1 class="text-4xl">Vector Stores</h1>
    </div>

    <div>
        <button on:click={create_vector_store} class="my-10 ml-10 px-2 py-2 border-2 rounded-lg bg-green-500 hover:bg-green-400">Create Vector Store</button>
        <input type="text" bind:value={vstore_name} placeholder="Name " class="text-black mx-4 px-2 rounded-md">
    </div>
    
    <div class="flex flex-col ml-10 my-10 bg-neutral-700"> 
        {#await vector_store_data}
            Loading...
        {:then data}
            {#each data as v_store}
            <VectorStoreCard
                vector_store_name={v_store.name}
                vector_store_ID={v_store.id}
                num_files={v_store.num_files}
                bytes={v_store.bytes}
                on_delete_click={() => remove_vector_store(v_store.id)}
            />
            {/each}
        {:catch error}
            Error: {error.message}
        {/await}
    </div>

</main>