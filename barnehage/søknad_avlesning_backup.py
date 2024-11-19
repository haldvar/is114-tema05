from dbexcel import barnehage
from kgcontroller import select_alle_barnehager

pri_string_test = "4, 6"
#pri_string = request.form('liste_over_barnehager_prioritert')
pri_list = (pri_string_test.split(',')) # [5, 1, 3, 7, 2]  ## skal egentlig komme input fra bruker. typ request form
#barnehage[barnehage['barnehage_id'] == 6]
print(pri_list)



alle_barnehager = select_alle_barnehager()


print(alle_barnehager[0].barnehage_ledige_plasser)
print(alle_barnehager)

print()

#for pri_nr in pri_list:
#    for bh in alle_barnehager:
#        if (int(pri_nr) == bh.barnehage_id and bh.barnehage_ledige_plasser != 0):
#            print("Du har fått tilbud om plass hos disse barnehagene: ", bh.barnehage_navn)
            

def behandle_soknad(): #definerer behandlingsprosessen
    tilgjengelige_barnehager = [] #tom liste, skal fylles med barnehager som tilfredstiller kravene fra bruker og det er plass til
    for pri_nr in pri_list: #for hvert tall i prioriteringslisten
        for bh in alle_barnehager: #for hver rad i tabellen med barnehager (barnehage_id)
            if (int(pri_nr) == bh.barnehage_id and bh.barnehage_ledige_plasser > 0): #hvis prioriteringstallet er lik et tall i (barnehage_id) OG den barnehagen har minst én plass
                tilgjengelige_barnehager = [bh.barnehage_navn] + tilgjengelige_barnehager # legg til den godkjente barnehagen i listen
    if(len(tilgjengelige_barnehager) == 0):
        print("Du har dessverre fått avslag på din søknad!")
    else:
        print("Du har fått tilbud om plass hos disse barnehagene: ", tilgjengelige_barnehager) 
    #print("Du har fått tilbud om plass hos disse barnehagene: ", tilgjengelige_barnehager) 
    
    
    
print(behandle_soknad())
#hvis man setter list() foran en liste så lager den en kopi



#def soknad_svar(pri_list):
##    for nr in pri_list:
#        
#        #selekter barnehager bruker har spurt etter
#        return ['barnehage_id'[pri_list[nr]]]
#    if
    
    
            
        
        
