SELECT 
  api.operation AS operation,
  actor.session.issuer AS role_arn,
  resources[1].uid AS key_id,
  accountid AS account_id,
  region,
  COUNT(*) AS usage_count
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
WHERE 
  api.service.name = 'kms.amazonaws.com'
  AND api.operation IN ('Decrypt', 'Encrypt', 'GenerateDataKey')
  AND cardinality(resources) > 0
  AND resources[1].uid IS NOT NULL
  AND actor.session.issuer IS NOT NULL
  AND time_dt > now() - interval '30' day
GROUP BY api.operation, actor.session.issuer, resources[1].uid, accountid, region;