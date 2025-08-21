import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path
import numpy as np

# Préparation dossier sortie
outdir = './figures'
outdir_path = Path(outdir)
outdir_path.mkdir(parents=True, exist_ok=True)

# Charger les données
df = pd.read_csv('train.csv')

# === Premier graphe : scatter 2D altitude vs gs_mps ===
plt.figure(figsize=(10, 7))
sns.scatterplot(data=df, x='alt_m', y='gs_mps', hue='phase', palette='Set1')
plt.title('Altitude vs Ground Speed')
plt.xlabel('Altitude (m)')
plt.ylabel('Ground Speed (m/s)')
plt.legend(title='Phase')
plt.tight_layout()

# Sauvegarder premier graphe
plt.savefig(outdir_path / 'scatter_alt_gs.png')
plt.close()

# === Deuxième graphe : scatter 3D alt_m, gs_mps, vs_mps ===
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Couleurs par phase
palette = sns.color_palette("Set1", n_colors=len(df['phase'].unique()))
phase_to_color = {phase: palette[i] for i, phase in enumerate(df['phase'].unique())}
colors = df['phase'].map(phase_to_color)

# Scatter 3D
ax.scatter(df['alt_m'], df['gs_mps'], df['vs_mps'], c=colors, s=20)

# Légende manuelle
for phase, color in phase_to_color.items():
    ax.scatter([], [], [], c=[color], label=phase)
ax.legend(title='Phase')

# Labels et titre
ax.set_xlabel('Altitude (m)')
ax.set_ylabel('Ground Speed (m/s)')
ax.set_zlabel('Vertical Speed (m/s)')
ax.set_title('Visualisation 3D des phases de vol')
plt.tight_layout()

# Sauvegarder deuxième graphe
plt.savefig(outdir_path / '3d_alt_gs_vs.png')
plt.close()

