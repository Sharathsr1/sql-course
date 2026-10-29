# ── Interview Questions & Answers per lesson slug ─────────────────────────────
# Each entry: { "q": "...", "a": "...", "level": "Fresher|Junior|Mid|Senior" }
# Oracle and MySQL syntax differences are shown inline in answers.

INTERVIEW_QA = {

    # ── What is SQL ────────────────────────────────────────────────────────────
    "what-is-sql": [
        {
            "level": "Fresher",
            "q": "What is SQL and why is it used?",
            "a": "SQL (Structured Query Language) is used to communicate with relational databases. It lets you create, read, update, and delete data stored in tables. Almost every application that stores data uses SQL behind the scenes — banking systems, e-commerce, social media all rely on it."
        },
        {
            "level": "Fresher",
            "q": "What are the different types of SQL commands?",
            "a": """SQL commands are grouped into 5 categories:
<ul>
<li><b>DDL</b> (Data Definition Language) — CREATE, ALTER, DROP, TRUNCATE</li>
<li><b>DML</b> (Data Manipulation Language) — SELECT, INSERT, UPDATE, DELETE</li>
<li><b>DCL</b> (Data Control Language) — GRANT, REVOKE</li>
<li><b>TCL</b> (Transaction Control Language) — COMMIT, ROLLBACK, SAVEPOINT</li>
<li><b>DQL</b> (Data Query Language) — SELECT (sometimes listed separately)</li>
</ul>"""
        },
        {
            "level": "Fresher",
            "q": "What is the difference between a database and a table?",
            "a": "A <b>database</b> is a container that holds multiple tables (and other objects). A <b>table</b> is a structured set of data organised into rows and columns — like a spreadsheet inside the database."
        },
        {
            "level": "Fresher",
            "q": "What is a primary key?",
            "a": "A primary key is a column (or combination of columns) that <b>uniquely identifies each row</b> in a table. It cannot be NULL and cannot have duplicate values. Every table should have one."
        },
        {
            "level": "Junior",
            "q": "What is the difference between CHAR and VARCHAR?",
            "a": """<ul>
<li><b>CHAR(n)</b> — fixed-length. Always stores exactly n characters, pads with spaces. Faster for fixed-size data like country codes.</li>
<li><b>VARCHAR(n)</b> — variable-length. Stores only as many characters as needed (up to n). More storage-efficient for variable text.</li>
</ul>
<b>Example:</b><br>
CHAR(10) storing 'Hi' → 'Hi        ' (8 spaces added)<br>
VARCHAR(10) storing 'Hi' → 'Hi' (only 2 bytes used)"""
        },
        {
            "level": "Junior",
            "q": "What is the difference between SQL and NoSQL databases?",
            "a": """<table class='ops-table'><tr><th></th><th>SQL (Relational)</th><th>NoSQL</th></tr>
<tr><td>Structure</td><td>Tables with fixed schema</td><td>Documents, key-value, graphs</td></tr>
<tr><td>Query</td><td>SQL</td><td>Varies (MongoDB, etc.)</td></tr>
<tr><td>Scaling</td><td>Vertical</td><td>Horizontal</td></tr>
<tr><td>Examples</td><td>Oracle, MySQL, PostgreSQL</td><td>MongoDB, Redis, Cassandra</td></tr>
</table>"""
        },
        {
            "level": "Mid",
            "q": "What is a schema in SQL?",
            "a": "A schema is a logical namespace inside a database that groups related objects (tables, views, indexes, procedures). In Oracle, a schema is tied to a user account. In MySQL, schema and database are synonymous. Example: <code>SELECT * FROM hr.employees</code> — 'hr' is the schema."
        },
        {
            "level": "Senior",
            "q": "Explain ACID properties with a real-world example.",
            "a": """ACID ensures reliable transactions:
<ul>
<li><b>Atomicity</b> — Bank transfer: debit + credit both succeed, or neither does.</li>
<li><b>Consistency</b> — Data rules (constraints) are always satisfied before and after.</li>
<li><b>Isolation</b> — Two simultaneous transfers don't interfere with each other.</li>
<li><b>Durability</b> — Once committed, the transfer persists even if the server crashes.</li>
</ul>
Implemented via <code>BEGIN / COMMIT / ROLLBACK</code>."""
        }
    ],

    # ── SELECT ─────────────────────────────────────────────────────────────────
    "select": [
        {
            "level": "Fresher",
            "q": "What does SELECT * mean and when should you avoid it?",
            "a": "<code>SELECT *</code> fetches all columns from a table. Avoid it in production code because: it fetches unnecessary data, wastes network bandwidth, breaks if column order changes, and prevents the optimizer from using covering indexes."
        },
        {
            "level": "Fresher",
            "q": "What is the use of DISTINCT in SQL?",
            "a": "<code>DISTINCT</code> removes duplicate rows from the result. Example: <code>SELECT DISTINCT category FROM products;</code> returns each category only once even if many products share it."
        },
        {
            "level": "Junior",
            "q": "How does SELECT work internally (order of execution)?",
            "a": """SQL clauses execute in this order (not the order you write them):
<ol>
<li>FROM / JOIN</li>
<li>WHERE</li>
<li>GROUP BY</li>
<li>HAVING</li>
<li>SELECT</li>
<li>DISTINCT</li>
<li>ORDER BY</li>
<li>LIMIT / FETCH</li>
</ol>
That's why you can't use a SELECT alias in WHERE — it hasn't been created yet."""
        },
        {
            "level": "Junior",
            "q": "What is the difference between WHERE and HAVING?",
            "a": "<b>WHERE</b> filters individual rows <em>before</em> grouping. <b>HAVING</b> filters groups <em>after</em> GROUP BY. You can't use aggregate functions (SUM, COUNT) in WHERE — use HAVING for that."
        },
        {
            "level": "Mid",
            "q": "How do you select the Nth highest salary?",
            "a": """<b>MySQL:</b>
<pre>SELECT DISTINCT salary FROM employees
ORDER BY salary DESC LIMIT 1 OFFSET N-1;</pre>
<b>Oracle:</b>
<pre>SELECT salary FROM (
  SELECT salary, RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) WHERE rnk = N;</pre>
<b>Both (subquery method):</b>
<pre>SELECT MIN(salary) FROM (
  SELECT DISTINCT salary FROM employees
  ORDER BY salary DESC LIMIT N
);</pre>"""
        },
        {
            "level": "Senior",
            "q": "How would you optimise a slow SELECT query?",
            "a": """Key steps:
<ol>
<li>Use <code>EXPLAIN / EXPLAIN PLAN</code> to see the execution plan</li>
<li>Add indexes on WHERE, JOIN, and ORDER BY columns</li>
<li>Avoid <code>SELECT *</code> — select only needed columns</li>
<li>Replace correlated subqueries with JOINs or CTEs</li>
<li>Avoid functions on indexed columns in WHERE</li>
<li>Use query result caching where appropriate</li>
<li>Partition large tables</li>
</ol>"""
        }
    ],

    # ── WHERE ──────────────────────────────────────────────────────────────────
    "where": [
        {
            "level": "Fresher",
            "q": "What is the difference between = and LIKE in SQL?",
            "a": "<code>=</code> is an exact match. <code>LIKE</code> allows pattern matching using <code>%</code> (any characters) and <code>_</code> (one character). Example: <code>WHERE name = 'Alice'</code> vs <code>WHERE name LIKE 'Ali%'</code>."
        },
        {
            "level": "Fresher",
            "q": "What does NULL mean in SQL and how do you check for it?",
            "a": "NULL means <em>missing</em> or <em>unknown</em> value — not zero, not empty string. You cannot use <code>= NULL</code>; you must use <code>IS NULL</code> or <code>IS NOT NULL</code>. Any comparison with NULL returns UNKNOWN, not TRUE or FALSE."
        },
        {
            "level": "Junior",
            "q": "What is the difference between IN and EXISTS?",
            "a": """<b>IN</b> compares a value to a list or subquery result set.
<b>EXISTS</b> checks if a subquery returns any rows at all.
<ul>
<li>EXISTS is generally faster for large datasets because it stops at the first match</li>
<li>IN loads the entire subquery result into memory</li>
<li>EXISTS handles NULLs better</li>
</ul>
<b>MySQL / Oracle:</b>
<pre>-- IN
SELECT * FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE city='NY');

-- EXISTS (faster on large tables)
SELECT * FROM employees e
WHERE EXISTS (SELECT 1 FROM departments d WHERE d.id = e.dept_id AND d.city='NY');</pre>"""
        },
        {
            "level": "Mid",
            "q": "How does SQL handle NULLs in WHERE conditions?",
            "a": "NULL comparisons always return UNKNOWN — neither TRUE nor FALSE. So <code>WHERE salary != 90000</code> will NOT return rows where salary is NULL. You must explicitly add <code>OR salary IS NULL</code> if you want those rows."
        },
        {
            "level": "Senior",
            "q": "What is a sargable predicate and why does it matter?",
            "a": """A <b>SARGable</b> (Search ARGument ABLE) predicate can use an index to speed up the query.
<ul>
<li>✅ Sargable: <code>WHERE salary > 80000</code></li>
<li>✅ Sargable: <code>WHERE hire_date BETWEEN '2020-01-01' AND '2021-01-01'</code></li>
<li>❌ NOT sargable: <code>WHERE YEAR(hire_date) = 2020</code> — function wraps the column, index can't be used</li>
<li>❌ NOT sargable: <code>WHERE UPPER(name) = 'ALICE'</code></li>
</ul>
Fix: rewrite as range conditions that don't wrap the indexed column."""
        }
    ],

    # ── ORDER BY & LIMIT ───────────────────────────────────────────────────────
    "order-limit": [
        {
            "level": "Fresher",
            "q": "What is the default sort order of ORDER BY?",
            "a": "ASC (ascending) — smallest to largest, A to Z. You must explicitly write DESC for descending order."
        },
        {
            "level": "Junior",
            "q": "How do you select the top 5 records in Oracle vs MySQL?",
            "a": """<b>MySQL / SQLite:</b>
<pre>SELECT * FROM employees ORDER BY salary DESC LIMIT 5;</pre>
<b>Oracle (12c+):</b>
<pre>SELECT * FROM employees ORDER BY salary DESC FETCH FIRST 5 ROWS ONLY;</pre>
<b>Oracle (older):</b>
<pre>SELECT * FROM (SELECT * FROM employees ORDER BY salary DESC) WHERE ROWNUM <= 5;</pre>
<b>SQL Server:</b>
<pre>SELECT TOP 5 * FROM employees ORDER BY salary DESC;</pre>"""
        },
        {
            "level": "Mid",
            "q": "How do you implement pagination in SQL?",
            "a": """<b>MySQL:</b>
<pre>-- Page 1 (rows 1-10):
SELECT * FROM employees ORDER BY id LIMIT 10 OFFSET 0;
-- Page 2 (rows 11-20):
SELECT * FROM employees ORDER BY id LIMIT 10 OFFSET 10;</pre>
<b>Oracle:</b>
<pre>SELECT * FROM employees ORDER BY id
OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;</pre>"""
        },
        {
            "level": "Senior",
            "q": "What are the performance implications of OFFSET-based pagination on large tables?",
            "a": """OFFSET pagination becomes slow on large tables because the database must scan and discard all rows before the offset.
<b>Better approach — keyset/cursor pagination:</b>
<pre>-- Instead of OFFSET, remember the last seen ID:
SELECT * FROM employees
WHERE id > :last_seen_id
ORDER BY id
LIMIT 10;</pre>
This is O(log n) with an index, while OFFSET is O(n)."""
        }
    ],

    # ── CHAR FUNCTIONS ─────────────────────────────────────────────────────────
    "char-functions": [
        {
            "level": "Fresher",
            "q": "What string functions are commonly used in SQL?",
            "a": """Most commonly asked:
<table class='ops-table'>
<tr><th>Function</th><th>MySQL</th><th>Oracle</th></tr>
<tr><td>Uppercase</td><td>UPPER(s)</td><td>UPPER(s)</td></tr>
<tr><td>Lowercase</td><td>LOWER(s)</td><td>LOWER(s)</td></tr>
<tr><td>Length</td><td>LENGTH(s)</td><td>LENGTH(s)</td></tr>
<tr><td>Substring</td><td>SUBSTRING(s,1,3)</td><td>SUBSTR(s,1,3)</td></tr>
<tr><td>Concatenate</td><td>CONCAT(a,b)</td><td>a || b or CONCAT(a,b)</td></tr>
<tr><td>Trim</td><td>TRIM(s)</td><td>TRIM(s)</td></tr>
<tr><td>Replace</td><td>REPLACE(s,old,new)</td><td>REPLACE(s,old,new)</td></tr>
</table>"""
        },
        {
            "level": "Junior",
            "q": "How do you extract the domain name from an email address?",
            "a": """<b>MySQL:</b>
<pre>SELECT SUBSTRING(email, LOCATE('@', email) + 1) AS domain FROM employees;</pre>
<b>Oracle:</b>
<pre>SELECT SUBSTR(email, INSTR(email,'@') + 1) AS domain FROM employees;</pre>"""
        },
        {
            "level": "Mid",
            "q": "How do you find employees whose name has exactly 5 characters?",
            "a": """<b>MySQL / Oracle:</b>
<pre>SELECT * FROM employees WHERE LENGTH(name) = 5;</pre>
Or using LIKE:
<pre>SELECT * FROM employees WHERE name LIKE '_____';  -- 5 underscores</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is the difference between CHAR_LENGTH and LENGTH in MySQL?",
            "a": "In MySQL, <code>LENGTH()</code> returns the byte length (differs for multibyte UTF-8 characters), while <code>CHAR_LENGTH()</code> returns the character count. For ASCII text they're the same. For Unicode (e.g. Chinese characters), use CHAR_LENGTH for counting characters."
        },
        {
            "level": "Senior",
            "q": "How would you mask sensitive data like credit card numbers in SQL?",
            "a": """<b>MySQL:</b>
<pre>SELECT CONCAT(REPEAT('*', LENGTH(card_number)-4),
       RIGHT(card_number, 4)) AS masked FROM payments;</pre>
<b>Oracle:</b>
<pre>SELECT RPAD('*', LENGTH(card_number)-4, '*') ||
       SUBSTR(card_number, -4) AS masked FROM payments;</pre>"""
        }
    ],

    # ── NUMBER FUNCTIONS ───────────────────────────────────────────────────────
    "number-functions": [
        {
            "level": "Fresher",
            "q": "What is the difference between ROUND, FLOOR, and CEIL?",
            "a": """<ul>
<li><b>ROUND(3.5)</b> → 4 (rounds to nearest)</li>
<li><b>FLOOR(3.9)</b> → 3 (always rounds down)</li>
<li><b>CEIL(3.1)</b> → 4 (always rounds up)</li>
</ul>
All work the same in MySQL and Oracle."""
        },
        {
            "level": "Junior",
            "q": "How do you calculate the percentage of total for each row?",
            "a": """<b>MySQL / Oracle:</b>
<pre>SELECT name, salary,
  ROUND(salary * 100.0 / SUM(salary) OVER (), 2) AS pct_of_total
FROM employees;</pre>
<b>Without window functions (MySQL 5.x / Oracle subquery):</b>
<pre>SELECT name, salary,
  ROUND(salary * 100.0 / (SELECT SUM(salary) FROM employees), 2) AS pct
FROM employees;</pre>"""
        },
        {
            "level": "Mid",
            "q": "How do you generate a random number in MySQL vs Oracle?",
            "a": """<b>MySQL:</b> <code>SELECT RAND();</code> — returns 0 to 1<br>
<b>Oracle:</b> <code>SELECT DBMS_RANDOM.VALUE FROM dual;</code><br>
<b>Random integer between 1 and 100:</b><br>
MySQL: <code>FLOOR(1 + RAND() * 100)</code><br>
Oracle: <code>ROUND(DBMS_RANDOM.VALUE(1, 100))</code>"""
        },
        {
            "level": "Senior",
            "q": "Explain floating-point precision issues in SQL and how to handle them.",
            "a": """REAL/FLOAT types can have precision errors (e.g., 0.1 + 0.2 ≠ 0.3 exactly). Solutions:
<ul>
<li>Use <b>DECIMAL(p,s)</b> for financial data — exact precision</li>
<li>Use <b>ROUND()</b> when comparing float results</li>
<li>Store money as integers (cents) and divide on display</li>
</ul>
<b>Example:</b> <code>DECIMAL(10,2)</code> stores up to 99,999,999.99 exactly."""
        }
    ],

    # ── DATE FUNCTIONS ─────────────────────────────────────────────────────────
    "date-functions": [
        {
            "level": "Fresher",
            "q": "How do you get the current date and time in MySQL and Oracle?",
            "a": """<b>MySQL:</b>
<pre>SELECT NOW();         -- date + time
SELECT CURDATE();     -- date only
SELECT CURTIME();     -- time only</pre>
<b>Oracle:</b>
<pre>SELECT SYSDATE FROM dual;       -- date + time
SELECT CURRENT_DATE FROM dual;  -- session date</pre>"""
        },
        {
            "level": "Junior",
            "q": "How do you find employees hired in the last 30 days?",
            "a": """<b>MySQL:</b>
<pre>SELECT * FROM employees
WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);</pre>
<b>Oracle:</b>
<pre>SELECT * FROM employees
WHERE hire_date >= SYSDATE - 30;</pre>"""
        },
        {
            "level": "Mid",
            "q": "How do you calculate the number of years between two dates?",
            "a": """<b>MySQL:</b>
<pre>SELECT name,
  TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_employed
FROM employees;</pre>
<b>Oracle:</b>
<pre>SELECT name,
  TRUNC(MONTHS_BETWEEN(SYSDATE, hire_date) / 12) AS years_employed
FROM employees;</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is the difference between DATE, DATETIME, and TIMESTAMP in MySQL?",
            "a": """<table class='ops-table'>
<tr><th>Type</th><th>Stores</th><th>Range</th></tr>
<tr><td>DATE</td><td>YYYY-MM-DD</td><td>1000-01-01 to 9999-12-31</td></tr>
<tr><td>DATETIME</td><td>YYYY-MM-DD HH:MM:SS</td><td>1000 to 9999</td></tr>
<tr><td>TIMESTAMP</td><td>YYYY-MM-DD HH:MM:SS</td><td>1970 to 2038 (Unix epoch)</td></tr>
</table>
TIMESTAMP auto-converts to UTC on storage and back on retrieval. DATETIME stores as-is."""
        },
        {
            "level": "Senior",
            "q": "How do you handle timezone conversions in SQL?",
            "a": """<b>MySQL:</b>
<pre>SELECT CONVERT_TZ(NOW(), 'UTC', 'Asia/Kolkata') AS ist_time;</pre>
<b>Oracle:</b>
<pre>SELECT SYSTIMESTAMP AT TIME ZONE 'Asia/Calcutta' FROM dual;</pre>
Best practice: always store datetimes in <b>UTC</b> in the database and convert to local time in the application layer."""
        }
    ],

    # ── AGGREGATE FUNCTIONS ────────────────────────────────────────────────────
    "aggregate-functions": [
        {
            "level": "Fresher",
            "q": "What aggregate functions are available in SQL?",
            "a": "COUNT, SUM, AVG, MAX, MIN — these operate on a set of rows and return a single value. They ignore NULL values (except COUNT(*) which counts all rows including NULLs)."
        },
        {
            "level": "Fresher",
            "q": "What is the difference between COUNT(*) and COUNT(column)?",
            "a": "<code>COUNT(*)</code> counts ALL rows including NULLs. <code>COUNT(column)</code> counts only rows where that column is NOT NULL. <code>COUNT(DISTINCT column)</code> counts unique non-null values."
        },
        {
            "level": "Junior",
            "q": "How do you find duplicate records in a table?",
            "a": """<b>MySQL / Oracle:</b>
<pre>SELECT name, COUNT(*) AS occurrences
FROM employees
GROUP BY name
HAVING COUNT(*) > 1;</pre>
To find full duplicate rows:
<pre>SELECT name, dept_id, COUNT(*)
FROM employees
GROUP BY name, dept_id
HAVING COUNT(*) > 1;</pre>"""
        },
        {
            "level": "Mid",
            "q": "How do you calculate a running total?",
            "a": """<b>MySQL 8+ / Oracle:</b>
<pre>SELECT name, salary,
  SUM(salary) OVER (ORDER BY id) AS running_total
FROM employees;</pre>
<b>MySQL 5.x (no window functions):</b>
<pre>SELECT e1.name, e1.salary,
  SUM(e2.salary) AS running_total
FROM employees e1
JOIN employees e2 ON e2.id <= e1.id
GROUP BY e1.id, e1.name, e1.salary
ORDER BY e1.id;</pre>"""
        },
        {
            "level": "Senior",
            "q": "How do you calculate a moving average (e.g., 3-row rolling average)?",
            "a": """<b>MySQL 8+ / Oracle:</b>
<pre>SELECT name, salary,
  AVG(salary) OVER (
    ORDER BY id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS moving_avg_3
FROM employees;</pre>
The window frame <code>ROWS BETWEEN 2 PRECEDING AND CURRENT ROW</code> includes the current row and the 2 rows before it."""
        }
    ],

    # ── CONVERSION FUNCTIONS ───────────────────────────────────────────────────
    "conversion-functions": [
        {
            "level": "Fresher",
            "q": "How do you convert a string to a number in SQL?",
            "a": """<b>MySQL:</b> <code>CAST('123' AS UNSIGNED)</code> or <code>CONVERT('123', UNSIGNED)</code><br>
<b>Oracle:</b> <code>TO_NUMBER('123')</code><br>
<b>Both:</b> <code>CAST('123.45' AS DECIMAL(10,2))</code>"""
        },
        {
            "level": "Junior",
            "q": "What is the difference between CAST and CONVERT?",
            "a": """<b>CAST</b> is ANSI SQL standard and works in all databases:
<pre>CAST(salary AS VARCHAR(20))</pre>
<b>CONVERT</b> is database-specific:
<ul>
<li>MySQL: <code>CONVERT(salary, CHAR)</code> — also handles charset conversion</li>
<li>SQL Server: <code>CONVERT(VARCHAR, salary, style)</code> — supports format styles</li>
<li>Oracle: uses <code>TO_CHAR / TO_NUMBER / TO_DATE</code> instead</li>
</ul>"""
        },
        {
            "level": "Mid",
            "q": "How do you format a number as currency in SQL?",
            "a": """<b>MySQL:</b>
<pre>SELECT CONCAT('$', FORMAT(salary, 2)) AS formatted FROM employees;</pre>
<b>Oracle:</b>
<pre>SELECT TO_CHAR(salary, '$999,999.99') AS formatted FROM employees;</pre>"""
        }
    ],

    # ── NULL FUNCTIONS ─────────────────────────────────────────────────────────
    "null-functions": [
        {
            "level": "Fresher",
            "q": "What is NULL in SQL?",
            "a": "NULL represents a missing, unknown, or inapplicable value. It is NOT the same as 0 or empty string ''. Any arithmetic or comparison with NULL produces NULL/UNKNOWN."
        },
        {
            "level": "Junior",
            "q": "What is the difference between COALESCE, ISNULL, IFNULL, and NVL?",
            "a": """All replace NULL with a default value but differ by database:
<table class='ops-table'>
<tr><th>Function</th><th>Database</th><th>Example</th></tr>
<tr><td>COALESCE(a,b,c)</td><td>All (ANSI standard)</td><td>Returns first non-NULL</td></tr>
<tr><td>IFNULL(a,b)</td><td>MySQL, SQLite</td><td>Returns b if a is NULL</td></tr>
<tr><td>NVL(a,b)</td><td>Oracle</td><td>Returns b if a is NULL</td></tr>
<tr><td>ISNULL(a,b)</td><td>SQL Server</td><td>Returns b if a is NULL</td></tr>
</table>
Prefer <b>COALESCE</b> — it's portable and accepts multiple fallback values."""
        },
        {
            "level": "Mid",
            "q": "How do NULLs affect aggregate functions?",
            "a": "SUM, AVG, MIN, MAX, COUNT(col) all <b>ignore NULL values</b>. COUNT(*) includes NULLs (it counts rows, not values). This means AVG(salary) divides by the count of non-null salaries, which may surprise you if many rows have NULL salary."
        },
        {
            "level": "Senior",
            "q": "How do you handle NULL in ORDER BY?",
            "a": """By default:
<ul>
<li><b>Oracle:</b> NULLs sort <em>last</em> in ASC, <em>first</em> in DESC</li>
<li><b>MySQL:</b> NULLs sort <em>first</em> in ASC</li>
</ul>
<b>Control NULL position in Oracle:</b>
<pre>SELECT * FROM employees ORDER BY salary ASC NULLS LAST;</pre>
<b>MySQL workaround:</b>
<pre>SELECT * FROM employees ORDER BY salary IS NULL ASC, salary ASC;</pre>"""
        }
    ],

    # ── CONDITIONAL ───────────────────────────────────────────────────────────
    "conditional-functions": [
        {
            "level": "Fresher",
            "q": "What is the CASE expression in SQL?",
            "a": "CASE is SQL's if-else. It evaluates conditions and returns a value based on the first match. There are two forms: Simple CASE (compares one value) and Searched CASE (evaluates multiple conditions)."
        },
        {
            "level": "Junior",
            "q": "What is the difference between CASE and DECODE?",
            "a": """<b>DECODE</b> is Oracle-specific and only does equality checks:
<pre>DECODE(dept_id, 1,'Engineering', 2,'Marketing', 'Other')</pre>
<b>CASE</b> is ANSI standard, works everywhere, and supports ranges, LIKE, IS NULL:
<pre>CASE WHEN salary > 100000 THEN 'Senior' ELSE 'Junior' END</pre>
Use CASE in new code — it's portable and more powerful."""
        },
        {
            "level": "Mid",
            "q": "How do you count rows conditionally (e.g., count only salaries > 80k)?",
            "a": """<b>MySQL / Oracle:</b>
<pre>SELECT
  COUNT(CASE WHEN salary > 80000 THEN 1 END) AS high_earners,
  COUNT(CASE WHEN salary <= 80000 THEN 1 END) AS others
FROM employees;</pre>
Or using SUM with boolean (MySQL):
<pre>SELECT SUM(salary > 80000) AS high_earners FROM employees;</pre>"""
        },
        {
            "level": "Senior",
            "q": "How do you use CASE in an ORDER BY clause?",
            "a": """You can sort by a custom order using CASE:
<b>MySQL / Oracle:</b>
<pre>SELECT name, status FROM orders
ORDER BY CASE status
  WHEN 'urgent'   THEN 1
  WHEN 'pending'  THEN 2
  WHEN 'shipped'  THEN 3
  ELSE 4
END;</pre>
This lets you define a business-driven sort order."""
        }
    ],

    # ── GROUP BY ───────────────────────────────────────────────────────────────
    "group-by": [
        {
            "level": "Fresher",
            "q": "What is the purpose of GROUP BY?",
            "a": "GROUP BY groups rows with the same value in specified columns so aggregate functions (COUNT, SUM, AVG) can be applied to each group separately. Without GROUP BY, aggregate functions return a single value for the whole table."
        },
        {
            "level": "Junior",
            "q": "Can you use a column alias in GROUP BY?",
            "a": "In <b>MySQL</b> — yes, you can use column aliases in GROUP BY. In <b>Oracle and SQL Server</b> — no, you must repeat the expression or use a subquery/CTE because GROUP BY runs before SELECT."
        },
        {
            "level": "Mid",
            "q": "How do you find the department with the highest total salary?",
            "a": """<b>MySQL:</b>
<pre>SELECT dept_id, SUM(salary) AS total
FROM employees
GROUP BY dept_id
ORDER BY total DESC
LIMIT 1;</pre>
<b>Oracle:</b>
<pre>SELECT * FROM (
  SELECT dept_id, SUM(salary) AS total
  FROM employees
  GROUP BY dept_id
  ORDER BY total DESC
) WHERE ROWNUM = 1;</pre>"""
        },
        {
            "level": "Senior",
            "q": "What is the difference between GROUP BY and PARTITION BY?",
            "a": """<b>GROUP BY</b> collapses rows into one row per group — you lose individual row data.
<b>PARTITION BY</b> (used with window functions) calculates per group but <em>keeps all rows</em>:
<pre>-- GROUP BY: one row per dept
SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id;

-- PARTITION BY: all rows, with dept avg alongside each
SELECT name, dept_id,
  AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees;</pre>"""
        }
    ],

    # ── HAVING ─────────────────────────────────────────────────────────────────
    "having": [
        {
            "level": "Fresher",
            "q": "What is the HAVING clause?",
            "a": "HAVING filters the result of GROUP BY — it's like WHERE but for groups. You use it when you need to filter based on an aggregate function result (like COUNT > 2 or AVG(salary) > 80000)."
        },
        {
            "level": "Junior",
            "q": "Can you use HAVING without GROUP BY?",
            "a": "Yes — HAVING without GROUP BY treats the entire table as one group. Example: <code>SELECT AVG(salary) FROM employees HAVING AVG(salary) > 80000</code> returns the average only if it exceeds 80000. Rarely useful but valid SQL."
        },
        {
            "level": "Mid",
            "q": "Find all categories where average price is above the overall average price.",
            "a": """<b>MySQL / Oracle:</b>
<pre>SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > (SELECT AVG(price) FROM products);</pre>"""
        }
    ],

    # ── INNER JOIN ─────────────────────────────────────────────────────────────
    "inner-join": [
        {
            "level": "Fresher",
            "q": "What is a JOIN in SQL?",
            "a": "A JOIN combines rows from two or more tables based on a related column. The most common is INNER JOIN which returns only rows that have matching values in both tables."
        },
        {
            "level": "Fresher",
            "q": "What is the difference between INNER JOIN and OUTER JOIN?",
            "a": "<b>INNER JOIN</b> returns only matching rows from both tables. <b>OUTER JOIN</b> (LEFT/RIGHT/FULL) includes non-matching rows from one or both tables, filling with NULLs where there's no match."
        },
        {
            "level": "Junior",
            "q": "What is a self-join and when would you use it?",
            "a": """A self-join joins a table with itself. Common use: employee-manager relationships where manager_id is a foreign key to the same employees table.
<b>MySQL / Oracle:</b>
<pre>SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is the difference between ON and USING in a JOIN?",
            "a": """<b>ON</b> lets you specify any join condition:
<pre>JOIN departments d ON e.dept_id = d.id</pre>
<b>USING</b> is shorthand when both tables have the same column name (removes duplicate column in result):
<pre>JOIN departments USING (dept_id)</pre>
USING is supported in MySQL and Oracle but not SQL Server."""
        },
        {
            "level": "Senior",
            "q": "How do you optimise JOIN performance on large tables?",
            "a": """Key optimisations:
<ol>
<li>Index join columns (foreign keys and the columns in ON clause)</li>
<li>Filter rows early with WHERE before joining</li>
<li>Join smaller tables first</li>
<li>Use EXPLAIN to check if indexes are being used</li>
<li>Consider denormalisation for very hot read paths</li>
<li>In Oracle: use hints like <code>/*+ USE_HASH(e d) */</code></li>
</ol>"""
        }
    ],

    # ── LEFT RIGHT JOIN ────────────────────────────────────────────────────────
    "left-right-join": [
        {
            "level": "Fresher",
            "q": "What is a LEFT JOIN?",
            "a": "LEFT JOIN returns all rows from the left (first) table and matching rows from the right table. Where there's no match, NULLs are returned for right-table columns."
        },
        {
            "level": "Junior",
            "q": "How do you find rows in Table A that have no match in Table B?",
            "a": """This is called an anti-join — use LEFT JOIN with a NULL check:
<b>MySQL / Oracle:</b>
<pre>SELECT a.* FROM employees a
LEFT JOIN departments b ON a.dept_id = b.id
WHERE b.id IS NULL;</pre>
Or using NOT EXISTS:
<pre>SELECT * FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM departments d WHERE d.id = e.dept_id);</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is a FULL OUTER JOIN?",
            "a": """FULL OUTER JOIN returns all rows from both tables — matches are joined, non-matches get NULLs on the missing side.
<b>MySQL (no native FULL OUTER JOIN):</b>
<pre>SELECT * FROM a LEFT JOIN b ON a.id = b.id
UNION
SELECT * FROM a RIGHT JOIN b ON a.id = b.id;</pre>
<b>Oracle:</b>
<pre>SELECT * FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.id;</pre>"""
        }
    ],

    # ── SELF JOIN ─────────────────────────────────────────────────────────────
    "self-join": [
        {
            "level": "Junior",
            "q": "What is a CROSS JOIN?",
            "a": "A CROSS JOIN returns the Cartesian product — every row from Table A combined with every row from Table B. If A has 5 rows and B has 3 rows, the result has 15 rows. Use carefully — without a WHERE condition it can create huge results."
        },
        {
            "level": "Mid",
            "q": "Give a practical use case for a CROSS JOIN.",
            "a": """Generating all combinations, like a size × colour product matrix:
<b>MySQL / Oracle:</b>
<pre>SELECT s.size_name, c.colour_name
FROM sizes s
CROSS JOIN colours c;</pre>
Also used for generating date ranges or test data.</pre>"""
        }
    ],

    # ── SUBQUERY WHERE ─────────────────────────────────────────────────────────
    "subquery-where": [
        {
            "level": "Fresher",
            "q": "What is a subquery?",
            "a": "A subquery is a SELECT statement nested inside another SQL statement. The inner query executes first and its result is used by the outer query. Also called an inner query or nested query."
        },
        {
            "level": "Junior",
            "q": "What is a correlated subquery?",
            "a": """A correlated subquery references columns from the outer query — it runs once <em>for each row</em> of the outer query.
<b>MySQL / Oracle:</b>
<pre>SELECT name, salary FROM employees e
WHERE salary > (
  SELECT AVG(salary) FROM employees
  WHERE dept_id = e.dept_id  -- references outer e
);</pre>
Correlated subqueries can be slow on large tables — consider rewriting as a JOIN or CTE."""
        },
        {
            "level": "Mid",
            "q": "What is the difference between a subquery and a JOIN?",
            "a": """Both can produce the same result but differ in:
<ul>
<li><b>Readability:</b> JOINs are often clearer</li>
<li><b>Performance:</b> JOINs are usually faster (optimiser can use indexes more easily)</li>
<li><b>Use case:</b> Subqueries are better for aggregated filters (HAVING subquery), existence checks (EXISTS), and derived tables</li>
</ul>"""
        },
        {
            "level": "Senior",
            "q": "When would you use EXISTS over IN?",
            "a": """Use <b>EXISTS</b> when:
<ul>
<li>The subquery returns a large result set (EXISTS stops at first match)</li>
<li>You only care whether rows exist, not what they contain</li>
<li>The subquery involves NULLs (IN with NULLs can give unexpected results)</li>
</ul>
Use <b>IN</b> for small, static lists: <code>WHERE status IN ('active','pending')</code>"""
        }
    ],

    # ── SUBQUERY FROM ─────────────────────────────────────────────────────────
    "subquery-from": [
        {
            "level": "Mid",
            "q": "What is a derived table?",
            "a": "A derived table is a subquery in the FROM clause. It acts as a temporary table for the outer query. In Oracle it's also called an inline view. Must have an alias: <code>SELECT * FROM (SELECT ...) AS t</code>"
        },
        {
            "level": "Senior",
            "q": "When would you use a CTE instead of a subquery?",
            "a": """CTEs are better when:
<ul>
<li>The same subquery is referenced multiple times</li>
<li>You want to make complex queries readable</li>
<li>You need recursion (RECURSIVE CTE)</li>
<li>You want to debug step-by-step (comment out CTE blocks)</li>
</ul>
Subqueries are fine for simple, one-time-use derived tables."""
        }
    ],

    # ── CREATE TABLE ───────────────────────────────────────────────────────────
    "create-table": [
        {
            "level": "Fresher",
            "q": "What is the syntax for creating a table in SQL?",
            "a": """<b>MySQL:</b>
<pre>CREATE TABLE employees (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  name   VARCHAR(100) NOT NULL,
  salary DECIMAL(10,2),
  dept_id INT,
  FOREIGN KEY (dept_id) REFERENCES departments(id)
);</pre>
<b>Oracle:</b>
<pre>CREATE TABLE employees (
  id     NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name   VARCHAR2(100) NOT NULL,
  salary NUMBER(10,2),
  dept_id NUMBER REFERENCES departments(id)
);</pre>"""
        },
        {
            "level": "Junior",
            "q": "What is the difference between VARCHAR and VARCHAR2?",
            "a": "<b>VARCHAR2</b> is Oracle-specific and is the recommended string type in Oracle. It stores variable-length strings up to 4000 bytes (or 32767 in PL/SQL). <b>VARCHAR</b> is ANSI standard and used in MySQL, SQL Server, PostgreSQL. In Oracle, always use VARCHAR2 — VARCHAR behaviour may change in future versions."
        },
        {
            "level": "Mid",
            "q": "What is the difference between NUMBER and INT in Oracle?",
            "a": "In Oracle, <code>NUMBER(p,s)</code> is the universal numeric type — it can store integers, decimals, etc. <code>NUMBER(10,0)</code> is effectively an integer. <code>INT</code> is just an alias for NUMBER(38,0). MySQL has distinct types: INT, BIGINT, DECIMAL, FLOAT, DOUBLE."
        },
        {
            "level": "Senior",
            "q": "How do you add a column with a default value to an existing large table without locking it?",
            "a": """Adding a column with a DEFAULT in modern MySQL (5.6+) and Oracle 12c+ is done online (no full table lock):
<b>MySQL:</b>
<pre>ALTER TABLE employees
ADD COLUMN bonus DECIMAL(10,2) DEFAULT 0.00,
ALGORITHM=INPLACE, LOCK=NONE;</pre>
<b>Oracle 12c+:</b>
<pre>ALTER TABLE employees ADD bonus NUMBER DEFAULT 0 NOT NULL;</pre>
Oracle 12c+ stores DEFAULT NOT NULL metadata without rewriting rows — O(1) operation."""
        }
    ],

    # ── ALTER DROP ─────────────────────────────────────────────────────────────
    "alter-drop": [
        {
            "level": "Fresher",
            "q": "What is the difference between DROP TABLE and TRUNCATE TABLE?",
            "a": """<table class='ops-table'>
<tr><th></th><th>DROP</th><th>TRUNCATE</th><th>DELETE</th></tr>
<tr><td>Removes structure</td><td>Yes</td><td>No</td><td>No</td></tr>
<tr><td>Removes data</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Rollback possible</td><td>No (DDL)</td><td>No (DDL)</td><td>Yes (DML)</td></tr>
<tr><td>Speed</td><td>Fast</td><td>Fast</td><td>Slow (row by row)</td></tr>
<tr><td>Triggers fired</td><td>No</td><td>No</td><td>Yes</td></tr>
</table>"""
        },
        {
            "level": "Mid",
            "q": "How do you rename a column in MySQL vs Oracle?",
            "a": """<b>MySQL 8+:</b>
<pre>ALTER TABLE employees RENAME COLUMN name TO full_name;</pre>
<b>MySQL 5.x:</b>
<pre>ALTER TABLE employees CHANGE name full_name VARCHAR(100);</pre>
<b>Oracle:</b>
<pre>ALTER TABLE employees RENAME COLUMN name TO full_name;</pre>"""
        }
    ],

    # ── INSERT ─────────────────────────────────────────────────────────────────
    "insert": [
        {
            "level": "Fresher",
            "q": "What is the syntax for INSERT in MySQL vs Oracle?",
            "a": """<b>MySQL:</b>
<pre>INSERT INTO employees (name, salary) VALUES ('Alice', 85000);
-- Multiple rows:
INSERT INTO employees (name, salary) VALUES ('Bob',72000), ('Carol',95000);</pre>
<b>Oracle (single row only in one INSERT... VALUES):</b>
<pre>INSERT INTO employees (name, salary) VALUES ('Alice', 85000);
-- Multiple rows use INSERT ALL:
INSERT ALL
  INTO employees (name, salary) VALUES ('Bob', 72000)
  INTO employees (name, salary) VALUES ('Carol', 95000)
SELECT * FROM dual;</pre>"""
        },
        {
            "level": "Junior",
            "q": "How do you insert data from one table into another?",
            "a": """<b>MySQL / Oracle:</b>
<pre>INSERT INTO archive_employees (name, salary, dept_id)
SELECT name, salary, dept_id
FROM employees
WHERE hire_date < '2015-01-01';</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is INSERT IGNORE in MySQL?",
            "a": "<code>INSERT IGNORE</code> skips rows that would cause a duplicate key error instead of failing. In Oracle, the equivalent is <code>INSERT INTO ... (SELECT ... WHERE NOT EXISTS (...))</code> or using <code>MERGE</code>."
        }
    ],

    # ── UPDATE ─────────────────────────────────────────────────────────────────
    "update": [
        {
            "level": "Fresher",
            "q": "What happens if you run UPDATE without a WHERE clause?",
            "a": "Every row in the table gets updated — a dangerous operation. Always test with a SELECT first using the same WHERE condition. Use transactions so you can ROLLBACK if needed."
        },
        {
            "level": "Junior",
            "q": "How do you update a table based on values from another table?",
            "a": """<b>MySQL:</b>
<pre>UPDATE employees e
JOIN departments d ON e.dept_id = d.id
SET e.salary = e.salary * 1.10
WHERE d.city = 'New York';</pre>
<b>Oracle:</b>
<pre>UPDATE employees
SET salary = salary * 1.10
WHERE dept_id IN (SELECT id FROM departments WHERE city = 'New York');</pre>"""
        },
        {
            "level": "Senior",
            "q": "How would you safely update millions of rows without locking the table?",
            "a": """Batch updates — update in chunks to avoid long locks:
<b>MySQL:</b>
<pre>-- Repeat until 0 rows affected:
UPDATE employees
SET salary = ROUND(salary * 1.05, 2)
WHERE salary < 80000
LIMIT 1000;</pre>
<b>Oracle:</b>
<pre>-- Use ROWNUM or ROWID-based batching:
UPDATE employees SET salary = salary * 1.05
WHERE ROWID IN (SELECT ROWID FROM employees WHERE salary < 80000 AND ROWNUM <= 1000);</pre>"""
        }
    ],

    # ── DELETE ─────────────────────────────────────────────────────────────────
    "delete": [
        {
            "level": "Fresher",
            "q": "What is the difference between DELETE and TRUNCATE?",
            "a": "DELETE removes specific rows (or all if no WHERE), fires triggers, can be rolled back, and is logged row-by-row. TRUNCATE removes ALL rows instantly, can't be rolled back (DDL), doesn't fire row-level triggers, and resets auto-increment."
        },
        {
            "level": "Junior",
            "q": "How do you delete duplicate rows keeping only one?",
            "a": """<b>MySQL:</b>
<pre>DELETE e1 FROM employees e1
INNER JOIN employees e2
WHERE e1.id > e2.id AND e1.name = e2.name;</pre>
<b>Oracle (using ROWID):</b>
<pre>DELETE FROM employees
WHERE ROWID NOT IN (
  SELECT MIN(ROWID) FROM employees GROUP BY name
);</pre>"""
        },
        {
            "level": "Mid",
            "q": "How do you delete rows from a table based on a condition in another table?",
            "a": """<b>MySQL:</b>
<pre>DELETE e FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE d.city = 'Chicago';</pre>
<b>Oracle:</b>
<pre>DELETE FROM employees
WHERE dept_id IN (SELECT id FROM departments WHERE city='Chicago');</pre>"""
        }
    ],

    # ── CTE ────────────────────────────────────────────────────────────────────
    "cte": [
        {
            "level": "Mid",
            "q": "What is a CTE and how is it different from a subquery?",
            "a": "A CTE (WITH clause) is a named temporary result set scoped to a single query. Unlike a subquery it can be referenced multiple times in the same query, improves readability, and supports recursion. Both MySQL 8+ and Oracle support CTEs."
        },
        {
            "level": "Mid",
            "q": "Write a recursive CTE to generate numbers 1 to 10.",
            "a": """<b>MySQL 8+ / Oracle:</b>
<pre>WITH RECURSIVE nums(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums;</pre>"""
        },
        {
            "level": "Senior",
            "q": "How would you use a recursive CTE to traverse a hierarchy (org chart)?",
            "a": """<b>MySQL 8+ / Oracle:</b>
<pre>WITH RECURSIVE org AS (
  -- Anchor: top-level (no manager)
  SELECT id, name, manager_id, 0 AS level
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  -- Recursive: find reports
  SELECT e.id, e.name, e.manager_id, o.level + 1
  FROM employees e
  JOIN org o ON e.manager_id = o.id
)
SELECT LPAD(' ', level*2, ' ') || name AS hierarchy, level
FROM org ORDER BY level, name;</pre>
Oracle also has the native <code>CONNECT BY PRIOR</code> syntax for hierarchies."""
        }
    ],

    # ── WINDOW FUNCTIONS ───────────────────────────────────────────────────────
    "window-functions": [
        {
            "level": "Mid",
            "q": "What is a window function?",
            "a": "A window function performs a calculation over a set of rows related to the current row — its 'window'. Unlike GROUP BY, it doesn't collapse rows. Syntax: <code>function() OVER (PARTITION BY col ORDER BY col)</code>. Available in MySQL 8+, Oracle, PostgreSQL, SQL Server."
        },
        {
            "level": "Mid",
            "q": "What is the difference between RANK, DENSE_RANK, and ROW_NUMBER?",
            "a": """Given salaries: 90000, 90000, 80000:
<table class='ops-table'>
<tr><th>Function</th><th>Result</th></tr>
<tr><td>ROW_NUMBER()</td><td>1, 2, 3 — always unique</td></tr>
<tr><td>RANK()</td><td>1, 1, 3 — ties get same rank, gap after</td></tr>
<tr><td>DENSE_RANK()</td><td>1, 1, 2 — ties get same rank, NO gap</td></tr>
</table>
<b>MySQL 8+ / Oracle:</b>
<pre>SELECT name, salary,
  RANK() OVER (ORDER BY salary DESC) AS rnk,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
FROM employees;</pre>"""
        },
        {
            "level": "Senior",
            "q": "How do you find the top N records per group using window functions?",
            "a": """<b>MySQL 8+ / Oracle:</b>
<pre>SELECT * FROM (
  SELECT name, dept_id, salary,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
) ranked
WHERE rnk <= 2;  -- top 2 per department</pre>
This is one of the most common interview questions for mid/senior roles."""
        },
        {
            "level": "Senior",
            "q": "What is the difference between ROWS and RANGE in window frame specification?",
            "a": """Both define the window frame within OVER():
<ul>
<li><b>ROWS</b> — physical rows: <code>ROWS BETWEEN 2 PRECEDING AND CURRENT ROW</code></li>
<li><b>RANGE</b> — logical range based on value: ties are treated as the same point</li>
</ul>
Example: with RANGE, if 3 rows have the same ORDER BY value, they're all included in each other's window. ROWS is usually preferred for running totals."""
        }
    ],

    # ── VIEWS ─────────────────────────────────────────────────────────────────
    "views": [
        {
            "level": "Fresher",
            "q": "What is a VIEW in SQL?",
            "a": "A VIEW is a stored SELECT query that you can query like a table. It doesn't store data itself — it re-executes the underlying query each time. Views simplify complex queries, enforce security (expose only certain columns), and provide a stable interface even if underlying tables change."
        },
        {
            "level": "Junior",
            "q": "What is an updatable view?",
            "a": "A view is updatable if it maps directly to a single table and doesn't use GROUP BY, DISTINCT, aggregate functions, UNION, or subqueries. You can then INSERT/UPDATE/DELETE through it. Complex views require INSTEAD OF triggers (Oracle/SQL Server)."
        },
        {
            "level": "Mid",
            "q": "What is a Materialized View?",
            "a": """A <b>Materialized View</b> (Oracle) / <b>summary table</b> (MySQL) stores the query result physically on disk — unlike a regular view which re-executes every time.
<ul>
<li>Faster reads — pre-computed result</li>
<li>Can have indexes built on them</li>
<li>Must be refreshed when underlying data changes (<code>DBMS_MVIEW.REFRESH</code>)</li>
</ul>
<b>Oracle:</b>
<pre>CREATE MATERIALIZED VIEW mv_dept_stats AS
SELECT dept_id, COUNT(*), AVG(salary) FROM employees GROUP BY dept_id;</pre>
MySQL doesn't have built-in materialized views — simulate with a table + scheduled refresh."""
        }
    ],

    # ── INDEXES ───────────────────────────────────────────────────────────────
    "indexes": [
        {
            "level": "Fresher",
            "q": "What is an index in SQL?",
            "a": "An index is a data structure (usually a B-tree) that makes lookups on a column faster — like a book index helping you find a topic without reading every page. Speeds up SELECT and WHERE but slightly slows INSERT/UPDATE/DELETE."
        },
        {
            "level": "Junior",
            "q": "What are the types of indexes?",
            "a": """<table class='ops-table'>
<tr><th>Type</th><th>Description</th></tr>
<tr><td>Primary Index</td><td>Automatically created on PRIMARY KEY</td></tr>
<tr><td>Unique Index</td><td>Enforces uniqueness, speeds lookups</td></tr>
<tr><td>Composite Index</td><td>On multiple columns — order matters!</td></tr>
<tr><td>Full-Text Index</td><td>For text search (MySQL FULLTEXT)</td></tr>
<tr><td>Bitmap Index</td><td>Oracle — for low-cardinality columns</td></tr>
<tr><td>Function-based Index</td><td>Oracle — index on UPPER(name)</td></tr>
</table>"""
        },
        {
            "level": "Mid",
            "q": "What is a composite index and what is the left-prefix rule?",
            "a": """A composite index on (col1, col2, col3) can be used for queries filtering on:
<ul>
<li>col1 alone ✅</li>
<li>col1 + col2 ✅</li>
<li>col1 + col2 + col3 ✅</li>
<li>col2 alone ❌ (skips the leftmost column)</li>
<li>col3 alone ❌</li>
</ul>
Always put the most selective or most-queried column first."""
        },
        {
            "level": "Senior",
            "q": "When should you NOT use an index?",
            "a": """Indexes have overhead — don't add them blindly:
<ul>
<li>Small tables (full scan is faster)</li>
<li>Columns rarely used in WHERE/JOIN</li>
<li>Columns with very low cardinality (e.g., boolean, gender — bitmap indexes are better)</li>
<li>Tables with heavy write load (every write must update all indexes)</li>
<li>Columns updated frequently</li>
</ul>"""
        }
    ],

    # ── TRANSACTIONS ─────────────────────────────────────────────────────────
    "transactions": [
        {
            "level": "Fresher",
            "q": "What is a transaction in SQL?",
            "a": "A transaction is a group of SQL operations treated as a single unit. Either ALL operations succeed (COMMIT) or ALL are undone (ROLLBACK). This ensures data integrity."
        },
        {
            "level": "Junior",
            "q": "What is a SAVEPOINT?",
            "a": """A SAVEPOINT marks a point within a transaction you can ROLLBACK to without undoing the entire transaction.
<b>MySQL / Oracle:</b>
<pre>BEGIN;
INSERT INTO orders ...;   -- step 1
SAVEPOINT sp1;
UPDATE inventory ...;     -- step 2
ROLLBACK TO sp1;          -- undo step 2 only
COMMIT;                   -- commits step 1</pre>"""
        },
        {
            "level": "Mid",
            "q": "What are transaction isolation levels?",
            "a": """<table class='ops-table'>
<tr><th>Level</th><th>Dirty Read</th><th>Non-repeatable Read</th><th>Phantom Read</th></tr>
<tr><td>READ UNCOMMITTED</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
<tr><td>READ COMMITTED</td><td>No</td><td>Yes</td><td>Yes</td></tr>
<tr><td>REPEATABLE READ</td><td>No</td><td>No</td><td>Yes</td></tr>
<tr><td>SERIALIZABLE</td><td>No</td><td>No</td><td>No</td></tr>
</table>
MySQL default: REPEATABLE READ. Oracle default: READ COMMITTED."""
        },
        {
            "level": "Senior",
            "q": "What is a deadlock and how do you prevent it?",
            "a": """A deadlock occurs when two transactions each hold a lock the other needs, so both wait forever.
<b>Prevention:</b>
<ul>
<li>Always acquire locks in the same order in all transactions</li>
<li>Keep transactions short</li>
<li>Use SELECT FOR UPDATE only when necessary</li>
<li>Use optimistic locking (version column) for low-contention scenarios</li>
</ul>
<b>MySQL:</b> <code>SHOW ENGINE INNODB STATUS</code> to diagnose deadlocks.<br>
<b>Oracle:</b> Deadlocks are logged in the alert log and trace files."""
        }
    ],

    # ── SET OPERATIONS ─────────────────────────────────────────────────────────
    "set-operations": [
        {
            "level": "Fresher",
            "q": "What is the difference between UNION and UNION ALL?",
            "a": "<b>UNION</b> removes duplicate rows from the combined result (requires extra sort/hash step). <b>UNION ALL</b> keeps all rows including duplicates and is faster. Use UNION ALL when you know there are no duplicates or you want all rows."
        },
        {
            "level": "Mid",
            "q": "What is the difference between UNION and JOIN?",
            "a": "<b>UNION</b> stacks rows vertically — combines rows from two queries with the same columns. <b>JOIN</b> combines columns horizontally — merges columns from related tables. UNION increases rows; JOIN increases columns."
        },
        {
            "level": "Mid",
            "q": "Does MySQL support INTERSECT and EXCEPT?",
            "a": """MySQL 8.0.31+ added INTERSECT and EXCEPT support. Before that, simulate them:
<b>INTERSECT:</b>
<pre>SELECT dept_id FROM employees WHERE salary > 80000
AND dept_id IN (SELECT dept_id FROM employees WHERE age > 30);</pre>
<b>EXCEPT (MINUS in Oracle):</b>
<pre>SELECT id FROM departments
WHERE id NOT IN (SELECT DISTINCT dept_id FROM employees);</pre>
<b>Oracle uses MINUS instead of EXCEPT:</b>
<pre>SELECT id FROM departments MINUS SELECT dept_id FROM employees;</pre>"""
        }
    ],

    # ── LPAD RPAD ─────────────────────────────────────────────────────────────
    "lpad-rpad-initcap": [
        {
            "level": "Junior",
            "q": "What is LPAD and RPAD?",
            "a": """<b>LPAD(str, n, pad)</b> — pads string from the left to length n.<br>
<b>RPAD(str, n, pad)</b> — pads string from the right to length n.<br>
<b>MySQL:</b>
<pre>SELECT LPAD('7', 5, '0');   -- '00007'
SELECT RPAD('Hi', 6, '.');  -- 'Hi....'</pre>
<b>Oracle:</b>
<pre>SELECT LPAD('7', 5, '0') FROM dual;
SELECT RPAD('Hi', 6, '.') FROM dual;</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is INITCAP and where is it available?",
            "a": """<b>INITCAP</b> capitalises the first letter of each word.
<b>Oracle (built-in):</b>
<pre>SELECT INITCAP('hello world') FROM dual;  -- 'Hello World'</pre>
<b>MySQL (simulate):</b>
<pre>-- For single word:
SELECT CONCAT(UPPER(LEFT(name,1)), LOWER(SUBSTRING(name,2))) FROM employees;</pre>
MySQL doesn't have native INITCAP — use a stored function or application-level formatting."""
        }
    ],

    # ── ASCII CHR ─────────────────────────────────────────────────────────────
    "ascii-chr-translate": [
        {
            "level": "Junior",
            "q": "What is the ASCII function in SQL?",
            "a": """<b>ASCII()</b> returns the ASCII code of the first character of a string.
<b>MySQL:</b> <code>SELECT ASCII('A');</code> → 65<br>
<b>Oracle:</b> <code>SELECT ASCII('A') FROM dual;</code> → 65<br>
<b>CHR()/CHAR()</b> does the reverse — code to character:
<b>MySQL:</b> <code>SELECT CHAR(65);</code> → 'A'<br>
<b>Oracle:</b> <code>SELECT CHR(65) FROM dual;</code> → 'A'"""
        }
    ],

    # ── GROUP CONCAT ─────────────────────────────────────────────────────────
    "group-concat": [
        {
            "level": "Mid",
            "q": "How do you concatenate multiple row values into a single string?",
            "a": """<b>MySQL:</b>
<pre>SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS team
FROM employees
GROUP BY dept_id;</pre>
<b>Oracle (LISTAGG):</b>
<pre>SELECT dept_id,
  LISTAGG(name, ', ') WITHIN GROUP (ORDER BY name) AS team
FROM employees
GROUP BY dept_id;</pre>
<b>PostgreSQL:</b> <code>STRING_AGG(name, ', ')</code>"""
        },
        {
            "level": "Senior",
            "q": "What is the maximum length for GROUP_CONCAT in MySQL and how do you increase it?",
            "a": """Default is 1024 characters. To increase:
<pre>SET SESSION group_concat_max_len = 100000;
-- or globally:
SET GLOBAL group_concat_max_len = 100000;</pre>
In Oracle LISTAGG, the limit is 4000 bytes — use <code>LISTAGG(...) ON OVERFLOW TRUNCATE</code> in Oracle 12.2+ to handle overflow gracefully."""
        }
    ],

    # ── DECODE ────────────────────────────────────────────────────────────────
    "decode": [
        {
            "level": "Junior",
            "q": "What is DECODE in Oracle SQL?",
            "a": """DECODE is Oracle's conditional function — works like a simple CASE:
<pre>SELECT name,
  DECODE(dept_id, 1,'Engineering', 2,'Marketing', 3,'Finance', 'Other') AS dept
FROM employees;</pre>
Equivalent CASE (works in all databases):
<pre>SELECT name,
  CASE dept_id WHEN 1 THEN 'Engineering'
               WHEN 2 THEN 'Marketing'
               WHEN 3 THEN 'Finance'
               ELSE 'Other' END AS dept
FROM employees;</pre>"""
        },
        {
            "level": "Mid",
            "q": "How does DECODE handle NULLs differently from CASE?",
            "a": "DECODE treats NULL = NULL as TRUE (two NULLs are equal). CASE uses <code>IS NULL</code> logic — the expression <code>NULL = NULL</code> is UNKNOWN. So <code>DECODE(col, NULL, 'missing', col)</code> works, but <code>CASE col WHEN NULL THEN 'missing'</code> does NOT — you must write <code>CASE WHEN col IS NULL THEN 'missing'</code>."
        }
    ],

    # ── SIGN TRUNC MOD ────────────────────────────────────────────────────────
    "sign-trunc-mod": [
        {
            "level": "Junior",
            "q": "What is the TRUNC function in Oracle?",
            "a": """<b>TRUNC(n, d)</b> — truncates to d decimal places (no rounding):
<b>Oracle:</b>
<pre>SELECT TRUNC(3.987, 2) FROM dual;  -- 3.98
SELECT TRUNC(3.987, 0) FROM dual;  -- 3
SELECT TRUNC(3.987)    FROM dual;  -- 3 (default 0)</pre>
TRUNC also works on dates in Oracle:
<pre>SELECT TRUNC(SYSDATE, 'MM') FROM dual;  -- first day of current month</pre>
<b>MySQL equivalent:</b> <code>TRUNCATE(3.987, 2)</code> → 3.98"""
        },
        {
            "level": "Mid",
            "q": "How is MOD different from the % operator?",
            "a": """Both return the remainder, but behaviour differs for negative numbers:
<pre>MOD(-7, 3)  -- Oracle: -1 (sign follows dividend)
-7 % 3      -- MySQL: -1
MOD(7, -3)  -- Oracle: 1
</pre>
In most practical cases they behave the same. Use <code>MOD()</code> for Oracle compatibility."""
        }
    ],

    # ── ADD MONTHS ────────────────────────────────────────────────────────────
    "date-add-months": [
        {
            "level": "Junior",
            "q": "What is ADD_MONTHS in Oracle?",
            "a": """<b>Oracle:</b>
<pre>SELECT ADD_MONTHS(SYSDATE, 3) FROM dual;  -- 3 months from now
SELECT ADD_MONTHS(hire_date, -6) FROM employees;  -- 6 months before hire</pre>
<b>MySQL equivalent:</b>
<pre>SELECT DATE_ADD(CURDATE(), INTERVAL 3 MONTH);
SELECT hire_date + INTERVAL 3 MONTH FROM employees;</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is LAST_DAY and MONTHS_BETWEEN in Oracle?",
            "a": """<b>LAST_DAY</b> — returns the last day of the given month:
<pre>SELECT LAST_DAY(SYSDATE) FROM dual;</pre>
<b>MySQL:</b> <code>LAST_DAY(CURDATE())</code><br><br>
<b>MONTHS_BETWEEN</b> — months between two dates (Oracle only):
<pre>SELECT MONTHS_BETWEEN(SYSDATE, hire_date) FROM employees;</pre>
<b>MySQL equivalent:</b>
<pre>SELECT TIMESTAMPDIFF(MONTH, hire_date, CURDATE()) FROM employees;</pre>"""
        }
    ],

    # ── TO CHAR TO DATE ───────────────────────────────────────────────────────
    "to-char-to-date": [
        {
            "level": "Junior",
            "q": "What is TO_CHAR in Oracle and its MySQL equivalent?",
            "a": """<b>Oracle TO_CHAR — number to string:</b>
<pre>SELECT TO_CHAR(salary, '$999,999.00') FROM employees;  -- $085,000.00
SELECT TO_CHAR(SYSDATE, 'DD-MON-YYYY') FROM dual;       -- 15-JAN-2024</pre>
<b>MySQL equivalent:</b>
<pre>SELECT FORMAT(salary, 2) FROM employees;
SELECT DATE_FORMAT(NOW(), '%d-%b-%Y');</pre>"""
        },
        {
            "level": "Mid",
            "q": "What is TO_DATE in Oracle?",
            "a": """<b>TO_DATE</b> converts a string to a DATE using a format mask:
<pre>SELECT * FROM employees
WHERE hire_date > TO_DATE('01-JAN-2020', 'DD-MON-YYYY');</pre>
<b>MySQL equivalent:</b>
<pre>SELECT * FROM employees
WHERE hire_date > STR_TO_DATE('01-01-2020', '%d-%m-%Y');</pre>"""
        }
    ],

    # ── PIVOT UNPIVOT ─────────────────────────────────────────────────────────
    "pivot-unpivot": [
        {
            "level": "Mid",
            "q": "How do you PIVOT data in Oracle vs MySQL?",
            "a": """<b>Oracle (native PIVOT):</b>
<pre>SELECT * FROM (
  SELECT dept_id, grade FROM students
)
PIVOT (COUNT(*) FOR grade IN ('A' AS grade_A, 'B' AS grade_B, 'C' AS grade_C));</pre>
<b>MySQL (conditional aggregation):</b>
<pre>SELECT dept_id,
  SUM(CASE WHEN grade='A' THEN 1 ELSE 0 END) AS grade_A,
  SUM(CASE WHEN grade='B' THEN 1 ELSE 0 END) AS grade_B,
  SUM(CASE WHEN grade='C' THEN 1 ELSE 0 END) AS grade_C
FROM students GROUP BY dept_id;</pre>"""
        }
    ],

    # ── ROLLUP CUBE ───────────────────────────────────────────────────────────
    "rollup-cube": [
        {
            "level": "Senior",
            "q": "What is ROLLUP in SQL and how does it work?",
            "a": """<b>ROLLUP</b> adds subtotal and grand total rows automatically:
<b>MySQL 8+ / Oracle:</b>
<pre>SELECT dept_id, COUNT(*), SUM(salary)
FROM employees
GROUP BY ROLLUP(dept_id);
-- Produces: per dept rows + one NULL (grand total) row</pre>
<b>CUBE</b> produces ALL possible combinations of subtotals:
<pre>GROUP BY CUBE(dept_id, grade)</pre>
<b>GROUPING(col)</b> returns 1 for subtotal rows, 0 for regular:
<pre>SELECT CASE WHEN GROUPING(dept_id)=1 THEN 'TOTAL' ELSE CAST(dept_id AS CHAR) END AS dept,
  SUM(salary) FROM employees GROUP BY ROLLUP(dept_id);</pre>"""
        }
    ],

    # ── MERGE UPSERT ─────────────────────────────────────────────────────────
    "merge-upsert": [
        {
            "level": "Senior",
            "q": "What is MERGE and when would you use it?",
            "a": """MERGE (UPSERT) updates a row if it exists, inserts if it doesn't — atomically.
<b>Oracle:</b>
<pre>MERGE INTO employees t
USING (SELECT 1 AS id, 99000 AS salary FROM dual) s
ON (t.id = s.id)
WHEN MATCHED THEN UPDATE SET t.salary = s.salary
WHEN NOT MATCHED THEN INSERT (id, salary) VALUES (s.id, s.salary);</pre>
<b>MySQL:</b>
<pre>INSERT INTO employees (id, name, salary) VALUES (1, 'Alice', 99000)
ON DUPLICATE KEY UPDATE salary = 99000;</pre>
Used in ETL pipelines, data warehouses, and sync operations."""
        }
    ],

    # ── REGEXP ────────────────────────────────────────────────────────────────
    "regexp-pattern": [
        {
            "level": "Mid",
            "q": "How do you use REGEXP in MySQL?",
            "a": """<b>MySQL:</b>
<pre>SELECT * FROM employees WHERE name REGEXP '^[A-E]';   -- starts A-E
SELECT * FROM employees WHERE email REGEXP '@.*\\.com$';  -- .com emails</pre>
<b>Oracle (REGEXP_LIKE):</b>
<pre>SELECT * FROM employees WHERE REGEXP_LIKE(name, '^[A-E]');
SELECT * FROM employees WHERE REGEXP_LIKE(email, '@.*\\.com$');</pre>
Oracle also has: <code>REGEXP_REPLACE, REGEXP_SUBSTR, REGEXP_INSTR, REGEXP_COUNT</code>"""
        }
    ],

    # ── FETCH OFFSET ─────────────────────────────────────────────────────────
    "fetch-offset": [
        {
            "level": "Junior",
            "q": "How do you get the top 5 records in SQL Server, Oracle, and MySQL?",
            "a": """<table class='ops-table'>
<tr><th>Database</th><th>Syntax</th></tr>
<tr><td>MySQL</td><td>SELECT ... LIMIT 5</td></tr>
<tr><td>Oracle 12c+</td><td>SELECT ... FETCH FIRST 5 ROWS ONLY</td></tr>
<tr><td>Oracle &lt;12c</td><td>SELECT ... WHERE ROWNUM &lt;= 5</td></tr>
<tr><td>SQL Server</td><td>SELECT TOP 5 ...</td></tr>
<tr><td>PostgreSQL</td><td>SELECT ... LIMIT 5</td></tr>
</table>"""
        }
    ],

    # ── CONSTRAINTS ───────────────────────────────────────────────────────────
    "constraints-deep": [
        {
            "level": "Fresher",
            "q": "What are the types of constraints in SQL?",
            "a": "PRIMARY KEY, NOT NULL, UNIQUE, CHECK, DEFAULT, FOREIGN KEY. Constraints enforce data integrity rules at the database level — invalid data is rejected automatically."
        },
        {
            "level": "Junior",
            "q": "What is the difference between PRIMARY KEY and UNIQUE constraint?",
            "a": """<table class='ops-table'>
<tr><th></th><th>PRIMARY KEY</th><th>UNIQUE</th></tr>
<tr><td>Nulls allowed</td><td>No</td><td>Yes (one NULL in most DBs)</td></tr>
<tr><td>Count per table</td><td>Only one</td><td>Multiple allowed</td></tr>
<tr><td>Creates index</td><td>Yes (clustered in SQL Server)</td><td>Yes</td></tr>
</table>"""
        },
        {
            "level": "Mid",
            "q": "What are ON DELETE CASCADE and ON DELETE SET NULL?",
            "a": """Foreign key actions when the parent row is deleted:
<b>MySQL / Oracle:</b>
<pre>-- CASCADE: delete child rows automatically
FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE CASCADE

-- SET NULL: set child FK to NULL
FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE SET NULL

-- RESTRICT: prevent deletion if children exist (default)
FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE RESTRICT</pre>"""
        },
        {
            "level": "Senior",
            "q": "How do you add a constraint to an existing table?",
            "a": """<b>MySQL:</b>
<pre>ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary > 0);
ALTER TABLE employees ADD CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(id);</pre>
<b>Oracle:</b>
<pre>ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary > 0);
ALTER TABLE employees ADD CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(id);</pre>
Disable/enable without dropping (Oracle): <code>ALTER TABLE employees DISABLE CONSTRAINT chk_salary;</code>"""
        }
    ],

    # ── SEQUENCES ─────────────────────────────────────────────────────────────
    "sequences-autoincrement": [
        {
            "level": "Fresher",
            "q": "How does AUTO_INCREMENT work in MySQL?",
            "a": "MySQL automatically assigns the next available integer to AUTO_INCREMENT columns on INSERT. You don't supply the value — the database generates it. Use <code>LAST_INSERT_ID()</code> to retrieve the generated value after an INSERT."
        },
        {
            "level": "Mid",
            "q": "How do you create and use a SEQUENCE in Oracle?",
            "a": """<b>Oracle:</b>
<pre>CREATE SEQUENCE emp_seq
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  NOCYCLE;

-- Use it:
INSERT INTO employees (id, name) VALUES (emp_seq.NEXTVAL, 'Alice');

-- See current value:
SELECT emp_seq.CURRVAL FROM dual;</pre>
Oracle 12c+ supports IDENTITY columns: <code>id NUMBER GENERATED ALWAYS AS IDENTITY</code>"""
        }
    ],

    # ── TRIGGERS ─────────────────────────────────────────────────────────────
    "triggers": [
        {
            "level": "Mid",
            "q": "What is a trigger and when would you use one?",
            "a": "A trigger is automatic SQL that runs when INSERT, UPDATE, or DELETE occurs on a table. Use cases: audit logging, enforcing business rules, auto-updating derived columns, preventing invalid operations."
        },
        {
            "level": "Mid",
            "q": "What is the difference between BEFORE and AFTER triggers?",
            "a": "<b>BEFORE</b> — runs before the DML operation. Can modify NEW values or cancel the operation with RAISE/SIGNAL. Use for validation. <b>AFTER</b> — runs after the DML succeeds. Cannot stop the operation. Use for logging and cascading actions."
        },
        {
            "level": "Senior",
            "q": "How do you create an audit trigger in MySQL vs Oracle?",
            "a": """<b>MySQL:</b>
<pre>DELIMITER //
CREATE TRIGGER trg_audit_salary
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
  IF OLD.salary != NEW.salary THEN
    INSERT INTO salary_log(emp_id, old_sal, new_sal, changed_at)
    VALUES(OLD.id, OLD.salary, NEW.salary, NOW());
  END IF;
END //
DELIMITER ;</pre>
<b>Oracle:</b>
<pre>CREATE OR REPLACE TRIGGER trg_audit_salary
AFTER UPDATE OF salary ON employees
FOR EACH ROW
BEGIN
  IF :OLD.salary != :NEW.salary THEN
    INSERT INTO salary_log VALUES(:OLD.id, :OLD.salary, :NEW.salary, SYSDATE);
  END IF;
END;</pre>"""
        }
    ],

    # ── STORED PROCEDURES ─────────────────────────────────────────────────────
    "stored-procedures": [
        {
            "level": "Mid",
            "q": "What is the difference between a stored procedure and a function?",
            "a": """<table class='ops-table'>
<tr><th></th><th>Stored Procedure</th><th>Function</th></tr>
<tr><td>Returns</td><td>Nothing (or OUT params)</td><td>A value (RETURN)</td></tr>
<tr><td>Can call in SELECT</td><td>No</td><td>Yes</td></tr>
<tr><td>DML inside</td><td>Yes</td><td>Restricted (Oracle)</td></tr>
<tr><td>Called with</td><td>EXEC / CALL</td><td>Used in expressions</td></tr>
</table>"""
        },
        {
            "level": "Senior",
            "q": "How do you create a stored procedure in MySQL vs Oracle?",
            "a": """<b>MySQL:</b>
<pre>DELIMITER //
CREATE PROCEDURE give_raise(IN p_dept INT, IN p_pct DECIMAL(5,2))
BEGIN
  UPDATE employees
  SET salary = ROUND(salary * (1 + p_pct/100), 2)
  WHERE dept_id = p_dept;
END //
DELIMITER ;

-- Call it:
CALL give_raise(1, 10.0);</pre>
<b>Oracle:</b>
<pre>CREATE OR REPLACE PROCEDURE give_raise(p_dept IN NUMBER, p_pct IN NUMBER) AS
BEGIN
  UPDATE employees SET salary = ROUND(salary*(1+p_pct/100), 2)
  WHERE dept_id = p_dept;
  COMMIT;
END;
-- Execute:
EXEC give_raise(1, 10);</pre>"""
        }
    ],

    # ── CURSORS ───────────────────────────────────────────────────────────────
    "cursors": [
        {
            "level": "Mid",
            "q": "What is a cursor in SQL?",
            "a": "A cursor is a pointer to a result set that allows processing rows one at a time inside a stored procedure. Use them only when set-based operations can't solve the problem — they're significantly slower."
        },
        {
            "level": "Senior",
            "q": "What are implicit and explicit cursors in Oracle?",
            "a": """<b>Implicit cursor</b> — Oracle creates automatically for every DML/SELECT. Access via SQL%ROWCOUNT, SQL%FOUND etc.<br><br>
<b>Explicit cursor</b> — You define and control it manually:
<pre>DECLARE
  CURSOR emp_cur IS SELECT name, salary FROM employees;
  v_name employees.name%TYPE;
  v_sal  employees.salary%TYPE;
BEGIN
  OPEN emp_cur;
  LOOP
    FETCH emp_cur INTO v_name, v_sal;
    EXIT WHEN emp_cur%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE(v_name || ': ' || v_sal);
  END LOOP;
  CLOSE emp_cur;
END;</pre>"""
        }
    ],

    # ── SYNONYMS ──────────────────────────────────────────────────────────────
    "synonyms-aliases": [
        {
            "level": "Mid",
            "q": "What is a synonym in Oracle SQL?",
            "a": """A synonym is an alias for a database object (table, view, sequence):
<pre>-- Private synonym (for your schema):
CREATE SYNONYM emp FOR hr.employees;
SELECT * FROM emp;  -- same as hr.employees

-- Public synonym (all users can use):
CREATE PUBLIC SYNONYM emp FOR hr.employees;

-- Drop it:
DROP SYNONYM emp;</pre>
Useful for hiding schema names and providing database independence."""
        }
    ],

    # ── NORMALIZATION ─────────────────────────────────────────────────────────
    "normalization": [
        {
            "level": "Junior",
            "q": "What is database normalization?",
            "a": "Normalization is organising a database to reduce data redundancy and improve integrity. It involves decomposing tables according to Normal Forms (1NF, 2NF, 3NF, BCNF) so each piece of data is stored in only one place."
        },
        {
            "level": "Mid",
            "q": "Explain 1NF, 2NF, and 3NF with examples.",
            "a": """<b>1NF:</b> Atomic values, no repeating groups.<br>
Bad: <code>| Alice | Math, Science |</code><br>
Good: <code>| Alice | Math |</code> and <code>| Alice | Science |</code><br><br>
<b>2NF:</b> 1NF + no partial dependencies (non-key cols depend on full PK).<br>
In order_items, product_name should NOT be there because it depends only on product_id, not the full composite key.<br><br>
<b>3NF:</b> 2NF + no transitive dependencies (non-key col depending on another non-key col).<br>
dept_name depending on dept_id (not emp_id) → move dept_name to a departments table."""
        },
        {
            "level": "Senior",
            "q": "When would you deliberately denormalise a database?",
            "a": """Denormalisation (intentional redundancy) is used to improve read performance:
<ul>
<li>Data warehouses / reporting — star schemas, pre-aggregated columns</li>
<li>High-traffic read queries that join too many tables</li>
<li>Storing computed values to avoid recalculation</li>
</ul>
Tradeoffs: faster reads, but harder writes (must update redundant data), risk of inconsistency. Always normalise first, then denormalise with measurement."""
        }
    ],

    # ── QUERY OPTIMIZATION ────────────────────────────────────────────────────
    "query-optimization": [
        {
            "level": "Mid",
            "q": "How do you use EXPLAIN in MySQL?",
            "a": """<b>MySQL:</b>
<pre>EXPLAIN SELECT * FROM employees WHERE salary > 80000;</pre>
Key columns to check:
<ul>
<li><b>type</b>: ALL (full scan, bad) → ref/eq_ref/const (index used, good)</li>
<li><b>key</b>: which index was used (NULL = no index)</li>
<li><b>rows</b>: estimated rows scanned</li>
<li><b>Extra</b>: 'Using filesort', 'Using temporary' indicate performance issues</li>
</ul>"""
        },
        {
            "level": "Senior",
            "q": "How do you use EXPLAIN PLAN in Oracle?",
            "a": """<b>Oracle:</b>
<pre>EXPLAIN PLAN FOR
SELECT * FROM employees WHERE salary > 80000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);</pre>
Look for:
<ul>
<li><b>TABLE ACCESS FULL</b> — bad (no index used)</li>
<li><b>INDEX RANGE SCAN</b> — good</li>
<li><b>HASH JOIN vs NESTED LOOPS</b> — hash join better for large sets</li>
<li>Cardinality estimates — large differences from reality indicate stale stats → run <code>DBMS_STATS.GATHER_TABLE_STATS</code></li>
</ul>"""
        },
        {
            "level": "Senior",
            "q": "What is the N+1 query problem?",
            "a": """N+1 happens when you run 1 query to get N rows, then N more queries to get related data for each row (one per row).
<br><br>Example: fetch 100 employees, then 100 separate queries to get each department name.
<br><br><b>Fix:</b> Use a JOIN to get everything in one query:
<pre>SELECT e.name, d.name AS dept
FROM employees e JOIN departments d ON e.dept_id = d.id;</pre>
Very common in ORMs (Hibernate, ActiveRecord) — use eager loading to prevent it."""
        }
    ],

    # ── DECODE SIGN TRUNC (section for new slugs) ─────────────────────────────
    "lpad-rpad-initcap": [
        {
            "level": "Junior",
            "q": "What is the difference between LPAD and RPAD?",
            "a": """<b>LPAD</b> pads from the left (useful for right-aligning numbers).<br>
<b>RPAD</b> pads from the right (useful for left-aligning text).<br>
<b>MySQL:</b>
<pre>SELECT LPAD('42', 6, '0');   -- '000042'
SELECT RPAD('Hi', 8, '-');   -- 'Hi------'</pre>
<b>Oracle:</b>
<pre>SELECT LPAD('42', 6, '0') FROM dual;
SELECT RPAD('Hi', 8, '-') FROM dual;</pre>"""
        }
    ],
}
