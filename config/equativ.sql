INSERT INTO tbl_aggregated (
        reporting_partner,
        date,
        demand_partner,
        deal_name,
        deal_ID,
        bundle_domain,
        interactions,
        biddingnt_interactions,
        impressions,
        revenue,
        publisher_name,
        seat_name,
        is_rewarded,
        company_vendor_cost,
        ecpm,buyer_spend,
        viewability_rate,
        auctions,
        video_complete,
        bids,
        bid_request_competing_deal,
        clicks,
        click_rate,
        winning_bids
    )
SELECT
    1 AS reporting_partner,
    date,
    "N/A" AS demand_partner,
    package_deal AS deal_name,
    "N/A" AS deal_ID,
    "N/A" AS bundle_domain,
    0 AS interactions,
    0 AS biddingnt_interactions,
    impressions,
    0 AS revenue,
    publisher_name,
    seat_name,
    is_rewarded,
    (
        1 / currency.EUR * company_vendor_cost_in_euro
    ) * currency.INR AS company_vendor_cost,
    (
        1 / currency.EUR * smart_gross_eCpm_euro
    ) * currency.INR AS ecpm,
    (
        1 / currency.EUR * buyer_spend_euro
    ) * currency.INR AS buyer_spend,
    viewability_rate,
    auctions,
    video_complete,
    bids,
    bid_request_competing_deal,
    clicks,
    click_rate,
    winning_bids
FROM
    tbl_equativ_[CURR_DT]
JOIN
    (
        SELECT
            EUR,
            INR
        FROM
            currency
        ORDER BY
            ID DESC
        LIMIT 1
    ) AS currency
WHERE
    DATE = "[CURR_DT] 00:00:00"
