# documentAI

A file assistant AI that supports file attachment for prompt enrichment. Built using Svelte, Flask, SQLite3, Tailwindcss, and OpenAI's API endpoints alongside its' GPT-3.5-Turbo model. 

![Demo screenshot](./assets/demo%20.png)

## Setup
1. Attain an OpenAI API key from https://platform.openai.com/api-keys
2. Configure the .env file at the root of the project:
    ```
    OPENAI_API_KEY=<your api key> 
    ```
3. Setup a Python virtual environment and install the following packages:
    ```
    db-sqlite3        0.0.1
    Flask             3.0.3
    Flask-Cors        4.0.1
    openai            1.33.0
    python-dotenv     1.0.1
    ```
4. Install frontend dependencies 
    ```
    npm install
    ```
5. Run the server in their respective directories  
    ```
    python3 main.py
    npm run dev
    ```
