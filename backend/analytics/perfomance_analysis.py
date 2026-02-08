import pandas as pd
from database import execute_query

def get_performance_stats(class_id=None):
    query = """
        SELECT 
            s.id,
            CONCAT(s.first_name, ' ', s.last_name) as student_name,
            g.subject,
            AVG(g.marks_obtained / g.total_marks * 100) as avg_percentage
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE 1=1
    """
    
    params = []
    if class_id:
        query += " AND g.class_id = %s"
        params.append(class_id)
    
    query += " GROUP BY s.id, student_name, g.subject"
    
    data = execute_query(query, tuple(params), fetch_all=True)
    
    if data:
        df = pd.DataFrame(data)
        return df.to_dict('records')
    
    return []
