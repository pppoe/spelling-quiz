import json, tqdm
import argparse
import requests
from datetime import datetime
import traceback
from openai import OpenAI
import os

if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--openai_token', type=str, default=None, required=True, help='OpenAI API key')
    args.add_argument('--name', required=False, type=str, default=None, help='quiz set name (use date by default)')
    args = args.parse_args()

    english_words_raw = input("English Words:")
    chinese_characters_raw = None#input("Chinese Characters:") # disabled for now, OpenAI's tts for Chinese does not work well
    english_sentences_raw = None#input("English Sentences:") # TBD

    if args.name is None: args.name = datetime.now().strftime('%Y%m%d')

    fpath = f'quiz/{args.name}.json'
    audio_root = f'docs/audio/'

    client = OpenAI(api_key=args.openai_token)
    res = {}

    if chinese_characters_raw is not None:
        prompt = f'''
            I am giving you a list of Chinese characters. Please organize them into a JSON file. For each Chinese character, make it a dict of the character and an example sentence using the character.
            The list of Chinese character is: {chinese_characters_raw}
            The format of the output JSON file is:
            ''' + json.dumps({ "ChineseCharacters": [ { "character":"","example_phrase":""}]})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        res.update(json.loads(response.choices[0].message.content))
    if english_words_raw is not None:
        prompt = f'''
            I am giving you a list of English words. Please organize them into a JSON file. For each English word, make it a dict of the word and an example sentence using the word. \n"
            The list of English words is: {english_words_raw}
            The format of the output JSON file is:
            ''' + json.dumps({ "EnglishWords": [ { "word":"","example_phrase":""}]})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        res.update(json.loads(response.choices[0].message.content))
    json.dump(res, open(fpath,'w'))
    res = json.load(open(fpath))
    audio_gen_tasks = []
    # for val in res.get("ChineseCharacters",[]):
        # ch = val["character"]
        # prompt = f'开始听写............... {val["character"]} ............ {val["example_phrase"]} ...'
        # audio_file_path = f'{audio_root}/zh_{ch}.mp3'
        # audio_gen_tasks.append([prompt, audio_file_path])

    for val in res.get("EnglishWords",[]):
        ch = val["word"]
        prompt = f'Spell this word ...... {val["word"]} ... as in {val["example_phrase"]}.'
        audio_file_path = f'{audio_root}/en_{ch}.mp3'
        audio_gen_tasks.append([prompt, audio_file_path])

    voice_names = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    voice_model = "tts-1"
    audio_file_names = []
    audio_keys = []
    for idx,[prompt, audio_file_path] in tqdm.tqdm(enumerate(audio_gen_tasks)):
        with client.audio.speech.with_streaming_response.create(
            model=voice_model,
            voice=voice_names[idx%len(voice_names)],
            input=prompt
        ) as response:
            response.stream_to_file(audio_file_path)
            audio_keys.append(prompt)
            audio_file_names.append(os.path.basename(audio_file_path))

    ## generate web page and key file
    key_fpath = f'keys/{args.name}.txt'
    with open(key_fpath, 'w') as f:
        f.write('\n'.join(audio_keys) + '\n')
    page_fpath = f'docs/{args.name}.html'
    lines = [l.replace('__NAME__',args.name) for l in open('_template.html').readlines()]
    content_line_ind = [l.strip().rstrip() for l in lines].index('__CONTENT__')
    lines[content_line_ind] = ','.join([f"'{k}'" for k in audio_file_names]) + '\n'
    minified = ''.join(lines) + '\n'
    with open(page_fpath, 'w') as f:
        f.write(minified)
    print (page_fpath)

    ## add to quiz_list.txt if not already there
    quiz_list_fpath = 'docs/quiz_list.txt'
    existing_quiz_list = [l.rstrip() for l in open(quiz_list_fpath).readlines()]
    if os.path.basename(page_fpath) not in existing_quiz_list:
        with open(quiz_list_fpath, 'a') as f:
            f.write(os.path.basename(page_fpath) + '\n')
