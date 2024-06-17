<script>
    import Navbar from "../../../components/navbar.svelte";
    import DropdownMenu from "../../../components/DropdownMenu.svelte";
    import toast, { Toaster } from 'svelte-french-toast';

    let vstore_id = '';
    let name = '';

    async function createThread() {
        if (!vstore_id || !name) {
            toast.error("Name and Vector Store need to be specified"); 
        } else {
            const response = await fetch('http://127.0.0.1:5000/api/threads/', {
                method: 'POST',
                body: JSON.stringify({name, vstore_id})
            });

            if (!response.ok) {
                toast.error(response); 
            } else {
                toast.success("Successfully created conversation"); 
                setTimeout(() => {
                    window.location.href = 'http://localhost:5173/conversations';
                }, 2000)
            }
        }
    }

</script>

<Toaster /> 

<main>
    <Navbar />
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">Conversations</h3>
        <h1 class="text-4xl">New Conversation</h1>
    </div>

    <div class="ml-10 my-10 bg-neutral-700 border-2 rounded-lg bg-neutral-800 px-4 py-4 w-3/4">
        <div class="flex my-2">
            <p class="mx-2 ">Name:</p> 
            <input bind:value={name} type="text" placeholder="Conversation Name" class="text-black mx-2 px-2 rounded-md">
        </div>

        <div class="flex my-2">
            <p class="mx-2">Vector Store:</p>
            <DropdownMenu bind:target_vstore_id={vstore_id}/>
        </div>
        <button on:click={createThread} class="my-10 ml-2 px-2 py-2 border-2 rounded-lg bg-green-500 hover:bg-green-400">Create New Conversation</button>
    </div>

</main>