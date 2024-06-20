<script>
    export let thread_name;
    export let thread_ID;
    export let vstore_id
    
    export let on_delete_click;
</script>

<div class="flex border-2 w-4/6 rounded-lg py-2 px-2 justify-between bg-neutral-800 my-2">
    <div class="flex flex-col">
        <h3 class="text-xl">{thread_name}</h3>
        <p>ID: {thread_ID}</p>
        <p>Vector Store: {vstore_id}</p>
    </div>
    <div class="flex flex-col">
        <a href='/vector_stores/{thread_ID}'>
            <button class="border-2 bg-green-500 px-8 my-2 rounded-lg hover:bg-green-400 h-10">Chat</button>
        </a>
        <button on:click={on_delete_click} class="border-2 bg-red-500 px-2 my-2 rounded-lg hover:bg-red-400 h-10">Delete</button>
    </div>
</div> 