import PySimpleGUI as sg
import keyring
import requests

def iniciar_login():
    email, senha = pegar_dados_login()

    layout = [
        [sg.Text("Insira seu login HayTek", key="texto")],
        [sg.Input("Email" if email is None else email, key="email", justification="c", text_color="grey", size=30)],
        [sg.Input("Senha" if senha is None else senha, key="password", password_char="" if senha is None else "*", justification="c", text_color="grey", size=30)],
        [sg.Text(visible=False, key="erro", text_color="red")],
        [sg.Button("Entrar"), sg.Button("Cancelar")]]
    
    window = sg.Window(title="Login", layout=layout, finalize=True)
    window['texto'].set_focus()
    window['email'].bind("<FocusIn>", "-foco")
    window['email'].bind("<FocusOut>", "-foco_saiu")
    window['password'].bind("<FocusIn>", "-foco")
    window['password'].bind("<FocusOut>", "-foco_saiu")

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "email-foco" and values['email'] == "Email":
            window['email'].update(value="")
        elif event == "email-foco_saiu" and values['email'] == "":
            window['email'].update(value="Email")

        elif event == "password-foco" and values['password'] == "Senha":
            window['password'].update(value="", password_char="*")
        elif event == "password-foco_saiu" and values['password'] == "":
            window['password'].update(value="Senha", password_char="")

        elif event == "Entrar":
            if values['email'] not in ("", "Email") and values['password'] not in ("", "Senha"):
                resultado = validar_login(values['email'], values['password'])
                if isinstance(resultado, dict):
                    window.close()
                    return resultado
                else:
                    window['erro'].update(value=resultado, visible=True)

    window.close()

def pegar_dados_login():
    try:
        return keyring.get_password("BuscadorHayTek", 'email'), keyring.get_password("BuscadorHayTek", 'senha')
    except:
        return None, None
    

def validar_login(email, senha):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    json = {
        "email": email,
        "password": senha}

    try:
        login = requests.post("https://api.haytek.com.br/api/v1/site-auth-api/user/login", headers=headers, json=json).json()
        if "token" in login:
            keyring.set_password("BuscadorHayTek", 'email', email)
            keyring.set_password("BuscadorHayTek", 'senha', senha)
            return {"ID": login['userId'], "TOKEN": login['token']}
        
        elif "statusCode" in login:
            if login['message'] == "invalid password":
                return "Senha incorreta."
            elif login['message'] == "user":
                return "Usuário não encontrado."
    except:
        return "Erro desconhecido."

