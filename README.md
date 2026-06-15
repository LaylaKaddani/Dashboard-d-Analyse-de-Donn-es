
# Dashboard d'Analyse - Qualité de l'Eau - Alpamare Saïdia

## Contexte
Projet réalisé lors de mon stage d'initiation chez **Alpamare Saïdia** (juillet 2024) dans le cadre de ma formation en Génie Informatique Embarquée.

## Mission
Développement d'un tableau de bord Python pour :
- **Analyser** la qualité de l'eau des piscines
- **Visualiser** la consommation des produits chimiques (chlore, pH-, etc.)
- **Automatiser** le suivi des indicateurs clés

## Technologies Utilisées
- **Python** (Pandas, Matplotlib, Seaborn)
- **Excel** pour la source de données
- **PyInstaller** pour le packaging

## Fonctionnalités
1. **Import automatisé** des données Excel
2. **Nettoyage et transformation** des données
3. **Visualisations interactives** :
   - Histogrammes par produit chimique
   - Suivi du pH (avec zone optimale 7-7.4)
   - Indicateurs clés (coût par client, totaux)
4. **Export graphique** pour reporting

## Installation & Exécution

```bash
# 1. Installer les dépendances
pip install -r code/requirements.txt

# 2. Exécuter le dashboard
python code/dashboard_alpamare.py


Note : Le programme nécessite un fichier Excel avec la structure spécifique.
Pour tester, vous pouvez créer un fichier Excel minimal avec les colonnes :

Métrique, Chlore Galet, Chlore Granulé, PH-, Floculent, Anti-algue, DPD1, DPD3, Redphenol
