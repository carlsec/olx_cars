import os.path
from flask import Flask, request #
import os
import pandas as pd
import main


app = Flask(__name__)

def get():
    
    data = pd.read_csv('data.csv')
    data = data.drop_duplicates().reset_index(drop=True)
		
    scrap = []
    for i in range(len(data)):
        scrap.append((data['Link'][i], data['Modelo'][i], data['Preco'][i], data['fipe'][i], data['rate'][i]))

    scrap = scrap[:300]

    scrap_formatted = []
    for e in scrap:
        #print(e)
        scrap_formatted.append("<tr><th><a href=\"{link}\">{title}</a></th><th>Valor do Anuncio: R${preco}</th><th>Valor da Fipe: R${fipe}</th><th>              {score}% Abaixo da Tabela Fipe</th></tr>".format(title=e[1], link=e[0], preco=e[2], fipe=e[3], score=e[4]))
  
    return '\n'.join(scrap_formatted) #

@app.route('/')
def main_page():
    preds = get() #
    return """<head><h1>Olx Scrap</h1></head>
    <body>
    <table>
             {}
    </table>
    </body>""".format(preds) #

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')