SELECT
  accountid,
  region,
  time_dt AS finding_time,
  REGEXP_EXTRACT(observables[1].value, 'arn:aws:secretsmanager:[^"]+') AS secret_arn,
  compliance.status AS compliance_status,
  unmapped['ProductFields.aws/config/ConfigRuleName'] AS config_rule_name,
  finding_info.created_time_dt AS config_evaluation_time
FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_sh_findings_2_0
WHERE
  finding_info.title = 'a-unused-secrets-check'
  AND compliance.status = 'FAILED';