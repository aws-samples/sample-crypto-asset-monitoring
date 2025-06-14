SELECT 
  actor.session.issuer AS role_arn,  -- Full IAM role ARN (AssumedRole or IAMUser ARN)
  actor.user.uid_alt AS principal_id,  -- Session name or username
  actor.user.type AS principal_type,
  COUNT(*) AS access_denied_count,
  region,
  accountid
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
WHERE 
  api.service.name = 'secretsmanager.amazonaws.com'
  AND api.response.error = 'AccessDenied'
GROUP BY 
  actor.session.issuer,
  actor.user.uid_alt,
  actor.user.type,
  region,
  accountid
ORDER BY 
  access_denied_count DESC
LIMIT 20;