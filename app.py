from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os
import json

app = Flask(__name__)
app.secret_key = "sql_course_secret_2024"

# ── Sandbox DB (per-user in memory via file per session) ──────────────────────
SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandboxes")
os.makedirs(SANDBOX_DIR, exist_ok=True)

SEED_SQL = """
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

CREATE TABLE departments (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    age        INTEGER,
    salary     REAL,
    dept_id    INTEGER REFERENCES departments(id),
    hire_date  TEXT
);

CREATE TABLE products (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    category TEXT,
    price    REAL,
    stock    INTEGER
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer    TEXT NOT NULL,
    order_date  TEXT,
    total       REAL
);

CREATE TABLE order_items (
    id         INTEGER PRIMARY KEY,
    order_id   INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    qty        INTEGER,
    unit_price REAL
);

CREATE TABLE students (
    id      INTEGER PRIMARY KEY,
    name    TEXT,
    grade   TEXT,
    score   INTEGER
);

CREATE TABLE courses (
    id         INTEGER PRIMARY KEY,
    title      TEXT,
    student_id INTEGER REFERENCES students(id),
    marks      INTEGER
);

INSERT INTO departments VALUES
  (1,'Engineering','New York'),
  (2,'Marketing','San Francisco'),
  (3,'Finance','Chicago'),
  (4,'HR','New York');

INSERT INTO employees VALUES
  (1,'Alice',30,85000,1,'2020-03-15'),
  (2,'Bob',28,72000,1,'2021-06-01'),
  (3,'Carol',35,95000,2,'2018-09-10'),
  (4,'David',42,110000,3,'2015-01-20'),
  (5,'Eve',26,65000,4,'2022-11-05'),
  (6,'Frank',38,88000,1,'2019-07-22'),
  (7,'Grace',31,77000,2,'2020-12-01'),
  (8,'Henry',45,120000,3,'2013-04-18'),
  (9,'Iris',29,70000,4,'2021-09-30'),
  (10,'Jack',33,93000,1,'2017-05-14');

INSERT INTO products VALUES
  (1,'Laptop','Electronics',999.99,50),
  (2,'Mouse','Electronics',29.99,200),
  (3,'Desk','Furniture',349.99,30),
  (4,'Chair','Furniture',199.99,45),
  (5,'Notebook','Stationery',4.99,500),
  (6,'Pen','Stationery',1.99,1000),
  (7,'Monitor','Electronics',399.99,75),
  (8,'Keyboard','Electronics',79.99,150);

INSERT INTO orders VALUES
  (1,'Alice','2024-01-10',1029.98),
  (2,'Bob','2024-01-15',349.99),
  (3,'Carol','2024-02-01',479.98),
  (4,'Alice','2024-02-20',6.98),
  (5,'David','2024-03-05',999.99);

INSERT INTO order_items VALUES
  (1,1,1,1,999.99),(2,1,2,1,29.99),
  (3,2,3,1,349.99),
  (4,3,4,1,199.99),(5,3,7,1,279.99),
  (6,4,5,1,4.99),(7,4,6,1,1.99),
  (8,5,1,1,999.99);

INSERT INTO students VALUES
  (1,'Liam','A',95),(2,'Mia','B',82),
  (3,'Noah','A',91),(4,'Ava','C',74),
  (5,'Ethan','B',85);

INSERT INTO courses VALUES
  (1,'Math',1,90),(2,'Science',1,95),
  (3,'Math',2,80),(4,'English',2,84),
  (5,'Science',3,92),(6,'Math',4,70),
  (7,'English',5,88),(8,'Science',5,82);
"""

def get_sandbox_db(uid):
    path = os.path.join(SANDBOX_DIR, f"user_{uid}.db")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn, path

def init_sandbox(uid):
    conn, _ = get_sandbox_db(uid)
    conn.executescript(SEED_SQL)
    conn.commit()
    conn.close()

# ── Course content ────────────────────────────────────────────────────────────
LESSONS = [
    {
        "id": 1, "slug": "intro",
        "title": "What is SQL?",
        "icon": "🗄️",
        "level": "Beginner",
        "theory": """
<h2>What is SQL?</h2>
<p><strong>SQL</strong> (Structured Query Language) is the language you use to talk to a database. Think of a database as a giant spreadsheet — SQL lets you search, add, update, and delete data in it.</p>
<h3>🍕 Real-world analogy</h3>
<p>Imagine a pizza restaurant's order book. SQL is how you ask:</p>
<ul>
  <li>"Show me all orders from today"</li>
  <li>"How many large pizzas did we sell?"</li>
  <li>"Add a new customer order"</li>
</ul>
<h3>📦 Tables</h3>
<p>Data lives in <strong>tables</strong> — just like Excel sheets. A table has <strong>rows</strong> (records) and <strong>columns</strong> (fields).</p>
<pre><code>employees table:
┌────┬───────┬─────┬────────┐
│ id │ name  │ age │ salary │
├────┼───────┼─────┼────────┤
│  1 │ Alice │  30 │ 85000  │
│  2 │ Bob   │  28 │ 72000  │
└────┴───────┴─────┴────────┘</code></pre>
<h3>📚 Tables in this course</h3>
<p>We'll use these tables throughout the course:</p>
<ul>
  <li><strong>employees</strong> — staff records with salary, age, department</li>
  <li><strong>departments</strong> — dept name and city</li>
  <li><strong>products</strong> — items with price and stock</li>
  <li><strong>orders / order_items</strong> — customer orders</li>
  <li><strong>students / courses</strong> — school data</li>
</ul>
""",
        "examples": [
            {"title": "See all employees", "sql": "SELECT * FROM employees;"},
            {"title": "See all departments", "sql": "SELECT * FROM departments;"},
            {"title": "See all products", "sql": "SELECT * FROM products;"},
        ],
        "challenge": {
            "question": "Write a query to see all rows from the <code>students</code> table.",
            "hint": "Use SELECT * FROM table_name;",
            "answer": "SELECT * FROM students;"
        }
    },
    {
        "id": 2, "slug": "select",
        "title": "SELECT — Fetching Data",
        "icon": "🔍",
        "level": "Beginner",
        "theory": """
<h2>SELECT — Fetching Data</h2>
<p><code>SELECT</code> is the most used SQL command. It retrieves data from a table.</p>
<h3>Syntax</h3>
<pre><code>SELECT column1, column2 FROM table_name;</code></pre>
<h3>🌟 Tips</h3>
<ul>
  <li>Use <code>*</code> to select ALL columns</li>
  <li>List specific columns to keep results clean</li>
  <li>Column names are separated by commas</li>
  <li>End every statement with <code>;</code></li>
</ul>
<h3>Renaming columns with AS</h3>
<p>You can rename a column in your result using <code>AS</code>:</p>
<pre><code>SELECT name AS employee_name, salary AS monthly_pay FROM employees;</code></pre>
""",
        "examples": [
            {"title": "Select all columns", "sql": "SELECT * FROM employees;"},
            {"title": "Select specific columns", "sql": "SELECT name, salary FROM employees;"},
            {"title": "Rename columns with AS", "sql": "SELECT name AS employee_name, salary AS pay\nFROM employees;"},
            {"title": "Select with math", "sql": "SELECT name, salary, salary * 12 AS annual_salary\nFROM employees;"},
        ],
        "challenge": {
            "question": "Select only the <code>name</code> and <code>price</code> columns from <code>products</code>, and rename <code>price</code> as <code>cost</code>.",
            "hint": "SELECT name, price AS cost FROM ...",
            "answer": "SELECT name, price AS cost FROM products;"
        }
    },
    {
        "id": 3, "slug": "where",
        "title": "WHERE — Filtering Rows",
        "icon": "🔎",
        "level": "Beginner",
        "theory": """
<h2>WHERE — Filtering Rows</h2>
<p><code>WHERE</code> filters which rows you get back. Only rows matching the condition are returned.</p>
<h3>Syntax</h3>
<pre><code>SELECT * FROM table WHERE condition;</code></pre>
<h3>🔧 Comparison Operators</h3>
<table class="ops-table">
  <tr><th>Operator</th><th>Meaning</th><th>Example</th></tr>
  <tr><td>=</td><td>Equal to</td><td>age = 30</td></tr>
  <tr><td>!= or &lt;&gt;</td><td>Not equal</td><td>age != 30</td></tr>
  <tr><td>&gt;</td><td>Greater than</td><td>salary &gt; 80000</td></tr>
  <tr><td>&lt;</td><td>Less than</td><td>age &lt; 35</td></tr>
  <tr><td>&gt;=</td><td>Greater or equal</td><td>salary &gt;= 90000</td></tr>
  <tr><td>BETWEEN</td><td>Range (inclusive)</td><td>age BETWEEN 25 AND 35</td></tr>
  <tr><td>LIKE</td><td>Pattern match</td><td>name LIKE 'A%'</td></tr>
  <tr><td>IN</td><td>Match a list</td><td>dept_id IN (1, 2)</td></tr>
  <tr><td>IS NULL</td><td>Value is missing</td><td>age IS NULL</td></tr>
</table>
<h3>🔗 Combining conditions</h3>
<ul>
  <li><strong>AND</strong> — both conditions must be true</li>
  <li><strong>OR</strong> — at least one must be true</li>
  <li><strong>NOT</strong> — reverses the condition</li>
</ul>
""",
        "examples": [
            {"title": "Equal filter", "sql": "SELECT * FROM employees\nWHERE dept_id = 1;"},
            {"title": "Greater than", "sql": "SELECT name, salary FROM employees\nWHERE salary > 90000;"},
            {"title": "BETWEEN range", "sql": "SELECT name, age FROM employees\nWHERE age BETWEEN 28 AND 35;"},
            {"title": "LIKE pattern (starts with A)", "sql": "SELECT * FROM employees\nWHERE name LIKE 'A%';"},
            {"title": "IN list", "sql": "SELECT * FROM employees\nWHERE dept_id IN (1, 3);"},
            {"title": "AND condition", "sql": "SELECT name, salary FROM employees\nWHERE dept_id = 1 AND salary > 80000;"},
            {"title": "OR condition", "sql": "SELECT * FROM products\nWHERE category = 'Electronics' OR price < 10;"},
        ],
        "challenge": {
            "question": "Find all products in the <code>Furniture</code> category with a price greater than 200.",
            "hint": "Use WHERE category = '...' AND price > ...",
            "answer": "SELECT * FROM products WHERE category = 'Furniture' AND price > 200;"
        }
    },
    {
        "id": 4, "slug": "order-limit",
        "title": "ORDER BY & LIMIT",
        "icon": "📊",
        "level": "Beginner",
        "theory": """
<h2>ORDER BY &amp; LIMIT</h2>
<h3>ORDER BY — Sort your results</h3>
<pre><code>SELECT * FROM table ORDER BY column ASC|DESC;</code></pre>
<ul>
  <li><strong>ASC</strong> = A→Z, 1→9 (default)</li>
  <li><strong>DESC</strong> = Z→A, 9→1</li>
  <li>You can sort by multiple columns: <code>ORDER BY dept_id, salary DESC</code></li>
</ul>
<h3>LIMIT — Cap the number of rows</h3>
<pre><code>SELECT * FROM table LIMIT 5;</code></pre>
<p>Only returns the first 5 rows. Great for previewing data or "top N" queries.</p>
<h3>OFFSET — Skip rows</h3>
<pre><code>SELECT * FROM table LIMIT 5 OFFSET 5;</code></pre>
<p>Skips the first 5, then returns the next 5 — useful for pagination.</p>
""",
        "examples": [
            {"title": "Sort by salary (highest first)", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC;"},
            {"title": "Sort by name A-Z", "sql": "SELECT name, age FROM employees\nORDER BY name ASC;"},
            {"title": "Top 3 highest paid", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC\nLIMIT 3;"},
            {"title": "Sort by dept then salary", "sql": "SELECT name, dept_id, salary FROM employees\nORDER BY dept_id ASC, salary DESC;"},
            {"title": "Page 2 (rows 6-10)", "sql": "SELECT * FROM employees\nLIMIT 5 OFFSET 5;"},
        ],
        "challenge": {
            "question": "Find the top 3 most expensive products. Show name and price.",
            "hint": "ORDER BY price DESC LIMIT 3",
            "answer": "SELECT name, price FROM products ORDER BY price DESC LIMIT 3;"
        }
    },
    {
        "id": 5, "slug": "aggregate",
        "title": "Aggregate Functions",
        "icon": "🔢",
        "level": "Intermediate",
        "theory": """
<h2>Aggregate Functions</h2>
<p>Aggregate functions <strong>calculate a single result from many rows</strong>.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>COUNT(*)</td><td>Count number of rows</td></tr>
  <tr><td>SUM(col)</td><td>Add up all values</td></tr>
  <tr><td>AVG(col)</td><td>Calculate average</td></tr>
  <tr><td>MAX(col)</td><td>Find the biggest value</td></tr>
  <tr><td>MIN(col)</td><td>Find the smallest value</td></tr>
</table>
<h3>🍕 Analogy</h3>
<p>If your table is a shopping receipt, aggregates answer:</p>
<ul>
  <li><strong>COUNT</strong> — how many items did I buy?</li>
  <li><strong>SUM</strong> — what's my total bill?</li>
  <li><strong>AVG</strong> — what's the average item price?</li>
  <li><strong>MAX/MIN</strong> — most/least expensive item?</li>
</ul>
<h3>DISTINCT</h3>
<p><code>COUNT(DISTINCT col)</code> counts unique values only.</p>
""",
        "examples": [
            {"title": "Count all employees", "sql": "SELECT COUNT(*) AS total_employees FROM employees;"},
            {"title": "Total salary bill", "sql": "SELECT SUM(salary) AS total_salaries FROM employees;"},
            {"title": "Average salary", "sql": "SELECT AVG(salary) AS avg_salary FROM employees;"},
            {"title": "Highest and lowest salary", "sql": "SELECT MAX(salary) AS highest, MIN(salary) AS lowest\nFROM employees;"},
            {"title": "Count distinct departments", "sql": "SELECT COUNT(DISTINCT dept_id) AS num_departments\nFROM employees;"},
            {"title": "Total value of stock", "sql": "SELECT SUM(price * stock) AS total_inventory_value\nFROM products;"},
        ],
        "challenge": {
            "question": "What is the average score of all students?",
            "hint": "Use AVG() on the score column",
            "answer": "SELECT AVG(score) AS average_score FROM students;"
        }
    },
    {
        "id": 6, "slug": "groupby",
        "title": "GROUP BY & HAVING",
        "icon": "📦",
        "level": "Intermediate",
        "theory": """
<h2>GROUP BY &amp; HAVING</h2>
<h3>GROUP BY — Group rows together</h3>
<p>GROUP BY splits rows into groups so you can run aggregates <em>per group</em>.</p>
<pre><code>SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id;</code></pre>
<p>This counts employees <strong>per department</strong> instead of the whole table.</p>
<h3>🍕 Analogy</h3>
<p>Instead of "how many total orders?", GROUP BY lets you ask "how many orders <strong>per customer</strong>?"</p>
<h3>HAVING — Filter groups</h3>
<p>HAVING is like WHERE, but for groups (after grouping):</p>
<pre><code>SELECT dept_id, AVG(salary)
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 80000;</code></pre>
<h3>⚠️ WHERE vs HAVING</h3>
<ul>
  <li><strong>WHERE</strong> filters rows <em>before</em> grouping</li>
  <li><strong>HAVING</strong> filters groups <em>after</em> grouping</li>
</ul>
""",
        "examples": [
            {"title": "Count employees per department", "sql": "SELECT dept_id, COUNT(*) AS headcount\nFROM employees\nGROUP BY dept_id;"},
            {"title": "Average salary per department", "sql": "SELECT dept_id, AVG(salary) AS avg_salary\nFROM employees\nGROUP BY dept_id;"},
            {"title": "Products count per category", "sql": "SELECT category, COUNT(*) AS num_products, AVG(price) AS avg_price\nFROM products\nGROUP BY category;"},
            {"title": "HAVING — depts with avg salary > 80k", "sql": "SELECT dept_id, AVG(salary) AS avg_sal\nFROM employees\nGROUP BY dept_id\nHAVING avg_sal > 80000;"},
            {"title": "WHERE + GROUP BY together", "sql": "SELECT dept_id, COUNT(*) AS count\nFROM employees\nWHERE age > 30\nGROUP BY dept_id;"},
        ],
        "challenge": {
            "question": "Show each grade and how many students have it, but only show grades with more than 1 student.",
            "hint": "GROUP BY grade HAVING COUNT(*) > 1",
            "answer": "SELECT grade, COUNT(*) AS count FROM students GROUP BY grade HAVING COUNT(*) > 1;"
        }
    },
    {
        "id": 7, "slug": "joins",
        "title": "JOINs — Combining Tables",
        "icon": "🔗",
        "level": "Intermediate",
        "theory": """
<h2>JOINs — Combining Tables</h2>
<p>A JOIN combines rows from two tables based on a related column.</p>
<h3>Types of JOINs</h3>
<table class="ops-table">
  <tr><th>Type</th><th>Returns</th></tr>
  <tr><td>INNER JOIN</td><td>Only rows with matches in BOTH tables</td></tr>
  <tr><td>LEFT JOIN</td><td>All rows from left + matched rows from right (NULL if no match)</td></tr>
  <tr><td>RIGHT JOIN</td><td>All from right + matched from left</td></tr>
  <tr><td>FULL OUTER JOIN</td><td>All rows from both tables</td></tr>
</table>
<h3>🍕 Analogy</h3>
<p>Employees table has <code>dept_id</code>. Departments table has <code>id</code> and <code>name</code>. JOIN connects them so you can see the department <em>name</em> next to each employee.</p>
<pre><code>SELECT e.name, d.name AS department
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;</code></pre>
<h3>Table Aliases</h3>
<p>Use short aliases (<code>e</code>, <code>d</code>) to avoid writing the full table name each time.</p>
""",
        "examples": [
            {"title": "INNER JOIN — employees with dept name", "sql": "SELECT e.name, e.salary, d.name AS department\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id;"},
            {"title": "LEFT JOIN — all depts even if no employees", "sql": "SELECT d.name AS department, e.name AS employee\nFROM departments d\nLEFT JOIN employees e ON d.id = e.dept_id;"},
            {"title": "JOIN with WHERE filter", "sql": "SELECT e.name, d.name AS dept, e.salary\nFROM employees e\nJOIN departments d ON e.dept_id = d.id\nWHERE d.city = 'New York';"},
            {"title": "JOIN with aggregate", "sql": "SELECT d.name, COUNT(e.id) AS headcount, AVG(e.salary) AS avg_salary\nFROM departments d\nLEFT JOIN employees e ON d.id = e.dept_id\nGROUP BY d.name;"},
            {"title": "3-table JOIN — orders with items", "sql": "SELECT o.customer, p.name AS product, oi.qty, oi.unit_price\nFROM orders o\nJOIN order_items oi ON o.id = oi.order_id\nJOIN products p ON oi.product_id = p.id;"},
        ],
        "challenge": {
            "question": "Show each student's name alongside their course titles and marks. Use a JOIN on students and courses.",
            "hint": "JOIN students s ON s.id = c.student_id",
            "answer": "SELECT s.name, c.title, c.marks FROM students s JOIN courses c ON s.id = c.student_id;"
        }
    },
    {
        "id": 8, "slug": "subquery",
        "title": "Subqueries",
        "icon": "🪆",
        "level": "Intermediate",
        "theory": """
<h2>Subqueries</h2>
<p>A subquery is a query <strong>inside another query</strong>. The inner query runs first, and its result is used by the outer query.</p>
<h3>🪆 Analogy</h3>
<p>Like a Russian doll — one query hidden inside another.</p>
<pre><code>SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);</code></pre>
<p>The inner query finds the average salary. The outer query finds everyone earning above it.</p>
<h3>Where can subqueries go?</h3>
<ul>
  <li>In <strong>WHERE</strong>: filter by a subquery result</li>
  <li>In <strong>FROM</strong>: use a subquery as a temporary table</li>
  <li>In <strong>SELECT</strong>: compute a value per row</li>
</ul>
<h3>IN with subquery</h3>
<pre><code>SELECT name FROM employees
WHERE dept_id IN (SELECT id FROM departments WHERE city = 'New York');</code></pre>
""",
        "examples": [
            {"title": "Above-average salary", "sql": "SELECT name, salary FROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);"},
            {"title": "Employees in NY departments", "sql": "SELECT name FROM employees\nWHERE dept_id IN (\n  SELECT id FROM departments WHERE city = 'New York'\n);"},
            {"title": "Most expensive product", "sql": "SELECT * FROM products\nWHERE price = (SELECT MAX(price) FROM products);"},
            {"title": "Subquery in FROM (derived table)", "sql": "SELECT dept_id, avg_sal\nFROM (\n  SELECT dept_id, AVG(salary) AS avg_sal\n  FROM employees\n  GROUP BY dept_id\n) AS dept_avg\nWHERE avg_sal > 85000;"},
            {"title": "Subquery in SELECT", "sql": "SELECT name, salary,\n  (SELECT AVG(salary) FROM employees) AS company_avg\nFROM employees;"},
        ],
        "challenge": {
            "question": "Find all students whose score is above the average score of all students.",
            "hint": "WHERE score > (SELECT AVG(score) FROM students)",
            "answer": "SELECT name, score FROM students WHERE score > (SELECT AVG(score) FROM students);"
        }
    },
    {
        "id": 9, "slug": "insert-update-delete",
        "title": "INSERT, UPDATE, DELETE",
        "icon": "✏️",
        "level": "Intermediate",
        "theory": """
<h2>INSERT, UPDATE, DELETE</h2>
<p>These three commands modify data in a table.</p>
<h3>INSERT — Add new rows</h3>
<pre><code>INSERT INTO table (col1, col2) VALUES (val1, val2);</code></pre>
<h3>UPDATE — Change existing rows</h3>
<pre><code>UPDATE table SET col1 = val1 WHERE condition;</code></pre>
<p>⚠️ <strong>Always use WHERE with UPDATE!</strong> Without it, every row gets updated.</p>
<h3>DELETE — Remove rows</h3>
<pre><code>DELETE FROM table WHERE condition;</code></pre>
<p>⚠️ <strong>Always use WHERE with DELETE!</strong> Without it, all rows are deleted.</p>
<h3>💡 Note</h3>
<p>After running these queries, use <code>SELECT * FROM ...</code> to see the effect.</p>
""",
        "examples": [
            {"title": "INSERT a new employee", "sql": "INSERT INTO employees (name, age, salary, dept_id, hire_date)\nVALUES ('Zara', 27, 68000, 2, '2024-01-01');\n\nSELECT * FROM employees ORDER BY id DESC LIMIT 3;"},
            {"title": "UPDATE salary", "sql": "UPDATE employees SET salary = 90000\nWHERE name = 'Bob';\n\nSELECT name, salary FROM employees WHERE name = 'Bob';"},
            {"title": "Give all Engineering employees a raise", "sql": "UPDATE employees SET salary = salary * 1.10\nWHERE dept_id = 1;\n\nSELECT name, salary FROM employees WHERE dept_id = 1;"},
            {"title": "DELETE a specific row", "sql": "DELETE FROM employees WHERE name = 'Zara';\n\nSELECT * FROM employees ORDER BY id DESC LIMIT 3;"},
        ],
        "challenge": {
            "question": "Insert a new student named 'Sam' with grade 'A' and score 97, then select all students.",
            "hint": "INSERT INTO students (name, grade, score) VALUES (...);",
            "answer": "INSERT INTO students (name, grade, score) VALUES ('Sam', 'A', 97);\nSELECT * FROM students;"
        }
    },
    {
        "id": 10, "slug": "advanced",
        "title": "Advanced — CTEs & Window Functions",
        "icon": "🚀",
        "level": "Advanced",
        "theory": """
<h2>Advanced SQL</h2>
<h3>CTEs (Common Table Expressions)</h3>
<p>A CTE is a <strong>named temporary result</strong> you define with <code>WITH</code>. It makes complex queries readable.</p>
<pre><code>WITH dept_stats AS (
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM employees
  GROUP BY dept_id
)
SELECT e.name, e.salary, ds.avg_sal
FROM employees e
JOIN dept_stats ds ON e.dept_id = ds.dept_id;</code></pre>
<h3>Window Functions</h3>
<p>Window functions compute a value for each row <strong>using related rows</strong>, without collapsing them like GROUP BY.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>ROW_NUMBER()</td><td>Sequential row number per group</td></tr>
  <tr><td>RANK()</td><td>Rank (ties share same rank, gaps after)</td></tr>
  <tr><td>DENSE_RANK()</td><td>Rank (ties share same rank, no gaps)</td></tr>
  <tr><td>SUM() OVER()</td><td>Running total</td></tr>
  <tr><td>LAG() / LEAD()</td><td>Access previous/next row</td></tr>
</table>
<pre><code>SELECT name, salary,
  RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;</code></pre>
""",
        "examples": [
            {"title": "CTE — dept averages then filter", "sql": "WITH dept_avg AS (\n  SELECT dept_id, AVG(salary) AS avg_sal\n  FROM employees GROUP BY dept_id\n)\nSELECT e.name, e.salary, ROUND(da.avg_sal,2) AS dept_avg\nFROM employees e\nJOIN dept_avg da ON e.dept_id = da.dept_id\nWHERE e.salary > da.avg_sal;"},
            {"title": "RANK by salary", "sql": "SELECT name, salary,\n  RANK() OVER (ORDER BY salary DESC) AS rank\nFROM employees;"},
            {"title": "ROW_NUMBER per department", "sql": "SELECT name, dept_id, salary,\n  ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rank_in_dept\nFROM employees;"},
            {"title": "Running total of salaries", "sql": "SELECT name, salary,\n  SUM(salary) OVER (ORDER BY id) AS running_total\nFROM employees;"},
            {"title": "Top earner per department", "sql": "SELECT * FROM (\n  SELECT name, dept_id, salary,\n    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk\n  FROM employees\n) WHERE rnk = 1;"},
        ],
        "challenge": {
            "question": "Use a window function to rank students by their score (highest = rank 1).",
            "hint": "RANK() OVER (ORDER BY score DESC)",
            "answer": "SELECT name, score, RANK() OVER (ORDER BY score DESC) AS rank FROM students;"
        }
    },
]

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", lessons=LESSONS)

@app.route("/lesson/<slug>")
def lesson(slug):
    les = next((l for l in LESSONS if l["slug"] == slug), None)
    if not les:
        return "Lesson not found", 404
    uid = session.get("uid")
    if not uid:
        import uuid
        uid = str(uuid.uuid4())[:8]
        session["uid"] = uid
        init_sandbox(uid)
    idx = LESSONS.index(les)
    prev_lesson = LESSONS[idx - 1] if idx > 0 else None
    next_lesson = LESSONS[idx + 1] if idx < len(LESSONS) - 1 else None
    return render_template("lesson.html", lesson=les, lessons=LESSONS,
                           prev_lesson=prev_lesson, next_lesson=next_lesson)

@app.route("/run_sql", methods=["POST"])
def run_sql():
    uid = session.get("uid")
    if not uid:
        return jsonify({"error": "Session expired. Please refresh the page."})
    data = request.get_json()
    sql = data.get("sql", "").strip()
    if not sql:
        return jsonify({"error": "No SQL provided."})
    # Safety: block dangerous statements for the sandbox
    blocked = ["DROP TABLE", "DROP DATABASE", "ATTACH", "DETACH", ".import"]
    upper_sql = sql.upper()
    for b in blocked:
        if b in upper_sql:
            return jsonify({"error": f"'{b}' is not allowed in the sandbox."})
    try:
        conn, _ = get_sandbox_db(uid)
        results = []
        # Execute multiple statements
        for stmt in sql.split(";"):
            stmt = stmt.strip()
            if not stmt:
                continue
            cur = conn.execute(stmt)
            if cur.description:
                cols = [d[0] for d in cur.description]
                rows = [list(r) for r in cur.fetchall()]
                results.append({"columns": cols, "rows": rows,
                                 "rowcount": len(rows), "type": "select"})
            else:
                conn.commit()
                results.append({"message": f"✅ Done. {cur.rowcount} row(s) affected.",
                                 "type": "modify"})
        conn.close()
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/reset_sandbox", methods=["POST"])
def reset_sandbox():
    uid = session.get("uid")
    if uid:
        init_sandbox(uid)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
