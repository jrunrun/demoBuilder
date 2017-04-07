
growth = [[1,.03],[1.15,.05],[1.175,.07],[1.20,.09],[1.225,.10]]
growth[0][0]=1
growth[0][1]=.03

#number of rows varies by day and year
n = v[0] * (growth[idx][0] + random.uniform(-growth[idx][1],growth[idx][1]))


#SIMPLE 
#number of rows varies by day and year
n = v[0] * growth[idx][0] 