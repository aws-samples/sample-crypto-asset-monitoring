SELECT api.operation,
   accountid AS account_id,
   region,
   COUNT(*) AS usage_count
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
WHERE  api.service.name = 'secretsmanager.amazonaws.com' 
GROUP By api.operation, accountid, region;