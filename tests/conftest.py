import sys
import os

# Verifique o caminho adicionado ao sys.path
print("Adicionando o seguinte caminho ao sys.path:")
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Adiciona o diretório src ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
