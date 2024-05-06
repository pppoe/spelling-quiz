## Example

[Quiz of 04292024](https://pppoe.github.io/spelling-quiz/04292024.html)

## README

This repo uses OpenAI's APIs to prepare spelling quiz for kids. You need to get an API key from OpenAI by yourself.

Assume your API key is stored in the file named ``secrets/OPENAI``, launch the script:

    python3 add_quiz.py --openai_token `cat secrets/OPENAI`  --name 04292024 
    
A html file named ``docs/04292024.html`` will be generated. Keys are under ``keys/04292024.txt``.

    python3 -m http.server -d docs --bind 0.0.0.0 8000

The webpage can be accessed via the URL: ``http://localhost:8000/04292024.html``
