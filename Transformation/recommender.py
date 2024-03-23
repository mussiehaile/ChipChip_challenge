from Database.postgres import database_extractor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config.config_static_files import ConfigStaticFiles
import pandas as pd




def preprocessing():
        # Extract data from the database tables
        product_name = database_extractor('product_names')
        categories = database_extractor('categories')
        products = database_extractor('products')


       # filter product tables
        filtered_product_name, filtered_products = product_name[product_name['id'].isin(products['name_id'])], products[products['name_id'].isin(product_name['id'])]

        # Renaming columns
        filtered_product_name = filtered_product_name.rename(columns={'id': 'product_id', 'name': 'product_name'})
        categories = categories.rename(columns={'name': 'categories_name', 'short_description': 'categories_short_description'})


        # Merging dataframes
        final_product = filtered_product_name.merge(filtered_products, left_on='product_id', right_on='name_id')
        processed = final_product.merge(categories, left_on='category_id', right_on='id')

        #extract relevant columns
        final_processed = processed[['product_id',  'product_name', 'categories_name', 'short_description', 'categories_short_description', 'tags']]
        df = final_processed.copy()


        df['tags'] = df['tags'].apply(lambda x: ' '.join(x))
        cols = ['categories_short_description', 'short_description']
        df[cols] = df[cols].apply(lambda x: x.str.replace(',', ''))

        # fill missing values
        df.loc[(df['categories_short_description'] == 'desc') & (df['categories_name'] == 'Vegetable'), 'categories_short_description'] = ConfigStaticFiles.vegitable_discription
        df.loc[(df['categories_short_description'] == 'desc') & (df['categories_name'] == 'Fruit'), 'categories_short_description'] = ConfigStaticFiles.fruit_discription

        # construct new column for for feature extraction
        df['summary'] = df['categories_name'] + ' ' + df['short_description'] + ' ' + df['categories_short_description'] + ' ' + df['tags']
        df.set_index('product_id', inplace=True)

        return df



def feature_extractor(df,column_name):

        # CountVectorizer and cosine similarity
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(df[column_name])
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        cosine_sim_df = pd.DataFrame(cosine_sim)
        return cosine_sim_df



def content_recommendation_v1(df,title,cosine_sim_df):
        a = df.copy().reset_index().drop('product_id', axis=1)
        index = a[a['product_name'] == title].index[0]
        top_n_index = list(cosine_sim_df[index].nlargest(6).index)
        try:
            top_n_index.remove(index)
        except ValueError:
            pass
        similar_products = []
        for idx in top_n_index:
            product = a['product_name'].iloc[idx]
            similarity = cosine_sim_df[index].iloc[idx]
            similar_products.append({"product_name": product, "cosine_similarity": similarity})
        return similar_products