<script>
    export let name;
    export let id; 
    export let datetime;
</script>

<div class="flex bg-neutral-700 rounded-lg px-2 py-2 border-2 border-neutral-400">
    <div class="flex-1">
        <h3 class="text-lg">{name}</h3>
        <p class="text-sm truncate w-40 text-neutral-400">{id}</p>
        <p class="text-sm text-neutral-400">{datetime}</p>
    </div>
    <input type="checkbox">
</div>