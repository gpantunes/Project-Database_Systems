import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import numpy as np

categories = ['Baseline', 'Final']

tpm_values = [249_908, 570_651]
nopm_values = [108_701, 248_823]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, tpm_values, width, label='TPM', color='skyblue')
bars2 = ax.bar(x + width/2, nopm_values, width, label='NOPM', color='lightgreen')

ax.set_xlabel('Category')
ax.set_ylabel('Performance')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:,}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plt.show()
