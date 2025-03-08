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
    cd /home/arthur_angelo/Redes/NTP-client-server
    ```

2. Execute o servidor:
    ```sh
    python3 NTPservidor.py
    ```

### Cliente

1. Navegue até o diretório do projeto:
    ```sh
    cd /home/arthur_angelo/Redes/NTP-client-server
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
Digite o IP do servidor NTP (pressione Enter para usar o servidor oficial do NTP.br): 
Servidor: Timestamp NTP: 3950382630 segundos e 4020537344 fração
Servidor: Tempo Unix: 1741393830 segundos
Servidor: Tempo UTC: Fri Mar  7 21:30:30 2025
timeClientRecive:  3950382630.936173
timeClientsend  :  3950382630.9358034
timeServerRecivce:  3950382630.936103
timeServerTransmit :  3950382630.9361043
Offset:0.0002307891845703125
Delay:0.0003681182861328125
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a licença Unlicense. Veja o arquivo LICENSE para mais detalhes.
