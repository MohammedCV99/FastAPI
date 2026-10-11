
Convertor={
    "show cdp neighbors":"ShowCDPN.textfsm",
        "show ip interface brief":"Showipinterfacebr.textfsm",
    "show interface status":"showinterfacestatus.textfsm",
    "show lldp neighbors":"ShowLLDPN.textfsm",
}
def FSMConvertor(pattren):
    return Convertor[pattren]
