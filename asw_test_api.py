import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

user_aws = 'postgres'
password_aws = 'Ulk9froba'  
host_aws = 'raman-spectra-simulated.cst66uws8ol9.us-east-1.rds.amazonaws.com'
database_aws = 'Raman_simulated'

    # Connect to the default 'postgres' database to create a new one
conn = psycopg2.connect(
    dbname=database_aws,
    user=user_aws,
    password="Ulk9froba",  # replace with the password you set earlier
    host=host_aws,
    port = '5432'
)


cur = conn.cursor()


query='SELECT * FROM "Raman_simulated_1"'
cur.execute(query)

df_aws=pd.DataFrame(cur.fetchall())

compound = st.selectbox(
    'Which chemical would you like to show raman spectra ?',
    df_aws[0].unique())
concentration= st.selectbox(
    'What concentration would you like to plot ?',
    df_aws[1].unique())

compound="Lactate"
concentration=0.5

df_sub=df_aws[(df_aws[0] == 'Lactate') & (df_aws[1] == 0.5)]

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df_sub[2], df_sub[3], label='Mixture', linewidth=2)
ax.set_xlabel("Raman shift (cm⁻¹)")
ax.set_ylabel("Intensity (a.u.)")
        
st.pyplot(fig)

cur.close()
conn.close()
