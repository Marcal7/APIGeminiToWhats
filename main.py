
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import time
import urllib
import google.generativeai as genai
import json


from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions

# Configura a API Google Gemini
genai.configure(api_key='Key')
model = genai.GenerativeModel(model_name="gemini-1.5-flash-001")

context_messages = []

chrome_options = ChromeOptions()
chrome_options.headless = False

# Add user data directory to keep the session
user_data_dir = "/Users/55169/PycharmProjects/WhatsIA"
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-running-insecure-content")


def conversaIA(question):
    if question == 'Sair':
        return False
    else:
        response = model.generate_content(question)
        response_dict = response.to_dict()
        response_json = json.dumps(response_dict)
        response_data = json.loads(response_json)
        answer = response_data['candidates'][0]['content']['parts'][0]['text']
        return answer

# Função para pegar a última mensagem recebida
def get_last_message(navegador, mensagem=None):
    while True:
        try:
            mensagem = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tab="3"]'))
            )

            # Verifica se há mensagens e obtém a última
            mensagens = mensagem.find_elements(By.CSS_SELECTOR, 'div.message-in span.selectable-text')

            main_div = navegador.find_element(By.CSS_SELECTOR, 'div#main')
            all_messages = main_div.find_elements(By.CSS_SELECTOR, 'div[role="row"]') #[-1].find_elements(By.CSS_SELECTOR, 'span.selectable-text')[-1]

            last_message_parent = all_messages[-1].find_element(By.CSS_SELECTOR, 'div.message-in')
            return last_message_parent

        except:
            print('Erro ao encontrar a ultima mensagem')
            time.sleep(10)
            get_last_message(navegador)

def enviar(navegador, answer):
    main_div = navegador.find_element(By.CSS_SELECTOR, 'div#main')
    input_box = main_div.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
    input_box.click()

    # send keys to the input box without the emojis
    input_box.send_keys(answer)

    send_button = main_div.find_element(By.CSS_SELECTOR, 'button span[data-icon="send"]')
    send_button.click()


# Configura o navegador
navegador = Chrome(options=chrome_options)
navegador.get("https://web.whatsapp.com/")

# Aguarda o carregamento completo do WhatsApp Web
while len(navegador.find_elements(By.ID, 'side')) < 1:
    time.sleep(1)

# Configura o número e a mensagem
tel = XXXXXXXXXXXX
texto = 'Olá, sou uma IA, e estou aqui para te ajudar, caso precise digite 1'
link = f"https://web.whatsapp.com/send?phone={tel}&text={texto}"
navegador.get(link)

# Aguarda o campo de mensagem carregar e envia a mensagem
try:
    WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.ID, 'side')))
    time.sleep(5)
    botao_enviar = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
    )
    botao_enviar.click()
    print("Mensagem enviada com sucesso!")

except Exception as e:
    print("Ocorreu um erro:", e)


while True:

    last_msg = get_last_message(navegador)

    if last_msg == "1":
        # Envia a pergunta para o usuário
        primeira = "Você ativou a IA, qual sua pergunta?"
        enviar(navegador, primeira)
        time.sleep(5)  # Aguarda a resposta

        nova_pergunta = get_last_message(navegador)

        # Chama a função da IA para obter a resposta
        resposta = conversaIA(nova_pergunta)

        enviar(navegador, resposta)
    else:
        time.sleep(5)
