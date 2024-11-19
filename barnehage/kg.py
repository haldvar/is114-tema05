from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import altair as alt
import pandas as pd
from dbexcel import soknad, barnehage, forelder, barn
from kgmodel import (Foresatt, Barn, Soknad, Barnehage)
from kgcontroller import (form_to_object_soknad, insert_soknad, commit_all, select_alle_barnehager, select_alle_soknader)

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' # nødvendig for session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barnehager')
def barnehager():
    information = select_alle_barnehager()
    return render_template('barnehager.html', data=information)

@app.route('/behandle', methods=['GET', 'POST'])
def behandle():
    if request.method == 'POST':
        sd = request.form
        print(sd) #husk denne!
        log = insert_soknad(form_to_object_soknad(sd))
        print(log)
        session['information'] = sd #global variabel
        return redirect(url_for('svar')) #[1]
    else:
        return render_template('soknad.html')

@app.route('/svar')
def svar():
    message = ""
    alle_barnehager = select_alle_barnehager()
    information = session['information']
    pri_str = information.get("liste_over_barnehager_prioritert_5")
    pri_list = pri_str.split(",")
    print(pri_list)
    print(type(information))
    tilgjengelige_barnehager = [] #tom liste, skal fylles med barnehager som tilfredstiller kravene fra bruker og det er plass til
    for pri_nr in pri_list: #for hvert tall i prioriteringslisten
        for bh in alle_barnehager: #for hver rad i tabellen med barnehager (barnehage_id)
            if (int(pri_nr) == bh.barnehage_id and bh.barnehage_ledige_plasser > 0): #hvis prioriteringstallet er lik et tall i (barnehage_id) OG den barnehagen har minst én plass
                tilgjengelige_barnehager = [bh.barnehage_navn] + tilgjengelige_barnehager # legg til den godkjente barnehagen i listen
    if(len(tilgjengelige_barnehager) == 0):
        print("Du har dessverre fått avslag på din søknad!")
        message = "Du har dessverre fått avslag på din søknad!"
        #return message
    else:
        print("Du har fått tilbud om plass hos disse barnehagene: ", tilgjengelige_barnehager)
        message = "Du har fått tilbud om plass hos disse barnehagene: "
        #return message
    return render_template('svar.html', data=information, displayed_message=message, tilbud_liste=tilgjengelige_barnehager)

@app.route('/commit')
def commit():
    commit_all()
    barn_dict = barn.to_dict(orient='records')
    barnehage_dict = barnehage.to_dict(orient='records')
    forelder_dict = forelder.to_dict(orient='records')
    soknad_dict = soknad.to_dict(orient='records')
    return render_template('commit.html', barn=barn_dict, forelder=forelder_dict, barnehage=barnehage_dict, soknad=soknad_dict)

@app.route('/soknader')
def soknader():
    tabell = soknad.to_dict(orient='records') #Copolit hjalp meg med bare denne linjen.
    #Klarte ikke å displaye verdiene fra dataframe i tabellen på egenhånd.
    pri = dict(soknad["barnehager_prioritert"])
    print(pri)
    #for soknader in soknad.barnehager_prioritert
    
    
    
    #Jeg er klar over at koden under ikke er bærekraftig. 
    #Jeg prøvde å gjøre den mest mulig uten å bruke hjelpemidler.
    #Hadde jeg hatt mer tid og erfaring hadde jeg nok prøvd å lage en kode som tok utgangspunkt i koden i oppg1 for å sjekke om søknaden gir 
    
    status_liste = []
    for index in pri:
        print(pri[index].replace(" ", "").split(",")) 
        if pri[index].replace(" ", "").split(",") == ['4', '6']:  
            status_liste = status_liste + ["Avslag"]
        elif pri[index].replace(" ", "").split(",") == ['6', '4']:
            status_liste = status_liste + ["Avslag"]
        elif pri[index].replace(" ", "").split(",") == ['6']:
            status_liste = status_liste + ["Avslag"]
        elif pri[index].replace(" ", "").split(",") == ['4']:
            status_liste = status_liste + ["Avslag"]
        else:
            status_liste = status_liste + ["Tilbud"]
    print(status_liste)
    
    for i in range(len(tabell)): #Copilot hjalp meg med denne. Den merger de to listene sånn at for loopen i soknader.html kan iterere over begge listene i én.
        tabell[i]['status_liste'] = status_liste[i]
    
        
    return render_template('soknader.html', tabell=tabell, soknad=soknad, status_liste=status_liste)

@app.route("/statistikk")
def statistikk():
    bhb_data = pd.read_excel(r"/Users/halli/Scripts/files/Oblig3-Barenhagedata.xlsx", sheet_name="Cleaned_data")
    ext_data = bhb_data[["Kommune", "y15", "y16", "y17", "y18", "y19", "y20", "y21", "y22", "y23"]]
    transposed = ext_data.T.reset_index()
    transposed.columns = transposed.iloc[0]
    transposed = transposed.drop(0).reset_index(drop=True)
    print(transposed.Alta)
    alt.renderers.enable("browser")
    
    chart = alt.Chart(transposed, width=600).mark_line().encode(
    alt.X('Kommune:O').title("Year"),
    # Plot the calculated field created by the transformation
    alt.Y('Alta:Q').title("Barn i barnehage i 1-2 års alderen, Alta, Prosent")
)
    
    #chart.show()
    chart.save("chart.png")
    return render_template('statistikk.html')
"""
Referanser
[1] https://stackoverflow.com/questions/21668481/difference-between-render-template-and-redirect
"""

"""
Søkeuttrykk

"""