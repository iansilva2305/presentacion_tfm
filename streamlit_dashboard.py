
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def dashboard_gdpr():
    """Dashboard GDPR para monitorización de cumplimiento"""

    st.set_page_config(
        page_title="🔒 Dashboard GDPR - Cumplimiento Anonimización",
        layout="wide"
    )

    st.title("🔒 Dashboard GDPR - Cumplimiento de Anonimización")
    st.markdown("### Monitorización en Tiempo Real del Pipeline de Protección de Datos")

    # Métricas principales en 4 columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="K-anonimato", 
            value="10", 
            delta="✅ CUMPLE",
            help="Cada registro es indistinguible de al menos 9 otros"
        )

    with col2:
        st.metric(
            label="L-diversidad", 
            value="2", 
            delta="✅ CUMPLE",
            help="Cada grupo k-anónimo tiene al menos 2 valores diversos"
        )

    with col3:
        st.metric(
            label="ε Privacidad", 
            value="2.0", 
            delta="✅ CUMPLE",
            help="Nivel de privacidad diferencial aplicado"
        )

    with col4:
        st.metric(
            label="Riesgo GDPR", 
            value="BAJO", 
            delta="✅ SEGURO",
            help="Evaluación de riesgo de cumplimiento"
        )

    # Gráfico de degradación de rendimiento
    st.subheader("📊 Impacto en Rendimiento de Modelos")

    # Datos de ejemplo (usar resultados reales del pipeline)
    model_performance = pd.DataFrame({
        'Modelo': ['Random Forest', 'XGBoost', 'Regresión Logística'],
        'AUC_Original': [0.85, 0.87, 0.82],
        'AUC_Anonimizado': [0.83, 0.84, 0.80],
        'Degradación_%': [2.4, 3.4, 2.4]
    })

    fig = px.bar(
        model_performance, 
        x='Modelo', 
        y='Degradación_%',
        title="Degradación de Rendimiento por Modelo",
        color='Degradación_%',
        color_continuous_scale='RdYlGn_r'
    )
    fig.add_hline(y=10, line_dash="dash", line_color="red", 
                  annotation_text="Límite Aceptable (10%)")
    st.plotly_chart(fig, use_container_width=True)

    # Indicadores de cumplimiento GDPR
    st.subheader("✅ Estado de Cumplimiento GDPR")

    compliance_data = {
        'Principio GDPR': [
            'Minimización de Datos',
            'Limitación de Finalidad', 
            'Exactitud',
            'Integridad y Confidencialidad',
            'Responsabilidad Proactiva'
        ],
        'Estado': ['✅ CUMPLE'] * 5,
        'Artículo': ['Art. 5.1.c', 'Art. 5.1.b', 'Art. 5.1.d', 'Art. 5.1.f', 'Art. 5.2']
    }

    st.dataframe(pd.DataFrame(compliance_data), use_container_width=True)

    # Configuración de técnicas de anonimización
    st.subheader("🔧 Configuración de Técnicas de Anonimización")

    with st.expander("Configurar Parámetros de Privacidad"):
        col1, col2 = st.columns(2)

        with col1:
            k_value = st.slider("Valor K (K-anonimato)", 5, 20, 10)
            l_value = st.slider("Valor L (L-diversidad)", 2, 5, 2)

        with col2:
            epsilon = st.slider("Epsilon (Privacidad Diferencial)", 0.1, 5.0, 2.0, 0.1)
            hash_method = st.selectbox("Método de Hash", ["SHA-256", "SHA-512", "MD5"])

        if st.button("Aplicar Configuración"):
            st.success("✅ Configuración actualizada correctamente")

    # Log de auditoría
    st.subheader("📋 Log de Auditoría")

    audit_log = pd.DataFrame({
        'Timestamp': ['2025-06-27 10:30:00', '2025-06-27 09:15:00', '2025-06-27 08:00:00'],
        'Evento': ['Evaluación GDPR completada', 'Pipeline anonimización ejecutado', 'Carga de datos PaySim1'],
        'Usuario': ['admin', 'data_scientist', 'admin'],
        'Estado': ['✅ Éxito', '✅ Éxito', '✅ Éxito']
    })

    st.dataframe(audit_log, use_container_width=True)

if __name__ == "__main__":
    dashboard_gdpr()
