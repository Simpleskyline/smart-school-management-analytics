import pandas as pd
from database import execute_query

def get_fee_collection_stats(academic_year=None):
    query = """
        SELECT 
            f.fee_type,
            COUNT(f.id) as total_fees,
            SUM(f.amount) as total_amount,
            SUM(CASE WHEN f.status = 'Paid' THEN f.amount ELSE 0 END) as collected,
            SUM(CASE WHEN f.status = 'Pending' THEN f.amount ELSE 0 END) as pending
        FROM fees f
        WHERE 1=1
    """
    
    params = []
    if academic_year:
        query += " AND f.academic_year = %s"
        params.append(academic_year)
    
    query += " GROUP BY f.fee_type"
    
    data = execute_query(query, tuple(params), fetch_all=True)
    
    if data:
        df = pd.DataFrame(data)
        df['collection_percentage'] = (df['collected'] / df['total_amount'] * 100).round(2)
        return df.to_dict('records')
    
    return []
