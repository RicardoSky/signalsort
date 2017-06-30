# signalsort
Describe:
You can use PDW to sort radar singal 
The signalsort.py is the main.  Just python signalsort.py
You need get the PDW.txt in the D:\\work\\*.txt  || Example: D:\\work\\TOA.txt 
All the input data : TOA.txt PW.txt DOA_fuyang.txt DOA_fangwei.txt CF.txt
About the .py:
The K-means algorithm is used to sort DOA and cf ,then use the SDIF algorithm to sort the pulse sequence.
We can recognized four kind : constant, stagger, jitter, hop-frequency radar  
