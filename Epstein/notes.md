# MODEL 1: Generalized Rebellion Against Central Authority

## Agent

Due componenti 
- __H__ (hardship) : il livello di sofferenza che l'agente percepisce. E' esogeno e eterogeneo tra i vari agenti. In questa prima implementazione ciascun valore individuale sarà estratto da una Uniforme(0,1) sull'intervallo (0, 1)
- __L__ (legitimacy) : la legittimità percepita del regime (autorità centrale). E' esogena e uguale per tutti gli agenti. Il suo valore verrà variato nel corso di diverse runs con un range di valori che vanno da 0 a 1.
- __G__ (grievance) : il livello di fastidio che ogni agente prova nei confronti del sistema. Sarà dato da $G = H(1 - L)$ dove $(1 -L)$ rappresenta l'illegittimità del sistema.
- __R__ (risk aversion) : il livello di avversione al rischio del singolo agente. Si comporta in maniera simile a __H__
- __v__ (vision) : il numero di celle a nord, sud, est, ovest dell'agente che può guardare. 

Definito $(C/A)_v$ il rapporto tra poliziotti/agenti attivi nel raggio v, la probabilità di essere arrestato viene definita come $P = 1 -exp[-k (C/A)_v]$. $k$ viene settata in modo da garantire una stima plausibile quando $C = 1$ e $A = 1$ . $A$ è sempre almeno 1 pedrchè ogni agente conta anche se stesso come attivo quando viene calcolata $P$. 

- __N = RP__ : il rischio netto dell'agente. 

Regola dell'agente : Se $G -N > T$ attivati, altrimenti resta quieto. 

## Cop
Gli attributi dei cop sono:
- $v^*$ simile a quella dell'agente.

La regola del poliziotto è : guarda in tutte le celle che puoi guardare e arresta un agente attivo.

## Movimento
La regola del movimento è semplice: vai in una cella random all'interno del tuo campo visivo.

## Grafici
Vengono sempre proiettati due grafici:
1. mostra il livello di Grievance dei vari agenti
2. mostra lo stato degli agenti in base alle loro azioni pubbliche rossi se attivi, blue se calmi. I poliziotti sono mostrati in nero.

## Runs
Lo user seleziona $L, J, v, v*$ e la densità di cop/agent. 

Agli agenti viene assegnato un valore random per $H$ e $R$ e agenti e poliziotti vengono disposti in posizioni randomiche sulla griglia. 
Successivamente il modello gira sotto la regola ${A, C, M}$. Un agente, o un poliziotto e selezionato randomicamente. Si muove in una cella random e esegue la sua azione.

