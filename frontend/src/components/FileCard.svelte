<script>
    export let file_id;
    export let file_name; 
    export let upload_time; 
    export let bytes; 
    export let on_delete;

    async function retrieve_file_info() {
        const response = await fetch(`http://127.0.0.1:5000/api/files/?id=${file_id}`, {method: 'GET'})
        .then(async function(response){
            if (response.ok) {
                const data = await response.json();
                file_name = data.filename;
                bytes = data.bytes;
                upload_time = data.created_at;
            }
        });
    }

    retrieve_file_info();
</script>

<div class="bg-neutral-800 flex border-2 w-4/6 rounded-lg justify-between py-2 px-2 my-2">
    <div class="flex flex-col">
        <h3 class="text-xl">{file_name}</h3>
        <p>ID: {file_id}</p>
        <p>Uploaded at: {upload_time}</p>
        <p>Bytes: {bytes}</p>
    </div>
    <button on:click={on_delete(file_id)} class="border-2 bg-red-500 px-8 my-auto mr-4 rounded-lg hover:bg-red-400 h-10 align-middle">Delete</button>
</div>