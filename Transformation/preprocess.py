import psycopg2
from Transformation.recommender import preprocessing,feature_extractor,content_recommendation_v1
from Database.postgres import databse_query,Database_connect



def get_recommendation(title):
    return content_recommendation_v1(df=preprocessing(),
                                      title=title,
                                        cosine_sim_df=feature_extractor(preprocessing(),column_name='summary'))



def database_operation(product_id):
    
    conn = Database_connect()
    cursor = conn.cursor()

    query= databse_query(product_id)
    cursor.execute(query)


    # format output
    columns = [column[0] for column in cursor.description]
    groups = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return groups
    