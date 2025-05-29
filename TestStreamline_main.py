import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del dashboard
st.title("Dashboard de Ventas - Vendedores")

# Carga del archivo
uploaded_file = st.file_uploader("Sube el archivo sellers.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("1. Vista previa de los datos")
    st.write(df.head())

    st.subheader("2. Resumen estadístico")
    st.write(df.describe())

    # ----------------------------
    # Filtro general (SIN CAMBIOS)
    # ----------------------------
    st.subheader("3. Filtrar datos (por cualquier columna)")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Selecciona una columna para filtrar", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Selecciona un valor", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    # ----------------------------
    # Punto 3: Selección de métrica para graficar por vendedor
    # ----------------------------
    st.subheader("3. Gráfico por Vendedor y Métrica")

    if 'NOMBRE' in df.columns and 'APELLIDO' in df.columns and 'UNIDADES VENDIDAS' in df.columns and 'VENTAS TOTALES' in df.columns:
        df['VENDEDOR'] = df['NOMBRE'] + ' ' + df['APELLIDO']
        grouped = df.groupby("VENDEDOR")[["UNIDADES VENDIDAS", "VENTAS TOTALES"]].sum()
        grouped["VENTA PROMEDIO"] = grouped["VENTAS TOTALES"] / grouped["UNIDADES VENDIDAS"]

        metric_options = {
            "Unidades Vendidas": "UNIDADES VENDIDAS",
            "Ventas Totales": "VENTAS TOTALES",
            "Venta Promedio": "VENTA PROMEDIO"
        }

        selected_metric = st.radio("Selecciona la métrica a graficar:", list(metric_options.keys()))

        st.write(f"📊 Gráfico de {selected_metric} por Vendedor")
        st.bar_chart(grouped[[metric_options[selected_metric]]])
    else:
        st.warning("Faltan columnas necesarias para graficar métricas por vendedor.")

    # ----------------------------
    # Detalles por vendedor específico
    # ----------------------------
    st.subheader("5. Datos específicos de un vendedor")

    if 'NOMBRE' in df.columns:
        df['VENDEDOR'] = df['NOMBRE'] + ' ' + df['APELLIDO']
        vendedores = df['VENDEDOR'].unique()
        selected_vendedor = st.selectbox("Selecciona un vendedor", vendedores)
        vendedor_data = df[df['VENDEDOR'] == selected_vendedor]
        st.write(vendedor_data)
    else:
        st.warning("Columnas 'NOMBRE' o 'APELLIDO' no encontradas.")

else:
    st.info("Por favor, sube el archivo sellers.csv para comenzar.")
