# Ready2Play (R2P) Web App - Prototipo Python

Questo archivio contiene il prototipo della web app Ready2Play.

##Esecuzione web
Cliccare sul collegamento chrome presente nella cartella
In alternativa usare questo link:
https://ready2play-7wfe4yv9vhufteeuiatkt7.streamlit.app/

## Requisiti
Per eseguire l'app è necessario avere Python installato con la libreria `streamlit` e `pytz`.

## Installazione
1. Estrai il contenuto del file ZIP.
2. Apri il terminale nella cartella estratta.
3. Installa Streamlit (se non lo hai già):
   `pip install streamlit`
4. Installa pytz (se non lo hai già):
   `pip install pytz`

## Esecuzione
Lancia l'applicazione con il comando:
`streamlit run app.py`

## Funzionalità Incluse
Home (Dashboard): Visualizzazione dinamica dei campi consigliati e sistema di prenotazione rapida integrato direttamente sotto ogni scheda.
Ricerca Avanzata: Sistema di filtri per sport, distanza e orario con generazione automatica dei risultati disponibili.
Social Matchmaking: Gestione degli inviti ricevuti, possibilità di unirsi a partite esistenti e monitoraggio dei partecipanti.
Chat: Sistema di messaggistica integrato per il coordinamento dei team prima del match.
Portafoglio & Prenotazioni: Gestione del saldo prepagato, riepilogo delle partite prenotate e scalabilità automatica dei costi.
Smart Access IoT: Automazione degli ingressi tramite controllo temporale. Lo sblocco del cancello e l'accensione delle luci sono abilitati solo nei 30 minuti precedenti l'inizio del match per garantire sicurezza e risparmio energetico.
