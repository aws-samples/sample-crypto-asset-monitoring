SELECT 
  accountid,
  region,
  actor.user.uid_alt AS principal_arn,
  COUNT(*) AS delete_count
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
WHERE 
  api.service.name = 'secretsmanager.amazonaws.com'
  AND api.operation = 'DeleteSecret'
  AND status = 'Success'
  AND time_dt >= current_date - interval '30' day
GROUP BY 
  accountid,
  region,
  actor.user.uid_alt
ORDER BY 
  delete_count DESC