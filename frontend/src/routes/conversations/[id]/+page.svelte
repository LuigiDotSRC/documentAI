<script>
    import Navbar from '../../../components/navbar.svelte';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    const id = $page.params.id;
    let name = "";
    let vstore_id = "";
    
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

</main>