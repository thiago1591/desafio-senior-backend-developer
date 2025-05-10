import os
import subprocess

def run_prod():
    if not os.path.isdir('venv'):
        print("Criando o ambiente virtual...")
        subprocess.run(['python', '-m', 'venv', 'venv'])
        print("Ambiente virtual criado.")
    else:
        print("Ambiente virtual já existe.")

    if os.name == 'posix': 
        if os.environ.get('VIRTUAL_ENV') is None:
            print("Ativando o ambiente virtual...")
            subprocess.run(['source', 'venv/bin/activate'], shell=True)
        else:
            print("O ambiente virtual já está ativado.")
    else:
        if os.environ.get('VIRTUAL_ENV') is None:
            print("Ativando o ambiente virtual...")
            subprocess.run(['venv\\Scripts\\activate'], shell=True)
        else:
            print("O ambiente virtual já está ativado.")

    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    subprocess.run(['docker-compose', 'up', '-d', 'db', 'api_prod'])

    print("Ambiente de produção iniciado.")

if __name__ == '__main__':
    run_prod()
