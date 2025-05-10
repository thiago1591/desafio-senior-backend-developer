from validate_docbr import CPF
import re
import unidecode
from typing import List, Optional
from difflib import SequenceMatcher

def format_user_input(step: int, message: str) -> bool:
    print(step)
    #nos steps intermediarios o usuário digita informações que não são o número da intenção
    if step is not 0: return message
    
    #no primeiro step precisa ser um valor numérico referente ao número da intention
    digits = ''.join(filter(str.isdigit, message))

    return int(digits)

def match_question(user_input: str, known_questions: List[dict], min_common_words: int = 2, min_similarity: float = 0.8) -> Optional[str]:
    #tenta encontrar a melhor correspondência entre a pergunta do usuário e perguntas conhecidas
    #implementação simplificada e limitada, sem uso de nlp
    user_tokens = tokenize(user_input)

    for entry in known_questions:
        question_tokens = tokenize(entry["pergunta"])
        if count_common_words(user_tokens, question_tokens) >= min_common_words:
            return entry["resposta"]

    for entry in known_questions:
        similarity = SequenceMatcher(None, normalize(user_input), normalize(entry["pergunta"])).ratio()
        if similarity >= min_similarity:
            return entry["resposta"]

    return None

def normalize(text: str) -> str:
    text = unidecode.unidecode(text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def tokenize(text: str) -> List[str]:
    return normalize(text).split()

def count_common_words(a: List[str], b: List[str]) -> int:
    return len(set(a) & set(b))

def get_mock_questions():
    return [
        {"pergunta": "como verificar saldo", "resposta": "Para verificar seu saldo, digite 1"},
        {"pergunta": "como carregar créditos no transporte público", "resposta": "Você pode carregar créditos no transporte público através da nossa plataforma, acessando o menu 'Créditos'."},
        {"pergunta": "como adicionar documentos à carteira digital", "resposta": "Você pode adicionar documentos digitalmente através da opção 'Adicionar Documento' no seu perfil."},
        {"pergunta": "o que é a carteira digital da prefeitura", "resposta": "A carteira digital da Prefeitura do Rio de Janeiro é uma plataforma onde você pode armazenar e gerenciar seus documentos digitais e créditos de transporte."}
    ]
