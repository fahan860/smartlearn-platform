"""
Script de diagnostic Spark
Vérifie toutes les dépendances et la configuration

Usage: python spark/check_spark.py
"""

import sys
import os

print("=" * 80)
print("🔍 DIAGNOSTIC SPARK")
print("=" * 80)

# 1. Java
print("\n1️⃣  Java (requis pour Spark):")
try:
    import subprocess
    result = subprocess.run(['java', '-version'], capture_output=True, text=True)
    java_version = result.stderr.split('\n')[0] if result.stderr else "Version inconnue"
    print(f"   ✅ {java_version}")
except Exception as e:
    print(f"   ❌ Java non trouvé: {e}")
    print("   💡 Installez Java JDK 11+ depuis: https://www.oracle.com/java/technologies/downloads/")
    sys.exit(1)

# 2. PySpark
print("\n2️⃣  PySpark:")
try:
    import pyspark
    print(f"   ✅ PySpark {pyspark.__version__} installé")
except ImportError:
    print("   ❌ PySpark non installé")
    print("   💡 Installez: pip install pyspark")
    sys.exit(1)

# 3. Pandas
print("\n3️⃣  Pandas:")
try:
    import pandas as pd
    print(f"   ✅ Pandas {pd.__version__} installé")
except ImportError:
    print("   ❌ Pandas non installé")
    print("   💡 Installez: pip install pandas")

# 4. Test Spark Session
print("\n4️⃣  Test Spark Session:")
try:
    from pyspark.sql import SparkSession
    
    print("   ⏳ Démarrage Spark (peut prendre 10-30s)...")
    spark = SparkSession.builder \
        .appName("DiagnosticTest") \
        .master("local[1]") \
        .config("spark.driver.memory", "512m") \
        .config("spark.ui.enabled", "false") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    
    print(f"   ✅ Spark {spark.version} fonctionne!")
    
    # Test simple
    data = [("Alice", 34), ("Bob", 45), ("Charlie", 23)]
    df = spark.createDataFrame(data, ["name", "age"])
    count = df.count()
    
    print(f"   ✅ Test DataFrame OK ({count} lignes)")
    
    spark.stop()
    print("   ✅ Spark arrêté proprement")
    
except Exception as e:
    print(f"   ❌ Erreur Spark: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. MySQL Connector
print("\n5️⃣  MySQL Connector:")
try:
    import mysql.connector
    print(f"   ✅ MySQL Connector installé")
except ImportError:
    print("   ⚠️  MySQL Connector non installé (optionnel)")
    print("   💡 Pour importer dans MySQL: pip install mysql-connector-python")

# 6. Vérifier les données
print("\n6️⃣  Données source:")
data_dirs = [
    ("data/raw/users", "Users JSON"),
    ("data/raw/courses", "Courses JSON"),
    ("data/raw/interactions", "Interactions JSON"),
    ("data/processed", "Features CSV")
]

for dir_path, desc in data_dirs:
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        if files:
            print(f"   ✅ {desc}: {len(files)} fichier(s)")
        else:
            print(f"   ⚠️  {desc}: répertoire vide")
    else:
        print(f"   ❌ {desc}: répertoire manquant")

# Résumé
print("\n" + "=" * 80)
print("✅ DIAGNOSTIC TERMINÉ - SPARK EST OPÉRATIONNEL")
print("=" * 80)
print("\n📋 Vous pouvez maintenant:")
print("   1. Exécuter le feature engineering:")
print("      python spark/jobs/run_feature_engineering.py")
print("")
print("   2. Version PySpark complète (si cluster Spark disponible):")
print("      python spark/jobs/feature_engineering.py")
print("")
print("   3. Importer dans MySQL:")
print("      python spark/jobs/load_to_mysql.py --password VOTRE_PASSWORD")
print("=" * 80)
