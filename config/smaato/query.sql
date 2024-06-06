INSERT INTO tbl_aggregated_daily(
    supply_partner,
    date,
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
    2 AS supply_partner,
    DATE_FORMAT(date,"%Y-%m-%d 10:30:00") AS date,
    DATE_FORMAT(date,"%H") as hour,
    deal_name,
    "" as deal_ID,
    SUM(impressions) AS impressions,
    SUM(revenue * currency.USD_INR) AS revenue,
    SUM((revenue * .88) * currency.USD_INR) AS media_cost,
    SUM((revenue * .12) * currency.USD_INR) AS media_margin,
    SUM(revenue) AS revenue_BASE,
    SUM(revenue * .88) AS media_cost_BASE,
    SUM(revenue * .12) AS media_margin_BASE

FROM
    tbl_smaato_[REPORT_DATE]
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
GROUP BY
    DATE,
    deal_name
