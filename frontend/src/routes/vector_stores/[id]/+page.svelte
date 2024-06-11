<script>
    import Navbar from '../../../components/navbar.svelte';
    import { onMount } from 'svelte';

    import { page } from '$app/stores';
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

    <div>
        <input id="fileInput" type="file" on:change={handleFileInputChange} />
        <button on:click={uploadFile}>Upload</button>
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

