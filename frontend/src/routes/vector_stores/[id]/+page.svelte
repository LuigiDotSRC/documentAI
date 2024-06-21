<script>
    import Navbar from '../../../components/Navbar.svelte';
    import { onMount } from 'svelte';

    import { page } from '$app/stores';
    import uploadIcon from '$lib/upload_icon.png'
    import FileCard from '../../../components/FileCard.svelte';
    import toast, { Toaster } from 'svelte-french-toast';

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

        let filePromises = response_json.files.map(async file => {
            const fileResponse = await fetch(`http://127.0.0.1:5000/api/files/?id=${file.id}`, { method: 'GET' });
            if (fileResponse.ok) {
                return fileResponse.json();
            }
        });
        let fileDataArray = await Promise.all(filePromises);
        files = fileDataArray.filter(fileData => fileData !== undefined);
    }

    function handleFileInputChange(event) {
        const file = event.target.files[0]; 
        selectedFile = file; 
    }

    async function uploadFile() {
        if (selectedFile) {
            toast('Working...', {
	            icon: '⏳',
            });

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('vstore_id', id);

            const response = await fetch('http://127.0.0.1:5000/api/files', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                toast.success('Successfully uploaded file!');
                fetchVectorStoreData();
            } else {
                toast.error(response.message); 
            }
        } else {
            toast.error('Must select a file');
        }

        document.getElementById('fileInput').value = '';
    }

    async function deleteFile(id) {
        toast('Working...', {
	        icon: '⏳',
        });
        const response = await fetch(`http://127.0.0.1:5000/api/files/?id=${id}`, { method: 'DELETE' });
        if (response.ok) {
            toast.success('Deleted file! Refresh the page');
        } else {
            toast.error(response.message); 
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
                <FileCard 
                    file_id={file.id}
                    file_name={file.filename}
                    upload_time={file.created_at}
                    bytes={file.bytes}
                    on_delete={deleteFile}
                />
            {/each}
        {:catch error}
            Error: {error.message}
        {/await}

    </div>
</main>

