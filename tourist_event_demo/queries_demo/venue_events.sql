WITH venue_events AS (
  SELECT 
    v.venue_name,
    COUNT(DISTINCT e.event_id) as total_events,
    COUNT(DISTINCT p.plan_id) as total_plans
  FROM venue v
  INNER JOIN plan p ON p.venue_id = v.venue_id
  INNER JOIN event e ON e.plan_id = p.plan_id
  WHERE p.status = 'ACTIVE'
  GROUP BY 1
)
SELECT 
  venue_name,
  total_events,
  total_plans,
  RANK() OVER (ORDER BY total_events DESC) as venue_rank
FROM venue_events
ORDER BY total_events DESC;