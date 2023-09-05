import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo CSV
@st.cache_data
def load_data():
    data = pd.read_csv("EMA_2021_2022.csv", sep=";")
    return data

data = load_data()

# Configuración de la aplicación
st.title("Análisis de Datos - EMA 2021-2022")
st.sidebar.title("Filtros")

years = data["anio_insc"].unique()
months = data["mes_insc"].unique()
nac_1 = data["nac_1"].unique()
nac_2 = data["nac_2"].unique()
sexo_1 = data["sexo_1"].unique()
sexo_2 = data["sexo_2"].unique()

# Filtrar datos por la columna "prov_insc"
selected_anio_insc = st.sidebar.selectbox("Año", ["Todos"] + list(years))
selected_mes_insc = st.sidebar.selectbox("Mes", ["Todos"] + list(months))
selected_nac_1 = st.sidebar.selectbox("Nacioalidad Contrayente 1", ["Todos"] + list(nac_1))
selected_nac_2 = st.sidebar.selectbox("Nacioalidad Contrayente 2", ["Todos"] + list(nac_2))

filtered_data = data.copy()

if selected_anio_insc != "Todos":
    filtered_data = filtered_data[filtered_data["anio_insc"] == selected_anio_insc]

if selected_mes_insc != "Todos":
    filtered_data = filtered_data[filtered_data["mes_insc"] == selected_mes_insc]

if selected_nac_1 != "Todos":
    filtered_data = filtered_data[filtered_data["nac_1"] == selected_nac_1]

if selected_nac_2 != "Todos":
    filtered_data = filtered_data[filtered_data["nac_2"] == selected_nac_2]

st.write(filtered_data)

# Gráfico de Barras para Estado Civil:
st.subheader("Estado Civil de Contrayentes")
state_counts_1 = filtered_data["est_civi1"].value_counts()
state_counts_2 = filtered_data["est_civi2"].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(state_counts_1.index, state_counts_1.values, label="Contrayente 1")
ax.bar(state_counts_2.index, state_counts_2.values, label="Contrayente 2", alpha=0.5)
ax.set_xlabel("Estado Civil")
ax.set_ylabel("Cantidad")
ax.legend()
st.pyplot(fig)

# Gráfico de Barras para Nivel de Instrucción:
st.subheader("Nivel de Instrucción de Contrayentes")
edu_counts_1 = filtered_data["niv_inst1"].value_counts()
edu_counts_2 = filtered_data["niv_inst2"].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(edu_counts_1.index, edu_counts_1.values, label="Contrayente 1")
ax.barh(edu_counts_2.index, edu_counts_2.values, label="Contrayente 2", alpha=0.5)
ax.set_xlabel("Cantidad")
ax.set_ylabel("Nivel de Instrucción")
ax.legend()
st.pyplot(fig)

# Determinar las provincias más pobladas del país (por ejemplo, las 5 más pobladas)
provincias_mas_pobladas = filtered_data["prov_insc"].value_counts().nlargest(5).index.tolist()
data_pobladas = filtered_data[filtered_data["prov_insc"].isin(provincias_mas_pobladas)]
marriages_by_province = data_pobladas["prov_insc"].value_counts()

# Crear el gráfico de pastel
st.subheader("Matrimonios por Provincia Más Pobladas")
fig, ax = plt.subplots()
ax.pie(marriages_by_province, labels=marriages_by_province.index, autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Asegura que el gráfico de pastel sea circular
st.pyplot(fig)

# Filtrar datos para incluir solo las personas divorciadas o solteras
data_divorciados_solteros = filtered_data[filtered_data["est_civi1"].isin(["Divorciado", "Soltero"])]
divorciados_solteros_por_provincia = data_divorciados_solteros.groupby(["prov_insc", "est_civi1"])["prov_insc"].count().unstack().fillna(0)

# Crear el gráfico de pastel para Guayas
st.subheader("Estado Civil de Contrayentes Divorciados y Solteros en Guayas")
divorciados_solteros_guayas = data_divorciados_solteros[data_divorciados_solteros["prov_insc"] == "Guayas"]
divorciados_solteros_guayas_counts = divorciados_solteros_guayas["est_civi1"].value_counts()
fig_guayas, ax_guayas = plt.subplots()
ax_guayas.pie(divorciados_solteros_guayas_counts, labels=divorciados_solteros_guayas_counts.index, autopct='%1.1f%%', startangle=90)
ax_guayas.axis('equal')
st.pyplot(fig_guayas)

# Crear el gráfico de pastel para Pichincha
st.subheader("Estado Civil de Contrayentes Divorciados y Solteros en Pichincha")
divorciados_solteros_pichincha = data_divorciados_solteros[data_divorciados_solteros["prov_insc"] == "Pichincha"]
divorciados_solteros_pichincha_counts = divorciados_solteros_pichincha["est_civi1"].value_counts()
fig_pichincha, ax_pichincha = plt.subplots()
ax_pichincha.pie(divorciados_solteros_pichincha_counts, labels=divorciados_solteros_pichincha_counts.index, autopct='%1.1f%%', startangle=90)
ax_pichincha.axis('equal')
st.pyplot(fig_pichincha)

# Fin de la aplicación