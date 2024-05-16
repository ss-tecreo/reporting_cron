
INSERT INTO tbl_aggregated_daily(
    supply_partner,
    date,
    deal_name,
    deal_ID,
    impressions,
    revenue,
    media_cost,
    margin
)
SELECT
    2 AS supply_partner,
    DATE,
    deal_name,
    deal_ID,
    SUM(impressions) AS impressions,
    SUM(revenue * currency.INR) AS revenue,
    SUM((revenue * .88) * currency.INR) AS media_cost,
    SUM((revenue * .12) * currency.INR) AS media_margin
FROM
    tbl_smaato_[REPORT_DATE]
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
WHERE
    DATE = "[REPORT_DATE_FORMATED]"
GROUP BY
    DATE,
    deal_name