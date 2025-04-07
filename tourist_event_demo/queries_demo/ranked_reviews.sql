WITH plan_reviews AS (
  SELECT 
    p.plan_id,
    p.plan_name,
    COUNT(r.review_id) as total_reviews,
    AVG(r.rating) as avg_rating,
    STRING_AGG(r.comment, ' | ') as all_comments
  FROM plan p
  INNER JOIN review r ON r.plan_id = p.plan_id
  WHERE p.status = 'ACTIVE'
    AND r.status = 'APPROVED'
  GROUP BY 1, 2
),
ranked_reviews AS (
  SELECT 
    plan_name,
    total_reviews,
    avg_rating,
    all_comments,
    RANK() OVER (ORDER BY avg_rating ASC) as worst_rank
  FROM plan_reviews
)
SELECT *
FROM ranked_reviews
WHERE worst_rank = 1;