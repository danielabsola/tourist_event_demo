# 🧭 tourist_event_demo

Este repositorio contiene una colección de demos orientadas al análisis y modelado de datos en el contexto de eventos turísticos. Incluye componentes de procesamiento de datos, consultas SQL avanzadas, jerarquías recursivas, y una API para información cambiaria.

---


### 1. `currency_api_demo/`

Este directorio contiene una demostración de una API diseñada para consultar y almacenar tasas de cambio de divisas.

- **`currency_job/dags/currency_daily_dag.py`**: Define un DAG para la extracción diaria de tasas de cambio, posiblemente para su uso con Apache Airflow.&#8203;:contentReference[oaicite:2]{index=2}
- **`src/`**:
  - **`db/__init__.py`**: :contentReference[oaicite:3]{index=3}&#8203;:contentReference[oaicite:4]{index=4}
  - **`currencyAPI.py`**: :contentReference[oaicite:5]{index=5}&#8203;:contentReference[oaicite:6]{index=6}
  - **`main.py`**: :contentReference[oaicite:7]{index=7}&#8203;:contentReference[oaicite:8]{index=8}

### 2. `hierarchy_people_demo/`

:contentReference[oaicite:9]{index=9}&#8203;:contentReference[oaicite:10]{index=10}

- **`insert_data_demo.sql`**: :contentReference[oaicite:11]{index=11}&#8203;:contentReference[oaicite:12]{index=12}
- **`recursive_demo.sql`**: :contentReference[oaicite:13]{index=13}&#8203;:contentReference[oaicite:14]{index=14}
- **`snowflake_final_person_hierarchy.sql`**: :contentReference[oaicite:15]{index=15}&#8203;:contentReference[oaicite:16]{index=16}
- **`snowflake_person_hierarchy.png`**: :contentReference[oaicite:17]{index=17}&#8203;:contentReference[oaicite:18]{index=18}

### 3. `queries_demo/`

:contentReference[oaicite:19]{index=19}&#8203;:contentReference[oaicite:20]{index=20}

- **`category_prices.sql`**: :contentReference[oaicite:21]{index=21}&#8203;:contentReference[oaicite:22]{index=22}
- **`diagram.jpg`**: :contentReference[oaicite:23]{index=23}&#8203;:contentReference[oaicite:24]{index=24}
- **`ranked_days.sql`**: :contentReference[oaicite:25]{index=25}&#8203;:contentReference[oaicite:26]{index=26}
- **`ranked_reviews.sql`**: :contentReference[oaicite:27]{index=27}&#8203;:contentReference[oaicite:28]{index=28}
- **`venue_events.sql`**: :contentReference[oaicite:29]{index=29}&#8203;:contentReference[oaicite:30]{index=30}

## 🚀 Cómo Empezar

Para explorar y ejecutar las demostraciones proporcionadas:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/danielabsola/tourist_event_demo.git


---


📎 Notas
Este proyecto es una demo técnica, ideal como base para proyectos más complejos.

Algunas consultas están optimizadas para bases de datos como Snowflake, aunque pueden adaptarse fácilmente a PostgreSQL u otros engines SQL.
