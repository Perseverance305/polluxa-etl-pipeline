CREATE TABLE IF NOT EXISTS pipeline_watermarks (
    pipeline_name TEXT PRIMARY KEY,

    watermark_value TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);