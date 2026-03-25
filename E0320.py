import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.pyplot import figure
import seaborn as sns

df = pd.read_csv(r'C:\Users\ASUS\Project\Project\data\penguins.csv')
print(df.info())
sns.jointplot(data=df ,x = 'bill_length_mm',y = 'flipper_length_mm',kind='hex')
plt.show()