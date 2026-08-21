CREATE TABLE IF NOT EXISTS dq_results (
    dq_result_id BIGSERIAL PRIMARY KEY,

    run_id UUID NOT NULL,

    pipeline_name TEXT NOT NULL,

    completeness_score DOUBLE PRECISION NOT NULL,
    uniqueness_score DOUBLE PRECISION NOT NULL,
    validity_score DOUBLE PRECISION NOT NULL,
    timeliness_score DOUBLE PRECISION NOT NULL,
    referential_integrity_score DOUBLE PRECISION NOT NULL,

    overall_score DOUBLE PRECISION NOT NULL,

    status TEXT NOT NULL,

    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dq_run
        FOREIGN KEY (run_id)
        REFERENCES pipeline_runs(run_id)
);