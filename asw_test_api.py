import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import streamlit as st
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

conn = st.connection("postgres", type="sql")


query='SELECT * FROM "Raman_simulated_1"'

df_aws=conn.query(query,ttl="10m")

st.dataframe(df_aws)

compound = st.selectbox(
    'Which chemical would you like to show raman spectra ?',
    df_aws['Label'].unique())
concentration= st.selectbox(
    'What concentration would you like to plot ?',
    df_aws['Concentration'].unique())

df_sub=df_aws[(df_aws['Label'] == compound) & (df_aws['Concentration'] == concentration)]

st.dataframe(df_sub)

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df_sub['wavenumber'], df_sub['intensity'], label='Mixture', linewidth=2)
ax.set_xlabel("Raman shift (cm⁻¹)")
ax.set_ylabel("Intensity (a.u.)")
        
st.pyplot(fig)


