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
        ecpm,
        buyer_spend,
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
        3 AS reporting_partner,
        date,
        demand_partner,
        deal_name,
        deal_ID,
        bundle_domain,
        interactions,
        biddingnt_interactions,
        impressions,
        revenue,
        'N/A' AS publisher_name,
        'N/A' AS seat_name,
        0 AS is_rewarded,
        0 AS company_vendor_cost,
        0 AS ecpm,
        0 AS buyer_spend,
        0 AS viewability_rate,
        0 AS auctions,
        0 AS video_complete,
        0 AS bids,
        0 AS bid_request_competing_deal,
        0 AS clicks,
        0 AS click_rate,
        0 AS winning_bids
    FROM
        tbl_smaato_amazon_20240508
    WHERE
        DATE = '2024-05-08 00:00:00'



