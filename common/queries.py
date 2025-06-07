# common/queries.py

STUDENT_ANALYTICS_QUERIES = {
    "count_by_major": """
        SELECT major, COUNT(*) AS total_students
        FROM students
        GROUP BY major
        ORDER BY total_students DESC;
    """,

    "average_gpa_by_major": """
        SELECT major, ROUND(AVG(gpa), 4) AS avg_gpa
        FROM students
        WHERE gpa IS NOT NULL
        GROUP BY major
        ORDER BY avg_gpa DESC
    """,

    "active_students_by_country": """
        SELECT country, COUNT(*) AS active_count
        FROM students
        WHERE is_active = true
        GROUP BY country
        ORDER BY active_count DESC
        LIMIT 100;
    """,

    "gpa_distribution_buckets": """
        SELECT 
            CASE 
                WHEN gpa >= 3.5 THEN 'High (3.5 - 4.0)'
                WHEN gpa >= 3.0 THEN 'Medium (3.0 - 3.49)'
                ELSE 'Low (< 3.0)'
            END AS gpa_range,
            COUNT(*) AS count
        FROM students
        WHERE gpa IS NOT NULL
        GROUP BY gpa_range
        LIMIT 100;
    """,

    "gender_ratio_per_major": """
        SELECT major, gender, COUNT(*) AS total
        FROM students
        GROUP BY major, gender
        ORDER BY major, total DESC
        LIMIT 100;
    """,

    "enrollments_over_time": """
        SELECT enrollment_year, COUNT(*) AS total_enrollments
        FROM students
        GROUP BY enrollment_year
        ORDER BY enrollment_year
        LIMIT 100;
    """,

    "top_majors_by_country": """
        SELECT country, major, COUNT(*) AS total
        FROM students
        GROUP BY country, major
        HAVING COUNT(*) > 20
        ORDER BY country, total DESC
        LIMIT 100;
    """,

    "recent_high_gpa_students": """
        SELECT student_id, full_name, major, gpa
        FROM students
        WHERE enrollment_year >= 2022 AND gpa >= 3.8
        ORDER BY gpa DESC
        LIMIT 100;
    """,

    "dropoff_by_enrollment": """
        SELECT
            enrollment_year,
            COUNT(CASE WHEN is_active = true THEN 1 END) AS active,
            COUNT(CASE WHEN is_active = false THEN 1 END) AS inactive
        FROM students
        GROUP BY enrollment_year
        ORDER BY enrollment_year
        LIMIT 100;
    """,

    "majors_with_low_gpa": """
        SELECT major, ROUND(AVG(gpa), 4) AS avg_gpa, COUNT(*) AS count
        FROM students
        WHERE gpa IS NOT NULL
        GROUP BY major
        ORDER BY avg_gpa ASC
        LIMIT 100;
    """
}
