<script>
    import Navbar from '../../../components/navbar.svelte';
    import { page } from '$app/stores';

    const id = $page.params.id;

</script>

<main>
    <Navbar /> 
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">{id}</h3>
        <h1 class="text-4xl">Conversation</h1>
    </div>

</main>