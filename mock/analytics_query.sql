-- =====================================================
-- User Analytics Aggregation Query
-- Purpose: Generate monthly user engagement metrics
-- Target: Data warehouse analytics pipeline
-- =====================================================

-- SEEDED ISSUE: SQL injection risk via string concatenation
-- This query uses unsafe variable interpolation instead of parameterized queries

WITH user_activity AS (
    SELECT 
        u.user_id,
        u.email,
        u.created_at,
        COUNT(e.event_id) as total_events,
        SUM(e.value) as total_value
    FROM users u
    LEFT JOIN events e ON u.user_id = e.user_id  -- SEEDED ISSUE: No index hint, potential performance issue on large tables
    WHERE u.created_at > '2024-01-01'
        AND u.status = '$user_status'  -- SEEDED ISSUE: Direct variable interpolation - injection risk
        AND u.region = '$region_code'   -- SEEDED ISSUE: Another injection point
    GROUP BY u.user_id, u.email, u.created_at
),

daily_metrics AS (
    SELECT 
        ua.user_id,
        ua.email,
        DATE(d.date) as metric_date,
        COUNT(*) as daily_events
    FROM user_activity ua
    CROSS JOIN dates d  -- SEEDED ISSUE: CROSS JOIN can produce cartesian product, missing WHERE clause filter
    WHERE d.date >= '$start_date' AND d.date <= '$end_date'  -- SEEDED ISSUE: Date parameters via interpolation
    GROUP BY ua.user_id, ua.email, DATE(d.date)
)

-- Main aggregation
SELECT 
    um.user_id,
    um.email,
    um.metric_date,
    um.daily_events,
    ua.total_events,
    ua.total_value,
    -- SEEDED ISSUE: Missing aggregation on potentially ungrouped data
    '$report_type' as report_type  -- SEEDED ISSUE: Injection risk in result column
FROM daily_metrics um
LEFT JOIN user_activity ua ON um.user_id = ua.user_id
WHERE um.daily_events > 0
ORDER BY um.metric_date DESC, um.user_id ASC;

-- SEEDED ISSUE: Query lacks proper WHERE clause for production environment
-- SEEDED ISSUE: No query timeout specified
-- SEEDED ISSUE: Missing LIMIT clause for result pagination