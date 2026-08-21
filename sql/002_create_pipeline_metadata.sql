CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id UUID PRIMARY KEY,

    pipeline_name TEXT NOT NULL,

    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,

    rows_extracted INTEGER DEFAULT 0,
    rows_valid INTEGER DEFAULT 0,
    rows_failed INTEGER DEFAULT 0,
    rows_loaded INTEGER DEFAULT 0,

    status TEXT NOT NULL,

    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);