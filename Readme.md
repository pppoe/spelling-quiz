## Blog Post

[Spelling Test](https://blog.haoxiang.org/2024/05/spelling-test/)

<img src="https://raw.githubusercontent.com/pppoe/images-repo/main/blog/misc/spelling-test-post.webp" width="512"/>


## Example

[Quiz of 04292024](https://pppoe.github.io/spelling-quiz/04292024.html)

## README

This repo uses OpenAI's APIs to prepare spelling quiz for kids. You need to get an API key from OpenAI by yourself.

Assume your API key is stored in the file named ``secrets/OPENAI``, launch the script:

    python3 add_quiz.py --openai_token `cat secrets/OPENAI`  --name 04292024 

You will be prompted to give a list of words:

    English Words:presale, preview, repaint, repeat, honor,unpack, unfinished, thankful, painless, useful
    
A html file named ``docs/04292024.html`` will be generated.

    python3 -m http.server -d docs --bind 0.0.0.0 8000

The webpage can be accessed via the URL: ``http://localhost:8000/04292024.html`` or lively via [Quiz of 04292024](https://pppoe.github.io/spelling-quiz/04292024.html)
