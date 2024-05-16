INSERT INTO tbl_aggregated_daily(
    supply_partner,
    DATE,
    deal_name,
    deal_ID,
    impressions,
    revenue,
    media_cost,
    margin
)
SELECT
    3 AS supply_partner,
    "[REPORT_DATE_FORMATED]" AS DATE,
    deal_name,
    deal_ID,
    SUM(impressions) AS impressions,
    SUM(revenue * currency.INR ) AS revenue,
    SUM(media_cost * currency.INR) AS media_cost,
    SUM(((revenue*.7) - media_cost - (media_cost*.20)) * currency.INR) AS margin
FROM
    tbl_loopme_[REPORT_DATE]
JOIN(
    SELECT
        EUR,
        INR
    FROM
        tbl_currency
    ORDER BY
        ID
    DESC
LIMIT 1
) AS currency
GROUP BY
    deal_name;