<script>
    import Navbar from "../../components/navbar.svelte";
    import ThreadCard from "../../components/ThreadCard.svelte";
</script>

<main>
    <Navbar /> 
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">Chat with documents</h3>
        <h1 class="text-4xl">Conversations</h1>
    </div>
    
    <div class="ml-10 my-8">
        <a href="/conversations/create" class="text-blue-400 underline hover:text-blue-600">Start new conversation</a>
    </div>

    <div class="flex flex-col ml-10 my-10 bg-neutral-700"> 
        <ThreadCard 
            thread_name="dummy"
        /> 

        <!-- {#await vector_store_data}
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
        {/await} -->
    </div>


</main>