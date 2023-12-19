# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 16:06:32 2023

Luis Ramon Garcia Vazquez

Mineria de Datos
"""
# Analysis per country. Do the following and explain the corresponding subpoints.
"""
 a. Find the 10 countries with more answers and draw a bar plot of the frequencies of answers for those 
 countries, i.e., how many persons are per country. If México is not in the top 10, include its frequency 
 in the bar plot.
 b. •Select only the 3 countries with more answersand add México if it is not there.
    •Compute the five-number   summary(minimum,   maximum   1st quartile, 3rd quartile, median), the mean, 
     and the standard deviation for  the  annual  salary  for each  of  the  top 3countries  and  México
     (4 countries  in  total) and  draw  the  corresponding  boxplotsand  the histograms (with 10 bins).
"""

import matplotlib.pyplot as plt
import pandas as pd

w_d = 'C:/Users/luisr/OneDrive - Universidad de Guanajuato/Documentos/DM/Code/Assigment_2/'
f_i = w_d + 'survey_results.csv'

df = pd.read_csv(f_i)

# Fucniones 
def chi_squared (c_t):
    e_v = {}
    t_o = sum([v2 for k1, v1 in c_t.items() for k2, v2 in v1.items()])
    chi_2 = 0
    for c in c_t:
        t_c = sum([v2 for k2, v2 in c_t[c].items()])
        if c not in e_v:
            e_v[c] = {}
        for r in c_t[c]:
            t_r = sum([v2 for k1, v1 in c_t.items()
                           for k2, v2 in v1.items() if k2 == r])
            ev = (t_c * t_r) / t_o
            ov = c_t[c][r]
            e_v[c][r] = ev    
            
            chi_cr = ((ov - ev)**2) / ev
            
            chi_2 += chi_cr
    
    return chi_2

# Obtener las 10 paises con mas participacion
top_countries = df['Country'].value_counts().head(10)

# Inclusión de Mexico.
if 'Mexico' not in top_countries.index:
    mexico_frequency = df['Country'].value_counts().get('Mexico', 0)
    top_countries = top_countries.append(pd.Series([mexico_frequency], index=['Mexico']))

top_countries = top_countries.sort_values(ascending=True)

# Grafico de barras
plt.barh(top_countries.index, top_countries.values, color='skyblue')
plt.xlabel('Número de respuestas')
plt.title('Top 10 Paises con más respuestas en la encuesta Stack Overflow')

plt.show()

# Obtener los 3 paises con mas respuestas
top_countries = df['Country'].value_counts().head(3)

# Incluir a Mexico
if 'Mexico' not in top_countries.index:
    mexico_frequency = df['Country'].value_counts().get('Mexico', 0)
    top_countries = top_countries.append(pd.Series([mexico_frequency], index=['Mexico']))

# Filtrar los datos solo para los tres primeros paises y Mexico
selected_countries = df[df['Country'].isin(top_countries.index)]

# Datos estadisticos
summary_stats = selected_countries.groupby('Country')['ConvertedCompYearly'].describe()

for country, stats in summary_stats.iterrows():
    print(f"\nEstadísticas para {country}:")
    print(f"Cuartiles: Q1={stats['25%']}, Q3={stats['75%']}")
    print(f"Mediana: {stats['50%']}")
    print(f"Media: {stats['mean']:.3f}")
    print(f"Desviación Estándar: {stats['std']:.3f}")
    print(f"Número de personas por cada genero:")
    print(selected_countries[selected_countries['Country'] == country]['Gender'].value_counts())

    # Diagrama de caja
    plt.figure(figsize=(8, 6))
    selected_countries[selected_countries['Country'] == country]['ConvertedCompYearly'].plot(kind='box')
    plt.title(f'Diagrama de Caja para {country}')
    plt.show()

    # Histograma
    plt.figure(figsize=(8, 6))
    selected_countries[selected_countries['Country'] == country]['ConvertedCompYearly'].plot(kind='hist', bins=10, edgecolor='black')
    plt.title(f'Histograma para {country}')
    plt.xlabel('Salario Anual (USD)')
    plt.ylabel('Frecuencia')
    plt.show()


"""
 d. Considering three types of annual salary: low(<=10000), medium(>10000, <=50000) and high(>50000), 
 transform the annual salary of each userto these categories.Only for the 4 selected countries.
"""
# Obtener los 3 paises con más respuestas y Mexico
top_countries = df['Country'].value_counts().head(3)

# Si Mexico no esta entre los 3 primeros, incluirlo
if 'Mexico' not in top_countries.index:
    mexico_frequency = df['Country'].value_counts().get('Mexico', 0)
    top_countries = top_countries.append(pd.Series([mexico_frequency], index=['Mexico']))

# Filtrar el conjunto de datos para incluir solo los 4 paises seleccionados
selected_countries = df[df['Country'].isin(top_countries.index)]

# Funcion para categorizar el salario
def categorize_salary(salary):
    if salary <= 10000:
        return 'Bajo'
    elif 10000 < salary <= 50000:
        return 'Medio'
    else:
        return 'Alto'

# Aplicar la categorizacion al conjunto de datos
selected_countries['SalaryCategory'] = selected_countries['ConvertedCompYearly'].apply(categorize_salary)

# Datos estadisticos basado en su salario
summary_stats = selected_countries.groupby(['Country', 'SalaryCategory'])['ConvertedCompYearly'].describe()

# Diagramas de caja y histogramas
for country in top_countries.index:
    for category in ['Bajo', 'Medio', 'Alto']:
        # Diagrama de caja
        plt.figure(figsize=(8, 6))
        subset = selected_countries[(selected_countries['Country'] == country) & (selected_countries['SalaryCategory'] == category)]
        subset['ConvertedCompYearly'].plot(kind='box')
        plt.title(f'Diagrama de Caja para {country} - {category}')
        plt.show()

        # Histograma
        plt.figure(figsize=(8, 6))
        subset['ConvertedCompYearly'].plot(kind='hist', bins=10, edgecolor='black')
        plt.title(f'Histograma para {country} - {category}')
        plt.xlabel('Salario Anual (USD)')
        plt.ylabel('Frecuencia')
        plt.show()

# Tabla de porbabilidad salarial en cada pais
print("Probabilidad salarial en cada pais:")
print(summary_stats)
"""
 e. Using the transformed salary from the previous subpointdofor the 4 selected countries:
   •Draw a bar plot of frequencies of persons in each salary category per country.
   •Computethe conditional probability to determine which countryhas a higher probability 
   of having a high salary(>50000), and which has a higher probability of a low salary(<=10000).
   •Compute the Pearson’s chi square to determineifthere is a relation betweenthecountryand the 
   annual salary.
"""

# Obtener los 3 paises con más respuestas y Mexico
top_countries = df['Country'].value_counts().head(3)

# Incluir a Mexico
if 'Mexico' not in top_countries.index:
    mexico_frequency = df['Country'].value_counts().get('Mexico', 0)
    top_countries = top_countries.append(pd.Series([mexico_frequency], index=['Mexico']))

# Aplicar la categorizacion al conjunto de datos
selected_countries = df[df['Country'].isin(top_countries.index)]

# Funcion para categorizar el salario
def categorize_salary(salary):
    if salary <= 10000:
        return 'Bajo'
    elif 10000 < salary <= 50000:
        return 'Medio'
    else:
        return 'Alto'

# Aplicar la categorizacion al conjunto de datos
selected_countries['SalaryCategory'] = selected_countries['ConvertedCompYearly'].apply(categorize_salary)

# Diagrama de barras por pais y categoria salarial
for country in top_countries.index:
    plt.figure(figsize=(8, 6))
    subset = selected_countries[selected_countries['Country'] == country]
    subset['SalaryCategory'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title(f'Diagrama de Barras de {country}')
    plt.xlabel('Categoria Salarial')
    plt.ylabel('Numero de Personas')
    plt.show()
    
# Porbabilidad salarial alta y baja por pais
for country in top_countries.index:
    total_people = len(selected_countries[selected_countries['Country'] == country])
    
    prob_high_salary = len(selected_countries[(selected_countries['Country'] == country) & (selected_countries['SalaryCategory'] == 'Alto')]) / total_people
    prob_low_salary = len(selected_countries[(selected_countries['Country'] == country) & (selected_countries['SalaryCategory'] == 'Bajo')]) / total_people
    
    print(f"Probabilidad condicional en {country}:")
    print(f"  Probabilidad de salario alto (>50000): {prob_high_salary:.2%}")
    print(f"  Probabilidad de salario bajo (<=10000): {prob_low_salary:.2%}")
    print()


# Categorizacion al conjunto de datos
selected_countries['SalaryCategory'] = selected_countries['ConvertedCompYearly'].apply(categorize_salary)

# Tabla de contingencia para cada pais y categoria salarial
contingency_table = pd.crosstab(selected_countries['Country'], selected_countries['SalaryCategory'])

# Valor de chi.
chi_square = chi_squared(contingency_table.to_dict())

print(f"Valor de chi: {chi_square:.3f}")

