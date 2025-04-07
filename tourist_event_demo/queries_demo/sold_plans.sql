WITH sold_plans AS (
  SELECT 
    c.country_name, 
    COUNT(DISTINCT p.plan_id) as active_plans,
    SUM(t.quantity) as total_tickets_sold
  FROM countries c 
  INNER JOIN city y 
    ON c.country_id = y.country_id
  INNER JOIN venue v 
    ON y.city_id = v.city_id
  INNER JOIN event t 
    ON t.venue_id = v.venue_id
  INNER JOIN plan p 
    ON p.plan_id = t.plan_id
  INNER JOIN ticket t 
    ON t.plan_id = p.plan_id
  WHERE p.status = 'ACTIVE'
    AND t.status = 'PAID'
    -- to filter by date range if needed
    -- AND t.created_at >= DATEADD(month, -1, CURRENT_DATE())
  GROUP BY 1
  ORDER BY total_tickets_sold DESC
)
SELECT 
  country_name,
  total_tickets_sold,
  DENSE_RANK() OVER (ORDER BY total_tickets_sold DESC) as country_rank
FROM sold_plans;