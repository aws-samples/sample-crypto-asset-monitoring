SELECT
  sl.accountid AS account_id,
  region,
  COUNT(DISTINCT regexp_extract(obs.value, 'arn:aws:kms:[^:]+:[0-9]+:key/[a-z0-9-]+')) AS non_compliant_kms_keys
FROM
  amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_sh_findings_2_0 sl,
  UNNEST(sl.observables) AS t(obs)
WHERE
  element_at(sl.unmapped, 'ProductFields.aws/config/ConfigRuleName') = 'cmk-backing-key-rotation-enabled'
  AND element_at(sl.unmapped, 'Compliance.Status') = 'FAILED'
  AND obs.value LIKE '%arn:aws:kms:%'
GROUP BY
  sl.accountid, region
ORDER BY
  non_compliant_kms_keys DESC;