<script>
    import Navbar from '../../../components/navbar.svelte';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import sendIcon from '$lib/paper-plane.png';
    import AttatchmentFile from '../../../components/AttatchmentFile.svelte';
    import Message from '../../../components/Message.svelte';

    const id = $page.params.id;
    let name = "";
    let vstore_id = "";
    let userPrompt = ""; 
    
    onMount(async () => {
        await fetchThreadData();
    });

    async function fetchThreadData() {
        const response = await fetch(`http://127.0.0.1:5000/api/threads/?id=${id}`, { method: "GET" });
        if (response.ok) {
            const data = await response.json(); 
            name = data.name;
            vstore_id = data.vstore_id; 
        }
    }

    function handleKeyPress(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSubmit(); 
        }
    }

    function handleSubmit() {
        console.log(userPrompt);
        userPrompt = ""; 
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
            {/await}
        </h1>
    </div>

    <div class="flex my-8 justify-center">
        <div class="mx-2 bg-neutral-800 w-80 h-[46rem] mr-8 rounded-lg px-4 py-4 overflow-auto">
            <AttatchmentFile />
        </div>

        <div class="flex-col">
            <div class="mx-2 bg-neutral-800 w-[90rem] h-[40rem] rounded-lg px-4 py-4 overflow-auto">
                <Message sender="user" />
                <Message sender="ai" />  
                <Message sender="ai" /> 
              

            </div>
            <div class="flex">
                <textarea type="text" placeholder="Prompt" bind:value={userPrompt} on:keydown={handleKeyPress} class="justify-center mx-2 my-4 px-2 py-2 rounded-lg w-[85rem] h-[5rem] text-white bg-neutral-500 border-2 border-neutral-400"></textarea>
                <button class="w-16 h-16 bg-neutral-100 my-6 px-2 rounded-lg hover:bg-neutral-200" on:click={handleSubmit}><img src="{sendIcon}" alt="Send icon"></button>
            </div>
            
        </div>
        
    </div>

    

</main>