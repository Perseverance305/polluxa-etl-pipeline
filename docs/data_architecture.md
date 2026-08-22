\# Part 3 — Data Architecture \& Modeling



\## 1. Architecture Overview



The Polluxa LinkedIn Agent Aanalytics Platform uses a layered architecture consisting of:



1\. Source / ingestion layer

2\. Operational PostgreSQL layer

3\. Data quality and pipeline metadata layer

4\. Analytical star schema

5\. Power BI presentation layer



The architecture separates operational pipeline metadata from analytical reporting structures.



\---



\## 2. End-to-End Data Flow



LinkedIn / Polluxa Source

&#x20;       |

&#x20;       v

Raw Source Data

&#x20;       |

&#x20;       v

Extraction

&#x20;       |

&#x20;       v

Transformation

&#x20;       |

&#x20;       v

Validation

&#x20;       |

&#x20;       v

Data Quality Checks

&#x20;       |

&#x20;       +--------------------+

&#x20;       |                    |

&#x20;       v                    v

Valid Records          Failed Records

&#x20;       |                    |

&#x20;       v                    v

PostgreSQL             Dead-Letter /

Operational Layer      Failed Record Capture

&#x20;       |

&#x20;       +--------------------------+

&#x20;       |            |             |

&#x20;       v            v             v

&#x20;    leads     pipeline\_runs   dq\_results

&#x20;       |

&#x20;       v

Aanalytics Star Schema

&#x20;       |

&#x20;       +-------------------------------+

&#x20;       |               |               |

&#x20;       v               v               v

&#x20;   Dimensions       Fact Table      Date Dimension

&#x20;       |               |

&#x20;       +-------+-------+

&#x20;               |

&#x20;               v

&#x20;            Power BI

&#x20;               |

&#x20;               v

&#x20;       Executive Aanalytics



\---



\## 3. Operational Data Layer



\### public.leads



Purpose:

Stores the validated LinkedIn lead records loaded by the ingestion pipeline.



Grain:

One row per unique LinkedIn lead.



Primary key:

`lead\_id`



Business key:

`linkedin\_url`



Uniqueness:

`linkedin\_url` is protected by a unique constraint.



\---



\### public.pipeline\_runs



Purpose:

Stores metadata for each pipeline execution.



Grain:

One row per pipeline execution.



Primary key:

`run\_id`



Key metrics include:



\- rows\_extracted

\- rows\_valid

\- rows\_failed

\- rows\_loaded

\- status

\- error\_message

\- started\_at

\- completed\_at



\---



\### public.pipeline\_watermarks



Purpose:

Stores the latest successfully processed timestamp used for incremental extraction.



Grain:

One row per pipeline.



Primary key:

`pipeline\_name`



\---



\### public.dq\_results



Purpose:

Stores historical data-quality results for pipeline executions.



Grain:

One row per data-quality evaluation per pipeline run.



Primary key:

`dq\_result\_id`



Foreign key:

`run\_id -> pipeline\_runs.run\_id`



Quality dimensions:



\- completeness

\- uniqueness

\- validity

\- timeliness

\- referential integrity

\- overall score



\---



\# 4. Analytical Star Schema



The analytical layer is implemented under the `aanalytics` PostgreSQL schema.



The star schema consists of:



\- `dim\_lead`

\- `dim\_agent`

\- `dim\_date`

\- `dim\_campaign`

\- `fact\_outreach`



\---



\## 5. Fact Table



\### aanalytics.fact\_outreach



Grain:



\*\*One row per outreach event for one lead.\*\*



Examples of event types include:



\- INVITE\_SENT

\- INVITE\_ACCEPTED

\- MESSAGE\_SENT

\- REPLY\_RECEIVED



Primary key:



`outreach\_key`



Foreign keys:



\- `date\_key -> dim\_date.date\_key`

\- `lead\_key -> dim\_lead.lead\_key`

\- `agent\_key -> dim\_agent.agent\_key`

\- `campaign\_key -> dim\_campaign.campaign\_key`



The fact table is designed to support:



\- invite volume

\- acceptance rate

\- reply rate

\- conversion

\- agent utilisation

\- campaign performance

\- campaign ROI

\- risk analysis



The current fact table contains zero rows because the available source extract does not currently contain a complete outreach-event history.



No synthetic outreach events have been created.



\---



\# 6. Dimension Tables



\## aanalytics.dim\_lead



Grain:



\*\*One row per lead version.\*\*



Surrogate key:



`lead\_key`



Business key:



`lead\_id`



Important attributes:



\- linkedin\_url

\- name

\- job\_title

\- company

\- industry

\- location

\- source

\- prioritized

\- hot\_score



\### SCD Strategy



`dim\_lead` uses a Slowly Changing Dimension Type 2 approach.



Historical versions are preserved using:



\- `effective\_from`

\- `effective\_to`

\- `is\_current`



When a tracked lead attribute changes, a new dimension version can be created while retaining the previous version.



Current records are identified using:



`is\_current = TRUE`



\---



\## aanalytics.dim\_agent



Grain:



\*\*One row per agent/account version.\*\*



Surrogate key:



`agent\_key`



Business key:



`agent\_name`



Important attributes:



\- agent\_name

\- account\_age\_tier

\- risk\_classification

\- daily\_invite\_limit

\- daily\_message\_limit



\### SCD Strategy



`dim\_agent` uses a Slowly Changing Dimension Type 2 strategy.



Historical account configuration can therefore be preserved when account risk classification or capacity limits change.



The account-age and daily-limit attributes are intended to incorporate the configuration captured during Part 1.



\---



\## aanalytics.dim\_date



Grain:



\*\*One row per calendar date.\*\*



Primary key:



`date\_key`



Attributes include:



\- full\_date

\- day\_of\_month

\- month\_number

\- month\_name

\- quarter\_number

\- year\_number

\- week\_number



The date dimension supports consistent time-series analysis in Power BI.



\---



\## aanalytics.dim\_campaign



Grain:



\*\*One row per campaign.\*\*



Surrogate key:



`campaign\_key`



Attributes include:



\- campaign\_name

\- target\_segment

\- source

\- created\_at



The campaign dimension has been created to support campaign-level aanalytics when genuine campaign metadata becomes available.



No synthetic campaigns have been created.



\---



\# 7. Relationships



The fact table connects to the dimensions using foreign keys.



| Fact Column | Dimension | Dimension Key | Relationship |

|---|---|---|---|

| fact\_outreach.date\_key | dim\_date | date\_key | Many-to-one |

| fact\_outreach.lead\_key | dim\_lead | lead\_key | Many-to-one |

| fact\_outreach.agent\_key | dim\_agent | agent\_key | Many-to-one |

| fact\_outreach.campaign\_key | dim\_campaign | campaign\_key | Many-to-one |



The resulting structure is a conventional star schema in which the fact table is at the centre and descriptive dimensions surround it.



\---



\# 8. Surrogate Keys



Surrogate keys are implemented using PostgreSQL `BIGSERIAL` keys.



Examples:



\- `dim\_lead.lead\_key`

\- `dim\_agent.agent\_key`

\- `dim\_campaign.campaign\_key`

\- `fact\_outreach.outreach\_key`



The surrogate keys decouple the analytical model from source-system identifiers and allow historical dimension versions to coexist.



\---



\# 9. Current Model Population



At the time of implementation:



| Table | Records |

|---|---:|

| dim\_lead | 10 |

| dim\_agent | 1 |

| dim\_date | 365 |

| dim\_campaign | 0 |

| fact\_outreach | 0 |



The operational database contains 10 validated lead records.



The source extract currently contains lead-level information but does not contain a complete event-level outreach history. Therefore, campaign and outreach-event tables remain structurally ready but unpopulated.



\---



\# 10. Design Rationale



The analytical model separates descriptive attributes from measurable business events.



The fact table is intentionally event-grained because outreach aanalytics requires the ability to distinguish between:



\- invitations

\- accepted connections

\- messages

\- replies



This allows measures such as acceptance rate and reply rate to be calculated from events rather than relying on static lead status fields.



The dimensional model also allows analysis by:



\- agent

\- campaign

\- target segment

\- lead

\- date



while preserving historical changes through SCD Type 2 dimensions.



\---



\# 11. Power BI Consumption Layer



Power BI should consume the analytical schema rather than relying exclusively on raw operational tables.



Recommended relationships:



dim\_date

&#x20;   |

&#x20;   v

fact\_outreach

&#x20;   ^

&#x20;   |

dim\_lead



dim\_agent ----> fact\_outreach <---- dim\_campaign



Relationships should generally be configured as:



\- One-to-many from dimensions to fact

\- Single-direction filtering

\- Explicit DAX measures

\- No unnecessary bidirectional relationships



\---



\# 12. Known Data Limitations



The current source extract contains 10 lead records.



The current lead data shows:



\- 10 connected leads

\- 0 invite timestamps

\- 10 connected timestamps

\- 10 last-contacted timestamps



Therefore, invite, reply, conversion, throughput, campaign ROI and anomaly analysis cannot be validly calculated from the current extract alone.



The analytical schema has been designed to support those measures once genuine outreach-event data becomes available.



No fabricated performance data has been introduced.



\---



\# 13. Assessment Mapping



This architecture addresses Part 3 requirements:



| Requirement | Implementation |

|---|---|

| Star schema | Aanalytics fact and dimension model |

| Declared grain | Documented for every analytical table |

| Surrogate keys | BIGSERIAL analytical keys |

| Relationships | Foreign keys from fact to dimensions |

| SCD strategy | Type 2 for lead and agent dimensions |

| End-to-end data flow | Documented above |

| Data dictionary | Table and column definitions documented |

| Presentation layer | Power BI consumes analytical model |

# 14. Data Dictionary

## 14.1 aanalytics.dim_agent

| Column | Type | Key | Definition |
|---|---|---|---|
| agent_key | BIGINT | PK | Surrogate identifier for an agent dimension record. |
| agent_name | TEXT | Business Key | Name of the LinkedIn automation agent/account. |
| account_age_tier | TEXT | Attribute | Account-age category declared during Part 1 configuration. |
| risk_classification | TEXT | Attribute | Risk category associated with the account-age tier. |
| daily_invite_limit | INTEGER | Attribute | Maximum recommended/allowed daily invitation capacity for the account tier. |
| daily_message_limit | INTEGER | Attribute | Maximum recommended/allowed daily message capacity for the account tier. |
| effective_from | TIMESTAMP | SCD | Start timestamp for the validity of this dimension version. |
| effective_to | TIMESTAMP | SCD | End timestamp for the validity of this dimension version. NULL indicates the current version. |
| is_current | BOOLEAN | SCD | Indicates whether the dimension record is the current version. |

### Grain

One row per agent/account version.

---

## 14.2 aanalytics.dim_campaign

| Column | Type | Key | Definition |
|---|---|---|---|
| campaign_key | BIGINT | PK | Surrogate identifier for a campaign. |
| campaign_name | TEXT | Business Identifier | Human-readable campaign name. |
| target_segment | TEXT | Attribute | Target audience or segment associated with the campaign. |
| source | TEXT | Attribute | Origin/source associated with the campaign. |
| created_at | TIMESTAMP | Attribute | Timestamp when the campaign record was created. |

### Grain

One row per campaign.

---

## 14.3 aanalytics.dim_date

| Column | Type | Key | Definition |
|---|---|---|---|
| date_key | INTEGER | PK | Integer representation of the calendar date used by the fact table. |
| full_date | DATE | Attribute | Complete calendar date. |
| day_of_month | INTEGER | Attribute | Numeric day within the month. |
| month_number | INTEGER | Attribute | Numeric month from 1 to 12. |
| month_name | TEXT | Attribute | Human-readable month name. |
| quarter_number | INTEGER | Attribute | Calendar quarter from 1 to 4. |
| year_number | INTEGER | Attribute | Calendar year. |
| week_number | INTEGER | Attribute | Calendar week number. |

### Grain

One row per calendar date.

---

## 14.4 aanalytics.dim_lead

| Column | Type | Key | Definition |
|---|---|---|---|
| lead_key | BIGINT | PK | Surrogate identifier for a lead dimension record. |
| lead_id | BIGINT | Business Key | Operational identifier of the lead. |
| linkedin_url | TEXT | Business Attribute | Unique LinkedIn profile URL used to identify the source lead. |
| name | TEXT | Attribute | Full name of the lead. |
| job_title | TEXT | Attribute | Job title associated with the lead. |
| company | TEXT | Attribute | Company associated with the lead. |
| industry | TEXT | Attribute | Industry associated with the lead. |
| location | TEXT | Attribute | Geographic location associated with the lead. |
| source | TEXT | Attribute | Source through which the lead entered the platform. |
| prioritized | BOOLEAN | Attribute | Indicates whether the lead was marked as prioritised. |
| hot_score | DOUBLE PRECISION | Measure/Attribute | Lead-level score indicating relative lead priority or engagement potential. |
| effective_from | TIMESTAMP | SCD | Start timestamp for the validity of this lead dimension version. |
| effective_to | TIMESTAMP | SCD | End timestamp for the validity of this lead dimension version. NULL indicates the current version. |
| is_current | BOOLEAN | SCD | Indicates whether the dimension record is the current version. |

### Grain

One row per lead version.

---

## 14.5 aanalytics.fact_outreach

| Column | Type | Key | Definition |
|---|---|---|---|
| outreach_key | BIGINT | PK | Surrogate identifier for an outreach event. |
| date_key | INTEGER | FK | Links the event to the calendar date dimension. |
| lead_key | BIGINT | FK | Links the event to the lead dimension. |
| agent_key | BIGINT | FK | Links the event to the agent dimension. |
| campaign_key | BIGINT | FK | Links the event to the campaign dimension when campaign attribution exists. |
| event_type | TEXT | Degenerate Attribute | Type of outreach event, such as invite sent, invite accepted, message sent, or reply received. |
| event_timestamp | TIMESTAMP | Event Time | Timestamp at which the outreach event occurred. |
| outcome | TEXT | Attribute | Result or outcome associated with the outreach event. |

### Grain

One row per outreach event for one lead.

---

# 15. Analytical Measures Supported

The star schema is designed to support explicit analytical measures including:

### Invites Sent

**Aggregation: COUNT of outreach events where `event_type = 'INVITE_SENT'`.**

### Acceptance Rate

**Aggregation: accepted invitations divided by invitations sent.**

### Reply Rate

**Aggregation: replies divided by relevant messaging/outreach population.**

### Conversion Rate

**Aggregation: successful conversions divided by the defined outreach population.**

### Throughput

**Aggregation: outreach events per agent per day.**

### Capacity Utilisation

**Aggregation: actual daily activity divided by the configured daily capacity limit.**

### Campaign Performance

**Aggregation: outreach outcomes grouped by campaign and target segment.**

### Agent Performance

**Aggregation: outreach outcomes grouped by agent.**

### Risk / Anomaly Score

Calculated analytical measure based on deviations in observed outreach outcomes from the expected baseline.

---

# 16. Key Constraints

The following constraints are applied by the analytical model:

- Fact records must reference valid date, lead and agent dimension records.
- Campaign attribution is optional because campaign information may not be present in every source record.
- Lead and agent dimensions preserve historical versions.
- Source-system identifiers are not used as analytical primary keys.
- Outreach events are not artificially generated when event-level source data is unavailable.

---

# 17. Current Data Availability

The current source extract contains 10 lead records.

Current populated lead-level events:

- Connected: 10
- Last contacted: 10
- Invite sent: 0

The absence of invite timestamps means that invite-volume and acceptance-rate metrics cannot currently be calculated from the source extract without additional event-level data.

Similarly, reply and conversion events are not present in the current source extract.

Therefore, these metrics must either be populated from genuine Polluxa outreach-event data or explicitly marked as unavailable.

No synthetic performance events should be introduced solely to populate the dashboard.


---

# 17. Current Warehouse Implementation Status

The analytical warehouse has now been populated and validated using the available source data.

## Current Record Counts

| Table | Current Rows |
|---|---:|
| public.leads | 10 |
| public.pipeline_runs | 19 |
| public.dq_results | 7 |
| public.pipeline_watermarks | 2 |
| analytics.dim_lead | 10 |
| analytics.dim_agent | 1 |
| analytics.dim_date | 365 |
| analytics.dim_campaign | 1 |
| analytics.fact_outreach | 20 |

## Current Agent Configuration

The active agent is Percy Maphanga.

| Attribute | Value |
|---|---|
| Account age tier | 1+ Year |
| Risk classification | Minimal Risk |
| Daily invite limit | 30 |
| Daily message limit | 60 |
| Current status | Active |

## Current Campaign

The populated campaign dimension contains:

- Campaign: Build Search
- Target segment: Data & Analytics Professionals
- Source: Build Search

## Current Outreach Events

The current fact table contains 20 validated outreach events:

| Event Type | Events | Unique Leads |
|---|---:|---:|
| CONTACTED | 10 | 10 |
| CONNECTED | 10 | 10 |

All 20 events are attributed to the Build Search campaign and Percy Maphanga.

## Current Analytical Results

Based on the currently available outreach events:

- Total leads: 10
- Leads contacted: 10
- Leads connected: 10
- Contact rate: 100%
- Connection rate among contacted leads: 100%
- Message capacity utilisation: 16.67%
- Invite capacity utilisation: 33.33%

These metrics represent the current populated analytical dataset and should be presented as the observed results for the available source records.

## Data Availability Limitation

The source dataset does not provide sufficient event-level information to calculate every theoretically supported outreach metric.

In particular, the current source does not provide reliable event-level records for:

- invitation acceptance independent of connection events
- replies
- conversions
- revenue or campaign ROI
- historical outreach activity beyond the available timestamps

Therefore, these measures must not be fabricated or inferred as actual business outcomes. They should be presented as unavailable or not currently measurable in the Power BI reporting layer.

The analytical model remains extensible so that these measures can be populated when the source system provides the required event-level data.

## Power BI Reporting Layer

Power BI is intended to consume the populated analytics star schema rather than the operational public tables.

The current reporting layer can therefore support:

- Executive outreach KPIs
- Agent performance
- Campaign performance
- Contact and connection rates
- Capacity utilisation
- Agent risk classification
- Lead and campaign filtering
- Data availability and limitation reporting

The Power BI layer should distinguish between observed metrics supported by the current fact data and metrics that cannot currently be calculated because the required source events are unavailable.




