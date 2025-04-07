# 🧭 tourist_event_demo

Este repositorio contiene una colección de demos orientadas al análisis y modelado de datos en el contexto de eventos turísticos. Incluye componentes de procesamiento de datos, consultas SQL avanzadas, jerarquías recursivas, y una API para información cambiaria.

---

## 📌 Descripción de Carpetas y Archivos Clave

### 🔄 `currency_api_demo/`
Contiene una pequeña API en Python para consultar valores de moneda y almacenarlos. También incluye un DAG (`currency_daily_dag.py`) que podría integrarse con Apache Airflow para orquestar la extracción diaria.

- `currencyAPI.py`: Implementa lógica de la API.
- `main.py`: Punto de entrada de la aplicación.
- `db/`: Inicialización de la base de datos.

### 🧪 `tests/`
Pruebas unitarias para los endpoints de la API.

### 🧬 `hierarchy_people_demo/`
Contiene ejemplos de modelado de datos jerárquicos con SQL recursivo. Incluye diagramas e implementaciones pensadas para Snowflake u otros motores compatibles con CTEs.

- `recursive_demo.sql`: CTE recursivo básico.
- `snowflake_final_person_hierarchy.sql`: Ejemplo final con optimizaciones.

### 📊 `queries_demo/`
Consultas SQL orientadas al análisis de eventos:

- `venue_events.sql`: Información de eventos por locación.
- `category_prices.sql`: Precios por categoría.
- `ranked_days.sql`, `ranked_reviews.sql`: Rankings por fechas y reseñas.
- `diagram.jpg`: Diagrama relacional asociado a las tablas utilizadas.

---


📎 Notas
Este proyecto es una demo técnica, ideal como base para proyectos más complejos.

Algunas consultas están optimizadas para bases de datos como Snowflake, aunque pueden adaptarse fácilmente a PostgreSQL u otros engines SQL.
