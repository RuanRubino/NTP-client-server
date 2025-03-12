# NTP Client-Server

Este projeto implementa um servidor e um cliente NTP (Network Time Protocol) para sincronização de tempo entre máquinas. A comunicação é feita via UDP e inclui autenticação HMAC-SHA256 para garantir a integridade e autenticidade das mensagens.

## Estrutura do Projeto

- `NTPservidor.py`: Implementação do servidor NTP.
- `NTPcliente.py`: Implementação do cliente NTP.

## Requisitos

- Python 3.x
- Bibliotecas: `socket`, `struct`, `time`, `hmac`, `hashlib`

## Como Executar

### Servidor

1. Navegue até o diretório do projeto:
    ```sh
    cd /home/seu_usuario/Redes/NTP-client-server
    ```

2. Execute o servidor:
    ```sh
    python3 NTPservidor.py
    ```

### Cliente

1. Navegue até o diretório do projeto:
    ```sh
    cd /home/seu_usuario/Redes/NTP-client-server
    ```

2. Execute o cliente:
    ```sh
    python3 NTPcliente.py
    ```

3. Insira o IP do servidor NTP quando solicitado.

## Funcionamento

### Servidor

- O servidor escuta na porta 123 por pacotes NTP.
- Ao receber um pacote, verifica a autenticação e processa a requisição.
- Envia uma resposta com os timestamps de recepção e transmissão.

### Cliente

- O cliente envia um pacote NTP para o servidor.
- Recebe a resposta do servidor e verifica a autenticação.
- Calcula o offset e o delay entre o cliente e o servidor.

## Autenticação

- A autenticação é feita usando HMAC-SHA256.
- A chave pré-compartilhada (`AUTH_KEY`) e o identificador da chave (`KEY_ID`) são usados para gerar e verificar o digest.

## Cálculo de Offset e Delay

- **Offset**: Estima a diferença de tempo entre o cliente e o servidor.
- **Delay**: Estima o tempo de ida e volta da mensagem entre o cliente e o servidor.

## Exemplo de Saída

```
Digite o IP do servidor NTP: 127.0.0.1
Servidor: Timestamp NTP: 3950383399 segundos e 3654799360 fração
Servidor: Tempo Unix: 1741394599 segundos
Servidor: Tempo UTC: Fri Mar  7 21:43:19 2025
timeClientRecive:  3950383399.8510275
timeClientsend  :  3950383399.850495
timeServerRecivce:  3950383399.8509455
timeServerTransmit :  3950383399.8509493
Offset:0.0001862049102783203
Delay:0.0005288124084472656
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a licença Unlicense. Veja o arquivo LICENSE para mais detalhes.
