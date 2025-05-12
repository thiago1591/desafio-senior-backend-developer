import logging
import sys

def setup_logger(name: str):
    """
    Configura o logger. No futuro, poderá ser trocado por outra ferramenta
    (Sentry, Logstash, Loki, etc.), sem mudar o código em todos os lugares.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO) 
    
    return logger


logger = setup_logger("myapp")
