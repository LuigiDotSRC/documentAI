<script>
    import Navbar from "../../components/navbar.svelte";
    import ThreadCard from "../../components/ThreadCard.svelte";
    import { onMount } from "svelte";
    import toast, { Toaster } from "svelte-french-toast";

    let threads = [];

    onMount(async () => {
        await fetchThreads();
        console.log(threads);
    });

    async function fetchThreads() {
        const response = await fetch("http://127.0.0.1:5000/api/threads/");
        threads = await response.json(); 
    }

    async function deleteThread(id) {
        const response = await fetch(`http://127.0.0.1:5000/api/threads/?id=${id}`, {method: "DELETE"});
        if (!response.ok) {
            toast.error(response.message); 
        } else {
            toast.success("Successfully deleted thread"); 
            fetchThreads(); 
        }
    }
</script>

<Toaster /> 

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
        {#await threads}
            Loading...
        {:then data}
            {#each data as thread}
            <ThreadCard 
                thread_name = {thread.name}
                thread_ID = {thread.id}
                vstore_id = {thread.vstore_id}
                on_delete_click = {() => deleteThread(thread.id)}
            />
            {/each}
        {:catch error}
            Error: {error.message}
        {/await} 
    </div>


</main>