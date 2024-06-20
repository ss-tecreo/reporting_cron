INSERT INTO tbl_aggregated_daily(
    supply_partner,
    DATE,
    hour,
    deal_name,
    deal_ID,
    impressions,
    revenue,
    media_cost,
    margin,
    revenue_BASE,
    media_cost_BASE,
    margin_BASE
)
SELECT
    3 AS supply_partner,
    DATE_FORMAT(date,"%Y-%m-%d 05:32:00") AS date,
    DATE_FORMAT(date,"%H") as hour,
    deal_name,
    "" as deal_ID,
    SUM(impressions) AS impressions,
    SUM(revenue * currency.USD_INR) AS revenue,
    SUM(media_cost * currency.USD_INR) AS media_cost,
    SUM(((revenue*.93) - media_cost*1.20) * currency.USD_INR) AS margin,
    SUM(revenue) AS revenue_BASE,
    SUM(media_cost) AS media_cost_BASE,
    SUM((revenue*.93) - media_cost*1.20) AS margin_BASE
FROM
    tbl_loopme_[REPORT_DATE]
JOIN(
    SELECT
        EUR_INR,
        USD_INR
    FROM
        tbl_currency
    ORDER BY
        ID
    DESC
LIMIT 1
) AS currency
WHERE
    DATE LIKE '%[REPORT_DATE_FORMATED]%'
    AND revenue > 0
GROUP BY
    date,
    deal_name;
