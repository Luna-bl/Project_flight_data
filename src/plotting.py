from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import Patch
from matplotlib import cm
from matplotlib.colors import to_hex


def set_style():
    plt.rcParams['figure.figsize'] = (10, 4)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

def plot_altitude(df: pd.DataFrame, outdir: str) -> str:
    set_style()
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(df['timestamp'], df['alt_m'])
    ax.set_title('Altitude Profile')
    ax.set_xlabel('Time')
    ax.set_ylabel('Altitude [m]')
    out = Path(outdir) / 'altitude_profile.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)

def plot_vs(df: pd.DataFrame, outdir: str) -> str:
    set_style()
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(df['timestamp'], df['vs_mps'])
    ax.set_title('Vertical Speed')
    ax.set_xlabel('Time')
    ax.set_ylabel('VS [m/s]')
    out = Path(outdir) / 'vertical_speed.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)

def plot_planview(df: pd.DataFrame, outdir: str) -> str:
    set_style()
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(df['lon'], df['lat'])
    ax.set_title('Plan-View Path')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    out = Path(outdir) / 'plan_view.png'
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return str(out)




def plot_speed_phase_timeline(df: pd.DataFrame, outdir: str) -> str:
    # créer une colonne 'phase_group' qui identifie chaque changement consécutif de phase dans le DataFrame
    # (df['phase'] != df['phase'].shift()) crée une série True chaque fois que la phase change par rapport à la ligne précédente
    # cumsum() fait une somme cumulée pour donner un identifiant unique à chaque groupe de phases consécutives
    df['phase_group'] = (df['phase'] != df['phase'].shift()).cumsum()

    # Groupe par séquence de phases continues
    grouped = df.groupby('phase_group')

    # Couleurs simples pour les phases
    color_map = {
        'taxi': '#1f77b4',       # bleu
        'transition': '#ff7f0e', # orange
        'climb': '#2ca02c',      # vert
        'cruise': '#d62728',     # rouge
        'descent': '#9467bd'     # violet
    }

    fig, ax = plt.subplots(figsize=(10, 2)) # sublots affiche les axes automatiquement
    start_time = df['timestamp'].iloc[0]  # Prendre le premier timestamp comme référence de départ pour la timeline


    for _, group in grouped:
        phase = group['phase'].iloc[0] # on recupere la phase 
        start = (group['timestamp'].iloc[0] - start_time).total_seconds()# Calculer le temps de début relatif en secondes depuis start_time
        end = (group['timestamp'].iloc[-1] - start_time).total_seconds()#Calculer le temps de fin relatif en secondes depuis start_time
        ax.barh(0, end - start, left=start, height=0.4, color=color_map.get(phase, 'gray')) # Dessiner une barre horizontale correspondant à la durée de la phase, à la position y=0, avec la couleur correspondante


    ax.set_yticks([]) # Ne pas afficher de graduation verticale sur l'axe y (car on a juste une ligne horizontale)
    ax.set_xlabel('Time( seconds)')
    ax.set_title('Flight Phases Timeline')
    ax.set_xlim(0, (df['timestamp'].iloc[-1] - start_time).total_seconds())

    # Légende 
    handles = [plt.Rectangle((0,0),1,1, color=color_map[phase]) for phase in color_map]
    ax.legend(handles, color_map.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout() # Ajuster la mise en page pour éviter que des éléments ne soient coupés
    out = Path(outdir) / 'speed_phase_timeline.png'
    fig.savefig(out)
    plt.close(fig)
    return str(out)



# def plot_speed_phase_timeline(df: pd.DataFrame, outdir: str) -> str:
#     set_style() # fonction definie au dessus, gere les parametres taille, grille
#     fig, ax = plt.subplots(figsize=(12, 5)) # subplot cree des axes automatiquement

#     # Identifier les changements de phase
#     df['phase_change'] = (df['phase'] != df['phase'].shift()).cumsum() # df['phase_change']  est la colonne avec les phases de vol 
#     grouped = df.groupby('phase_change')

#     # Définir une couleur unique par phase
#     unique_phases = df['phase'].unique()
#     cmap = cm.get_cmap('tab20', len(unique_phases))
#     phase_colors = {phase: to_hex(cmap(i)) for i, phase in enumerate(unique_phases)}

#     # Début du vol pour l’axe des temps (en secondes)
#     start_time = df['timestamp'].iloc[0]

#     for _, group in grouped:
#         phase = group['phase'].iloc[0]
#         phase_start = group['timestamp'].iloc[0]
#         phase_end = group['timestamp'].iloc[-1]
#         duration = (phase_end - phase_start).total_seconds()
#         offset = (phase_start - start_time).total_seconds()

#         ax.barh(
#             y=phase,
#             width=duration,
#             left=offset,
#             height=0.5,
#             color=phase_colors.get(phase, 'gray'),
#             edgecolor='black'
#         )

#     ax.set_xlabel("Time [seconds]")
#     ax.set_title("Flight Phases Timeline (Gantt Style)")
#     ax.set_yticks(range(len(unique_phases)))
#     ax.set_yticklabels(unique_phases)
#     ax.invert_yaxis()  # Gantt-style: phases from top to bottom

#     # Créer une légende propre
#     legend_elements = [Patch(facecolor=color, label=phase) for phase, color in phase_colors.items()]
#     ax.legend(handles=legend_elements, title='Phases', loc='lower right')

#     out = Path(outdir) / 'speed_phase_timeline.png'
#     fig.tight_layout()
#     fig.savefig(out)
#     plt.close(fig)

#     return str(out)


# def plot_speed_phase_timeline(df: pd.DataFrame, outdir: str) -> str:
#     fig, ax = plt.subplots(figsize=(10, 3))
#     # On parcourt les phases consécutives pour tracer des barres horizontales
#     start_time = df['timestamp'].iloc[0]
#     prev_phase = df['phase'].iloc[0]
#     phase_start = start_time

#     for i, (ts, phase) in enumerate(zip(df['timestamp'], df['phase'])):
#         if phase != prev_phase or i == len(df) - 1:
#             ax.barh(0, (ts - phase_start).total_seconds(), left=(phase_start - start_time).total_seconds(),
#                     height=0.5, label=prev_phase, alpha=0.6)
#             phase_start = ts
#             prev_phase = phase

#     ax.set_yticks([])
#     ax.set_xlabel('Time (seconds)')
#     ax.set_title('Speed Phase Timeline (Gantt)')
#     ax.legend(loc='upper right') 

#     out = Path(outdir) / 'speed_phase_timeline.png'
#     fig.tight_layout()
#     fig.savefig(out)
#     plt.close(fig)
#     return str(out)



# def plot_speed_with_phase_timeline(df: pd.DataFrame, outdir: str) -> str:
#     fig, ax = plt.subplots(figsize=(10, 3))

#     # Fond coloré pour chaque phase
#     df['phase_change'] = (df['phase'] != df['phase'].shift()).cumsum()
#     grouped = df.groupby('phase_change')
#     color_map = {
#         'taxi': '#1f77b4', 'climb': '#9467bd', 'cruise': '#2ca02c',
#         'descent': '#d62728', 'transition': '#ff7f0e'
#     }

#     for _, group in grouped:
#         start = group['timestamp'].iloc[0]
#         end = group['timestamp'].iloc[-1]
#         phase = group['phase'].iloc[0]
#         ax.axvspan(start, end, color=color_map.get(phase, 'gray'), alpha=0.3)

#     # Courbe de vitesse
#     ax.plot(df['timestamp'], df['tas_mps'], label='Speed (m/s)', color='black')

#     ax.set_title('Speed over Time with Flight Phases')
#     ax.set_xlabel('Time')
#     ax.set_ylabel('Speed (m/s)')
#     ax.legend()
#     fig.tight_layout()

#     out_path = Path(outdir) / 'speed_phase_timeline.png'
#     fig.savefig(out_path)
#     plt.close(fig)
#     return str(out_path)
