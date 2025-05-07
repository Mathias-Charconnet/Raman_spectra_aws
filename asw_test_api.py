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

# Load database credentials
config = st.secrets["connections.sql"]

DATABASE_URL = (
    f"{config['dialect']}://{config['username']}:{config['password']}@"
    f"{config['host']}:{config['port']}/{config['database']}"
)

# Use standard SQLAlchemy engine (not async)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
        result = session.execute(query)
        df_aws=pd.DataFrame(result.fetchall())

compound = st.selectbox(
    'Which chemical would you like to show raman spectra ?',
    df_aws[0].unique())
concentration= st.selectbox(
    'What concentration would you like to plot ?',
    df_aws[1].unique())

df_sub=df_aws[(df_aws[0] == compound) & (df_aws[1] == concentration)]

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df_sub[2], df_sub[3], label='Mixture', linewidth=2)
ax.set_xlabel("Raman shift (cm⁻¹)")
ax.set_ylabel("Intensity (a.u.)")
        
st.pyplot(fig)


