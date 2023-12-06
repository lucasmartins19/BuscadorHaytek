import login
import requests
import PySimpleGUI as sg
from concurrent.futures import ThreadPoolExecutor


def main():
    empresas = usuario.verificar_empresas()
    empresas = [f"{empresa}: {empresas[empresa]['Nome']}" for empresa in empresas]
    usuario.codigo_empresa = empresas[0].split(":")[0]

    layout_principal = [
        [sg.Text("Empresa:"), sg.Combo(values=empresas, default_value=empresas[0], key="empresa", enable_events=True, readonly=True, size=(30))]
    ]
    window_principal = sg.Window("BuscadorHayTek", layout=layout_principal)
    while True:
        event, values = window_principal.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "empresa":
            usuario.codigo_empresa = values['empresa'].split(":")[0]

    window_principal.close()

    print(usuario.extrair_dados_pedidos())

class Usuario:
    def __init__(self, dados_login):
        self.id = dados_login['ID']
        self.token = dados_login['TOKEN']
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Token": self.token,
        "Iduser": str(self.id)}

    def requisicoes_get(self, url):
        try:
            print("OI")
            return requests.get(url, headers=self.headers)
        except:
            return None
        
    def verificar_empresas(self):
        requisicao = self.requisicoes_get("https://api.haytek.com.br/api/v1/user/legacy/users/24342/config")
        if requisicao is not None:
            empresas = requisicao.json()['RESULT']['COMPANIES']
            empresas_dict = dict()
            for empresa in empresas:
                empresas_dict[empresa['A1_COD']] = {}
                empresas_dict[empresa['A1_COD']]['Nome'] = empresa['A1_NOME']
            return empresas_dict
        return None
    
    def extrair_dados_pedidos(self):
        pedidos = self.lista_pedidos()
        if pedidos is not None:
                with ThreadPoolExecutor(max_workers=30) as pool:
                    pool.map(main, [])
        
    def lista_pedidos(self):
        try:
            json = {
                "id_ini": 0,
                "id_qtd": 0,
                "status": "T",
                "data_ini": "19000101",
                "data_fim": "21000101",
                "companies": [self.codigo_empresa]
            }
            pedidos = requests.post(f"https://api.haytek.com.br/v1.1/orders/history/v2/{self.codigo_empresa}", headers=self.headers, json=json).json()['RESULT']
            return [pedido['Pedhtk'] for pedido in pedidos]
        except:
            return None

if __name__ == "__main__":
    dados_login = login.iniciar_login()
    if dados_login is not None:
        usuario = Usuario(dados_login)
        main()