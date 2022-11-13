import pandas as pd
import numpy as np

df =  pd.read_csv("/Users/vaps/Documents/GitHub/Analisis-de-series-de-tiempo/Practica 2/prueba.csv")


data = df["prediction"]
x = np.array(data)

# Mean
mean = np.mean(data)

# Variance
var = np.var(data)

# Normalized data
ndata = data - mean

acorr = np.correlate(ndata, ndata, 'full')[len(ndata)-1:] 
acorr = acorr / var / len(ndata)

print(acorr)


