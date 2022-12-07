import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import random

url = "http://34.193.183.16/mercadolibre"

payload = json.dumps({
    "producto": "televisor",
    "limite": 500
})
headers = {
    'Content-Type': 'application/json'
}

print("\n\t--------------- EN PROCESO ... --------------------")

response = requests.request("GET", url, headers=headers, data=payload).text
response = json.loads(response)

precios = response['datos']['precios']
precios = [int(i.replace(',', '')) for i in precios]
titulos = response['datos']['titulos']
url = response['datos']['urls']

lista_descuento = list()
lista_x = list()

cont = 0

for i in precios:
    
    dias = list()
    lista_pre = list()
    
    for x in range(28):
        lista_pre.append(random.randint(i-(round(i*0.3)), i))
        dias.append(x+1)
    
    lista_pre.append(i)
    dias.append(29)

    x = np.array(dias)
    y = np.array(lista_pre)

    dia = 30
    coef = np.polyfit(x, y, 4)
    p = np.polyval(coef, dia)
    print(f"\nPara el dia {dia} la prediccion de {titulos[cont]}es de {p} | Precio actual: {i} | {url[cont]}")
    cont += 1
    
    lista_x.append(cont)
    lista_descuento.append(p)

orden = sorted(lista_descuento)
xme = lista_descuento.index(orden[0]) + 1
xma = lista_descuento.index(orden[-1]) + 1

print("\n--------------- PRODUCTO MAS BARATO ---------------")
print(titulos[xme-1], "| precio actual: ", precios[xme-1], " | precio predecido: ", lista_descuento[xme-1], ": ", url[xme-1])

print("\n--------------- PRODUCTO MAS CARO ---------------")
print(titulos[xma-1], "| precio actual: ", precios[xma-1], " | precio predecido: ", lista_descuento[xma-1], ": ", url[xma-1])

fig = plt.figure(figsize=(12,7))
plt.style.use('ggplot')
fig.tight_layout()
axs = plt.subplot(1, 1, 1)
axs.grid(True)

plt.scatter(lista_x, lista_descuento,  c="purple", s=30)
plt.scatter(xma, orden[-1],  c="red", s=30, label="Mas caro")
plt.scatter(xme, orden[0],  c="green", s=30, label="Mas barato")

plt.title("Prediccion")
axs.set_ylabel("Precios")
plt.legend(loc='lower right')
plt.show()

