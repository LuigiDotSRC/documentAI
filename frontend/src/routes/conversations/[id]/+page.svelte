<script>
    import Navbar from '../../../components/Navbar.svelte';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import sendIcon from '$lib/paper-plane.png';
    import AttatchmentFile from '../../../components/AttatchmentFile.svelte';
    import Message from '../../../components/Message.svelte';
    import toast, { Toaster } from 'svelte-french-toast';

    const id = $page.params.id;
    let name = "";
    let vstore_id = "";
    let userPrompt = ""; 
    let messages = []; 
    let files = []; 
    let attatchedFiles = []; 
    
    onMount(async () => {
        await fetchThreadData();
        await fetchConversationData(); 
        await fetchVectorStoreData(); 
    });

    async function fetchThreadData() {
        const response = await fetch(`http://127.0.0.1:5000/api/threads/?id=${id}`, { method: "GET" });
        if (response.ok) {
            const data = await response.json(); 
            name = data.name;
            vstore_id = data.vstore_id; 
        }
    }

    async function fetchConversationData() {
        const response = await fetch(`http://127.0.0.1:5000/api/messages/?thread_id=${id}`, { method: "GET" }); 
        if (response.ok) {
            const data = await response.json();
            messages = data; 
            console.log(messages);
        }
    }

    async function fetchVectorStoreData() {
        const response = await fetch(`http://127.0.0.1:5000/api/vector_stores?id=${vstore_id}`);
        const response_json = await response.json();

        let filePromises = response_json.files.map(async file => {
            const fileResponse = await fetch(`http://127.0.0.1:5000/api/files/?id=${file.id}`, { method: 'GET' });
            if (fileResponse.ok) {
                return fileResponse.json();
            }
        });
        let fileDataArray = await Promise.all(filePromises);
        files = fileDataArray.filter(fileData => fileData !== undefined);
    }

    function handleSelectedFile(id) {
        if (attatchedFiles.includes(id)) {
            const index = attatchedFiles.indexOf(id);
            attatchedFiles.splice(index,1)
        } else {
            attatchedFiles.push(id);
        }
    }

    async function handleKeyPress(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            await handleSubmit(); 
        }
    }

    async function handleSubmit() {
        console.log(userPrompt);
        console.log(attatchedFiles, attatchedFiles.join(','));

        if (!userPrompt) {
            toast.error("Prompt cannot be empty")
        } else {
            toast('Working...', {
	            icon: '⏳',
            });
            const response = await fetch(`http://127.0.0.1:5000/api/messages/?thread_id=${id}&message=${userPrompt}&file_ids=${attatchedFiles.join(',')}`, { method: 'POST' });
            if (response.ok) {
                fetchConversationData(); 
                userPrompt = ""; 
            }
        }
    }

</script>

<Toaster />

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
            {#await files}
                Loading ...
            {:then} 
                {#each files as file}
                    <AttatchmentFile 
                        name={file.filename} 
                        id={file.id} 
                        datetime={file.created_at}
                        onChange={() => {handleSelectedFile(file.id)}}
                    />
                {/each}
            {/await}
        </div>

        <div class="flex-col">
            <div class="mx-2 bg-neutral-800 w-[90rem] h-[40rem] rounded-lg px-4 py-4 overflow-auto">
                {#await messages}
                    Loading...
                {:then} 
                    {#each messages as message}
                        <Message sender={message.role} message={message.message}/>
                    {/each}
                {/await}
            </div>
            <div class="flex">
                <textarea type="text" placeholder="Prompt" bind:value={userPrompt} on:keydown={handleKeyPress} class="justify-center mx-2 my-4 px-2 py-2 rounded-lg w-[85rem] h-[5rem] text-white bg-neutral-500 border-2 border-neutral-400"></textarea>
                <button class="w-16 h-16 bg-neutral-100 my-6 px-2 rounded-lg hover:bg-neutral-200" on:click={handleSubmit}><img src="{sendIcon}" alt="Send icon"></button>
            </div>
            
        </div>
        
    </div>

    

</main>