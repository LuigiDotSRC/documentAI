<script>
    import Navbar from "../../components/navbar.svelte";
    import VectorStoreCard from "../../components/vector_store_card.svelte";
</script>

<main class="bg-neutral-700">
    <Navbar />
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">Upload Files</h3>
        <h1 class="text-4xl">Vector Stores</h1>
    </div>

    <button class="my-10 ml-10 px-2 py-2 border-2 rounded-lg bg-green-500 hover:bg-green-400">New Vector Store</button>

    <div class="flex flex-col ml-10 my-10">
        <VectorStoreCard/>
        <VectorStoreCard/>
    </div>
</main>