
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
    1 AS supply_partner,
    date,
    package_deal AS deal_name, 
    "N/A" AS deal_ID,
    sum(impressions) as impressions,
    sum((
        1 / currency.EUR * buyer_spend_euro
    ) * currency.INR ) AS revenue,
    sum((
        1 / currency.EUR * company_vendor_cost_in_euro
    ) * currency.INR) AS media_cost,
    0 as media_margin

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
    DATE = "[REPORT_DATE_FORMATED]"

GROUP BY 
    date,
    deal_name