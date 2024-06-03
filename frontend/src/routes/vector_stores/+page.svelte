<script>
    import Navbar from "../../components/navbar.svelte";
    import VectorStoreCard from "../../components/vector_store_card.svelte";

    let vector_store_data = get_vector_store();
    async function get_vector_store() {
        const response = await fetch('http://127.0.0.1:5000/api/vector_stores', {method: ['GET']});
        return response.json(); 
    }
</script>

<main class="bg-neutral-700">
    <Navbar />
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">Upload Files</h3>
        <h1 class="text-4xl">Vector Stores</h1>
    </div>

    <button class="my-10 ml-10 px-2 py-2 border-2 rounded-lg bg-green-500 hover:bg-green-400">New Vector Store</button>

    <div class="flex flex-col ml-10 my-10"> 
        {#await vector_store_data}
            Loading...
        {:then data}
            {#each data as v_store}
            <VectorStoreCard
                vector_store_name={v_store.name}
                vector_store_ID={v_store.id}
                num_files={v_store.num_files}
                bytes={v_store.bytes}
            />
            {/each}
        {:catch error}
            Error: {error.message}
        {/await}
    </div>

</main>