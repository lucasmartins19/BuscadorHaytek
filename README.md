# Script Python com Interface Gráfica para a API da Haytek

## Descrição

Este repositório contém um script Python com interface gráfica que se conecta diretamente à API da empresa Haytek. O script fornece funcionalidades como buscar um serviço específico dentre o histórico de pedidos e validar através da dioptria em qual lente monofocal acabada existe disponibilidade.

## Requisitos

- Python 3.x
- Bibliotecas Python: `requests`, `PySimpleGUI`, `keyring`

## Autenticação

O script utiliza autenticação direta para se conectar à API da Haytek. As credenciais de autenticação são as mesmas utilizadas no site e devem ser inseridas na interface gráfica ao executar o script.

## Funcionalidades

### Buscar Serviço Específico

O script permite ao usuário buscar um serviço específico dentre o histórico de pedidos. O usuário poderá realizar o download de todos os pedidos realizados por sua empresa e filtrar com base em qualquer dos conteúdos das colunas disponíveis.

### Validar Disponibilidade de Lente Monofocal

O script também permite ao usuário validar a disponibilidade de uma lente monofocal de uma dioptria específica. O usuário pode inserir a dioptria na interface gráfica e o script verificará em qual lente monofocal acabada a dioptria está disponível.

## Uso

Para executar o script, navegue até o diretório que contém o script e execute o seguinte comando no terminal:

```bash
python main.py
```

## Motivação

A motivação da criação desse script é para automatizar processos que deveriam ser feitos manualmente utilizando o website diretamente.

