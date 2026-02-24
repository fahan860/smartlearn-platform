"""
Script d'exécution: Pipeline Spark complet
Exécute le feature engineering Spark + chargement MySQL

Usage:
    python spark/run_pipeline.py [--clear] [--mysql-password PASSWORD]
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime


def run_command(cmd, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*80}")
    print(f"🚀 {description}")
    print(f"{'='*80}")
    print(f"Commande: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Erreur lors de {description}")
        return False
    
    print(f"\n✓ {description} terminé")
    return True


def main():
    parser = argparse.ArgumentParser(description="Pipeline Spark complet")
    parser.add_argument("--clear", action="store_true", help="Vider les tables MySQL avant import")
    parser.add_argument("--mysql-host", default="localhost", help="Hôte MySQL")
    parser.add_argument("--mysql-user", default="root", help="Utilisateur MySQL")
    parser.add_argument("--mysql-password", default="", help="Mot de passe MySQL")
    parser.add_argument("--skip-spark", action="store_true", help="Sauter le job Spark (utiliser données existantes)")
    parser.add_argument("--skip-mysql", action="store_true", help="Sauter l'import MySQL")
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    
    print("=" * 80)
    print("🎯 PIPELINE SPARK - LEARNING PLATFORM")
    print("=" * 80)
    print(f"⏰ Démarrage: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Répertoire: {os.getcwd()}")
    print("=" * 80)
    
    # Étape 1: Feature Engineering avec Spark
    if not args.skip_spark:
        spark_cmd = [
            sys.executable,
            "spark/jobs/feature_engineering.py"
        ]
        
        if not run_command(spark_cmd, "ÉTAPE 1/2: Feature Engineering (Spark)"):
            sys.exit(1)
    else:
        print("\n⏩ Spark ignoré (--skip-spark)")
    
    # Étape 2: Chargement dans MySQL
    if not args.skip_mysql:
        mysql_cmd = [
            sys.executable,
            "spark/jobs/load_to_mysql.py",
            "--host", args.mysql_host,
            "--user", args.mysql_user,
            "--password", args.mysql_password,
        ]
        
        if args.clear:
            mysql_cmd.append("--clear")
        
        if not run_command(mysql_cmd, "ÉTAPE 2/2: Chargement MySQL"):
            sys.exit(1)
    else:
        print("\n⏩ MySQL ignoré (--skip-mysql)")
    
    # Résumé final
    duration = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 80)
    print("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 80)
    print(f"⏱️  Durée totale: {duration:.2f}s")
    print(f"📂 Données: data/processed/")
    print(f"🗄️  Base: MySQL smartlearn")
    print("=" * 80)
    print("\n🎉 Phase 2 complète! Vous pouvez maintenant:")
    print("   1. Tester les requêtes ML sur MySQL")
    print("   2. Entraîner les modèles de recommandation")
    print("   3. Configurer Airflow pour l'automatisation")
    print("=" * 80)


if __name__ == "__main__":
    main()
