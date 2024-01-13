# Esame_MCF_Savinelli_Martina
Esame Savinelli Martina: Simulazione Sciame di Particelle

"""
Codice per la simulazione dell'andamento di uno sciame di particelle.
L'utente può scegliere il passo(s) della simulazione, l'angolo rispetto allo Zenit d'ingresso della particella,
    il tipo di particella(elettrone o fotone), il numero di particelle iniziali presenti nello sciame e l'energia iniziale della singola particella.
La simulazione avrà dunque inizio e calcolerà la probabilità che le particelle interagiscano, per produzione di coppie nei fotoni o per Bremmstrahlung per elettroni o positroni; a questi due farà inoltre perdere energia (e conseguentemente quota) per ionizzazione.
Alla fine della simulazione verrà restituito il numero di particelle arrivate al detector.
Si consiglia di notare la differenza di particelle presenti nello sciame all'aumentare dell'angolo(La differenza maggiore si noterà per l'angolo 0° e 45°) e dell'energia.
"""
Nuovo Codice aggiornato, ha lo stesso procedimento descritto sopra.

"Simulazione_Ene" è un codice preimpostato che una volta avviato simula l'andamento dello sciame per 1 fotone e 1 elettrone per diverse energia e angoli con un passo prestabilito di 1. Sarebbe in grado di salvare anche i dati ottenuti, ma questa parte è stata commentata.
"Simulazione_angolo" è anch'essa una simulazione automatica che simula l'andamento di un elettrone e un fotone per diversi angoli di inclinazione rispetto allo Zenit, tutti con energia iniziale=10^6Mev e s=1; come sopra è in grado di salvare i dati in un file .csv ma anche qui questa parte di codice è stata commentata.
