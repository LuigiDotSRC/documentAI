<script>
    export let vector_store_name;
    export let vector_store_ID;
    export let num_files;
    export let bytes;
    
    export let on_delete_click;
</script>

<div class="flex border-2 w-4/6 rounded-lg py-2 px-2 justify-between bg-neutral-800 my-2">
    <div class="flex flex-col">
        <h3 class="text-xl">{vector_store_name}</h3>
        <p>ID: {vector_store_ID}</p>
        <p>Number of Files: {num_files}</p>
        <p>Bytes: {bytes}</p>
    </div>
    <div class="flex flex-col">
        <a href='/vector_stores/{vector_store_ID}'>
            <button class="border-2 bg-green-500 px-2 my-2 rounded-lg hover:bg-green-400 h-10">Edit Contents</button>
        </a>
        <button on:click={on_delete_click} class="border-2 bg-red-500 px-2 my-2 rounded-lg hover:bg-red-400 h-10">Delete</button>
    </div>
</div> 