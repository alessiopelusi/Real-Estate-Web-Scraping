import mysql.connector

# Parametri per effettuare la connessione al database
def conn():
    host="localhost"
    user="root"
    passw=""
    database_nome="immobiliare"
    mydb = mysql.connector.connect(
        host = host,
        username = user,
        password = passw,
        database = database_nome
    )
    return mydb

# Richiede al database tutti gli annunci presenti in esso, li salva in una lista e li ritorna in output
def database_select():
    mydb = conn()
    mycursor = mydb.cursor()
    with mycursor:
        sql = "SELECT * FROM case_in_vendita_test ORDER BY id DESC"
        mycursor.execute(sql)
        annunci_presenti_nel_database = mycursor.fetchall()
        return annunci_presenti_nel_database

# Controlla se l'annuncio in input è già presente nel database, se lo è -> ritorna 1, se non lo è -> ritorna 0
def database_controllo_occorrenza(annuncio_da_controllare):
    mydb = conn()
    mycursor = mydb.cursor()
    with mycursor:
        sql = "SELECT * FROM case_in_vendita_test WHERE Titolo = %s AND Prezzo = %s AND Descrizione LIKE %s"
        valori = (annuncio_da_controllare['Titolo'], annuncio_da_controllare['Prezzo'], f"{annuncio_da_controllare['Descrizione']}%")
        mycursor.execute(sql, valori)

        occorrenze = mycursor.fetchall()
        if len(occorrenze): return 1
        else: return 0

# 1. Se l'annuncio in input è già presente nel database allora è un annuncio vecchio ripubblicato, quindi viene aggiornato in questo modo: eliminato e poi inserito
# 2. Se l'annuncio in input non è già presente nel databse allora è un vero nuovo annuncio, quindi non viene eliminato (in quanto non sarà trovato) e viene inserito
# Invece di usare una select query per controllare se l'annuncio è presente o meno nel db, controlliamo semplicente il numero di righe affette dopo l'eliminazione: 
    # se una riga sarà eliminata (check = 1)-> la funzione ritorna 0 -> l'annuncio è del caso 1); se nessuna riga sarà eliminata (check = 0)-> la funzione ritorna 1 -> l'annuncio è del caso 2)
def aggiornamento_database(annuncio):
    
    mydb = conn()
    mycursor = mydb.cursor()
    with mycursor:

        # Creazione della query di eliminazione
        query = "DELETE FROM case_in_vendita_test WHERE Titolo = %s AND Prezzo = %s AND Descrizione LIKE %s"
        values = (annuncio['Titolo'], annuncio['Prezzo'], f"{annuncio['Descrizione']}%")

        # Esecuzione della query di eliminazione
        mycursor.execute(query, values)
        check = mycursor.rowcount
        if check: print("-> L'annuncio è già presente nel database, è stato eliminato e ora verrà reinserito nella posizione aggiornata.")
        else: print("-> L'annuncio non è presente nel database, verrà inserito.")

        # Creazione della query di inserimento
        query = "INSERT INTO case_in_vendita_test (titolo, prezzo, locali, superficie, bagni, piano, descrizione) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (annuncio['Titolo'], annuncio['Prezzo'], annuncio['Locali'], annuncio['Superficie'], annuncio['Bagni'], annuncio['Piano'], annuncio['Descrizione'])
        
        # Esecuzione della query di inserimento 
        mycursor.execute(query, values)

        if mycursor.rowcount == 1: print("Processo andato a buon fine.")
        else: print("Inserimento annuncio nel database fallito")

        mydb.commit() # salvataggio modifiche nel database

        if check == 0: return 1
        else: return 0

def eliminazione_annunci_vecchi_database():
    mydb = conn()
    mycursor = mydb.cursor()
    with mycursor:
        # Si Utilizza una sottoquery per selezionare gli ID dei primi 1000 record in ordine decrescente. 
        # La query principale esegue un'eliminazione dei record che non corrispondono agli ID selezionati nella sottoquery.
        query = "DELETE FROM case_in_vendita_test WHERE ID NOT IN (SELECT ID FROM (SELECT ID FROM case_in_vendita_test ORDER BY ID DESC LIMIT 1000) AS subquery)"
        mycursor.execute(query)
        print("\nSono stati eliminati", mycursor.rowcount, "annunci nel database.")

        mydb.commit() # salvataggio modifiche nel database