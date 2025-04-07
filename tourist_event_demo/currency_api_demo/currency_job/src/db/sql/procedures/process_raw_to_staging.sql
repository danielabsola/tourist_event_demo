CREATE OR REPLACE PROCEDURE process_raw_to_staging()
LANGUAGE plpgsql
AS $$
DECLARE
    v_raw_count INTEGER;
    v_stg_count INTEGER;
BEGIN
    -- Log initial counts
    SELECT COUNT(*) INTO v_raw_count FROM raw_currency_list;
    RAISE NOTICE 'Initial raw_currency_list count: %', v_raw_count;
    
    SELECT COUNT(*) INTO v_raw_count FROM raw_live_rates;
    RAISE NOTICE 'Initial raw_live_rates count: %', v_raw_count;

    WITH latest_currencies AS (
        SELECT DISTINCT ON (curr.currency_code)
            curr.currency_code,
            curr.currency as currency_name,
            rcl.id as source_id
        FROM raw_currency_list rcl,
             json_each(rcl.raw_data) as curr(currency_code, currency)
        WHERE curr.currency_code IS NOT NULL 
        AND curr.currency IS NOT NULL
        ORDER BY curr.currency_code, rcl.id DESC
    )
    INSERT INTO stg_currencies (
        currency_code,
        currency_name,
        processed_at,
        source_id
    )
    SELECT 
        currency_code,
        currency_name,
        CURRENT_TIMESTAMP as processed_at,
        source_id
    FROM latest_currencies
    ON CONFLICT (currency_code) 
    DO UPDATE SET
        currency_name = EXCLUDED.currency_name,
        processed_at = EXCLUDED.processed_at,
        source_id = EXCLUDED.source_id; 
    
    GET DIAGNOSTICS v_stg_count = ROW_COUNT;
    RAISE NOTICE 'Inserted % rows into stg_currencies', v_stg_count;
    
    INSERT INTO stg_rates (
        rate_date,
        source_currency,
        target_currency,
        rate,
        is_live,
        processed_at,
        source_id
    )
    SELECT 
        to_timestamp((raw_data->>'timestamp')::bigint) as rate_date,
        raw_data->>'source' as source_currency,
        SUBSTRING(rate_pair.key, 4, 3) as target_currency,
        rate_pair.value::numeric(20,6) as rate,
        true as is_live,
        CURRENT_TIMESTAMP,
        rlr.id
    FROM raw_live_rates rlr,
         jsonb_each((raw_data->>'quotes')::jsonb) as rate_pair
    WHERE NOT EXISTS (
        SELECT 1 
        FROM stg_rates sr 
        WHERE sr.source_id = rlr.id
    );
    
    GET DIAGNOSTICS v_stg_count = ROW_COUNT;
    RAISE NOTICE 'Inserted % rows into stg_rates', v_stg_count;

    -- Final counts
    SELECT COUNT(*) INTO v_stg_count FROM stg_currencies;
    RAISE NOTICE 'Final stg_currencies count: %', v_stg_count;
    
    SELECT COUNT(*) INTO v_stg_count FROM stg_rates;
    RAISE NOTICE 'Final stg_rates count: %', v_stg_count;


    RAISE NOTICE 'Processing completed successfully';
EXCEPTION WHEN OTHERS THEN

    RAISE NOTICE 'Error in process_raw_to_staging: %', SQLERRM;
    RAISE;
END;
$$;