import mysql.connector
import pandas as pd

# Connect to your EMS database
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="hemanth",
    password="Hemanth",
    database="EMS",
    port=3306
)

# Query all employees with project info
query = """
    SELECT 
        e.id, e.name, e.department, e.role, e.email, e.phone, e.address,
        e.salary, e.bonus, e.performance_rating, e.number_of_working_days,
        p.name AS project_name, p.status AS project_status
    FROM Employees e
    LEFT JOIN Projects p ON e.current_project_id = p.id
"""

# Load to DataFrame
df = pd.read_sql(query, conn)
conn.close()

# Export to CSV
df.to_csv("employees_data.csv", index=False)
print("✅ Exported employees_data.csv")
