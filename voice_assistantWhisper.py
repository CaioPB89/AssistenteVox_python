#Usa text to speech e Whisper
import openai
import speech_recognition as SP
import pyttsx3

#key = "" # sua chave API do ChatGPT vai aqui
key = input("Digite a sua chave: ")
openai.api_key = key

personalidade = "personalidade.txt"

with open(personalidade,"r") as file:
    mode = file.read() #leia o arquivo

messages = [
    {"role":"system", "content":f"{mode}"}
]

engine = pyttsx3.init() # inicializa a engine do speech to text
voices = engine.getProperty("voices")

engine.setProperty("voice", "brazil") # 0 para masculino, 1 para feminino

r = SP.Recognizer() # install pyaudio
mic = SP.Microphone(device_index=0) # decide o microfone aqui, 0 para o basico do sistema
r.dynamic_energy_threshold = False #desliga o ajuste de tempo de fala, para o som ambiente não deixa-lo infinito
r.energy_threshold=400

def whisper(waudio): #função do whisper
    with open("speech.wav","wb") as f: #wb é write bytes
        f.write(waudio.get_wav_data())
    speech = open("speech.wav","rb")
    wcompletion = openai.audio.transcriptions.create(
        model = "whisper-1",
        file = speech,
        language = "pt", # qual a linguagem
        response_format="text" #espera o retorno assim
    )
    user_input = wcompletion
    print(user_input)
    return user_input


while True: #para continuar a conversa
    with mic as source:
        print("Escutando...")
        r.adjust_for_ambient_noise(source, duration=0.5)#limita o tempo de ajuste do som background
        waudio=r.listen(source)
        try:
            user_input = whisper(waudio)
            
        except:
            print("tentando")
            continue # fica iterando o try até houvver algo dito
    #user_input = input("Qual a pergunta: ")
    print('Enviando')
    messages.append ({"role":"user","content": user_input}) # append a pergunta do usuario na conversa

    completion = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature=0.8 #aleatoriedade das respostas
    )

    response = completion.choices[0].message.content # retorna a resposta mais recente(choice[0])
    messages.append({"role":"assistant","content":response}) # o append vai guardando a conversa
    print(f"/n{response}/n")
    engine.say(f"{response}")
    engine.runAndWait() # espera a resposta acabar para retornar
    # a transformação do texto em outra linguaguem zoa o entendimento de palavras como firewall