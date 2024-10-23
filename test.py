from nepalicalender import nepali_details
d=nepali_details(2002,2,6)
for k,v in d.items():
    print(f"{k} : {v}")

d=nepali_details(2007,10,7)
for k,v in d.items():
    print(f"{k} : {v}")