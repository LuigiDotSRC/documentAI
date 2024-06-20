<script>
    export let sender;
    export let message;
 
    let header = ""; 
    let styling = ""; 

    if (sender === "user") {
        header = "👤 User:";
        styling = "bg-green-600 ml-auto";        
    } else {
        header = "🤖 DocAI:";
        styling = "bg-blue-600 ml-0"; 
    }
</script>

<div class="{styling} rounded-lg px-2 py-2 my-4 w-[50rem]">
    <h3 class="text-xl">{header}</h3>
    <p class="w-auto break-words">{message}</p>
</div>