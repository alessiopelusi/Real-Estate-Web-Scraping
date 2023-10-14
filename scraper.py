from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as BrowserService
from selenium.webdriver.common.by import By


# Ottiene tutte le informazioni degli annunci presenti sulla pagina
def web_scraper_annunci(url):
    driver = webdriver.Chrome(service=BrowserService(ChromeDriverManager().install()))
    driver.get(url) # Visita l'url sul browser

    lista_annunci = driver.find_elements(By.CSS_SELECTOR, "li[class*='in-realEstateResults__item']")
    annunci_presenti_nella_pagina = []

    for annuncio in lista_annunci:
        informazioni_casa = {"Titolo": None, "Prezzo": None, "Locali": None, "Superficie": None, "Bagni": None, "Piano": None, "Descrizione": None, "Url": None}

        contenitore_informazioni = annuncio.find_elements(By.CSS_SELECTOR, "div[class*='in-card__content'] > *")
        informazioni_casa["Titolo"] = contenitore_informazioni[0].text
        informazioni_casa["Url"] = contenitore_informazioni[0].get_attribute("href")
        try: 
            informazioni_casa["Descrizione"] = " ".join(((contenitore_informazioni[2].text).split())[:30])
        except IndexError: informazioni_casa["Descrizione"] = contenitore_informazioni[2].text
        altre_info = contenitore_informazioni[1].find_elements(By.CSS_SELECTOR, "li[class*='in-feat__item']")
        informazioni_casa["Prezzo"] = altre_info[0].text
        for info in altre_info[1:]:
            aria_label = info.get_attribute("aria-label")
            valore = info.text
            if "local" in aria_label: informazioni_casa["Locali"] = valore
            elif "superficie" in aria_label: informazioni_casa["Superficie"] = valore
            elif "bagn" in aria_label: informazioni_casa["Bagni"] = valore
            elif "piano" in aria_label: informazioni_casa["Piano"] = valore
        annunci_presenti_nella_pagina.append(informazioni_casa)
        
        annunci_presenti_nella_pagina_senza_duplicati = rimuovi_duplicati(annunci_presenti_nella_pagina)

    driver.quit()
    return annunci_presenti_nella_pagina_senza_duplicati

# Rimuove tutti gli annunci duplicati così da non tenerli in considerazione
def rimuovi_duplicati(annunci_presenti_nella_pagina_con_duplicati):
    unici = set()
    annunci_presenti_nella_pagina_senza_duplicati = []
    for annuncio in annunci_presenti_nella_pagina_con_duplicati:
        if (annuncio["Titolo"], annuncio["Descrizione"], annuncio["Prezzo"]) not in unici: # Per verificare l'unicità, un annuncio viene definito "copia" se la tupla <titolo, descrizione, prezzo> è già presente nella lista 
            unici.add((annuncio["Titolo"], annuncio["Descrizione"], annuncio["Prezzo"]))
            annunci_presenti_nella_pagina_senza_duplicati.append(annuncio)
    
    return annunci_presenti_nella_pagina_senza_duplicati
