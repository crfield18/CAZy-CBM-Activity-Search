# CAZy Database Parse

<!-- Brief description -->

This is a series of scripts that parse and extract information about each carbohydrate binding module (CBM) family from the [**C**arbohydrate **A**ctive en**ZY**me Database](http://www.cazy.org/Carbohydrate-Binding-Modules.html).

___
<!-- What is CAZy? -->
## What is the **C**arbohydrate **A**ctive en**ZY**me Database?

CAZy is an online database created in 1998 that holds genomic, structural and biochemical information about Carbohydrate-Active Enzymes (CAZymes) and their associated modules.

These include:

* Glycoside Hydrolases (GH)
* GlycosylTransferases (GT)
* Polysaccharide Lyases (PL)
* Carbohydrate Esterases (CE)
* Auxilliary Activities (AA)
* Carbohydrate Binding Modules (CBM)

___
<!-- How do the scripts work? -->
## Included Scripts

### **cazy_parse.py**

Consolidates the 'Activity in Family' information from each CBM page into a single excel file. 'Note' information is used in place of 'Activity in Fimily' if that field is not populated.

### **database_trim.py**

Downloads and extracts each CBM listed in the CAZy database across bacteria, archaea, viruses and eukaryota.

### **functions.py**

Generic functions used across the other scripts.
___
<!-- Dependencies -->
## Dependencies

* pandas 1.5.2
* python3-wget 3.2

Written in **Python 3.10.9**
