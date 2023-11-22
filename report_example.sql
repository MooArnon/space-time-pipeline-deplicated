SELECT *
FROM (
	SELECT 
		prediction_signnal,
		CASE
			WHEN percentile > 0.9 THEN 'high-confidence'
			WHEN percentile BETWEEN 0.7 AND 0.9 THEN 'confidence'
			ELSE 'low-confidence'
		END AS confidence,
		MIN(CASE
            WHEN percentile >= 0.9 THEN prediction_diff_ratio
            WHEN percentile > 0.7 AND percentile < 0.9 THEN prediction_diff_ratio
            ELSE 'lower-than-those-above'
        END) AS confidence_value__more_than,
	    COUNT(*) AS total,
	    SUM(CASE WHEN correctness = 'correct' THEN 1 ELSE 0 END) AS correct,
	    SUM(CASE WHEN correctness = 'wrong' THEN 1 ELSE 0 END) AS wrong,
	    SUM(CASE WHEN correctness = 'correct' THEN 1 ELSE 0 END) / COUNT(*) AS accuracy
	FROM (
		SELECT 
			*,
			CASE 
				WHEN prediction_diff < 0 THEN 'sell'
				WHEN prediction_diff > 0 THEN 'buy'
				ELSE 'nope'
			END AS prediction_signnal,
			percent_rank() OVER (ORDER BY ABS(prediction_diff)) percentile,
			100*prediction_diff/price_scraped_t0 as prediction_diff_ratio
		FROM predict_summary
		WHERE correctness != 'wait_rediction'
			AND insert_datetime >= DATE_SUB(CONVERT_TZ(CURRENT_TIMESTAMP, 'UTC', '+7:00'), INTERVAL 100 HOUR)
			AND actual_diff IS NOT NULL
		ORDER  BY insert_datetime DESC 
	) as a
	GROUP BY prediction_signnal, confidence
) as b
ORDER BY prediction_signnal, 
	CASE WHEN confidence = 'high-confidence' THEN 1
		 WHEN confidence = 'confidence' THEN 2
		 WHEN confidence = 'low-confidence' THEN 3
	END
;
