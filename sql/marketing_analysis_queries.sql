-- Segment performance
SELECT
  customer_segment,
  COUNT(*) AS customers,
  AVG(Response) AS response_rate,
  AVG(customer_value) AS avg_customer_value,
  SUM(customer_value) AS total_customer_value,
  AVG(Recency) AS avg_recency
FROM customers_marketing_scored
GROUP BY customer_segment
ORDER BY avg_customer_value DESC;

-- Campaign response by income band
SELECT
  income_band,
  COUNT(*) AS customers,
  AVG(Response) AS response_rate,
  AVG(customer_value) AS avg_customer_value
FROM customers_marketing_scored
GROUP BY income_band
ORDER BY response_rate DESC;

-- Product category spend
SELECT 'Wine' AS product_category, SUM(MntWines) AS total_spend FROM customers_marketing_scored
UNION ALL
SELECT 'Meat', SUM(MntMeatProducts) FROM customers_marketing_scored
UNION ALL
SELECT 'Gold', SUM(MntGoldProds) FROM customers_marketing_scored
UNION ALL
SELECT 'Fish', SUM(MntFishProducts) FROM customers_marketing_scored
UNION ALL
SELECT 'Fruits', SUM(MntFruits) FROM customers_marketing_scored
UNION ALL
SELECT 'Sweets', SUM(MntSweetProducts) FROM customers_marketing_scored;

-- Targeting recommendation queue
SELECT
  ID,
  customer_segment,
  Income,
  customer_value,
  Recency,
  Response,
  targeting_action
FROM customers_marketing_scored
WHERE targeting_action <> 'Monitor'
ORDER BY customer_value DESC, Recency ASC;

