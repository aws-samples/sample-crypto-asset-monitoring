SELECT 
  cloud.account.uid AS aws_account, 
  cloud.region AS region, 
  observables[1].value AS cert_arn,
  compliance.status AS dns_validation_check
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_sh_findings_2_0
WHERE 
  finding_info.title = 'pca-dns-val-pending' AND 
  compliance.status = 'FAILED';