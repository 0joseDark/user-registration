# user registration and e-mail server
- registo e-mail e de utilizadores
### 1. Instalar o Flask:
```sh
pip install Flask
```
### Explicação:
1. **Importação de módulos**:
   - `Flask`, `request` e `jsonify` são importados do Flask.
   - `re` é usado para operações com expressões regulares para validar a senha.

2. **Função de validação de senha**:
   - `is_strong_password` verifica se a senha atende aos critérios: pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial.

3. **Endpoint de registo**:
   - A rota `/signup` lida com pedidos POST.
   - Extrai `username` e `password` do JSON recebido.
   - Verifica se ambos são fornecidos.
   - Utiliza `is_strong_password` para validar a senha.
   - Se a senha não for forte o suficiente, retorna um erro 400.
   - Se for válida, pode-se adicionar código para guardar o utilizador na base de dados e retorna-se uma mensagem de sucesso (201).

4. **Executar a aplicação**:
   - A aplicação corre no modo debug, útil para desenvolvimento.

Este exemplo fornece um endpoint básico de registo com validação de senha forte. Pode melhorá-lo adicionando recursos como verificação de email, hashing de senha e integração com uma base de dados para armazenar os detalhes dos utilizadores.
### e-mail
### Explicação do Código

1. **Importação de Módulos**:
   - O módulo `re` é usado para trabalhar com expressões regulares. Ele é essencial para criar padrões que podem ser usados para identificar e validar formatos de texto, como endereços de e-mail.

2. **Função `validar_email`**:
   - Esta função recebe um endereço de e-mail como entrada.
   - O padrão `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` descreve o formato de um e-mail válido:
     - `^[a-zA-Z0-9._%+-]+`: O início do e-mail deve conter caracteres alfanuméricos ou os símbolos `._%+-`.
     - `@[a-zA-Z0-9.-]+`: O domínio (após o `@`) pode conter caracteres alfanuméricos, pontos ou hifens.
     - `\.[a-zA-Z]{2,}$`: O TLD (como `.com`, `.br`) deve conter pelo menos dois caracteres alfabéticos.
   - A função usa `re.match` para verificar se o e-mail combina com o padrão e retorna `True` ou `False`.

3. **Função `main`**:
   - É a interface do usuário para testar a validação.
   - Solicita entradas ao usuário em um loop contínuo até que ele digite "sair".
   - Exibe mensagens claras indicando se o e-mail fornecido é válido ou não.

4. **Estrutura `if __name__ == "__main__"`**:
   - Garante que o script só seja executado se chamado diretamente, prevenindo a execução automática ao ser importado como módulo.
---
### Testes de Exemplos

- **Entrada**: `teste@exemplo.com`
  - **Saída**: O e-mail é válido.
- **Entrada**: `email_incorreto@exemplo`
  - **Saída**: O e-mail é inválido.
---
### Estrutura do Servidor de E-mail:
1. **Servidor Flask**  
   - Incluirá uma janela gráfica com botões para "Ligar Servidor", "Desligar" e "Sair".
   - Servirá páginas web para interação com os e-mails.

2. **Funcionalidades da Página Web:**  
   - Caixa de entrada, rascunhos, enviados, spam, lixeira.
   - Possibilidade de mover, arquivar, apagar e-mails.
   - Composição e envio de novos e-mails.
   - Validação de contas via link.
   - Anexos para e-mails.

3. **Autenticação e Registo:**  
   - Integração do sistema de registo e validação de e-mails.
   - Base de dados para armazenar utilizadores e e-mails.

Aqui está o início do servidor de e-mail em Flask. Ele inclui:
- Uma interface gráfica para iniciar e desligar o servidor.
- Um banco de dados SQLite para armazenar utilizadores e e-mails.
- Um endpoint `/signup` para registo de utilizadores com validação de e-mail.

Próximos passos:
- index.html – Página inicial com login e registo.
- dashboard.html – Interface principal com caixa de entrada, opções de e-mail.
- compose.html – Página para compor e enviar e-mails.
