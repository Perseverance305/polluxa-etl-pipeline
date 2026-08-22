-- ============================================================
-- Power BI Reporting Layer
-- Polluxa LinkedIn Agent Analytics
-- ============================================================

CREATE OR REPLACE VIEW analytics.vw_powerbi_outreach_summary AS
SELECT
    d.full_date,
    a.agent_name,
    a.account_age_tier,
    a.risk_classification,
    a.daily_invite_limit,
    a.daily_message_limit,
    c.campaign_name,
    c.target_segment,
    c.source AS campaign_source,

    COUNT(*) AS total_events,

    COUNT(*) FILTER (
        WHERE f.event_type = 'CONTACTED'
    ) AS contacts_sent,

    COUNT(*) FILTER (
        WHERE f.event_type = 'CONNECTED'
    ) AS connections,

    COUNT(DISTINCT f.lead_key) AS unique_leads,

    COUNT(DISTINCT f.lead_key) FILTER (
        WHERE f.event_type = 'CONTACTED'
    ) AS contacted_leads,

    COUNT(DISTINCT f.lead_key) FILTER (
        WHERE f.event_type = 'CONNECTED'
    ) AS connected_leads,

    ROUND(
        100.0 *
        COUNT(DISTINCT f.lead_key) FILTER (
            WHERE f.event_type = 'CONTACTED'
        )
        / NULLIF(COUNT(DISTINCT f.lead_key), 0),
        2
    ) AS contact_rate_pct,

    ROUND(
        100.0 *
        COUNT(DISTINCT f.lead_key) FILTER (
            WHERE f.event_type = 'CONNECTED'
        )
        /
        NULLIF(
            COUNT(DISTINCT f.lead_key) FILTER (
                WHERE f.event_type = 'CONTACTED'
            ),
            0
        ),
        2
    ) AS connection_rate_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE f.event_type = 'CONTACTED'
        )
        / NULLIF(a.daily_message_limit, 0),
        2
    ) AS message_capacity_utilisation_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE f.event_type = 'CONNECTED'
        )
        / NULLIF(a.daily_invite_limit, 0),
        2
    ) AS invite_capacity_utilisation_pct

FROM analytics.fact_outreach f

JOIN analytics.dim_date d
    ON f.date_key = d.date_key

JOIN analytics.dim_agent a
    ON f.agent_key = a.agent_key
    AND a.is_current = TRUE

LEFT JOIN analytics.dim_campaign c
    ON f.campaign_key = c.campaign_key

GROUP BY
    d.full_date,
    a.agent_name,
    a.account_age_tier,
    a.risk_classification,
    a.daily_invite_limit,
    a.daily_message_limit,
    c.campaign_name,
    c.target_segment,
    c.source;