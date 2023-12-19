#Digita e responde com voz
import openai
import pyttsx3

#key = "" # sua chave API do ChatGPT vai aqui
key = input("Digite a sua chave: ")
openai.api_key = key

personalidade = "personalidade.txt" # use este arquivo para criar a personalidade para o chat

with open(personalidade,"r") as file:
    mode = file.read() #leia o arquivo personalidade

messages = [
    {"role":"system", "content":f"{mode}"}
]
engine = pyttsx3.init() # inicializa a engine do speech to text
engine.setProperty("voice","brazil")
while True: #para continuar a conversa

    user_input = input("Qual a pergunta: ")
    print("Enviando")
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
