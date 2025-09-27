from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_steam():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Configuração do Selenium para rodar sem abrir o navegador (headless)
    options = Options()
    options.add_argument("--headless")  # Executa sem abrir a janela do navegador

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://store.steampowered.com/login/')

        # Espera explícita para garantir que os campos de login estejam visíveis
        wait = WebDriverWait(driver, 20)

        # Espera até que o campo de nome de usuário esteja visível
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[1]/input')))
        
        # Espera até que o campo de senha esteja visível
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[2]/input')))
        
        # Espera até que o botão de login esteja visível
        sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[4]/button')))

        # Preenche os campos com as credenciais fornecidas
        username_field.send_keys(username)
        password_field.send_keys(password)
        sign_in_button.click()

        # Espera para garantir que a página de login foi carregada
        time.sleep(5)

        # Verifica se aparece a mensagem de erro (exemplo de XPath para erro)
        try:
            error_message = driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[3]/div')
            return jsonify({"status": "failure", "message": "Nome de usuário ou senha incorretos."})
        except:
            # Caso não encontre a mensagem de erro, assume que o login foi bem-sucedido
            if "store.steampowered.com" in driver.current_url:
                return jsonify({"status": "success", "message": "Login bem-sucedido!"})

        return jsonify({"status": "failure", "message": "Falha no login. A senha ou o usuário estão incorretos."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

