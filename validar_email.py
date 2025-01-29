import re  # Importa o módulo de expressões regulares

def validar_email(email):
    """
    Função para validar um endereço de e-mail.

    Parâmetros:
    - email (str): O endereço de e-mail que será validado.

    Retorna:
    - bool: True se o e-mail for válido, False caso contrário.
    """
    # Definindo o padrão de uma expressão regular para e-mails válidos
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Utiliza re.match para comparar o e-mail com o padrão
    if re.match(padrao, email):
        return True
    else:
        return False

def main():
    """
    Função principal para testar a validação de e-mails.
    """
    print("Validador de E-mails\n")
    while True:
        # Solicita ao usuário um endereço de e-mail
        email = input("Digite um endereço de e-mail (ou 'sair' para terminar): ")
        
        # Permite sair do loop ao digitar 'sair'
        if email.lower() == 'sair':
            print("Encerrando o validador. Até breve!")
            break
        
        # Valida o e-mail e informa o resultado ao usuário
        if validar_email(email):
            print(f"O e-mail '{email}' é válido!\n")
        else:
            print(f"O e-mail '{email}' é inválido. Tente novamente.\n")

# Garantir que o script seja executado apenas se chamado diretamente
if __name__ == "__main__":
    main()
