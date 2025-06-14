SELECT 
  REGEXP_EXTRACT(api.request.data, '"secretId":"([^"]+)"') AS secret_id,
  region,
  accountid,
  COUNT(*) as get_count
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
WHERE 
  api.service.name = 'secretsmanager.amazonaws.com'
  AND api.operation = 'GetSecretValue'
  AND status = 'Success'
GROUP BY region, accountid, api.request.data
ORDER By get_count DESC
LIMIT 10;