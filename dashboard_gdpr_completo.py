
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(
    page_title="🔒 Dashboard GDPR - Cumplimiento Anonimización",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el aspecto visual
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .compliance-high {
        border-left-color: #2ecc71 !important;
    }
    .compliance-medium {
        border-left-color: #f39c12 !important;
    }
    .compliance-low {
        border-left-color: #e74c3c !important;
    }
    .stMetric > div > div > div > div {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal del dashboard"""

    # HEADER PRINCIPAL
    st.title("🔒 Dashboard de Cumplimiento GDPR")
    st.markdown("### Anonimización de Datos Personales y Cumplimiento del GDPR en Modelos LLM")
    st.markdown("---")

    # SIDEBAR - PANEL DE CONFIGURACIÓN LATERAL
    st.sidebar.header("🔧 Panel de Configuración")
    st.sidebar.markdown("Ajustar parámetros de anonimización dinámicamente")

    # Controles interactivos
    k_value = st.sidebar.slider(
        "K-anonimato", 
        min_value=5, max_value=50, value=10, step=5,
        help="Cada registro debe ser indistinguible de al menos k-1 otros"
    )

    l_value = st.sidebar.slider(
        "L-diversidad", 
        min_value=2, max_value=10, value=2, step=1,
        help="Cada grupo k-anónimo debe tener al menos l valores diversos"
    )

    epsilon = st.sidebar.slider(
        "Epsilon (ε) - Privacidad Diferencial", 
        min_value=0.1, max_value=10.0, value=2.0, step=0.1,
        help="Menor ε = mayor privacidad, mayor degradación de utilidad"
    )

    # Información técnica en sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Información Técnica")
    st.sidebar.info("""
    **Modelo Seleccionado**: Random Forest (100 estimadores)

    **Dataset**: PaySim1 (6.3M transacciones)

    **Técnicas Aplicadas**:
    - Seudonimización SHA-256
    - K-anonimato
    - L-diversidad  
    - Privacidad Diferencial
    """)

    # SECCIÓN 1: INDICADORES DE CUMPLIMIENTO CENTRALES
    st.header("🔍 Panel de Control GDPR")

    # Calcular métricas dinámicas basadas en sliders
    def calculate_risk_level(k, l, eps):
        risk_score = (k/10 * 0.4) + (l/2 * 0.3) + ((10-eps)/10 * 0.3)
        if risk_score >= 0.8:
            return "BAJO", "🟢"
        elif risk_score >= 0.6:
            return "MEDIO", "🟡"
        else:
            return "ALTO", "🔴"

    risk_level, risk_emoji = calculate_risk_level(k_value, l_value, epsilon)

    # Métricas principales en 4 columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="K-anonimato",
            value=str(k_value),
            delta="✅ CUMPLE" if k_value >= 10 else "⚠️ REVISA",
            help="Indistinguibilidad garantizada"
        )

    with col2:
        st.metric(
            label="L-diversidad",
            value=str(l_value),
            delta="✅ CUMPLE" if l_value >= 2 else "⚠️ REVISA",
            help="Diversidad en atributos sensibles"
        )

    with col3:
        st.metric(
            label="ε Privacidad",
            value=f"{epsilon:.1f}",
            delta="✅ CUMPLE" if epsilon <= 3.0 else "⚠️ ALTO",
            help="Nivel de privacidad diferencial"
        )

    with col4:
        st.metric(
            label="Riesgo Global",
            value=risk_level,
            delta=f"{risk_emoji} EVALUADO",
            help="Evaluación integral de riesgo GDPR"
        )

    st.markdown("---")

    # SECCIÓN 2: EVALUACIÓN COMPARATIVA DE IMPACTO
    st.header("📊 Evaluación Comparativa de Impacto")

    # Simular impacto dinámico basado en parámetros
    def simulate_impact(k, l, eps, base_metrics):
        # Factor de degradación basado en parámetros
        k_factor = max(0, (k - 10) / 40)  # Más k = más degradación
        l_factor = max(0, (l - 2) / 8)    # Más l = más degradación  
        eps_factor = max(0, (3 - eps) / 3) # Menos ε = más degradación

        total_degradation = (k_factor + l_factor + eps_factor) / 3 * 0.15  # Max 15% degradación

        return {
            'Precisión': base_metrics['precision'] * (1 - total_degradation),
            'Sensibilidad': base_metrics['sensitivity'] * (1 - total_degradation),
            'AUC-ROC': base_metrics['auc'] * (1 - total_degradation),
            'Degradación_%': total_degradation * 100
        }

    base_metrics = {
        'precision': 95.7,
        'sensitivity': 91.4,
        'auc': 87.1
    }

    current_impact = simulate_impact(k_value, l_value, epsilon, base_metrics)

    # Tabla comparativa
    comparison_data = {
        'Métrica': ['Precisión', 'Sensibilidad', 'AUC-ROC'],
        'Sin anonimización': [95.7, 91.4, 87.1],
        'Con anonimización': [
            current_impact['Precisión'],
            current_impact['Sensibilidad'], 
            current_impact['AUC-ROC']
        ],
        'Cambio (%)': [
            (current_impact['Precisión'] - 95.7) / 95.7 * 100,
            (current_impact['Sensibilidad'] - 91.4) / 91.4 * 100,
            (current_impact['AUC-ROC'] - 87.1) / 87.1 * 100
        ]
    }

    df_comparison = pd.DataFrame(comparison_data)

    # Mostrar tabla con formato
    st.markdown("### 📋 Tabla Comparativa del Impacto")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.dataframe(
            df_comparison.round(2),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        # Indicador de degradación total
        degradacion_total = current_impact['Degradación_%']
        color = "🟢" if degradacion_total < 5 else "🟡" if degradacion_total < 10 else "🔴"

        st.metric(
            "Degradación Total",
            f"{degradacion_total:.1f}%",
            delta=f"{color} {'EXCELENTE' if degradacion_total < 5 else 'BUENO' if degradacion_total < 10 else 'CRÍTICO'}"
        )

    # Gráfico de barras comparativo
    fig_comparison = go.Figure()

    fig_comparison.add_trace(go.Bar(
        name='Sin anonimización',
        x=comparison_data['Métrica'],
        y=comparison_data['Sin anonimización'],
        marker_color='steelblue',
        text=[f"{v:.1f}%" for v in comparison_data['Sin anonimización']],
        textposition='outside'
    ))

    fig_comparison.add_trace(go.Bar(
        name='Con anonimización',
        x=comparison_data['Métrica'],
        y=comparison_data['Con anonimización'],
        marker_color='lightcoral',
        text=[f"{v:.1f}%" for v in comparison_data['Con anonimización']],
        textposition='outside'
    ))

    fig_comparison.update_layout(
        title="Comparación de Métricas: Original vs Anonimizado",
        xaxis_title="Métricas de Rendimiento",
        yaxis_title="Porcentaje (%)",
        barmode='group',
        height=400
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

    st.markdown("---")

    # SECCIÓN 3: CUMPLIMIENTO GDPR POR ARTÍCULOS
    st.header("⚖️ Cumplimiento GDPR por Artículos")

    # Evaluación dinámica de cumplimiento
    def evaluate_gdpr_compliance(k, l, eps, degradation):
        compliance = {}

        compliance['Art. 5.1.c - Minimización'] = {
            'score': 95 if k >= 10 else 80,
            'status': 'CUMPLE' if k >= 10 else 'PARCIAL'
        }

        compliance['Art. 5.1.b - Limitación'] = {
            'score': 100,
            'status': 'CUMPLE'
        }

        compliance['Art. 5.1.d - Exactitud'] = {
            'score': 95 if degradation < 5 else 80 if degradation < 10 else 60,
            'status': 'CUMPLE' if degradation < 10 else 'CRÍTICO'
        }

        compliance['Art. 5.1.f - Integridad'] = {
            'score': 90 if eps <= 3.0 and l >= 2 else 75,
            'status': 'CUMPLE' if eps <= 3.0 and l >= 2 else 'PARCIAL'
        }

        compliance['Art. 5.2 - Responsabilidad'] = {
            'score': 95,
            'status': 'CUMPLE'
        }

        return compliance

    gdpr_compliance = evaluate_gdpr_compliance(k_value, l_value, epsilon, current_impact['Degradación_%'])

    # Mostrar compliance por artículo
    for articulo, data in gdpr_compliance.items():
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{articulo}**")

        with col2:
            score = data['score']
            color = "🟢" if score >= 90 else "🟡" if score >= 75 else "🔴"
            st.write(f"{color} {score}/100")

        with col3:
            status_color = "success" if data['status'] == 'CUMPLE' else "warning" if data['status'] == 'PARCIAL' else "error"
            st.success(data['status']) if data['status'] == 'CUMPLE' else st.warning(data['status']) if data['status'] == 'PARCIAL' else st.error(data['status'])

    # Score promedio
    avg_score = np.mean([data['score'] for data in gdpr_compliance.values()])

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col2:
        st.metric(
            "Score GDPR Promedio",
            f"{avg_score:.1f}/100",
            delta="✅ APROBADO" if avg_score >= 85 else "⚠️ REQUIERE AJUSTES"
        )

    # SECCIÓN 4: MONITOREO Y LOGS
    st.header("📋 Log de Auditoría y Monitoreo")

    # Simular log de eventos
    def generate_audit_log():
        events = []
        base_time = datetime.now()

        events_data = [
            ("Evaluación GDPR completada", "admin", "Éxito"),
            ("Parámetros actualizados", "data_scientist", "Éxito"), 
            ("Modelo reentrenado", "ml_engineer", "Éxito"),
            ("Dashboard accedido", "auditor", "Info"),
            ("Configuración modificada", "admin", "Éxito")
        ]

        for i, (evento, usuario, estado) in enumerate(events_data):
            events.append({
                'Timestamp': (base_time - timedelta(hours=i*2)).strftime('%Y-%m-%d %H:%M:%S'),
                'Evento': evento,
                'Usuario': usuario,
                'Estado': f"{'✅' if estado == 'Éxito' else 'ℹ️'} {estado}",
                'Parámetros': f"k={k_value}, l={l_value}, ε={epsilon:.1f}"
            })

        return pd.DataFrame(events)

    audit_df = generate_audit_log()
    st.dataframe(audit_df, use_container_width=True, hide_index=True)

    # SECCIÓN 5: CONFIGURACIÓN AVANZADA
    with st.expander("🔧 Configuración Avanzada", expanded=False):
        st.markdown("### Parámetros Técnicos Detallados")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Random Forest Config:**")
            st.code("""
n_estimators: 100
max_depth: 10
min_samples_split: 2
class_weight: 'balanced'
random_state: 42
            """)

        with col2:
            st.markdown("**Técnicas de Anonimización:**")
            st.code(f"""
SHA-256: Activo
K-anonimato: {k_value}
L-diversidad: {l_value}
Privacidad Diferencial: ε={epsilon:.1f}
            """)

        # Exportación de configuración
        if st.button("📥 Exportar Configuración"):
            config_data = {
                'timestamp': datetime.now().isoformat(),
                'k_anonimato': k_value,
                'l_diversidad': l_value,
                'epsilon': epsilon,
                'compliance_score': avg_score,
                'degradacion': current_impact['Degradación_%']
            }

            st.download_button(
                label="Descargar configuración JSON",
                data=pd.Series(config_data).to_json(indent=2),
                file_name=f"gdpr_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>Dashboard GDPR - TFM Anonimización de Datos Personales</strong></p>
        <p>Universidad UNIE - Madrid 2025 | Autores: Armando Ita, Daniel Mendoza, David González</p>
        <p>Tutor: Prof. D. Desirée Delgado Linares</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
