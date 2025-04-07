WITH plan_normalized_prices AS (
  SELECT 
    c.category_name,
    p.plan_name,
    r.type as price_type,
    CASE 
      WHEN r.type = 'SINGLE' THEN r.import
      ELSE r.import / r.quantity
    END as price_per_person
  FROM category_main c 
  LEFT JOIN category_child cc 
    ON c.category_main_id = cc.category_main_id
  INNER JOIN plan p 
    ON p.category_main_id = c.category_main_id
  INNER JOIN prices r
    ON r.plan_id = p.plan_id
  WHERE p.status = 'ACTIVE'
),
category_prices AS (
  SELECT 
    category_name,
    MIN(CASE WHEN price_type = 'SINGLE' THEN price_per_person END) as min_single_price,
    MIN(CASE WHEN price_type != 'SINGLE' THEN price_per_person END) as min_group_price_per_person
  FROM plan_normalized_prices
  GROUP BY 1
)
SELECT 
  category_name,
  min_single_price,
  min_group_price_per_person,
  RANK() OVER (ORDER BY LEAST(min_single_price, min_group_price_per_person) ASC) as price_rank
FROM category_prices
ORDER BY price_rank;