import os
import subprocess
import shutil

def run_local_with_docker():
    if not os.path.isfile('.env'):
        shutil.copy('.env.example', '.env')
        print(".env example copiado para .env")

    with open('.env', 'r') as file:
        data = file.readlines()

    with open('.env', 'w') as file:
        for line in data:
            file.write(line.replace('DB_HOST=localhost', 'DB_HOST=db'))

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

    subprocess.run(['docker-compose', 'up', '-d', 'db', 'api'])

    try:
        subprocess.run(['docker-compose', 'exec', 'api', 'uvicorn', 'src.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'])
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário. Processo finalizado com sucesso.")

if __name__ == '__main__':
    run_local_with_docker()
