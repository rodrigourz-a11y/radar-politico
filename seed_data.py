import pymysql
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 4000)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cur = conn.cursor()

    politicians = [
        ("Concejal 1 LG", "Concejal", "La Granja", "Izquierda", "concejal1_lg", "concejal1_lg", "concejal1_lg"),
        ("Concejal 2 LG", "Concejal", "La Granja", "Izquierda", "concejal2_lg", "concejal2_lg", "concejal2_lg"),
        ("Concejal 3 LG", "Concejal", "La Granja", "Derecha", "concejal3_lg", "concejal3_lg", "concejal3_lg"),
        ("Concejal 4 LG", "Concejal", "La Granja", "Izquierda", "concejal4_lg", "concejal4_lg", "concejal4_lg"),
        ("Concejal 5 LG", "Concejal", "La Granja", "Derecha", "concejal5_lg", "concejal5_lg", "concejal5_lg"),
        ("Concejal 6 LG", "Concejal", "La Granja", "Izquierda", "concejal6_lg", "concejal6_lg", "concejal6_lg"),
        ("Concejal 7 LG", "Concejal", "La Granja", "Independiente", "concejal7_lg", "concejal7_lg", "concejal7_lg"),
        ("Concejal 8 LG", "Concejal", "La Granja", "Izquierda", "concejal8_lg", "concejal8_lg", "concejal8_lg"),
        ("Prospecto Alcalde 1", "Prospecto", "La Granja", "Izquierda", "prospecto1_lg", "prospecto1_lg", "prospecto1_lg"),
        ("Prospecto Alcalde 2", "Prospecto", "La Granja", "Derecha", "prospecto2_lg", "prospecto2_lg", "prospecto2_lg"),
        ("Alcalde Ñuñoa", "Benchmark", "Ñuñoa", "Izquierda", "alcalde_nunoa", "alcalde_nunoa", "alcalde_nunoa"),
        ("Alcalde Providencia", "Benchmark", "Providencia", "Derecha", "alcalde_providencia", "alcalde_providencia", "alcalde_providencia"),
        ("Alcalde Santiago", "Benchmark", "Santiago Centro", "Izquierda", "alcalde_santiago", "alcalde_santiago", "alcalde_santiago"),
        ("Alcalde Maipú", "Benchmark", "Maipú", "Derecha", "alcalde_maipu", "alcalde_maipu", "alcalde_maipu")
    ]

    for p in politicians:
        cur.execute("""
            INSERT IGNORE INTO politicians (name, role, commune, political_leaning, instagram_handle, facebook_handle, tiktok_handle)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, p)
    
    conn.commit()

    cur.execute("SELECT id, name FROM politicians")
    db_politicians = cur.fetchall()
    
    today = datetime.now().date()
    
    for pol_id, pol_name in db_politicians:
        base_followers = 5000 if "Concejal" in pol_name else (20000 if "Prospecto" in pol_name else 80000)
        
        for week in range(12, 0, -1):
            metric_date = today - timedelta(weeks=week-1)
            growth_factor = random.uniform(1.01, 1.05) 
            base_followers = int(base_followers * growth_factor)
            
            engagement = round(random.uniform(1.0, 4.0), 2)
            is_spike = 0
            
            if random.random() < 0.15:
                engagement = round(random.uniform(6.0, 12.0), 2)
                is_spike = 1

            cur.execute("""
                INSERT IGNORE INTO social_metrics 
                (politician_id, platform, metric_date, followers_count, total_posts, engagement_rate, is_activity_spike)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (pol_id, 'Instagram', metric_date, base_followers, random.randint(3, 7), engagement, is_spike))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Datos históricos ficticios inyectados correctamente.")

if __name__ == "__main__":
    seed_database()