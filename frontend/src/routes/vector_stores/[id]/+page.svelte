<script>
    import Navbar from '../../../components/navbar.svelte';
    import { onMount } from 'svelte';

    import { page } from '$app/stores';
    import uploadIcon from '$lib/upload_icon.png'
    import FileCard from '../../../components/fileCard.svelte';

    const id = $page.params.id;

    let name = '';
    let files = []; 
    let selectedFile = null;

    onMount(async () => {
        await fetchVectorStoreData(); 
    });

    async function fetchVectorStoreData() {
        const response = await fetch(`http://127.0.0.1:5000/api/vector_stores?id=${id}`);
        const response_json = await response.json();
        name = response_json.name;
        files = response_json.files;  
    }

    function handleFileInputChange(event) {
        const file = event.target.files[0]; 
        selectedFile = file; 
    }

    async function uploadFile() {
        if (selectedFile) {
            console.log("Uploading file:", selectedFile);

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('vstore_id', id);

            const response = await fetch('http://127.0.0.1:5000/api/files', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
            } else {
                console.log('error')
            }
        } else {
            console.log("No file selected.")
        }

        document.getElementById('fileInput').value = '';
    }
</script>

<style>
    #fileInput {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
    }

    .truncate {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    max-width: 400px; 
    }
</style>

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
    
    <div class="mt-10 mb-5 ml-10 w-[600px] h-[150px]"> 
        <div class="bg-neutral-800 w-full h-full my-2 rounded-lg relative">
            <h2 class="text-3xl text-center">Upload a file</h2>
            <img id="colorized-image" src="{uploadIcon}" alt="Upload Icon" class="w-20 mx-auto">
            <p class="text-center">Click here or drag and drop</p>
            <input id="fileInput" type="file" on:change={handleFileInputChange} />
        </div>
    </div>

    <div class="flex ml-10 align-middle">
        {#if selectedFile}
            <p class="text-lg my-auto truncate">Selected file: {selectedFile.name}</p>
        {:else}
            <p class="text-lg my-auto">No selected file</p>
        {/if}
        <button on:click={uploadFile} class="ml-10 px-2 py-2 border-2 rounded-lg bg-green-500 hover:bg-green-400">Upload File</button>
    </div>

    <div class="my-10 ml-10">
        <h2 class="text-3xl">Files</h2>
        {#await files}
            Loading...
        {:then}
            {#each files as file}
                <FileCard file_id={file.id}/>
            {/each}
        {:catch error}
            Error: {error.message}
        {/await}

    </div>
</main>

