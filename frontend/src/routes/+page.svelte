<script>
    import Navbar from "../components/navbar.svelte";
</script>

<main class="bg-neutral-700">
    <Navbar />
    <div class="ml-10 my-2">
        <h3 class="text-xl text-neutral-400">Welcome To</h3>
        <h1 class="text-4xl">DocumentAI</h1>
    </div>

    <div class="ml-10 my-10">
        <p class="my-4">A webapp interface to chat with your documents. Powered by Flask, Svelte, TailwindCSS, and OpenAI's APIs.</p>
        <p class="mt-8 mb-2">To get started:</p>
        <ol>
            <li class="ml-8"><span class="text-slate-400 mr-2">1.</span> Ensure that your OpenAI API Key is set in the .env file</li>
            <li class="ml-8"><span class="text-slate-400 mr-2">2.</span> Upload your files to a <a href="/" class="text-blue-400 underline hover:text-blue-600">Vector Store</a></li>
            <li class="ml-8"><span class="text-slate-400 mr-2">3.</span> Start a <a href="/" class="text-blue-400 underline hover:text-blue-600">Conversation</a> with your files</li>
        </ol>
    </div>
</main>