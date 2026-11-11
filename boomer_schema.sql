-- BOOMER Financial Command Centre — PostgreSQL schema
-- Run with: psql "$DATABASE_URL" -f boomer_schema.sql
CREATE TABLE IF NOT EXISTS boomer_model_runs (
    run_id VARCHAR(36) PRIMARY KEY,
    model_version VARCHAR(30) NOT NULL,
    scenario VARCHAR(40) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    assumptions JSONB NOT NULL,
    kpis JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS boomer_products (
    product_id BIGSERIAL PRIMARY KEY,
    product_name TEXT UNIQUE NOT NULL,
    product_data JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS boomer_period_financials (
    run_id VARCHAR(36) NOT NULL REFERENCES boomer_model_runs(run_id) ON DELETE CASCADE,
    period_label TEXT NOT NULL,
    frequency TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    amount NUMERIC(20,2) NOT NULL,
    PRIMARY KEY (run_id, period_label, frequency, metric_name)
);

CREATE TABLE IF NOT EXISTS boomer_historical_financials (
    record_id BIGSERIAL PRIMARY KEY,
    period_label TEXT NOT NULL,
    frequency TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    amount NUMERIC(20,2) NOT NULL,
    source_file TEXT,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_boomer_runs_created_at ON boomer_model_runs(created_at);
CREATE INDEX IF NOT EXISTS idx_boomer_period_metric ON boomer_period_financials(metric_name, period_label);

-- BI views
CREATE OR REPLACE VIEW vw_boomer_financials AS
SELECT r.run_id, r.model_version, r.scenario, r.created_at,
       p.period_label, p.frequency, p.metric_name, p.amount
FROM boomer_model_runs r
JOIN boomer_period_financials p ON p.run_id = r.run_id;

CREATE OR REPLACE VIEW vw_boomer_latest_run AS
SELECT r.run_id, r.model_version, r.scenario, r.created_at,
       r.assumptions, r.kpis
FROM boomer_model_runs r
ORDER BY r.created_at DESC
LIMIT 1;

CREATE OR REPLACE VIEW vw_boomer_product_master AS
SELECT product_id, product_name, product_data, updated_at
FROM boomer_products;
