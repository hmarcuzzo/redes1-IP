<!-- Este projeto pode ser encontrado no GitHub atráves deste link: https://github.com/hmarcuzzo/redes1_IP -->

# Conceitos da implementação

Este trabalho consiste em obter a partir de um Endereço de IP e uma Máscara de Rede as seguintes etapas:
 * validar se esses IPs estão corretos
 
 * obter a quantidade de Bits de rede, Bits de host e quantos Host podem existir dentro da rede

 * a que classe pertence este IP
 
 * qual é o IP que representa o IP de Rede e o de Broadcast
 
 * exibir quais são as faixas de IPs livre (inicio e fim)      
 
 * E dizer se o IP em questão é reservado ou não, no caso afirmativo dizer para qual finalidade.          

# Como compilar

python3 main.py input.json output.json

* main.py - É o código que ira pegar o IP e a Máscara de IP que estaram no input.json e gerará todas as informações a respeiteo da rede em um arquivo JSON de saida

* input.json - O arquivo que conterá o IP que deseja testar e também a Máscara da Rede

    * Obs - pode ser passado qual quer arquivo de parâmetro, desde que seja um arquivo JSON e que siga as especificações dadas de exemplo

* output.json - O arquivo onde será escrito as informações de saida

    * Obs - Em caso de auxência deste parâmetro será tomado como padrão o nome "output.json"

# Como executar

Para alterar a entrada deve-se criar um novo arquivo JSON que siga estes padrões:

    { 
    "ipAddr": "XXX.XXX.XXX.XXX", 
    "netMask": "YYY.YYY.YYY.YYY"
    }

* XXX - representa o Endereço de IP
* YYY - representa a Máscada de IP

# Bibliotecas usadas (as não padrões)

* sys - da acesso à variaveis usadas pelo terminal e para funções que interagem diretamente com ele. Neste projeto foi utilizada apenas para pegar variáveis por linha de comando

* json - permite importar e exportar configurações de/em arquivos json

* deepcopy from copy - permite fazer cópia profundas de variaveis

# Exemplo de uso

Arquivo input.json de entrada:
```
{
    "ipAddr": "192.168.0.1",
    "netMask": "255.255.255.0"
}
```

Entrada do terminal:
```
python3 main.py input.json output.json
```

Saida do terminal:
```
Bits de rede: 24
Bits de host: 8
Hosts na rede: 254
Classe: C
Ip da rede: 192.168.0.0
Ip de broadcast: 192.168.0.255
Faixa de hosts válidos: 192.168.0.1 - 192.168.0.254
Status do IP: Rede privada
```

Saida do arquivo output.json:
```
{
    "Bits_de_rede": 24,
    "Bits_de_host": 8,
    "Hosts_na_rede": 254,
    "Classe_da_Rede": "C",
    "Ip_da_rede": "192.168.0.0",
    "Ip_de_broadcast": "192.168.0.255",
    "Ip_valido_inicial": "192.168.0.1",
    "Ip_valido_final": "192.168.0.254",
    "Status_do_IP": "Rede privada"
}
```
