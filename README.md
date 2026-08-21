# Polluxa ETL Pipeline

A production-oriented Python ETL pipeline for extracting, validating, transforming, loading, and monitoring LinkedIn lead data.

## Architecture

Source CSV -> Extraction -> Incremental Filtering -> Validation -> Data Quality Checks -> Transformation -> PostgreSQL Loading -> Pipeline Metadata -> Watermark Management

## Technology Stack

- Python 3.13
- Pandas
- PostgreSQL 16
- SQLAlchemy
- psycopg2
- Pytest
- Docker / Docker Compose

## Project Structure

- airflow/dags - orchestration
- data/raw - source data
- data/failed - failed validation records
- sql - database schemas
- src - ETL pipeline implementation
- tests - automated tests
- powerbi - reporting layer
- docs - project documentation

## Pipeline Features

### Extraction
Reads lead data from the source CSV file into a Pandas DataFrame.

### Validation
Validates required fields and LinkedIn URLs before loading records into PostgreSQL. Invalid records are separated for review.

### Transformation
Transforms source fields into the warehouse schema, including column renaming, text cleaning, Hot Score conversion, Prioritized boolean conversion, and timestamp conversion.

### Incremental Loading
Uses the Added On timestamp as an incremental watermark. Records at or after the current watermark are processed. Timestamp ties are retained to prevent records from being missed.

### Data Quality
Evaluates Completeness, Uniqueness, Validity, Timeliness, and Referential Integrity. The weighted overall Data Quality score must be at least 90% for the pipeline to continue.

### Pipeline Metadata
Each execution records a Run ID, pipeline name, timestamps, row counts, status, and error information.

### Watermark Management
Pipeline watermarks are stored in PostgreSQL and are only advanced after a successful load.

### Idempotency
LinkedIn URL is used as the business uniqueness key. PostgreSQL ON CONFLICT handling prevents duplicate records from being inserted.

## Database Tables

- leads - validated and transformed lead records
- pipeline_runs - pipeline execution metadata
- pipeline_watermarks - incremental processing state
- dq_results - Data Quality results

## Running the Pipeline

Start PostgreSQL:

docker compose up -d postgres

Run tests:

docker compose run --rm pipeline pytest -v

Run the pipeline:

docker compose run --rm pipeline python -m src.main

## Testing

The automated test suite covers database connectivity, extraction, transformation, validation, incremental filtering, timestamp ties, idempotent loading, watermark management, Data Quality scoring, and pipeline failure handling.

Current test suite: 22 tests passing.

## Data Quality Example

Completeness: 100%
Uniqueness: 100%
Validity: 100%
Timeliness: 100%
Referential Integrity: 100%
Overall DQ Score: 100%
DQ Status: PASS

## Current Validation

The pipeline has been successfully tested with 10 source records, 10 valid records, 0 failed records, a 100% Data Quality score, successful pipeline metadata persistence, successful DQ result persistence, watermark management, and idempotent database loading.

## Design Considerations

Extraction, validation, transformation, loading, Data Quality, metadata, and watermark responsibilities are separated into independent modules to improve maintainability and testability.

## Future Enhancements

Potential extensions include Apache Airflow orchestration, retry and alerting mechanisms, structured logging, additional Data Quality rules, Power BI reporting, monitoring dashboards, and automated database migrations.
