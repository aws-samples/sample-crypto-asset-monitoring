SELECT 
  actor.session.issuer AS role_arn,
  api.operation AS operation,
  resources[1].uid AS key_id,
  accountid AS account_id,
  region,
  api.response.error AS error_code,
  COUNT(*) AS operation_count
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
WHERE 
  api.service.name = 'kms.amazonaws.com'
  AND api.response.error IN ('AccessDenied', 'UnauthorizedOperation', 'AccessDeniedException')
GROUP BY 
  api.operation,
  actor.session.issuer,
  resources[1].uid,
  accountid,
  region,
  api.response.error;