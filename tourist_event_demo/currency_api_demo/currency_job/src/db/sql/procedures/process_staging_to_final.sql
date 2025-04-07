CREATE OR REPLACE PROCEDURE process_staging_to_final()
LANGUAGE plpgsql
AS $$
DECLARE
    v_final_count INTEGER;
BEGIN

    INSERT INTO currencies (
        currency_code, 
        currency_name, 
        is_active, 
        last_updated)
    SELECT 
        currency_code,
        currency_name,
        true as is_active,
        CURRENT_TIMESTAMP as last_updated
    FROM stg_currencies
    WHERE currency_code IS NOT NULL
    AND currency_name IS NOT NULL
    ON CONFLICT (currency_code) 
    DO UPDATE SET 
        currency_name = EXCLUDED.currency_name,
        last_updated = CURRENT_TIMESTAMP;

    GET DIAGNOSTICS v_final_count = ROW_COUNT;
    RAISE NOTICE 'Processed % rows in currencies table', v_final_count;

    INSERT INTO exchange_rates (
        rate_date, 
        source_currency, 
        target_currency, 
        rate, 
        is_live, 
        created_at, 
        updated_at
    )
    SELECT 
        rate_date,
        source_currency,
        target_currency,
        rate,
        is_live,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    FROM (
        SELECT 
            rate_date,
            source_currency,
            target_currency,
            rate,
            is_live,
            ROW_NUMBER() OVER (PARTITION BY rate_date, source_currency, target_currency ORDER BY processed_at DESC) as rn
        FROM stg_rates
    ) subquery_stg_rates
    WHERE rn = 1
    ON CONFLICT (rate_date, source_currency, target_currency) 
    DO UPDATE SET 
        rate = EXCLUDED.rate,
        updated_at = CURRENT_TIMESTAMP;

    GET DIAGNOSTICS v_final_count = ROW_COUNT;
    RAISE NOTICE 'Processed % rows in exchange_rates table', v_final_count;

    -- Final counts
    SELECT COUNT(*) INTO v_final_count FROM currencies;
    RAISE NOTICE 'Final currencies count: %', v_final_count;
    
    SELECT COUNT(*) INTO v_final_count FROM exchange_rates;
    RAISE NOTICE 'Final exchange_rates count: %', v_final_count;

    RAISE NOTICE 'Successfully processed staging data to final tables';
EXCEPTION WHEN OTHERS THEN

    RAISE NOTICE 'Error in process_staging_data: %', SQLERRM;
    RAISE;
END;
$$;