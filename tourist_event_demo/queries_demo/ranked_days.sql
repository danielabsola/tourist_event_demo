WITH plans_by_day AS (
  SELECT 
    c.city_name as city, 
    TO_CHAR(p.dt_start, 'Day') as day_of_week,
    COUNT(DISTINCT p.plan_id) as plans_count
  FROM city c 
  INNER JOIN venue v ON c.city_id = v.city_id
  INNER JOIN plan p ON p.place_id = v.place_id
  WHERE p.status = 'ACTIVE'
  GROUP BY 1, 2
),
ranked_days AS (
  SELECT 
    city,
    day_of_week,
    plans_count,
    RANK() OVER (PARTITION BY city ORDER BY plans_count DESC) as day_rank  -- Rank days within each city
  FROM plans_by_day
)
SELECT 
  city,
  day_of_week,
  plans_count
FROM ranked_days
WHERE day_rank = 1;