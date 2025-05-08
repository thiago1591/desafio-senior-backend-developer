import os
from fastapi import requests


def send_email(subject, recipient_email, body):
    #envia email aqui
    
    response = {
        "status_code": 200
    }
    
    if response.status_code == 200:
        print("Email enviado com sucesso!")
        return True
    else:
        print("Falha ao enviar email.")
        print("Status:", response.status_code)
        print("Detalhes:", response.text)
        return False