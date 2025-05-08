from validate_docbr import CPF

def is_valid_cpf(cpf: str) -> bool:
    cpf_instance = CPF()
    return cpf_instance.validate(cpf)
