import speech_recognition as sr
import requests
import json
import pyttsx3
import webbrowser
import os


def func(answer):
    
    with microphone as source:
        audio = recognizer.listen(source)
    try:
        text = list(map(lambda x: x.lower(), recognizer.recognize_google(audio, language='en').split()))
    except sr.exceptions.UnknownValueError:
        text = ''
    print('You just said: ' + ' '.join(text) + '\n')
    if 'find' in text:
        try:
            answer = json.loads(requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{text[text.index('find') + 1]}').content)
            print(f"""These are results of your request 
word: {answer[0]['word']} 
definition: {answer[0]['meanings'][0]['definitions'][0]['definition']}
part of speech: {answer[0]['meanings'][0]['partOfSpeech']}""" + '\n')
            tts.say(f"""These are results of your request 
                    word {answer[0]['word']} 
                    definition {answer[0]['meanings'][0]['definitions'][0]['definition']}
                    part of speech {answer[0]['meanings'][0]['partOfSpeech']}""")
            tts.runAndWait()
        except Exception:
            print('Something went wrong')
            tts.say('Something went wrong')
            tts.runAndWait()
    elif 'save' in text:
        if not answer:
            print('No recent words' + '\n')
            tts.say('No recent words')
            tts.runAndWait()
        else:
            with open(f'words\\{answer[0]['word']}.txt', encoding='utf-8', mode='w') as file:
                file.write(json.dumps(answer))
            print(f'Information on word {answer[0]['word']} saved' + '\n')
            tts.say(f'Information on word {answer[0]['word']} saved')
            tts.runAndWait()
    elif 'open' in text:
        if not answer:
            print('No recent words' + '\n')
            tts.say('No recent words')
            tts.runAndWait()
        else:
            for source in answer[0]['sourceUrls']:
                webbrowser.open(source)
    elif 'meaning' in text:
        if not answer:
            print('No recent words' + '\n')
            tts.say('No recent words')
            tts.runAndWait()
            
        else:
            print(f'The word {answer[0]['word']} means {answer[0]['meanings'][0]['definitions'][0]['definition']}' + '\n')
            tts.say(f'The word {answer[0]['word']} means {answer[0]['meanings'][0]['definitions'][0]['definition']}')
            tts.runAndWait()
            
    elif 'example' in text:
        if not answer:
            print('No recent words' + '\n')
            tts.say('No recent words')
            tts.runAndWait()
            
        else:
            examples = list(filter(lambda x: x != '', map(lambda x: x['example'] if 'example' in x.keys() else '', answer[0]['meanings'][0]['definitions'])))
            if len(examples) != 0:
                print(examples[0] + '\n')
                tts.say(examples[0])
                tts.runAndWait()
            else:
                print('No examples stated\n')
                tts.say('No examples stated\n')
                tts.runAndWait()
            
    elif 'part' in text:
        if not answer:
            print('No recent words' + '\n')
            tts.say('No recent words')
            tts.runAndWait()
            
        else:
            print(f'The word {answer[0]['word']} is {answer[0]['meanings'][0]['partOfSpeech']}')
            tts.say(f'The word {answer[0]['word']} is {answer[0]['meanings'][0]['partOfSpeech']}')
            tts.runAndWait()
    elif 'synonyms' in text:
        if not answer:
            print('No recent words' + '\n')
            tts.say('No recent words')
            tts.runAndWait()
            
        else:
            if len(answer[0]['meanings'][0]['synonyms']) != 0:
                print(f'Synonyms of the word {answer[0]['word']} are:' + '\n')
                tts.say(f'Synonyms of the word {answer[0]['word']} are')
                tts.runAndWait()
                
                for word in answer[0]['meanings'][0]['synonyms']:
                    print(word)
                    tts.say(word)
                    tts.runAndWait()
                    
            else:
                print('There are no synonyms stated' + '\n')
                tts.say('There are no synonyms stated')
                tts.runAndWait()
    elif 'load' in text:
        word = text[text.index('load') + 1]
        try:
            with open(f'words\\{word}.txt', mode='r') as file:
                answer = json.loads(file.read())
        except Exception:
            print('Didn\'t find this word')
            tts.say('Didn\'t find this word')
            tts.runAndWait()
    elif 'stop' in text:
        print('Goodbye!')
        tts.say('Goodbye!')
        tts.runAndWait()
        quit()
    elif 'help' in text:
        print("""These are available commands:
find <word> - search in dictionary
save - save info on current word in a file
open - open word's page in browser
meaning - read word's definition
example - read an example of word's usage
part - read word's part of speech
synonyms - read known word's synonyms
stop - quit program
help - show this message""")
                
    elif len(text) != 0:
        print('Didn\'t hear any known commands' + '\n')
        tts.say('Didn\'t hear any known commands')
        tts.runAndWait()
        
    return answer
    # except Exception:
    #     print('Something went wrong\n')
    #     tts.say('Something went wrong')
    #     tts.runAndWait()
    #     return answer


if __name__ == '__main__':
    print('Loading...')
    try:
        os.makedirs(os.getcwd() + '\\words')
    except FileExistsError:
        # directory already exists
        pass
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = 1)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
    tts = pyttsx3.init()
    answer = None
    print('You can now speak. To see available commands say <help>')
    tts.say('You can now speak')
    tts.runAndWait()
    
    while True:
        answer = func(answer)