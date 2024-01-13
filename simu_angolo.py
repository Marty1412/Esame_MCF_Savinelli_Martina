import random
import math
import numpy as np
import pandas as pd
from tqdm import tqdm

class Elettrone:
    def __init__(self, energia, altezza):
        """
+        crea un elettrone.
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
            self.altezza -= s

    def emissione_bremsstrahlung(self, s,  sciame):
        """
+        Simula il processo di Bremsstrahlung dell'elettrone.
+
+        Parametri:
+        - s (float): passo di avanzamento della simulazione;
+        - sciame (list): sciame in cui aggiungere la particella.
+
+        Returns:
+        - bool: Vero se l'emissione avviene, Falso altrimenti
+        """
        if self.energia > self.energia_critica:
            probabilita = random.SystemRandom().random()
            if probabilita < (1 - math.exp(-s/X0)):
                en_residua=self.energia /2
                altezza1=self.altezza - s
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
+        Crea Positrone.
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
            self.altezza -= s
                
    def emissione_bremsstrahlung(self, s, sciame):
        """
+        Simula il processo di Bremsstrahlung del Positrone.
+
+        Parametri:
+        - s (float): passo di avanzamento della simulazione;
+        - sciame (list): sciame in cui aggiungere la particella.
+
+        Returns:
+        - bool: Vero se l'emissione avviene, Falso altrimenti
+        """
        if self.energia > self.energia_critica:
            probabilita = random.SystemRandom().random()
            if probabilita < (1 - math.exp(-s/X0)):
                en_residua=self.energia /2
                altezza1=self.altezza - s
                nuovo_fotone= Fotone(en_residua, altezza1)  
                sciame.append(nuovo_fotone)
                nuovo_p=Positrone(en_residua, altezza1)
                sciame.append(nuovo_p)
            else:
                sciame.append(self)
        return sciame
               
class Fotone:
    def __init__(self, energia, altezza):
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
+            bool: Vero se la produzione avviene, Falso altrimenti.
+        """
        probabilita = random.SystemRandom().random()
        if self.energia > 2 * 0.511 :
            if probabilita < (1 - math.exp((-7 * s )/ (9*X0))):
                en_residua=self.energia /2
                #print("energia residua= ", en_residua)
                altezza1=self.altezza - s
                #print("altezza= ", altezza1)
                nuovo_e= Elettrone(en_residua, altezza1)
                nuovo_p = Positrone(en_residua, altezza1)
                sciame.append(nuovo_e)
                sciame.append(nuovo_p)
            else:
                sciame.append(self)
        return sciame
        
def simulazione_1e0g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 0* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)

def simulazione_1f0g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un fotone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 0* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e5g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 5
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 5* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):  

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f5g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 5* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e10g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 10* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f10g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 10* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e15g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 15* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f15g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 15* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e20g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 20* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f20g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 20* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e25g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 25* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f25g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 25* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e30g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 30* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f30g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 30* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e35g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 35* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f35g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 35* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e40g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 40* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f40g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 40* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1e45g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 45* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Elettrone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)
def simulazione_1f45g(s, altezza_sciame, altezza_detector):
    """
+    Funzione che simula l'andamento di un elettrone con angolo 0
+    prima di arrivare al detector con e_iniziale=10^6
+
+    Parameters:
+        s (float): passo della simulazione.
+        t (int): Numero effettivo di passi fatti.
+        X0 (float): Lunghezza di radiazione.
+        altezza_sciame (float): Altezza iniziale dello sciame.
+        altezza_detector (float): Altezza del detector.
+        
+    Returns:
+        int: Il numero di particelle che sono state rilevate.
    """
    alfa = 45* np.pi / 180
    
    t = math.ceil((altezza_sciame - altezza_detector)/np.cos(alfa)/s)
    
    sciame = [Fotone(10**6, altezza_sciame)]
   
    particelle_rilevate = []
    particelle_da_aggiungere = []
    particelle_da_rimuovere=[]
    
    for i in tqdm(range(t)):
        #print('Lunghezza sciame:', len(sciame))

        for particella in sciame:
            
            if particella.altezza <= altezza_detector or particella.energia < particella.energia_critica:
                particelle_rilevate.append(particella)
                particelle_da_rimuovere.append(particella)
            
            if isinstance(particella, Elettrone) or isinstance(particella,Positrone):
                if particella.energia <= 9.495*10e-4*X0:
                    particelle_rilevate.append(particella)
                    particelle_da_rimuovere.append(particella)
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

            particelle_da_aggiungere=[]
            particelle_da_rimuovere=[]
        
        if i==t:
            particelle_rilevate.extend(sciame)
            particelle_rilevate.extend(particelle_da_aggiungere)
            break        

    return len(particelle_rilevate)

altezza_detector = 4000  # Altezza del detector
altezza_sciame = 20000  # Altezza iniziale del sciame
energia_iniziale=1000000
X0= 7*10**2 #fornito dal prof
s=1*X0
num_simu= 10
    
risu_1e0g=[]
risu_1f0g=[]
risu_1e5g=[]
risu_1f5g=[]
risu_1e10g=[]
risu_1f10g=[]
risu_1e15g=[]
risu_1f15g=[]
risu_1e20g=[]
risu_1f20g=[]
risu_1e25g=[]
risu_1f25g=[]
risu_1e30g=[]
risu_1f30g=[]
risu_1e35g=[]
risu_1f35g=[]
risu_1e40g=[]
risu_1f40g=[]
risu_1e45g=[]
risu_1f45g=[]

for t in range(num_simu):
    risu_1e0g.append(simulazione_1e0g(s, altezza_sciame, altezza_detector))
    risu_1f0g.append(simulazione_1f0g(s, altezza_sciame, altezza_detector))
    risu_1e5g.append(simulazione_1e5g(s, altezza_sciame, altezza_detector))
    risu_1f5g.append(simulazione_1f5g(s, altezza_sciame, altezza_detector))
    risu_1e10g.append(simulazione_1e10g(s, altezza_sciame, altezza_detector))
    risu_1f10g.append(simulazione_1f10g(s, altezza_sciame, altezza_detector))
    risu_1e15g.append(simulazione_1e15g(s, altezza_sciame, altezza_detector))
    risu_1f15g.append(simulazione_1f15g(s, altezza_sciame, altezza_detector))
    risu_1e20g.append(simulazione_1e20g(s, altezza_sciame, altezza_detector))
    risu_1f20g.append(simulazione_1f20g(s, altezza_sciame, altezza_detector))
    risu_1e25g.append(simulazione_1e25g(s, altezza_sciame, altezza_detector))
    risu_1f25g.append(simulazione_1f25g(s, altezza_sciame, altezza_detector))
    risu_1e30g.append(simulazione_1e30g(s, altezza_sciame, altezza_detector))
    risu_1f30g.append(simulazione_1f30g(s, altezza_sciame, altezza_detector))
    risu_1e35g.append(simulazione_1e35g(s, altezza_sciame, altezza_detector))
    risu_1f35g.append(simulazione_1f35g(s, altezza_sciame, altezza_detector))
    risu_1e40g.append(simulazione_1e40g(s, altezza_sciame, altezza_detector))
    risu_1f40g.append(simulazione_1f40g(s, altezza_sciame, altezza_detector))
    risu_1e45g.append(simulazione_1e45g(s, altezza_sciame, altezza_detector))
    risu_1f45g.append(simulazione_1f45g(s, altezza_sciame, altezza_detector))
'''
df_risu_1e0g = pd.DataFrame(risu_1e0g, columns=["Simulazione 1e-, angolo=0"])
percorso_file = "simulazione_1e0g.csv"
df_risu_1e0g.to_csv(percorso_file, index=False)

df_risu_1f0g = pd.DataFrame(risu_1f0g, columns=["Simulazione 1f-, angolo=0"])
percorso_file = "simulazione_1f0g.csv"
df_risu_1f0g.to_csv(percorso_file, index=False)

df_risu_1e5g = pd.DataFrame(risu_1e5g, columns=["Simulazione 1e-, angolo=5"])
percorso_file = "simulazione_1e5g.csv"
df_risu_1e5g.to_csv(percorso_file, index=False)

df_risu_1f5g = pd.DataFrame(risu_1f5g, columns=["Simulazione 1f-, angolo=5"])
percorso_file = "simulazione_1f5g.csv"
df_risu_1f5g.to_csv(percorso_file, index=False)

df_risu_1e10g = pd.DataFrame(risu_1e10g, columns=["Simulazione 1e-, angolo=10"])
percorso_file = "simulazione_1e10g.csv"
df_risu_1e10g.to_csv(percorso_file, index=False)

df_risu_1f10g = pd.DataFrame(risu_1f10g, columns=["Simulazione 1f-, angolo=10"])
percorso_file = "simulazione_1f10g.csv"
df_risu_1f10g.to_csv(percorso_file, index=False)

df_risu_1e15g = pd.DataFrame(risu_1e15g, columns=["Simulazione 1e-, angolo=15"])
percorso_file = "simulazione_1e15g.csv"
df_risu_1e15g.to_csv(percorso_file, index=False)

df_risu_1f15g = pd.DataFrame(risu_1f15g, columns=["Simulazione 1f-, angolo=15"])
percorso_file = "simulazione_1f15g.csv"
df_risu_1f15g.to_csv(percorso_file, index=False)

df_risu_1e20g = pd.DataFrame(risu_1e20g, columns=["Simulazione 1e-, angolo=20"])
percorso_file = "simulazione_1e20g.csv"
df_risu_1e20g.to_csv(percorso_file, index=False)

df_risu_1f20g = pd.DataFrame(risu_1f20g, columns=["Simulazione 1f-, angolo=20"])
percorso_file = "simulazione_1f20g.csv"
df_risu_1f20g.to_csv(percorso_file, index=False)

df_risu_1e25g = pd.DataFrame(risu_1e25g, columns=["Simulazione 1e-, angolo=25"])
percorso_file = "simulazione_1e15g.csv"
df_risu_1e25g.to_csv(percorso_file, index=False)

df_risu_1f25g = pd.DataFrame(risu_1f25g, columns=["Simulazione 1f-, angolo=25"])
percorso_file = "simulazione_1f25g.csv"
df_risu_1f25g.to_csv(percorso_file, index=False)

df_risu_1e30g = pd.DataFrame(risu_1e30g, columns=["Simulazione 1e-, angolo=30"])
percorso_file = "simulazione_1e30g.csv"
df_risu_1e30g.to_csv(percorso_file, index=False)

df_risu_1f30g = pd.DataFrame(risu_1f30g, columns=["Simulazione 1f-, angolo=30"])
percorso_file = "simulazione_1f30g.csv"
df_risu_1f30g.to_csv(percorso_file, index=False)

df_risu_1e35g = pd.DataFrame(risu_1e35g, columns=["Simulazione 1e-, angolo=35"])
percorso_file = "simulazione_1e35g.csv"
df_risu_1e35g.to_csv(percorso_file, index=False)

df_risu_1f35g = pd.DataFrame(risu_1f35g, columns=["Simulazione 1f-, angolo=35"])
percorso_file = "simulazione_1f35g.csv"
df_risu_1f35g.to_csv(percorso_file, index=False)

df_risu_1e40g = pd.DataFrame(risu_1e40g, columns=["Simulazione 1e-, angolo=40"])
percorso_file = "simulazione_1e40g.csv"
df_risu_1e40g.to_csv(percorso_file, index=False)

df_risu_1f40g = pd.DataFrame(risu_1f40g, columns=["Simulazione 1f-, angolo=40"])
percorso_file = "simulazione_1f40g.csv"
df_risu_1f40g.to_csv(percorso_file, index=False)

df_risu_1e45g = pd.DataFrame(risu_1e45g, columns=["Simulazione 1e-, angolo=45"])
percorso_file = "simulazione_1e45g.csv"
df_risu_1e45g.to_csv(percorso_file, index=False)

df_risu_1f45g = pd.DataFrame(risu_1f45g, columns=["Simulazione 1f-, angolo=45"])
percorso_file = "simulazione_1f45g.csv"
df_risu_1f45g.to_csv(percorso_file, index=False)
'''
print(risu_1e0g, 
risu_1f0g,
risu_1e5g,
risu_1f5g,
risu_1e10g,
risu_1f10g,
risu_1e15g,
risu_1f15g,
risu_1e20g,
risu_1f20g,
risu_1e25g,
risu_1f25g,
risu_1e30g,
risu_1f30g,
risu_1e35g,
risu_1f35g,
risu_1e40g,
risu_1f40g,
risu_1e45g,
risu_1f45g)

