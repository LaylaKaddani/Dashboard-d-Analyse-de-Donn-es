
```python
"""
Extrait de code 
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
import os


def renommer_colonnes(df):
    """Renomme les colonnes du DataFrame"""
    df.columns = ['Métrique', 'Chlore Galet', 'Chlore Granulé', 'PH-',
                  'Floculent', 'Anti-algue', 'DPD1', 'DPD3', 'Redphenol']
    return df


def filtrer_donnees(df, métriques_interet):
    """Filtre les données selon les métriques d'intérêt"""
    return df[df['Métrique'].isin(métriques_interet)]


def convertir_donnees_long_format(df):
    """Convertit les données en format long pour la visualisation"""
    return df.melt(id_vars='Métrique', var_name='Variable', value_name='Valeur')


def tracer_histogramme(ax, données, titre, couleur):
    """Crée un histogramme pour un produit chimique"""
    sns.barplot(data=données, x='Métrique', y='Valeur', ax=ax, color=couleur)
    ax.set_title(titre)
    for label in ax.get_xticklabels():
        label.set_rotation(8)
    ax.set_xlabel('')
    ax.set_ylabel('')


def tracer_comparaison_ph(ax, données_ph):
    """Crée un graphique de comparaison des pH"""
    sns.barplot(x='Jour', y='Moyenne PH', data=données_ph,
                palette='viridis', hue='Jour', dodge=False, ax=ax)
    ax.set_title('Comparaison des moyennes de pH')
    ax.set_xlabel('Jour')
    ax.set_ylabel('Moyenne de pH')
    ax.axhspan(7, 7.4, color='lightgreen', alpha=0.4)
    for label in ax.get_xticklabels():
        label.set_rotation(90)


def obtenir_metriques_supplementaires(df):
    """Récupère les métriques supplémentaires (clients, coûts)"""
    return df[df['Métrique'].isin(['Total des consomation ', 'Cout /client ', 'Total des clients'])]


def ajouter_boites_texte(fig, total_clients, cout_par_client, total_consommations):
    """Ajoute des boîtes de texte avec les indicateurs clés"""
    fig.text(0.1, 0.97, 'Total Client', fontsize=14, weight='bold')
    fig.text(0.1, 0.934, f"{total_clients:.0f}", fontsize=16)
    fig.text(0.4, 0.97, 'Cout /client', fontsize=14, weight='bold')
    fig.text(0.4, 0.934, f"{cout_par_client:.3f}", fontsize=16)
    fig.text(0.7, 0.97, 'Total des consommations', fontsize=14, weight='bold')
    fig.text(0.7, 0.934, f"{total_consommations:.3f}", fontsize=16)
    fig.text(0.01, 0.02, "Tableau de Bord d'Alpamare Saidia", 
             fontsize=20, color='blue', weight='bold')


def dessiner_rectangles(fig):
    """Ajoute des rectangles colorés pour les indicateurs"""
    rect1 = Rectangle((0.07, 0.92), 0.15, 0.1, fill=True, 
                      color='cyan', transform=fig.transFigure, figure=fig)
    rect2 = Rectangle((0.37, 0.92), 0.15, 0.1, fill=True, 
                      color='red', transform=fig.transFigure, figure=fig)
    rect3 = Rectangle((0.67, 0.92), 0.25, 0.1, fill=True, 
                      color='yellow', transform=fig.transFigure, figure=fig)
    fig.patches.extend([rect1, rect2, rect3])


def main():
    """Fonction principale - Orchestre le dashboard"""
    # Charger les données
    chemin_fichier = os.path.join(Path.cwd(), "Traitement d'eau - Copie.xlsx")
    df = pd.read_excel(chemin_fichier, sheet_name="Tableau de bord")
    df = renommer_colonnes(df)

    # Filtrer les données
    métriques_interet = ['Cumulé de la consomation/Qté', 'Cumulé de la consomation/Prix']
    données_filtrées = filtrer_donnees(df, métriques_interet)
    données_long_format = convertir_donnees_long_format(données_filtrées)

    # Créer la figure avec sous-graphiques
    fig, axs = plt.subplots(2, 4, figsize=(12, 5))

    # Graphiques pour chaque produit chimique
    produits = [
        ('Chlore Galet', 'blue', axs[0, 0]),
        ('Chlore Granulé', 'green', axs[0, 1]),
        ('PH-', 'red', axs[0, 2]),
        ('Anti-algue', 'cyan', axs[1, 0]),
        ('DPD1', 'purple', axs[1, 1]),
        ('DPD3', 'brown', axs[1, 2]),
        ('Redphenol', 'pink', axs[1, 3])
    ]

    for produit, couleur, ax in produits:
        données_produit = données_long_format[données_long_format['Variable'] == produit]
        tracer_histogramme(ax, données_produit, produit, couleur)

    # Comparaison des pH
    pf = pd.read_excel(chemin_fichier, sheet_name="Piscine à vague")
    pf['Jour'] = pd.to_datetime(pf['Jour'], format='%d/%m/%Y')
    
    jours_interet = pd.to_datetime(['01/06/2024', '09/06/2024', '19/06/2024', '30/06/2024'], 
                                   format='%d/%m/%Y')
    données_ph = pf[pf['Jour'].isin(jours_interet)][['Jour', 'moyenne PH']]
    données_ph.rename(columns={'moyenne PH': 'Moyenne PH'}, inplace=True)
    
    # Créer un nouvel axe pour le graphique pH
    tracer_comparaison_ph(axs[0, 3], données_ph)

    # Métriques supplémentaires
    métriques_supplementaires = obtenir_metriques_supplementaires(df)
    total_consommations = métriques_supplementaires[
        métriques_supplementaires['Métrique'] == 'Total des consomation '
    ]['Chlore Galet'].values[0]
    
    cout_par_client = métriques_supplementaires[
        métriques_supplementaires['Métrique'] == 'Cout /client '
    ]['Chlore Galet'].values[0]
    
    total_clients = métriques_supplementaires[
        métriques_supplementaires['Métrique'] == 'Total des clients'
    ]['Chlore Galet'].values[0]

    # Ajouter indicateurs
    ajouter_boites_texte(fig, total_clients, cout_par_client, total_consommations)
    dessiner_rectangles(fig)
    
    # Ajuster la disposition
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


if __name__ == "__main__":
    main()
