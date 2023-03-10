import openai
import datetime
import mysql.connector
dbc=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='psswd',
    database='Chatbot')
mycursor = dbc.cursor()

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['JAX:', 'USER:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text


if __name__ == '__main__':
    conversation = list()
    #D_t=datetime.datetime.now()
    #mycursor.execute("CREATE TABLE Chat_h (id INT, Speaker VARCHAR(5), TEXT VARCHAR(255)")
    while True:
        user_input = input('USER: ')
        mycursor.execute("INSERT INTO chat_h  (Speaker, TEXT) VALUES (%s,%s)", ('USER',user_input))
        conversation.append('USER: %s' % user_input)#takes input and adds it to memory
        
        text_block = '\n'.join(conversation)#response of the chatbot
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nBOT:'
        response = gpt3_completion(prompt)
        print('BOT:', response)
        conversation.append('BOT: %s' % response)#adds chatbot's answers to the memory
        mycursor.execute("INSERT INTO chat_h  (Speaker, TEXT) VALUES (%s,%s)", ('BOT',response))
        dbc.commit()
        
