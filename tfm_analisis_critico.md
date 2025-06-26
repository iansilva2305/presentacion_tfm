# Análisis Crítico del TFM: Anonimización de Datos y Cumplimiento GDPR

**Trabajo Final de Máster**  
**Autores:** Armando Ita, Alexis Mendoza, David González  
**Tutor:** Prof. D. Desirée Delgado Linares  
**Universidad UNIE - Madrid, 2025**

---

## Preguntas de Evaluación Crítica

### 1. ¿Qué tipo de limpieza de datos se ha aplicado?
### 2. ¿Otros modelos que se pueden aplicar para la casuística establecida?
### 3. ¿Qué otras variables puedes haber tenido en cuenta para el análisis?
### 4. ¿Considere que esta data ha sido correspondiente para un entorno de Big Data?

---

## 🧹 1. LIMPIEZA DE DATOS APLICADA

Según el TFM desarrollado, se aplicaron las siguientes técnicas de limpieza y preprocesamiento:

### Preprocesamiento Básico

```python
# Manejo de valores faltantes
df.dropna(subset=['nameOrig', 'nameDest', 'amount'], inplace=True)

# Eliminación de duplicados exactos
df.drop_duplicates(inplace=True)

# Filtrado de transacciones válidas (amount > 0)
df = df[df['amount'] > 0]

# Tratamiento de outliers extremos en montos
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
df = df[df['amount'] <= Q3 + 3*IQR]  # Eliminar outliers extremos
```

### Transformaciones Específicas

- **Normalización temporal:** Conversión de `step` a períodos interpretables (madrugada, mañana, tarde, noche)
- **Codificación categórica:** LabelEncoder para variables tipo `type`
- **Feature engineering:** Creación de ratios (`amount_to_balance_ratio_orig`, `amount_to_balance_ratio_dest`)
- **Tratamiento de infinitos:** Reemplazo de `inf` y `-inf` por valores finitos
- **Limpieza de caracteres especiales:** En identificadores antes de aplicar SHA-256
- **Validación de tipos de datos:** Asegurar consistencia en tipos numéricos y categóricos

### Limpieza Específica para Anonimización

```python
# Preparación para seudonimización
df['nameOrig'] = df['nameOrig'].astype(str).str.strip()
df['nameDest'] = df['nameDest'].astype(str).str.strip()

# Normalización de montos para agrupación k-anónima
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df = df[df['amount'].notna()]

# Validación de rangos temporales
df = df[(df['step'] >= 1) & (df['step'] <= 744)]  # 1 mes = 744 horas
```

---

## 🤖 2. OTROS MODELOS APLICABLES

Además de Random Forest, XGBoost y Regresión Logística evaluados en el TFM, otros modelos relevantes para detección de fraudes incluyen:

### Modelos de Ensemble Avanzados

```python
# Voting Classifier (combinación de modelos)
from sklearn.ensemble import VotingClassifier
voting_clf = VotingClassifier([
    ('rf', RandomForestClassifier()),
    ('xgb', XGBClassifier()),
    ('lr', LogisticRegression())
], voting='soft')

# AdaBoost
from sklearn.ensemble import AdaBoostClassifier
ada_clf = AdaBoostClassifier(
    n_estimators=100,
    learning_rate=1.0,
    random_state=42
)

# CatBoost (manejo nativo de categóricas)
from catboost import CatBoostClassifier
cat_clf = CatBoostClassifier(
    iterations=100,
    learning_rate=0.1,
    depth=6,
    verbose=False
)

# LightGBM (alternativa eficiente a XGBoost)
import lightgbm as lgb
lgb_clf = lgb.LGBMClassifier(
    n_estimators=100,
    learning_rate=0.1,
    num_leaves=31
)
```

### Modelos para Datos Desbalanceados

```python
# SMOTE + Random Forest
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

smote_pipeline = ImbPipeline([
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier())
])

# Isolation Forest (detección de anomalías)
from sklearn.ensemble import IsolationForest
iso_forest = IsolationForest(
    contamination=0.001,
    random_state=42,
    n_estimators=100
)

# One-Class SVM
from sklearn.svm import OneClassSVM
oc_svm = OneClassSVM(
    gamma='scale',
    nu=0.001
)

# Local Outlier Factor
from sklearn.neighbors import LocalOutlierFactor
lof = LocalOutlierFactor(
    n_neighbors=20,
    contamination=0.001
)
```

### Modelos de Deep Learning

```python
# Autoencoder para detección de anomalías
import tensorflow as tf

def create_autoencoder(input_dim):
    autoencoder = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(4, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(input_dim, activation='sigmoid')
    ])
    return autoencoder

# LSTM para patrones secuenciales temporales
def create_lstm_model(sequence_length, features):
    lstm_model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, 
                           input_shape=(sequence_length, features)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(50, return_sequences=False),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(25),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    return lstm_model

# Red Neuronal con DP-SGD (Privacidad Diferencial)
import tensorflow_privacy as tfp

def create_dp_neural_network(input_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Optimizador con privacidad diferencial
    optimizer = tfp.DPKerasAdamOptimizer(
        l2_norm_clip=1.0,
        noise_multiplier=1.1,
        num_microbatches=250,
        learning_rate=0.15
    )
    
    return model, optimizer
```

### Modelos Probabilísticos

```python
# Naive Bayes Gaussiano
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()

# Análisis Discriminante Cuadrático
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
qda = QuadraticDiscriminantAnalysis()

# Modelos Bayesianos con PyMC3
import pymc3 as pm

def bayesian_logistic_regression(X, y):
    with pm.Model() as model:
        # Priors
        alpha = pm.Normal('alpha', mu=0, sigma=10)
        beta = pm.Normal('beta', mu=0, sigma=10, shape=X.shape[1])
        
        # Linear combination
        mu = alpha + pm.math.dot(X, beta)
        
        # Likelihood
        p = pm.Deterministic('p', pm.math.sigmoid(mu))
        observed = pm.Bernoulli('observed', p=p, observed=y)
        
        # Inference
        trace = pm.sample(2000, tune=1000)
    
    return model, trace
```

---

## 📊 3. VARIABLES ADICIONALES PARA EL ANÁLISIS

Más allá de las variables básicas de PaySim1, se podrían considerar:

### Variables Temporales Avanzadas

```python
# Patrones temporales más sofisticados
df['hour'] = df['step'] % 24
df['day_of_week'] = (df['step'] // 24) % 7
df['week_of_month'] = (df['step'] // (24 * 7)) % 4
df['is_weekend'] = df['day_of_week'].isin([5, 6])
df['is_business_hours'] = df['hour'].between(9, 17)
df['is_night_time'] = df['hour'].between(22, 6)

# Frecuencia de transacciones por usuario
df['user_transaction_count'] = df.groupby('nameOrig')['step'].transform('count')
df['time_since_last_transaction'] = df.groupby('nameOrig')['step'].diff()
df['avg_time_between_transactions'] = df.groupby('nameOrig')['time_since_last_transaction'].transform('mean')

# Patrones de actividad
df['transactions_this_hour'] = df.groupby(['nameOrig', 'hour'])['step'].transform('count')
df['transactions_this_day'] = df.groupby(['nameOrig', df['step']//24])['step'].transform('count')
```

### Variables de Comportamiento del Usuario

```python
# Patrones de gasto
df['avg_amount_user'] = df.groupby('nameOrig')['amount'].transform('mean')
df['std_amount_user'] = df.groupby('nameOrig')['amount'].transform('std')
df['median_amount_user'] = df.groupby('nameOrig')['amount'].transform('median')
df['amount_deviation'] = (df['amount'] - df['avg_amount_user']) / (df['std_amount_user'] + 1e-6)

# Diversidad de comportamiento
df['user_transaction_types'] = df.groupby('nameOrig')['type'].transform('nunique')
df['user_unique_destinations'] = df.groupby('nameOrig')['nameDest'].transform('nunique')
df['destination_frequency'] = df.groupby(['nameOrig', 'nameDest']).cumcount() + 1

# Velocidad y frecuencia
df['transactions_per_day'] = df.groupby(['nameOrig', df['step']//24]).size()
df['avg_daily_transactions'] = df.groupby('nameOrig')['transactions_per_day'].transform('mean')
df['transaction_velocity'] = df['amount'] / (df['time_since_last_transaction'] + 1)

# Patrones de balance
df['balance_change_orig'] = df['newbalanceOrig'] - df['oldbalanceOrg']
df['balance_change_dest'] = df['newbalanceDest'] - df['oldbalanceDest']
df['balance_inconsistency'] = abs(df['balance_change_orig'] + df['amount'])
```

### Variables de Red y Grafos

```python
# Análisis de red de transacciones
import networkx as nx
import pandas as pd

# Construir grafo de transacciones
def create_transaction_network(df):
    G = nx.from_pandas_edgelist(
        df, 'nameOrig', 'nameDest', 
        edge_attr=['amount', 'type'], 
        create_using=nx.DiGraph()
    )
    return G

# Métricas de centralidad
def add_network_features(df):
    G = create_transaction_network(df)
    
    # Grado de conectividad
    df['out_degree'] = df.groupby('nameOrig')['nameDest'].transform('nunique')
    df['in_degree'] = df.groupby('nameDest')['nameOrig'].transform('nunique')
    
    # Centralidad (si el grafo no es muy grande)
    if len(G.nodes()) < 10000:
        centrality = nx.degree_centrality(G)
        betweenness = nx.betweenness_centrality(G, k=1000)  # Muestra para eficiencia
        pagerank = nx.pagerank(G)
        
        df['centrality'] = df['nameOrig'].map(centrality).fillna(0)
        df['betweenness'] = df['nameOrig'].map(betweenness).fillna(0)
        df['pagerank'] = df['nameOrig'].map(pagerank).fillna(0)
    
    return df

# Detección de comunidades
def detect_communities(df):
    G = create_transaction_network(df)
    communities = nx.community.greedy_modularity_communities(G.to_undirected())
    
    # Mapear nodos a comunidades
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i
    
    df['community'] = df['nameOrig'].map(node_to_community).fillna(-1)
    return df
```

### Variables de Contexto y Riesgo

```python
# Variables de riesgo acumulativo
df['user_fraud_history'] = df.groupby('nameOrig')['isFraud'].transform('cumsum')
df['user_fraud_rate'] = df['user_fraud_history'] / df.groupby('nameOrig').cumcount()

# Patrones de montos
df['amount_percentile_user'] = df.groupby('nameOrig')['amount'].transform(
    lambda x: x.rank(pct=True)
)
df['is_unusual_amount'] = (df['amount_percentile_user'] > 0.95) | (df['amount_percentile_user'] < 0.05)

# Variables de sesión/secuencia
df['session_id'] = (df.groupby('nameOrig')['step'].diff() > 1).cumsum()
df['transactions_in_session'] = df.groupby(['nameOrig', 'session_id']).cumcount() + 1
df['session_total_amount'] = df.groupby(['nameOrig', 'session_id'])['amount'].transform('sum')
```

### Variables Macroeconómicas (Si Disponibles)

```python
# Si tuviéramos datos externos
def add_macro_features(df, market_data, economic_data, security_data):
    # Unir por fecha/hora
    df['date'] = pd.to_datetime(df['step'], unit='h', origin='2016-01-01')
    
    # Variables macroeconómicas
    df = df.merge(market_data[['date', 'volatility', 'market_stress']], 
                  on='date', how='left')
    df = df.merge(economic_data[['date', 'economic_indicator', 'inflation']], 
                  on='date', how='left')
    df = df.merge(security_data[['date', 'fraud_alert_level', 'cyber_threat_level']], 
                  on='date', how='left')
    
    # Variables derivadas
    df['high_volatility_period'] = df['volatility'] > df['volatility'].quantile(0.8)
    df['economic_stress'] = df['economic_indicator'] < df['economic_indicator'].quantile(0.2)
    
    return df
```

---

## 🏗️ 4. CONSIDERACIONES PARA BIG DATA

El PaySim1 (6.3M transacciones) es moderadamente grande, pero para **verdadero Big Data** (100M+ transacciones), se requieren adaptaciones significativas:

### Arquitectura Big Data Sugerida

```python
# Apache Spark para procesamiento distribuido
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.sql.functions import *

# Configuración optimizada para Big Data
spark = SparkSession.builder \
    .appName("FraudDetectionGDPR") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB") \
    .getOrCreate()

# Leer datos distribuidos desde múltiples fuentes
df_spark = spark.read \
    .option("multiline", "true") \
    .option("inferSchema", "true") \
    .parquet("s3://fraud-data/paysim_partitioned/year=*/month=*/day=*/")
```

### Procesamiento Distribuido

```python
# Particionamiento inteligente para optimizar JOIN operations
df_partitioned = df_spark.repartition(200, "nameOrig")  # Por usuario para análisis de comportamiento

# Agregaciones distribuidas para k-anonimato
from pyspark.sql.window import Window

# K-anonimato distribuido
window_spec = Window.partitionBy("amount_group", "step_group")
k_anonymity_groups = df_spark.withColumn(
    "group_size", 
    count("*").over(window_spec)
).filter(col("group_size") >= 10)

# Caching estratégico para operaciones repetitivas
df_spark.cache()
k_anonymity_groups.cache()

# MLlib para modelos escalables
from pyspark.ml.classification import GBTClassifier, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Pipeline de ML distribuido
assembler = VectorAssembler(
    inputCols=["amount", "oldbalanceOrg", "newbalanceOrig"], 
    outputCol="features"
)

rf_spark = RandomForestClassifier(
    featuresCol="features", 
    labelCol="isFraud",
    numTrees=100,
    maxDepth=10
)

pipeline = Pipeline(stages=[assembler, rf_spark])
```

### Almacenamiento Optimizado

```python
# Formato Parquet con compresión y particionado inteligente
df.write.mode("overwrite") \
  .option("compression", "snappy") \
  .partitionBy("year", "month", "type") \
  .option("maxRecordsPerFile", 1000000) \
  .parquet("s3://fraud-data/processed/")

# Delta Lake para ACID transactions y versionado
df.write.format("delta") \
  .option("mergeSchema", "true") \
  .save("/path/to/delta-table")

# Iceberg para schema evolution
df.write.format("iceberg") \
  .option("write.target-file-size-bytes", 134217728) \
  .save("warehouse.fraud_transactions")
```

### Anonimización Distribuida

```python
# Hash SHA-256 distribuido con UDF optimizada
from pyspark.sql.functions import sha2, col, udf
from pyspark.sql.types import StringType

# UDF para SHA-256 (más eficiente que aplicar a cada fila)
@udf(returnType=StringType())
def hash_sha256_udf(value):
    import hashlib
    if value is None:
        return None
    return hashlib.sha256(str(value).encode()).hexdigest()

# Aplicar seudonimización distribuida
df_anonymized = df_spark.withColumn(
    "nameOrig_hash", 
    sha2(col("nameOrig"), 256)
).withColumn(
    "nameDest_hash", 
    sha2(col("nameDest"), 256)
)

# K-anonimato con window functions optimizadas
window_k_anon = Window.partitionBy("amount_group", "step_group")
df_k_anon = df_anonymized.withColumn(
    "group_size", 
    count("*").over(window_k_anon)
).filter(col("group_size") >= 10)

# Persistir resultados con optimización
df_k_anon.write \
    .mode("overwrite") \
    .option("compression", "gzip") \
    .partitionBy("amount_group") \
    .parquet("s3://fraud-data/anonymized/")
```

### Streaming y Tiempo Real

```python
# Kafka para streaming de transacciones en tiempo real
from pyspark.streaming import StreamingContext
from pyspark.sql.types import *

# Schema para datos de streaming
transaction_schema = StructType([
    StructField("nameOrig", StringType(), True),
    StructField("nameDest", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("type", StringType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Leer stream de Kafka
stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "fraud_transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Deserializar y procesar
parsed_stream = stream.select(
    from_json(col("value").cast("string"), transaction_schema).alias("data")
).select("data.*")

# Aplicar modelo pre-entrenado a stream
model_broadcast = spark.sparkContext.broadcast(trained_model)

def apply_fraud_detection(batch_df, batch_id):
    if batch_df.count() > 0:
        # Aplicar anonimización
        anonymized_batch = apply_anonymization(batch_df)
        
        # Aplicar modelo de fraude
        predictions = model_broadcast.value.transform(anonymized_batch)
        
        # Escribir resultados
        predictions.write \
            .mode("append") \
            .format("delta") \
            .save("/path/to/fraud_results/")

# Procesar stream
query = parsed_stream.writeStream \
    .foreachBatch(apply_fraud_detection) \
    .trigger(processingTime='30 seconds') \
    .start()
```

### Optimizaciones Específicas para Big Data

```python
# 1. Bucketing para optimizar JOINs
df.write \
    .bucketBy(42, "nameOrig") \
    .sortBy("step") \
    .saveAsTable("fraud_transactions_bucketed")

# 2. Z-ordering para mejor localidad de datos (Delta Lake)
from delta.tables import DeltaTable

DeltaTable.forPath(spark, "/path/to/delta-table") \
    .optimize() \
    .executeZOrderBy("nameOrig", "step", "amount")

# 3. Estadísticas de tabla para optimización de queries
spark.sql("ANALYZE TABLE fraud_transactions COMPUTE STATISTICS FOR ALL COLUMNS")

# 4. Broadcast para tablas pequeñas (mapeos, configuraciones)
broadcast_mapping = broadcast(spark.table("user_risk_mapping"))
df_enriched = df_spark.join(broadcast_mapping, "nameOrig", "left")

# 5. Particionado temporal inteligente
df.write \
    .partitionBy(year("timestamp"), month("timestamp"), dayofmonth("timestamp")) \
    .mode("overwrite") \
    .parquet("s3://fraud-data/time_partitioned/")
```

### Monitorización y Observabilidad

```python
# Métricas de rendimiento
from pyspark.sql.functions import spark_partition_id

# Monitorizar distribución de datos
partition_counts = df_spark.withColumn("partition_id", spark_partition_id()) \
    .groupBy("partition_id").count() \
    .collect()

# Logging estructurado
import logging
import json

def log_performance_metrics(stage_name, start_time, end_time, record_count):
    metrics = {
        "stage": stage_name,
        "duration_seconds": (end_time - start_time).total_seconds(),
        "records_processed": record_count,
        "records_per_second": record_count / (end_time - start_time).total_seconds()
    }
    logging.info(f"Performance metrics: {json.dumps(metrics)}")

# Alertas automáticas
def check_data_quality(df):
    total_records = df.count()
    null_records = df.filter(col("nameOrig").isNull()).count()
    null_percentage = (null_records / total_records) * 100
    
    if null_percentage > 5:
        # Enviar alerta
        send_alert(f"High null percentage in nameOrig: {null_percentage}%")
```

---

## 🎯 EVALUACIÓN CRÍTICA DEL TFM

### Fortalezas Identificadas

✅ **Metodología sólida:** CRISP-DM bien aplicada y documentada  
✅ **Cumplimiento legal:** GDPR técnicamente implementado con validación  
✅ **Código reproducible:** Framework reutilizable y bien documentado  
✅ **Análisis comparativo:** 3 algoritmos evaluados sistemáticamente  
✅ **Resultados consistentes:** Random Forest identificado como más robusto  
✅ **Documentación completa:** 81 páginas con evidencia técnica  

### Áreas de Mejora Potenciales

⚠️ **Escalabilidad:** Adaptación necesaria para Big Data real (100M+ transacciones)  
⚠️ **Variables adicionales:** Más features de comportamiento y contexto  
⚠️ **Modelos avanzados:** Deep Learning, ensemble methods más sofisticados  
⚠️ **Tiempo real:** Detección online vs procesamiento batch  
⚠️ **Validación externa:** Testing con otros datasets financieros  
⚠️ **Técnicas adicionales:** T-closeness, δ-presence, synthetic data generation  

### Impacto y Aplicabilidad

🏆 **Contribución académica:** Puente exitoso entre teoría GDPR y práctica ML  
🏭 **Relevancia industrial:** Framework aplicable en instituciones financieras  
📊 **Evidencia empírica:** Trade-off privacidad-utilidad cuantificado  
🔒 **Cumplimiento normativo:** 100% verificado técnicamente  

### Recomendaciones para Trabajo Futuro

1. **Implementar Spark/Dask** para escalabilidad a datasets masivos
2. **Añadir variables de grafos** para detectar redes fraudulentas complejas
3. **Probar autoencoders** para detección de anomalías no lineales
4. **Desarrollar pipeline streaming** para detección en tiempo real
5. **Integrar más técnicas** de anonimización (t-closeness, δ-presence)
6. **Validar con datos reales** de instituciones financieras
7. **Desarrollar métricas** de utilidad específicas del dominio
8. **Implementar federated learning** para colaboración inter-institucional

---

## 📝 Conclusión

El TFM desarrollado es **metodológicamente sólido** y **técnicamente correcto**, cumpliendo con todos los objetivos planteados. La investigación demuestra exitosamente que es posible mantener **97.98% del rendimiento original** de modelos ML mientras se cumple **100% con GDPR**.

Las preguntas planteadas revelan **oportunidades de expansión** hacia:
- Arquitecturas más escalables (Big Data)
- Modelos más sofisticados (Deep Learning)
- Variables adicionales (comportamiento, red, contexto)
- Aplicación en tiempo real (streaming)

Esto posiciona el trabajo como una **base sólida** para futuras investigaciones en la intersección de **privacidad, ética y eficacia** en sistemas de IA financiera.

---

**Documento generado:** `r format(Sys.Date(), "%B %d, %Y")`  
**Versión:** 1.0  
**Estado:** Completo para evaluación académica