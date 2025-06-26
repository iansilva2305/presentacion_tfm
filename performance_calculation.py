# Cálculo del Rendimiento Conservado - Random Forest
# ================================================

# Datos originales de la tabla de resultados
f1_original = 86.76      # F1-Score datos originales
f1_anonimizado = 84.74   # F1-Score datos anonimizados

print("=" * 60)
print("📊 CÁLCULO DE RENDIMIENTO CONSERVADO")
print("=" * 60)

print(f"F1-Score Original:     {f1_original:.2f}%")
print(f"F1-Score Anonimizado:  {f1_anonimizado:.2f}%")

# MÉTODO 1: Rendimiento Conservado (Porcentaje del original mantenido)
rendimiento_conservado = (f1_anonimizado / f1_original) * 100

print(f"\n🧮 CÁLCULO:")
print(f"Rendimiento Conservado = (F1_Anonimizado / F1_Original) × 100")
print(f"Rendimiento Conservado = ({f1_anonimizado} / {f1_original}) × 100")
print(f"Rendimiento Conservado = {f1_anonimizado/f1_original:.4f} × 100")
print(f"Rendimiento Conservado = {rendimiento_conservado:.1f}%")

# MÉTODO 2: Degradación (Pérdida porcentual)
degradacion = ((f1_original - f1_anonimizado) / f1_original) * 100

print(f"\n📉 DEGRADACIÓN:")
print(f"Degradación = ((F1_Original - F1_Anonimizado) / F1_Original) × 100")
print(f"Degradación = (({f1_original} - {f1_anonimizado}) / {f1_original}) × 100")
print(f"Degradación = {(f1_original - f1_anonimizado):.2f} / {f1_original} × 100")
print(f"Degradación = {degradacion:.2f}%")

# VERIFICACIÓN: Rendimiento Conservado + Degradación = 100%
print(f"\n✅ VERIFICACIÓN:")
print(f"Rendimiento Conservado + Degradación = {rendimiento_conservado:.1f}% + {degradacion:.2f}% = {rendimiento_conservado + degradacion:.1f}%")

print(f"\n🏆 CONCLUSIÓN:")
print(f"Random Forest mantiene {rendimiento_conservado:.1f}% del rendimiento original")
print(f"La degradación es solo del {degradacion:.2f}%")

print("\n" + "=" * 60)
print("📋 COMPARATIVA CON OTROS MODELOS")
print("=" * 60)

# Datos de otros modelos para comparación
modelos = {
    'Random Forest': {'original': 86.76, 'anonimizado': 84.74},
    'XGBoost': {'original': 86.33, 'anonimizado': 66.43},
    'Regresión Logística': {'original': 52.46, 'anonimizado': 54.86}
}

for modelo, datos in modelos.items():
    orig = datos['original']
    anon = datos['anonimizado']
    
    # Calcular rendimiento conservado
    if orig > 0:  # Evitar división por cero
        conservado = (anon / orig) * 100
        degradacion_modelo = ((orig - anon) / orig) * 100
    else:
        conservado = 0
        degradacion_modelo = 0
    
    print(f"\n{modelo}:")
    print(f"  Original: {orig:.2f}% → Anonimizado: {anon:.2f}%")
    print(f"  Rendimiento Conservado: {conservado:.1f}%")
    print(f"  Degradación: {degradacion_modelo:.2f}%")
    
    # Clasificación de rendimiento
    if conservado >= 95:
        clasificacion = "🟢 EXCELENTE"
    elif conservado >= 85:
        clasificacion = "🟡 BUENO"
    elif conservado >= 70:
        clasificacion = "🟠 ACEPTABLE"
    else:
        clasificacion = "🔴 DEFICIENTE"
    
    print(f"  Clasificación: {clasificacion}")

print("\n" + "=" * 60)
print("🎯 INTERPRETACIÓN DE RESULTADOS")
print("=" * 60)

print("""
📈 SIGNIFICADO DEL 97.7%:
   • Random Forest conserva 97.7% de su efectividad original
   • Solo pierde 2.3% de rendimiento tras anonimización
   • Es el modelo más robusto ante transformaciones de privacidad

🔍 COMPARACIÓN:
   • Random Forest: 97.7% conservado (EXCELENTE)
   • XGBoost: 76.9% conservado (ACEPTABLE)  
   • Reg. Logística: 104.6% conservado (MEJORA PARADÓJICA)

✅ CONCLUSIÓN TÉCNICA:
   Random Forest demuestra la mejor relación privacidad-utilidad,
   manteniendo prácticamente intacta su capacidad predictiva
   mientras cumple completamente con los requisitos GDPR.
""")

# Función para calcular rendimiento conservado de cualquier modelo
def calcular_rendimiento_conservado(f1_orig, f1_anon):
    """
    Calcula el porcentaje de rendimiento conservado tras anonimización
    
    Args:
        f1_orig (float): F1-Score con datos originales
        f1_anon (float): F1-Score con datos anonimizados
    
    Returns:
        dict: Diccionario con métricas calculadas
    """
    rendimiento_conservado = (f1_anon / f1_orig) * 100 if f1_orig > 0 else 0
    degradacion = ((f1_orig - f1_anon) / f1_orig) * 100 if f1_orig > 0 else 0
    
    return {
        'rendimiento_conservado': round(rendimiento_conservado, 1),
        'degradacion': round(degradacion, 2),
        'diferencia_absoluta': round(f1_orig - f1_anon, 2),
        'clasificacion': (
            'EXCELENTE' if rendimiento_conservado >= 95 else
            'BUENO' if rendimiento_conservado >= 85 else
            'ACEPTABLE' if rendimiento_conservado >= 70 else
            'DEFICIENTE'
        )
    }

# Ejemplo de uso de la función
resultado_rf = calcular_rendimiento_conservado(86.76, 84.74)
print(f"\n🔧 FUNCIÓN REUTILIZABLE:")
print(f"Random Forest: {resultado_rf}")
