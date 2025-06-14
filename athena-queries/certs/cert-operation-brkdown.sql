WITH base_events AS (
  SELECT 
    accountid,
    region,
    DATE(from_unixtime(CAST(time / 1000 AS BIGINT))) AS event_date,
    api.service.name AS service_name,
    api.operation AS operation_type
  FROM amazon_security_lake_glue_db_us_east_1.amazon_security_lake_table_us_east_1_cloud_trail_mgmt_2_0
  WHERE 
    (
      api.service.name = 'acm-pca.amazonaws.com'
      AND api.operation IN ('IssueCertificate', 'RevokeCertificate', 'CreateCertificateAuthority', 'UpdateCertificateAuthority', 'DeleteCertificateAuthority')
    )
    OR (
      api.service.name = 'acm.amazonaws.com'
      AND api.operation IN ('RequestCertificate', 'DeleteCertificate')
    )
    AND from_unixtime(CAST(time / 1000 AS BIGINT)) >= current_date - INTERVAL '30' DAY
)

SELECT 
  accountid,
  region,
  service_name,
  event_date,
  operation_type,
  COUNT(*) AS event_count
FROM base_events
GROUP BY 
  accountid, 
  region,
  service_name,
  event_date,
  operation_type
ORDER BY 
  event_date DESC,
  accountid,
  region;