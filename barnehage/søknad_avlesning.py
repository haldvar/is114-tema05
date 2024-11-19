from dbexcel import barnehage
from kgcontroller import select_alle_barnehager

pri_string_test = "6, 5, 1"
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
            

def behandle_soknad(priority):
    tilgjengelige_barnehager = []
    for pri_nr in pri_list:
        for bh in alle_barnehager:
            if (int(pri_nr) == bh.barnehage_id and bh.barnehage_ledige_plasser > 0):
                tilgjengelige_barnehager = [bh.barnehage_navn] + tilgjengelige_barnehager
    print("Du har fått tilbud om plass hos disse barnehagene: ", tilgjengelige_barnehager)
    
    
    
print(behandle_soknad(pri_list))
#hvis man setter list() foran en liste så lager den en kopi



#def soknad_svar(pri_list):
##    for nr in pri_list:
#        
#        #selekter barnehager bruker har spurt etter
#        return ['barnehage_id'[pri_list[nr]]]
#    if
    
    
            
        
        
