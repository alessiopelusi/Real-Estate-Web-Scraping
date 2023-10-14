from scraper import web_scraper_annunci
from database import database_select, aggiornamento_database, eliminazione_annunci_vecchi_database
import webbrowser

#Ricerca di tutti gli annunci presenti nella pagina
annunci_presenti_sulla_pagina = web_scraper_annunci( "https://www.immobiliare.it/vendita-case/roma/?criterio=dataModifica&ordine=desc")

# Ricerca tra gli annunci presenti in pagina della prima corrispondenza con gli annunci già presenti nel database
annunci_presenti_nel_database = database_select()


trovata_corrispondenza = False  # Flag per indicare se è stata trovata una corrispondenza
for annuncio_vecchio in annunci_presenti_nel_database:
    for i in range(len(annunci_presenti_sulla_pagina)):

        # la corrispondenza viene rilevata quando vi è l'uguaglianza della tupla <Titolo, Prezzo, Descrizione> 
        if annuncio_vecchio[1] == annunci_presenti_sulla_pagina[i]["Titolo"] and annuncio_vecchio[2] == annunci_presenti_sulla_pagina[i]["Prezzo"] and annuncio_vecchio[7] in annunci_presenti_sulla_pagina[i]["Descrizione"]:
            trovata_corrispondenza = True
            break
    if trovata_corrispondenza:
        print("L'annuncio in posizione", i+1, "è la prima corrispondenza nel database")
        break


if trovata_corrispondenza: 
    print("Si procede all'aggiornamento dell'annuncio trovato e al controllo degli annunci precedenti:")
else: 
    print("Non è stata trovata alcuna corrispondenza: si procede all'inserimento di tutti i nuovi annunci presenti sulla pagina:")
    i = len(annunci_presenti_sulla_pagina)

for annuncio_nuovo in annunci_presenti_sulla_pagina[:i+1][::-1]:
    annuncio_veramente_nuovo = aggiornamento_database(annuncio_nuovo) # PUNTO 4
    if annuncio_veramente_nuovo: webbrowser.open(annuncio_nuovo["Url"])


eliminazione_annunci_vecchi_database()
