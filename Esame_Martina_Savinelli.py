import random
import math
import numpy as np

class Elettrone:
    def __init__(self, energia, altezza):
        """
+        Crea un elettrone con i parametri passati come argomento.
+
+        Parametri:
+            energia (float): energia particella;
+            altezza (float): altezza particella;
+            energia_critica (float): energia critica dell'elettrone.
+
+        Returns:
+            None
+        """
        self.energia=energia
        self.altezza=altezza
        self.energia_critica= 87.92
    
    def __str__(self) -> str:
        return f"Elettrone con energia {self.energia} e altezza {self.altezza}"

    def perdita_ionizzazione(self, s):
        """
+       Decresce energia e altezza della particella in base ai parametri
+       dati per la perdita per ionizzazione.
+
+        Parametri:
+            s (float): passo di avanzamento della simulazione in frazioni di X0;
+            energia_iniziale (float): energia iniziale dell'elettrone.
+
+        Returns:
+            None
+        """
        En_ionizzazione=9.495*10e-4*X0
        if self.energia > En_ionizzazione*s/X0:
            self.energia -= En_ionizzazione*s/X0
            self.altezza -= s*np.cos(alfa)

    def emissione_bremsstrahlung(self, s,  sciame):
        """
+        Simula il processo di Bremsstrahlung dell'elettrone.
+
+        Parametri:
+        - s (float): passo di avanzamento della simulazione;
+        - sciame (list): sciame in cui aggiungere le particelle eventualmente generate.
+
+        Returns:
+        - sciame: restituisce l'array aggiornato con le particelle generate/la particella madre
+        se l'emissione non avviene
+        """
        if self.energia > self.energia_critica:
            probabilita = random.SystemRandom().random()
            if probabilita < (1 - math.exp(-s/X0)):
                en_residua=self.energia /2
                altezza1=self.altezza - s*np.cos(alfa)
                nuovo_fotone= Fotone(en_residua, altezza1)  
                sciame.append(nuovo_fotone)
                nuovo_e=Elettrone(en_residua, altezza1)
                sciame.append(nuovo_e)
            else:
                sciame.append(self)
        return sciame

class Positrone:
    def __init__(self, energia, altezza):
        """
+        Crea un nuovo positrone con i parametri passati come argomento.
+
+        Parametri:
+            energia (float): energia particella;
+            altezza (float): altezza particella;
+            energia_critica (float): energia critica del Positrone.
+
+        Returns:
+            None
+        """
        self.energia= energia
        self.altezza=altezza
        self.energia_critica = 85.97
        
    def __str__(self) -> str:
        return f"Positrone con energia {self.energia} e altezza {self.altezza}"

    def perdita_ionizzazione(self, s):
        """
+       Decresce energia e altezza della particella in base ai parametri
+       dati per la perdita per ionizzazione.
+
+        Parametri:
+            s (float): passo di avanzamento della simulazione in frazioni di X0;
+            energia_iniziale (float): energia iniziale del positrone.
+
+        Returns:
+            None
+        """
        En_ionizzazione=9.495*10e-4*X0
        if self.energia > En_ionizzazione*s/X0:
            self.energia -= En_ionizzazione*s/X0
            self.altezza -= s*np.cos(alfa)
        
    def emissione_bremsstrahlung(self, s, sciame):
        """
+        Simula il processo di Bremsstrahlung del Positrone.
+
+        Parametri:
+        - s (float): passo di avanzamento della simulazione;
+        - sciame (list): sciame in cui aggiungere la particella.
+
+        Returns:
+        - sciame: restituisce l'array aggiornato con le particelle generate/la particella madre
+        se l'emissione non avviene
+        """
        if self.energia > self.energia_critica:
            probabilita = random.SystemRandom().random()
            if probabilita < (1 - math.exp(-s/X0)):
                en_residua=self.energia /2
                altezza1=self.altezza - s*np.cos(alfa)
                nuovo_fotone= Fotone(en_residua, altezza1)  
                sciame.append(nuovo_fotone)
                nuovo_p=Positrone(en_residua, altezza1)
                sciame.append(nuovo_p)
            else:
                sciame.append(self)
        return sciame
               
class Fotone:
    def __init__(self, energia, altezza):
        """
+        Crea un fotone con i parametri passati come argomento.
+
+        Parameters:
+            energia (float): energia inizale fotone.
+            altezza (float): altezza iniziale fotone.
+
+        Returns:
+            None
+        """
        self.energia=energia
        self.altezza=altezza
        self.energia_critica = 0.0
    def __str__(self) -> str:
        return f"Fotone con energia {self.energia} e altezza {self.altezza}"
    
    def produzione_coppie(self, s, sciame):
        """
+        Simula l'interazione di un fotone per produzione di coppie.
+
+        Parameters:
+            s (float): passo della simulazione;
+            sciame (list): sciame in cui aggiungere le particelle.
+
+        Returns:
+           - sciame: restituisce l'array aggiornato con le particelle generate/la particella madre
+        se l'emissione non avviene
+        """
        probabilita = random.SystemRandom().random()
        if self.energia > 2 * 0.511 :
            if probabilita < (1 - math.exp((-7 * s )/ 9*X0)):
                en_residua=self.energia /2
                altezza1=self.altezza - s*np.cos(alfa)
                nuovo_e= Elettrone(en_residua, altezza1)
                nuovo_p = Positrone(en_residua, altezza1)
                sciame.append(nuovo_e)
                sciame.append(nuovo_p)
            else:
                sciame.append(self)
        return sciame
        
def simulazione_sciame_iniziale(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento dello sciame di particelle 
+    prima di arrivare al detector.
+
+    Parameters:
+        s (float): passo della simulazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    while True:
        tipo_particella = input("Inserisci il tipo di particella iniziale (elettrone o fotone): ").lower()
    
        if tipo_particella in ["elettrone", "fotone"]:
            break
        else:
            print("Tipo di particella non valido. Il tipo deve essere 'elettrone' o 'fotone'.")

    while True:
        try:
            num_particelle = int(input("Inserisci il numero di particelle iniziali nello sciame: "))
            break 
        except ValueError:
            print("Inserisci un numero intero valido.")
            
    while True:
        energia_iniziale = float(input("Inserisci l'energia iniziale delle particelle in MeV, tra 1 e 100TeV(1Tev=10^6 MeV)): "))
    
        if energia_iniziale > 10**8 or energia_iniziale < 10**6:    
            print("Errore: l'energia iniziale deve essere compresa tra 1 e 100 TeV.")
        else:
            break
        
    sciame = []
   
    if tipo_particella.lower() == "elettrone":
        sciame = [Elettrone(energia_iniziale, altezza_sciame) for _ in range(num_particelle)]
    elif tipo_particella.lower() == "fotone":
        sciame = [Fotone(energia_iniziale, altezza_sciame) for _ in range(num_particelle)]  
    
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in range(t):

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella, Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
                    '''
                elif X0*np.log(energia_iniziale/particella.energia_critica)/np.log(2)<particella.altezza:
                    particella.perdita_ionizzazione(s)
                    '''
                else:
                    particella.perdita_ionizzazione(s)
                    particella.emissione_bremsstrahlung(s, particelle_da_aggiungere)
                    particelle_da_rimuovere.append(particella)
                    
            if isinstance(particella, Fotone):
                if particella.energia <= 2 * 0.511:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
                
                else:
                    particella.produzione_coppie(s, particelle_da_aggiungere)
                    particelle_da_rimuovere.append(particella)               
        
            sciame = [particella for particella in sciame if particella not in particelle_da_rimuovere]
            sciame.extend(particelle_da_aggiungere)
            #print("Particelle analizzate correttamente, abbiamo aggiunto {} particelle".format(len(particelle_da_aggiungere)))
            #print(len(particelle_da_aggiungere), ", ", len(particelle_da_rimuovere), ", ", len(sciame))
            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)

altezza_detector = 4000  # Altezza del detector
altezza_sciame = 20000  # Altezza iniziale del sciame

X0= 7*10**2 #fornito dal prof

while True:
        s = X0* float(input("Inserisci il passo compreso tra 0 e 1: ")) #percentuale lunghezza d'onda
        if (s/X0) > 1 or (s/X0) <= 0:
            print("Errore: il passo deve essere compreso tra 0 e 1")
        else:
            break
while True:
        angolo=float(input("Inserire angolo in gradi compreso tra 0 e 45: "))
        if angolo > 45 or angolo < 0:
            print("Errore: l'angolo deve essere compreso tra 0 e 45")
        else:
            break
    
alfa = angolo * np.pi / 180
t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)

risultato_simulazione = simulazione_sciame_iniziale(s, altezza_sciame, altezza_detector)

print("Numero di particelle arrivate al detector:", risultato_simulazione)