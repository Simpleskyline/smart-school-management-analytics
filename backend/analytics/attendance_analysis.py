import pandas as pd
from database import execute_query

def get_attendance_stats(class_id=None, start_date=None, end_date=None):
    query = """
        SELECT 
            s.id, 
            CONCAT(s.first_name, ' ', s.last_name) as student_name,
            COUNT(a.id) as total_days,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
            SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_days,
            SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_days
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        WHERE 1=1
    """
    
    params = []
    if class_id:
        query += " AND a.class_id = %s"
        params.append(class_id)
    if start_date:
        query += " AND a.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND a.date <= %s"
        params.append(end_date)
    
    query += " GROUP BY s.id, student_name"
    
    data = execute_query(query, tuple(params), fetch_all=True)
    
    if data:
        df = pd.DataFrame(data)
        df['attendance_percentage'] = (df['present_days'] / df['total_days'] * 100).round(2)
        return df.to_dict('records')
    
    return []
