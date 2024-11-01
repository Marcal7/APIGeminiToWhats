from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import time
import google.generativeai as genai
import json

# Configura a API Google Gemini
genai.configure(api_key='AIzaSyCUNeoSQTLsWoQIBqng14e-bfHT6Sk95pI')
model = genai.GenerativeModel(model_name="gemini-1.5-flash-001")

def conversaIA(question):
    #Conversa com a IA
    if question == 'Sair':
        return False
    else:
        response = model.generate_content(question)
        response_dict = response.to_dict()
        response_json = json.dumps(response_dict)
        response_data = json.loads(response_json)
        answer = response_data['candidates'][0]['content']['parts'][0]['text']
        return answer


def get_last_message(nav_last):
    # Função para pegar a última mensagem recebida
    try:
        post = nav_last.find_element(By.CLASS_NAME, '_3_7SH')
        last = len(post) - 1
        x = post[last]
        msg = x.find_element(By.CSS_SELECTOR, "span.selectable-text").text
        return msg

    except (NoSuchElementException, IndexError) as e:
        print("Erro ao obter a última mensagem:", e)
        return None

'''    try:
        # Aumenta o tempo de espera
        time.sleep(3)

        # Seleciona o elemento pai da mensagem
        mensagem_pai = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[16]/div/div/div[1]'))
        )

        # Verifica se há mensagens e obtém a última
        mensagens = mensagem_pai.find_elements(By.XPATH, './/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span')
        if mensagens:
            ultima_msg = mensagens[-1].text
            return ultima_msg
        else:
            print("Não há mensagens novas.")
    except (NoSuchElementException, IndexError) as e:
        print("Erro ao obter a última mensagem:", e)
        return None'''

def send(nav_send, answer_send):
    #Função para enviar a ultima mensagem
    main_div = nav_send.find_element(By.CSS_SELECTOR, 'div#main')
    input_box = main_div.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
    input_box.click()

    input_box.send_keys(answer_send)

    send_button = main_div.find_element(By.CSS_SELECTOR, 'button span[data-icon="send"]')
    send_button.click()


# Configura o navegador
navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")
navegador.implicitly_wait(15)

# Aguarda o carregamento completo do WhatsApp Web
while len(navegador.find_elements(By.ID, 'side')) < 1:
    time.sleep(1)

# Configura o número e a mensagem
tel = 5514991816253
texto = 'Olá, sou uma IA, e estou aqui para te ajudar, caso precise digite 1'
link = f"https://web.whatsapp.com/send?phone={tel}&text={texto}"
navegador.get(link)

# Aguarda o campo de mensagem carregar e envia a mensagem
try:
    # Aguarda o carregamento
    while len(navegador.find_elements(By.ID, 'side')) < 1:
        time.sleep(1)
    botao_enviar = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
    )
    botao_enviar.click()
    print("Mensagem de < oi > enviada com sucesso")

except Exception as e:
    print("Ocorreu um erro ao enviar a primeira mensagem:", e)

while True:
    last_msg = get_last_message(navegador)

    if last_msg == "1":
        # Envia a pergunta para o usuário
        first_msg = "Você ativou a IA, qual sua pergunta?"
        send(navegador, first_msg)
        time.sleep(5)  # Aguarda a resposta

        while True:
            new_question = get_last_message(navegador)

            # Chama a função da IA para obter a resposta
            request = conversaIA(new_question)

            send(navegador, request)
            time.sleep(5)  # Aguarda a resposta

    else:
        time.sleep(5)
        print('Esperando o 1')