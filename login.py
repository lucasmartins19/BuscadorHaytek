import PySimpleGUI as sg
import keyring

def iniciar_login():
    dados = pegar_dados_login()
    
    layout = [
        [sg.Text("Insira seu login HayTek", key="texto")],
        [sg.Input("Email", key="email", justification="c", text_color="grey", size=30)],
        [sg.Input("Senha", key="password", justification="c", text_color="grey", size=30)],
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

    window.close()

def pegar_dados_login():
    try:
        return keyring.get_password("BuscadorHayTek", 'email'), keyring.get_password("BuscadorHayTek", 'senha')
    except:
        return None
    
    keyring.set_password(service_id, 'email', 'exemplo@email.com')
keyring.set_password(service_id, 'senha', 'senha_secreta')
