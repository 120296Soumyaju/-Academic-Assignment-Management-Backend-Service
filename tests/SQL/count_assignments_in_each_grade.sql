-- Write query to get count of assignments in each grade

SELECT grade, COUNT(*) as assignment_count
FROM assignments
WHERE state = 'GRADED'
GROUP BY grade;

