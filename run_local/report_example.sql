SELECT
    prediction_signal,
    CASE
        WHEN percentile >= 0.85 THEN 'high-confidence'
        WHEN percentile < 0.85 AND percentile >= 0.70 THEN 'confidence'
        ELSE 'distrust'
    END AS confidence,
    MIN(diff_percent) AS floor_confidence_value,
    (COUNT(CASE WHEN correctness = 'correct' THEN 1 END) * 100.0) / COUNT(*) AS correct_percentage,
    COUNT(1) AS predicted_number
FROM (
    SELECT
        prediction_signal,
        100 * prediction_diff / price_predicted_t1 AS diff_percent,
        PERCENT_RANK() OVER (PARTITION BY prediction_signal ORDER BY ABS(100 * prediction_diff / price_predicted_t1)) AS percentile,
        correctness
    FROM
        predict_summary_96
    WHERE
        correctness != 'wait_prediction'
) AS subquery
GROUP BY
    1, 2
ORDER BY
    prediction_signal,
    CASE
        WHEN confidence = 'high-confidence' THEN 1
        WHEN confidence = 'confidence' THEN 2
        WHEN confidence = 'distrust' THEN 3
    END
;
