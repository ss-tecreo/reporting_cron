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
    1 AS supply_partner,
    DATE_FORMAT(date,"%Y-%m-%d 07:30:00") AS date,
    DATE_FORMAT(date,"%H") as hour,
    package_deal AS deal_name, 
    "N/A" AS deal_ID,
    sum(impressions) as impressions,
    sum(( currency.INR / currency.EUR ) * buyer_spend_euro) AS revenue,
    sum(( currency.INR / currency.EUR ) * company_vendor_cost_in_euro) AS media_cost,
    currency.INR / currency.EUR * ( sum(buyer_spend_euro) - sum(company_vendor_cost_in_euro)) as media_margin,
    sum(buyer_spend_euro) AS revenue_BASE,
    sum(company_vendor_cost_in_euro) AS media_cost_BASE,
    sum(buyer_spend_euro) - sum(company_vendor_cost_in_euro) as media_margin_BASE
FROM
    tbl_equativ_[REPORT_DATE]
JOIN
    (
        SELECT
            EUR,
            INR
        FROM
            tbl_currency
        ORDER BY
            ID DESC
        LIMIT 1
    ) AS currency
WHERE
    DATE LIKE '%[REPORT_DATE_FORMATED]%'

GROUP BY 
    date,
    deal_name
