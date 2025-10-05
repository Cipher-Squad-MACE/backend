import json
import psycopg2

# Load JSON file
with open("phenophases.json", "r", encoding="utf-8") as f:
    phenophases_data = json.load(f)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="vegetation data",
    user="postgres",
    password="root"
)
cur = conn.cursor()

# Insert each phenophase
for ph in phenophases_data:
    cur.execute("""
        INSERT INTO phenophases (phenophase_id, phenophase_name, phenophase_category, color, pheno_class_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (phenophase_id) DO NOTHING
    """, (
        ph.get('phenophase_id'),
        ph.get('phenophase_name'),
        ph.get('phenophase_category'),
        ph.get('color'),
        ph.get('pheno_class_id')
    ))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Phenophases inserted successfully!")
