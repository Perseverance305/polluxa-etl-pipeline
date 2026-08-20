CREATE TABLE IF NOT EXISTS leads (
    lead_id BIGSERIAL PRIMARY KEY,

    name TEXT NOT NULL,

    job_title TEXT,

    company TEXT NOT NULL,

    industry TEXT,

    location TEXT,

    agent TEXT,

    sdr_status TEXT,

    comment_status TEXT,

    hot_score DOUBLE PRECISION,

    source TEXT,

    prioritized BOOLEAN,

    linkedin_url TEXT NOT NULL,

    added_at TIMESTAMP,

    last_contacted_at TIMESTAMP,

    invite_sent_at TIMESTAMP,

    connected_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_linkedin_url
        UNIQUE (linkedin_url)
);