# -*- coding: utf-8 -*-
"""
Created on wed Nov 11 12:27:11 2023

Luis Ramon Garcia Vazquez

Mineria de Datos
"""
# Analysis per genderper country. Considering the data for only the 4 selectedcountries of the 
# previous points, do the following and explain the corresponding subpoints.

""" 
    a. Draw a bar plot of the frequencies of answers per gender per country, i.e.,how many persons 
    are per gender in each of the 4 selected countries. The data considers three genders; you must
    compute  the frequencies for each one. 
"""
import matplotlib.pyplot as plt
import pandas as pd

w_d = 'C:/Users/luisr/OneDrive - Universidad de Guanajuato/Documentos/DM/Code/Assigment_2/'
f_i = w_d + 'survey_results.csv'

df = pd.read_csv(f_i)

# Se recuperan los 4 paises
top_countries = df['Country'].value_counts().head(3).index
selected_countries = list(top_countries) + ['Mexico']

# Filtrar solo para los 4 paises
selected_data = df[df['Country'].isin(selected_countries)]

# Diagrama de barras
plt.figure(figsize=(12, 8))

for i, country in enumerate(selected_countries, start=1):
    country_data = selected_data[selected_data['Country'] == country]
    gender_counts = country_data['Gender'].value_counts()

    # Crear un color para cada genero
    colors = ['blue', 'purple', 'green']
    plt.bar(i - 0.2, gender_counts.get('Man', 0), color=colors[0], width=0.2, label='Hombre')
    plt.bar(i, gender_counts.get('Woman', 0), color=colors[1], width=0.2, label='Mujer')
    plt.bar(i + 0.2, gender_counts.get('Other', 0), color=colors[2], width=0.2, label='Otro')

    # Mostrar cantidad/numero en cada genero
    for j, count in enumerate(gender_counts):
        plt.text(i + (j - 1) * 0.2, count + 50, str(count), color='black', ha='center')

plt.xticks(range(1, len(selected_countries) + 1), selected_countries)
plt.xlabel('País')
plt.ylabel('Número de respuestas')
plt.title('Distribución de géneros por país')
plt.legend()
plt.show()

"""
    b. Compute the five-number summary (minimum, maximum 1st quartile, 3rd quartile, median), the 
    mean, and the standard deviation for the annual salary per gender per country and draw the 
    corresponding boxplots and the histograms (using 10 bins).
"""


# Calcular el resumen estadístico para el salario anual por genero por pais
summary_stats = selected_data.groupby(['Country', 'Gender'])['ConvertedCompYearly'].describe()

selected_data = df[df['Country'].isin(selected_countries)]

# Diagrama de caja e histogramas
for (country, gender), stats in summary_stats.iterrows():
    
    print(f"\nEstadisticas para {country} - {gender}:")
    print(f"Cuartiles: Q1={stats['25%']}, Q3={stats['75%']}")
    print(f"Mediana: {stats['50%']}")
    print(f"Media: {stats['mean']:.3f}")
    print(f"Desviacion Estandar: {stats['std']:.3f}")
    print(f"Numero de personas: {stats['count']}")
    
    # Diagrama de caja
    plt.figure(figsize=(8, 6))
    selected_data[(selected_data['Country'] == country) & (selected_data['Gender'] == gender)]['ConvertedCompYearly'].plot(kind='box')
    plt.title(f'Diagrama de Caja para {country} - {gender}')
    plt.show()

    # Histograma
    plt.figure(figsize=(8, 6))
    selected_data[(selected_data['Country'] == country) & (selected_data['Gender'] == gender)]['ConvertedCompYearly'].plot(kind='hist', bins=10, edgecolor='black')
    plt.title(f'Histograma para {country} - {gender}')
    plt.xlabel('Salario Anual (USD)')
    plt.ylabel('Frecuencia')
    plt.show()

# Mostrar el resumen estadistico
print("Resumen estadistico para el salario anual por género por pais:")
print(summary_stats)

"""
    d. Considerando tres tipos de salario anual: bajo (<=10000), medio (>10000, <=50000) y alto (>50000),
    transforme el salario anual de cada usuario a estas categorías. Solo en los 4 países seleccionados.
    e. Usando el salario transformado del subpuntodo anterior para cada uno de los 4 países: 
        • Dibuje un diagrama de barras de frecuencias de personas en cada categoría salarial por género en 
        cada país.
        • Calcule la probabilidad condicional para determinar qué género tiene una mayor probabilidad de 
        tener un salario alto (>50000 )en cada país, y qué género tiene mayor probabilidad de tener un 
        salario bajo (<=10000) en cada país. 
        •Calcule el chi cuadrado de Pearson para determinar si existe una relación entre el género y el 
        salario anual en cada país.
"""

# Obtener los 3 paises con mas respuestas y Mexico
top_countries = df['Country'].value_counts().head(3).index
selected_countries = list(top_countries) + ['Mexico']

# Filtrar el conjunto de datos para incluir solo los 4 paises seleccionados
selected_data = df[df['Country'].isin(selected_countries)]

# Definir los umbrales para las categorias de salario anual
umbrales = [0, 10000, 50000, float('inf')]
categorias = ['Bajo', 'Medio', 'Alto']

# Crear una nueva columna que represente la categoria de salario para cada usuario
selected_data['SalaryCategory'] = pd.cut(selected_data['ConvertedCompYearly'], bins=umbrales, labels=categorias, right=False)

# Diagrama de barras de frecuencias de personas en cada categoría salarial por genero en cada pais
for (country, gender), subset in selected_data.groupby(['Country', 'Gender']):
    plt.figure(figsize=(8, 6))
    subset['SalaryCategory'].value_counts().sort_index().plot(kind='bar', color=['skyblue', 'lightgreen', 'coral'])
    plt.title(f'Diagrama de Barras para {country} - {gender}')
    plt.xlabel('Categoría Salarial')
    plt.ylabel('Frecuencia')
    plt.show()

# Probabilidad condicional para cada pais y genero
for (country, gender), subset in selected_data.groupby(['Country', 'Gender']):
    total = len(subset)
    prob_alto = len(subset[subset['SalaryCategory'] == 'Alto']) / total
    prob_medio = len(subset[subset['SalaryCategory'] == 'Medio']) / total
    prob_bajo = len(subset[subset['SalaryCategory'] == 'Bajo']) / total
    print(f"Probabilidad de salario Alto en {country} - {gender}: {(prob_alto)*100:.3f}")
    print(f"Probabilidad de salario Medio en {country} - {gender}: {(prob_medio)*100:.3f}")
    print(f"Probabilidad de salario Bajo en {country} - {gender}: {(prob_bajo)*100:.3f}")

# Chi cuadrado para cada pais
for (country, gender), subset in selected_data.groupby(['Country', 'Gender']):
    contingency_table = pd.crosstab(subset['SalaryCategory'], subset['Gender'])
    chi_squared = contingency_table.apply(lambda x: x / x.sum(), axis=1).apply(lambda x: (x - x.sum())**2 / x.sum()).sum().sum()
    print(f"Chi cuadrado de Pearson para {country} - {gender}: {chi_squared:.3f}")

