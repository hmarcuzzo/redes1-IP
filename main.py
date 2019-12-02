
"""*******************************************************************
* NOME DO ARQUIVO :    main.py                                       *
*                                                                    *
* DESCRIÇÂO :                                                        *
*                                                                    *
*        Este trabalho consiste em obter a partir de um Endereço     *
*           de IP e uma Máscara de Rede, validar se esses IPs        *
*           estão corretos, obter a quantidade de Bits de rede,      *
*           Bits de host, quantos Host podem existir dentro da rede, *
*           a que classe pertence este IP, qual é o IP que           *
*           representa o IP de Rede e o de Broadcast, exibir quais   *
*           são as faixas de IPs livre (inicio e fim) e também       *
*           dizer se o IP em questão é reservado ou não, no caso     *
*           afirmativo dizer para qual finalidade.                   *
*                                                                    *
*                                                                    *
*                                                                    *
*                                                                    *
* AUTORES :    Enzo Italiano, Henrique Marcuzzo                      *
*                                                                    *
* DATA DE CRIAÇÃO :    29/11/2019                                    *   
*                                                                    *
* MODIFICAÇÕES :       30/11/2019                                    *
*                                                                    * 
**********************************************************************"""


import sys                      # biblioteca que me permite captar parametros por linha de comando
import json                     # biblioteca para importar e exportar configurações de/em arquivos json
from copy import deepcopy       # biblitoca para fazer cópia profundas de vetores

# ------------------------- Funções -------------------------

""" Pegando as informações necessárias do arquivo JSON passado por parâmetro """
def init():
    configFile = sys.argv[1]   
    inputFile = open(configFile, 'r')
    datas = json.load(inputFile)
    
    ipAddr = datas['ipAddr']
    netMask = datas['netMask']

    return ipAddr, netMask


""" Convertando a string adquirida do arquivo JSON para inteiros """
def convertToInteger(ipAddr, netMask):
    ipAddr = ipAddr.split(".")
    netMask = netMask.split(".")

    for i in range(len(ipAddr)):
        ipAddr[i] = int(ipAddr[i])
    
    for i in range(len(netMask)):
        netMask[i] = int(netMask[i])

    return ipAddr, netMask


""" Convertendo os inteiros para binários """
def convertToBinary(ipAddr, netMask):
    auxIP = ipAddr
    auxNet = netMask

    for i in range(4):
        auxIP[i] = bin(auxIP[i])
        auxNet[i] = bin(auxNet[i])


    return auxIP, auxNet


""" Verificando se os IPs (Endereço IP e Máscara IP) são válidos """
def isValid(ipAddrI, netMaskI, ipAddrB, netMaskB):
    flag_zero = 0

    for i in range(4):
        if (ipAddrI[i] > 255 or ipAddrI[i] < 0):
            print("O IP digitado é inválido!\n")
            exit()

        if (netMaskI[i] > 255 or netMaskI[i] < 0):
            print("A mascara de IP digitada é inválida!\n")
            exit()
    
    for i in range(len(netMaskB)):
        for j in range(2, len(netMaskB[i])):
            if netMaskB[i][j] is '1' and flag_zero is 1:
                print("A mascara de IP digitada é inválida!\n")
                exit()
            if netMaskB[i][j] is '0':
                flag_zero = 1


""" Descobrindo quantos bits são de Rede e quantos bits são de Host """
def host_NetWork(netMask):
    netID = 0
    hostID = 0
    flag = 0

    for i in range(len(netMask)):
        for j in range(2, len(netMask[i])):
            if netMask[i][j] is '0':
                flag = 1
            if flag == 0:
                netID += 1
    
    hostID = 32 - netID
    
    return netID, hostID


""" Pelo IP descobrindo a que classe esse IP pertence"""
def isClass(ipAddr):
    if (ipAddr[0] >= 0 and ipAddr[0] <= 127):
        classe = "A"
    elif (ipAddr[0] >= 128 and ipAddr[0] <= 191):
        classe = "B"
    elif (ipAddr[0] >= 192 and ipAddr[0] <= 223):
        classe = "C"
    elif (ipAddr[0] >= 224 and ipAddr[0] <= 239):
        classe = "D"
    elif (ipAddr[0] >= 240 and ipAddr[0] <= 255):
        classe = "E"

    return classe


""" Achando o IP de Rede pelo Endereço de IP binário e a quantidade de bits que representam a rede """
def findIpNetwork(ipAddrB, netID):
    IpNetwork = []
    
    for i in range(4):
        aux = ''
        for j in range(10):
            if (netID != 0):
                if (j < len(ipAddrB[i])):
                    aux += ipAddrB[i][j]
                if (j > 1):
                    netID -= 1
            else:
                if (j > 1):
                    aux += '0'
        IpNetwork.append(int(aux, 2))
        

    return IpNetwork


""" Achando o IP de Broadcast pelo Endereço de IP binário e a quantidade de bits que representam a rede """
def findIpBroadcast(ipAddrB, netID):
    IpBroadcast = []
    
    for i in range(4):
        aux = ''
        for j in range(10):
            if (netID != 0):
                if (j < len(ipAddrB[i])):
                    aux += ipAddrB[i][j]
                if (j > 1):
                    netID -= 1
            else:
                if (j > 1):
                    aux += '1'
        IpBroadcast.append(int(aux, 2))

    return IpBroadcast


""" Descobrindo o intervalo válido de IPs para host atráves do IP de Rede e o IP de Broadcast """
def findIpValid(ipNetwork, ipBroadcast):

    ipNetwork[3] = ipNetwork[3] + 1
    ipBroadcast[3] = ipBroadcast[3] - 1

    return ipNetwork, ipBroadcast


""" Descobrindo se o IP passado é reservado ou não """
def networkState(ipAddr):

    if (ipAddr[0] == 0):
        status = "Rede corrente"
    elif ((ipAddr[0] == 10) or (ipAddr[0] == 172 and ipAddr[1] == 16) or (ipAddr[0] == 192 and ipAddr[1] == 168)):
        status = "Rede privada"
    elif (ipAddr[0] == 14):
        status = "Rede pública"
    elif ((ipAddr[0] == 39) or (ipAddr[0] == 128 and ipAddr[1] == 0) or (ipAddr[0] == 191 and ipAddr[1] == 255)
            or (ipAddr[0] == 223 and ipAddr[1] == 255 and ipAddr[2] == 255) or (ipAddr[0] == 240)):
        status = "Reservado"
    elif (ipAddr[0] == 127):
        status = "Localhost"
    elif (ipAddr[0] == 169 and ipAddr[1] == 254):
        status = "Localhost"
    elif (ipAddr[0] == 192 and ipAddr[1] == 0 and ipAddr[2] == 2):
        status = "Documentação"
    elif (ipAddr[0] == 192 and ipAddr[1] == 88 and ipAddr[2] == 99):
        status = "IPv6 para IPv4"
    elif (ipAddr[0] == 198 and ipAddr[1] == 18):
        status = "Teste de benchmark de redes"
    elif (ipAddr[0] == 224):
        status = "Multicasts"
    elif (ipAddr[0] == 255 and ipAddr[1] == 255 and ipAddr[2] == 255 and ipAddr[3] == 255):
        status = "Broadcast"
    else:
        status = "Ip não reservado"


    return status


""" Escrevendo no arquivo JSON passado por parâmetro as informações obtidas """
def output(netID_hostID, classe, ipNetwork, ipBroadcast, ipValid, status):
    
    results = {
        "Bits_de_rede": netID_hostID[0],
        "Bits_de_host": netID_hostID[1], 
        "Hosts_na_rede": (2 ** netID_hostID[1]) - 2, 
        "Classe_da_Rede": classe,
        "Ip_da_rede": str(ipNetwork[0]) + "." + str(ipNetwork[1]) + "." + str(ipNetwork[2]) + "." + str(ipNetwork[3]),
        "Ip_de_broadcast": str(ipBroadcast[0]) + "." + str(ipBroadcast[1]) + "." + str(ipBroadcast[2]) + "." + str(ipBroadcast[3]),
        "Ip_valido_inicial": str(ipValid[0][0]) + "." + str(ipValid[0][1]) + "." + str(ipValid[0][2]) + "." + str(ipValid[0][3]),
        "Ip_valido_final": str(ipValid[1][0]) + "." + str(ipValid[1][1]) + "." + str(ipValid[1][2]) + "." + str(ipValid[1][3]),
        "Status_do_IP": status
    }
    
    if len(sys.argv[1:]) > 1:
        outputFile = sys.argv[2]
    else:
        outputFile = "output.json"

    with open(outputFile, 'w') as file:
            json.dump(results, file, indent = 4)



# --------------------- Fluxo Principal ---------------------

def main():

    ipsVector = init()

    ipsVectorInteger = convertToInteger(ipsVector[0], ipsVector[1])

    ipsVectorBinary = deepcopy(ipsVectorInteger)
    ipsVectorBinary = convertToBinary(ipsVectorBinary[0], ipsVectorBinary[1])

    isValid(ipsVectorInteger[0], ipsVectorInteger[1], ipsVectorBinary[0], ipsVectorBinary[1])
    
    netID_hostID = host_NetWork(ipsVectorBinary[1])
    print("Bits de rede: " + str(netID_hostID[0]))
    print("Bits de host: " + str(netID_hostID[1]))
    print("Hosts na rede: " + str( ((2 ** netID_hostID[1]) - 2) ))
    
    classe = isClass(ipsVectorInteger[0])
    print("Classe: " + classe)

    ipNetwork = findIpNetwork(ipsVectorBinary[0], netID_hostID[0])
    print("Ip da rede: " + str(ipNetwork[0]) + "." + str(ipNetwork[1]) + "." + str(ipNetwork[2]) + "." + str(ipNetwork[3]))

    ipBroadcast = findIpBroadcast(ipsVectorBinary[0], netID_hostID[0])
    print("Ip de broadcast: " + str(ipBroadcast[0]) + "." + str(ipBroadcast[1]) + "." + str(ipBroadcast[2]) + "." + str(ipBroadcast[3]))

    ipValid = findIpValid(deepcopy(ipNetwork), deepcopy(ipBroadcast))
    print("Faixa de hosts válidos: " + str(ipValid[0][0]) + "." + str(ipValid[0][1]) + "." + str(ipValid[0][2]) + "." + str(ipValid[0][3])
            + " - " + str(ipValid[1][0]) + "." + str(ipValid[1][1]) + "." + str(ipValid[1][2]) + "." + str(ipValid[1][3]))

    status = networkState(ipsVectorInteger[0])
    print("Status do IP: " + status)

    output(netID_hostID, classe, ipNetwork, ipBroadcast, ipValid, status)


if __name__ == "__main__":
    main()