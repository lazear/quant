
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from datetime import timedelta
from scipy.interpolate import CubicSpline

df = pd.read_csv('data/yields.csv')
df.dropna(inplace=True)
x = []
y = []
z = []

header = []
# header = [1, 3, 6, 12, 24, 36, 60, 72, 120, 240, 360]
for name in df.columns[1:]:
    maturity = float(name.split(" ")[0])
    if name.split(" ")[1] == 'Mo':
        maturity = maturity / 12
    header.append(maturity)

YEAR = 2019

xs = np.arange(0, len(header))
print(xs, header)
for idx, row in df.iterrows():
	d = (datetime.strptime(row['Date'], '%m/%d/%Y') - datetime(YEAR, 1, 1)).days
	if d < 0:
		continue
	x.append([d for x in range(0, len(xs))])
	y.append(header)
	z.append(CubicSpline(xs, row[1:])(xs))

x = np.array(x)
y = np.array(y)
z = np.array(z)


fig = plt.figure()
ax = fig.gca(projection='3d')

print(x.shape, y.shape, z.shape)
surf = ax.plot_surface(x, y, z, cmap='viridis', rstride=1, cstride=1,
                       linewidth=0, antialiased=True)
# ax.set_xlabel('Date')
ax.set_ylabel('Time to maturity (years)')
ax.set_zlabel('Yield')

plt.title('Daily yield curve')
def format_date(x, pos=None):
     return (datetime(YEAR, 1, 1) + timedelta(days = x)).strftime("%Y-%m-%d")
ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()