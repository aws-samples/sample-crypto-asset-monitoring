SELECT 
  accountid,
  region,
  REGEXP_EXTRACT(observables[1].value, 'arn:aws:secretsmanager:[^"]+') AS secret_id,
  compliance.status AS rotation_enabled_check_status
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_sh_findings_2_0
WHERE 
  finding_info.title = 'secretsmanager-rotation-enabled-check'
  AND compliance.status = 'FAILED';