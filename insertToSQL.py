import json
import psycopg2

# Load JSON
with open("angiospecies.json", "r", encoding="utf-8") as f:
    species_data = json.load(f)

# Connect to Postgres
conn = psycopg2.connect(
    host="localhost",
    dbname="vegetation data",
    user="postgres",
    password="root"
)
cur = conn.cursor()

# Insert species and species_type
for sp in species_data:
    # Insert main species table
    cur.execute("""
        INSERT INTO species (
            species_id, common_name, genus, genus_id, genus_common_name, species,
            kingdom, itis_taxonomic_sn, functional_type, class_id, class_common_name,
            class_name, order_id, order_common_name, order_name, family_id, family_name, family_common_name
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (species_id) DO NOTHING
    """, (
        sp.get('species_id'), sp.get('common_name'), sp.get('genus'), sp.get('genus_id'),
        sp.get('genus_common_name'), sp.get('species'), sp.get('kingdom'), sp.get('itis_taxonomic_sn'),
        sp.get('functional_type'), sp.get('class_id'), sp.get('class_common_name'), sp.get('class_name'),
        sp.get('order_id'), sp.get('order_common_name'), sp.get('order_name'),
        sp.get('family_id'), sp.get('family_name'), sp.get('family_common_name')
    ))

    # Insert nested species_type entries
    for st in sp.get('species_type', []):
        # Convert User_Display to boolean
        user_display_bool = bool(st.get('User_Display')) if st.get('User_Display') is not None else None

        cur.execute("""
            INSERT INTO species_type (
                species_id, species_type_id, species_type, comment, user_display, kingdom, image_path
            ) VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            sp.get('species_id'), st.get('Species_Type_ID'), st.get('Species_Type'),
            st.get('Comment'), user_display_bool, st.get('Kingdom'), st.get('Image_Path')
        ))

# Commit and close
conn.commit()
cur.close()
conn.close()
