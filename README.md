
# Data Warehouse ETL Pipeline Project

## Project Overview

This project builds an ETL pipeline that extracts data from Amazon S3, stages it in Amazon Redshift, and transforms it into a star schema for analytics. The data includes song and log data, which will be used to analyze user activity on a music streaming platform.

### Key Steps:
- **Extract**: Load data from S3.
- **Transform**: Clean and process the data.
- **Load**: Insert data into Redshift tables.

---

## Project Files

1. **`create_table.py`**: 
   - Creates fact and dimension tables in Redshift for the star schema.
   
2. **`etl.py`**: 
   - Loads data from S3 into staging tables and transforms it into the final analytics tables.

3. **`sql_queries.py`**: 
   - Contains all SQL queries for creating, dropping, and inserting data into tables.

4. **`main.py`**: 
   - Checks what type of data we are going to work with.
   - All 3 folders downloaded to check all columns.

5. **`create_redsshift_cluster.py`**: 
   - To create Redshift Cluster remotely.
   - Apply Group Policy.
   - Create Rule to access S3 for reading.

6. **`README.md`**: 
   - Explains the project and your approach.

7. **`samples`**
   - to store the downloaded files from `main.py` file.

8. **`dwh.cfg`**
    - Please include following intels:
    - AWS.
    - CLUSTER.
    - IAM role ARN that give access to Redshift to read from S3.
    - Also, please remove ending folders of SONG_DATA='s3://udacity-dend/song_data/A/B' as it gets data from folder A/B/ in case if you want to load full access to all songs, so replace it with SONG_DATA='s3://udacity-dend/song_data'
---

## Database Schema Design

We use a **star schema** with one fact table and four dimension tables:

- **Fact Table**:
  - `songplay`: Stores song play events, referencing user, song, artist, and time.

- **Dimension Tables**:
  - `users`: Info about users.
  - `songs`: Info about songs.
  - `artists`: Info about artists.
  - `time`: Timestamps broken into units like hour, day, month, etc.

---

## ETL Pipeline Process

1. **Run `create_table.py`**:
   - This will create the necessary tables in Redshift.

   ```bash
   python create_table.py
   ```

2. **Run `etl.py`**:
   - This will load data from S3, stage it, and insert it into the final tables.

   ```bash
   python etl.py
   ```

---

## How the ETL Works

- **Staging Tables**: Data is first loaded from S3 into temporary staging tables in Redshift.
- **Fact and Dimension Tables**: The data is then processed and inserted into the `songplay` fact table and the `users`, `songs`, `artists`, and `time` dimension tables.

---

## Key Considerations

- **Star Schema**: This schema was chosen to make querying easier and faster for analytics.
- **Redshift**: Redshift integrates with S3, making it suitable for handling large datasets like ours.
- **Data Cleaning**: Data is cleaned and filtered (e.g., timestamps converted) in the ETL process.

---

## Summary

This project shows how to build an ETL pipeline using Redshift and S3, loading raw data, transforming it, and inserting it into a star schema for analysis. By doing this, you can perform fast, efficient queries on song play data.
