# USED CAR PRICE PREDICTION PLATFORM 
TOOLS:
- PYTHON
- PANDAS
- NUMPY
- FASTAPI
- STREAMLIT
- AIRFLOW
- POSTGRESQL
- PANDERA
- GRAFANA

# A MODEL AS A SERVICE PLATFORM FOR PREDICTING PRICES OF USED CARS(SECOND HAND CARS) BASED ON SOME KEY FEATURES.
A USER HAS TWO OPTIONS:
- ENTER PARAMETERS BY HAND
- UPLOAD A CSV FILE

*USER ENTRY UNDERGOES SOME CHECKS AND IS SERVED TO THE MODEL THROUGH AN API.
*THE MODEL RUNS THE PREDICTION AND SAVES THE RESULT TO THE DATABASE.
*A USER CAN QUERY DATABASE TO VIEW PAST PREDICTIONS

ON THE OTHER HAND WE HAVE SCHEDULED DATA INGESTION AND PREDICTION JOBS USING AIRFLOW. 
THE INGESTION TASK GET DATA FROM SOME FILES AND RUN DATA QUALITY CHECK USING PANDERA.
IF A FILE PASSES IT IS THE INGESTED INTO PASSED OTHER IT IS KEPT IN FAILED. 
THE PASSED DATA IS THEN SERVED TO THE MODEL FOR PREDICTION. WE PUT UP A GRAFANA FOR MONITORING.

