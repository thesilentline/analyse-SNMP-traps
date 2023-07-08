import pandas as pd

def decoding_snmp_traps(trap_oid):
    df= pd.read_csv("traplogs_oid.csv")
    oid_values_dict = {}
    for i in range(df.shape[0]-1):
        oid_values_dict[df["Trap OIDs"][i]]=df["Description"][i]
    return oid_values_dict[trap_oid]
    