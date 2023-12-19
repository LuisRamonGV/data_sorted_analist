# -*- coding: utf-8 -*-
"""
Created on wed Nov 16 17:48:32 2023

Luis Ramon Garcia Vazquez

Mineria de Datos
"""
# Considering the df for only the 4 selectedcountries of the previous points, do the 
# following and explain the corresponding subpoints.
""" a. Compute the Pearson’scorrelation between YearsCodeProand the annual salary, per 
    country.
"""
import pandas as pd

w_d = 'C:/Users/luisr/OneDrive - Universidad de Guanajuato/Documentos/DM/Code/Assigment_2/'
f_i = w_d + 'survey_results.csv'

df = pd.read_csv(f_i)

# Obtener los 3 paises con mas respuestas y Mexico
top_countries = df['Country'].value_counts().head(3).index
selected_countries = list(top_countries) + ['Mexico']

# Filtrar el conjunto de datos para incluir solo los 4 paises seleccionados
selected_df = df[df['Country'].isin(selected_countries)]

# Calcular el salario anual promedio por pais con dos decimales
average_salary_by_country = selected_df.groupby('Country')['ConvertedCompYearly'].mean().round(2)

# Mostrar el salario anual promedio por pais
print("Salario anual promedio por país:")
print(average_salary_by_country)

# Calcular la correlación de Pearson por pais
for country, subset in selected_df.groupby('Country'):
    correlation = subset['YearsCodePro'].corr(subset['ConvertedCompYearly'])
    print(f"Correlación de Pearson para {country}: {correlation:.3f}")
