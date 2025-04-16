import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter1d
import streamlit as st
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine


st.set_page_config(layout="wide")

def lorentzian(x, x0, gamma): #Lorentzian model used to simulate raman spectra
    return 1 /(1 + ((x - x0) / gamma) ** 2)

def resolution_nm_cm(res_nm,exc_wavelength):
    
    #res_cm=(10000000*res_nm)/exc_wavelength**2
    res_cm=10000000*abs(-1/(exc_wavelength+res_nm)+(1/exc_wavelength))

    return(res_cm)

def return_raman_spectra_broadened(peak_shifts, noise_intensity=0.05,fluorescence_intensity=5,res_nm=0.5,exc_wavelength=785):
        
        sigma=resolution_nm_cm(res_nm,exc_wavelength)/2.355
        
        x = np.linspace(0, 2000, 2000) #Raman shift range
        y = np.zeros_like(x)  # Baseline

        # Simulate fluorescence background
        
        fluorescence = fluorescence_intensity * np.exp(-x / max(x) * 5)  # Exponential decay background due to fluorescence


        # Generate random noise to reproduce sensor thermal noise 
        
        noise = noise_intensity * np.random.normal(size=len(x))

        # Add Raman peaks (using lorentzian function from previous function
        
        for shift in zip(peak_shifts):
            y += 2* lorentzian(x, shift, gamma=5)
        
        broadened_spectrum = gaussian_filter1d(y, sigma)
        
        
        return(broadened_spectrum)
    
col1, col2 = st.columns([1, 3])

peak_shifts_dict = {'Lactate':[543,853,876,989,1040,1053,1081,1459],'Glucose':[437, 518, 1060, 1125, 1365, 1461],'Urea':[1005,1170,1461,1532],'Glutamate':[606,768,871,938,1004,1073,1140,1346,1416,1612],'Glutamine':[622,652,776,848,895,1097,1330,1417],'Sodium Acetate':[82,166,667,927,1416,1464]}

excitation=520

with col1:
    st.subheader("Excitation wavelength")
    if st.checkbox('520 nm'):
        excitation=520

    if st.checkbox('785 nm'):
        excitation=785
        
with col2:
    st.subheader("Single chemical")
    chemical = st.selectbox(
        'Which chemical would you like to show raman spectra ?',
         peak_shifts_dict.keys())
    
    resolution_nm = st.slider('Detector resolution (nm)', min_value=0.1, max_value=5.0, value=1.0, step=0.05)
    
    shifts=peak_shifts_dict[chemical]
    raman_spectra=return_raman_spectra_broadened(shifts, noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
    
    st.line_chart(raman_spectra)
    st.subheader("Mix of chemicals")
    x = np.linspace(0, 2000, 2000)
    y=np.zeros(2000)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.checkbox('Lactate'):
            lactate_spectrum = return_raman_spectra_broadened(peak_shifts_dict['Lactate'], noise_intensity=0.05,
                                                      fluorescence_intensity=5, res_nm=resolution_nm,
                                                      exc_wavelength=excitation)
            y+=return_raman_spectra_broadened(peak_shifts_dict['Lactate'], noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
            ax.plot(x, lactate_spectrum, linestyle='--', marker='.', markersize=3, linewidth=4, label='Lactate only')
        
        if st.checkbox('Glucose'):
            glucose_spectrum = return_raman_spectra_broadened(peak_shifts_dict['Glucose'], noise_intensity=0.05,
                                                      fluorescence_intensity=5, res_nm=resolution_nm,
                                                      exc_wavelength=excitation)
            y+=return_raman_spectra_broadened(peak_shifts_dict['Glucose'], noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
            ax.plot(x, glucose_spectrum, linestyle='--', marker='.', markersize=3, linewidth=4, label='Glucose only')
    with col2:
        if st.checkbox('Urea'):
            urea_spectrum = return_raman_spectra_broadened(peak_shifts_dict['Urea'], noise_intensity=0.05,
                                                      fluorescence_intensity=5, res_nm=resolution_nm,
                                                      exc_wavelength=excitation)
            y+=return_raman_spectra_broadened(peak_shifts_dict['Urea'], noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
            ax.plot(x, urea_spectrum, linestyle='--', marker='.', markersize=3, linewidth=4, label='Urea only')
        
        if st.checkbox('Glutamate'):
            glutamate_spectrum = return_raman_spectra_broadened(peak_shifts_dict['Glutamate'], noise_intensity=0.05,
                                                      fluorescence_intensity=5, res_nm=resolution_nm,
                                                      exc_wavelength=excitation)
            y+=return_raman_spectra_broadened(peak_shifts_dict['Glutamate'], noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
            ax.plot(x, glutamate_spectrum, linestyle='--', marker='.', markersize=3, linewidth=4, label='Glutamate only')
    with col3:    
        if st.checkbox('Glutamine'):
            glutamine_spectrum = return_raman_spectra_broadened(peak_shifts_dict['Glutamine'], noise_intensity=0.05,
                                                      fluorescence_intensity=5, res_nm=resolution_nm,
                                                      exc_wavelength=excitation)
            y+=return_raman_spectra_broadened(peak_shifts_dict['Glutamine'], noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
            ax.plot(x, glutamine_spectrum, linestyle='--', marker='.', markersize=3, linewidth=4, label='Glutamine only')
        
        if st.checkbox('Sodium Acetate'):
            acetate_spectrum = return_raman_spectra_broadened(peak_shifts_dict['Sodium Acetate'], noise_intensity=0.05,
                                                      fluorescence_intensity=5, res_nm=resolution_nm,
                                                      exc_wavelength=excitation)
            y+=return_raman_spectra_broadened(peak_shifts_dict['Sodium Acetate'], noise_intensity=0.05,fluorescence_intensity=5,res_nm=resolution_nm,exc_wavelength=excitation)
            ax.plot(x, acetate_spectrum, linestyle='--', marker='.', markersize=3, linewidth=4, label='Sodium Acetate')
        
    ax.plot(x, y, label='Mixture', linewidth=2)
    ax.set_xlabel("Raman shift (cm⁻¹)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.legend()
    
    st.pyplot(fig)

