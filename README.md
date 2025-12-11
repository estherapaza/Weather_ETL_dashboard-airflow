# Author Esther Guadalupe Apaza Hacho

# Weather ETL Dashboard Project
This project implements a fully containerized Extract, Transform, Load (ETL) pipeline using Apache Airflow to collect, process, and visualize meteorological data. The system loads weather data into a PostgreSQL database and generates an interactive dashboard using Streamlit. This fulfills the requirements of the Data Engineering course project.

---

## 1. PHASE 1: Project Justification
### Problem Identified and Beneficiaries
Weather variability directly impacts critical sectors such as energy management, agriculture, transportation, and public safety. Accurate and timely weather insights help organizations anticipate risks such as energy demand spikes, crop-impacting conditions, or severe weather alerts that could endanger communities.

This project addresses the need for automated, reliable, and routinely updated weather intelligence. By collecting and transforming meteorological variables such as temperature, precipitation, humidity, wind metrics, and alert conditions, the system provides a structured foundation for decision-making.

Primary beneficiaries include:
- Energy and utility companies requiring demand forecasting  
- Agricultural producers needing climatic risk assessment  
- Emergency response and public safety agencies  
- General users seeking consolidated and easy-to-read weather insights  

The automated ETL pipeline ensures data consistency through daily scheduling and centralizes information into analytical formats suitable for visualization and external analysis.

---

## 2. PHASE 2: Apache Airflow ETL Pipeline Design
The ETL workflow is implemented using an Airflow DAG (`weather_etl.py`), which manages the extraction, transformation, and loading of weather data into a PostgreSQL database. All components are orchestrated through Docker Compose for reproducibility and portability.

### ETL Components and Implementation Details

| Component       | Implementation Detail |
|----------------|------------------------|
| **Extract** | Retrieves meteorological data from the configured API using geographical coordinates defined in the `.env` file (latitude and longitude). |
| **Transform** | Processes raw API responses, standardizes formats, handles missing values, organizes records by timestamps, and prepares datasets for storage. |
| **Load** | Inserts the structured data into PostgreSQL tables and exports CSV files into the `data/` directory. |
| **Scheduling** | The DAG runs on a daily interval (`SCHEDULE=0 0 * * *`), executing at midnight (UTC). |
| **Error Handling** | Airflow default configuration applies: task retries and log-based debugging. |
| **Data Storage** | Tables and CSV outputs include metrics such as hourly/daily temperature, humidity, precipitation, wind, and active weather alerts. |
| **Automation Environment** | Fully containerized using Docker Compose to manage Airflow, PostgreSQL, and Streamlit services. |

### Additional Pipeline Characteristics
- **Data Folder Initialization:** The `data/` folder is created (and assigned correct permissions) before pipeline execution.  
- **Configuration Control:** All key parameters (API coordinates, timezone, DB credentials, scheduling) are managed through environment variables in the `.env` file.  
- **Manual DAG Execution:** Users can trigger ETL runs directly via the Airflow interface at `http://localhost:8080`.  

---

## 3. PHASE 3: Dashboard Analysis and Impact
### 3.1 Purpose of the Dashboard
The interactive dashboard developed with Streamlit presents the transformed meteorological data to end-users in a clear and actionable format. It enables users to explore:

- Hourly, daily, and weekly temperature patterns  
- Precipitation levels  
- Wind speed and direction  
- Humidity trends  
- Active weather alerts  

These visualizations allow for rapid identification of climatic patterns relevant for planning, safety, and operational decision-making.

### 3.2 Impact of the Insights
The dashboard supports various real-world applications:

- **Operational Planning:** Organizations can anticipate weather-sensitive conditions such as storms, extreme heat, or heavy rainfall.  
- **Public Safety:** Alerts displayed in real time assist in evaluating risk and planning emergency responses.  
- **Agricultural Efficiency:** Insights into humidity, temperature variation, and precipitation support crop care decisions.  
- **Energy Demand Forecasting:** Temperature patterns help predict energy consumption peaks.  

The structured information provided by the dashboard helps reduce uncertainty and improve the reaction time for weather-dependent activities.

