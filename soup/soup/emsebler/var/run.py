import pandas as pd
import os
import re

dir_path = os.path.dirname(os.path.abspath(__file__))

#### !!! VARIABLE ======================== !!!  #####
#### !!! VARIABLE ======================== !!!  #####
#### !!! VARIABLE ======================== !!!  #####

marque = pd.read_excel(f"{dir_path}/MILWAUKEE.xlsx")
idf    = pd.read_excel(f"{dir_path}/idf_total.xlsx")
tool   = pd.read_excel(f"{dir_path}/tool_total.xlsx")
double_data = 0
total = 0



#TOTAL PRODUIT =20552


marque_details
marque_su


print(len(marque) + len(idf) + len(tool))
# END !!!
"""
for index_marque in marque.index:
    reference = marque.loc[index_marque, "Référence"]
    for index_tool in tool.index:
        #if "MILWAUKEE" in str(tool.loc[index_tool, 'marque']):
            tool_reference = tool.loc[index_tool, "Reference"]
            tool_reference = str(tool_reference).replace("'", "")

            ###################################
            ###### UNTIL HERE IS GOOD !!! #####
            ###################################

            if str(reference) in str(tool_reference):
                #print(tool_reference)
                ##print(reference)
                double_data += 1
                print(f"Time : {double_data} & REFERENCE: {tool.loc[index_tool, 'marque']} ")
                tool.drop(index_tool,)
        #else:
        #continue
else:
     tool.to_excel("idf_total.xlsx", index=False)

"""
