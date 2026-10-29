from flask import Flask, render_template, request, jsonify, session, Response
import sqlite3
import os
import json
from datetime import datetime
from interview_data import INTERVIEW_QA

app = Flask(__name__)
app.secret_key = "sql_course_secret_2024"

# ── Sandbox DB ────────────────────────────────────────────────────────────────
SANDBOX_DIR = os.environ.get("SANDBOX_DIR", os.path.join(os.path.dirname(__file__), "sandboxes"))
os.makedirs(SANDBOX_DIR, exist_ok=True)

SEED_SQL = """
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS inventory;

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
    hire_date  TEXT,
    email      TEXT,
    phone      TEXT
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
    total       REAL,
    status      TEXT DEFAULT 'pending'
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
    score   INTEGER,
    email   TEXT
);

CREATE TABLE courses (
    id         INTEGER PRIMARY KEY,
    title      TEXT,
    student_id INTEGER REFERENCES students(id),
    marks      INTEGER
);

CREATE TABLE customers (
    id      INTEGER PRIMARY KEY,
    name    TEXT,
    city    TEXT,
    country TEXT,
    joined  TEXT
);

CREATE TABLE inventory (
    id         INTEGER PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity   INTEGER,
    updated_at TEXT
);

INSERT INTO departments VALUES
  (1,'Engineering','New York'),
  (2,'Marketing','San Francisco'),
  (3,'Finance','Chicago'),
  (4,'HR','New York');

INSERT INTO employees VALUES
  (1,'Alice',30,85000,1,'2020-03-15','alice@company.com','555-1001'),
  (2,'Bob',28,72000,1,'2021-06-01','bob@company.com','555-1002'),
  (3,'Carol',35,95000,2,'2018-09-10','carol@company.com','555-1003'),
  (4,'David',42,110000,3,'2015-01-20','david@company.com','555-1004'),
  (5,'Eve',26,65000,4,'2022-11-05','eve@company.com','555-1005'),
  (6,'Frank',38,88000,1,'2019-07-22','frank@company.com','555-1006'),
  (7,'Grace',31,77000,2,'2020-12-01','grace@company.com','555-1007'),
  (8,'Henry',45,120000,3,'2013-04-18','henry@company.com','555-1008'),
  (9,'Iris',29,70000,4,'2021-09-30','iris@company.com','555-1009'),
  (10,'Jack',33,93000,1,'2017-05-14','jack@company.com','555-1010');

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
  (1,'Alice','2024-01-10',1029.98,'completed'),
  (2,'Bob','2024-01-15',349.99,'completed'),
  (3,'Carol','2024-02-01',479.98,'pending'),
  (4,'Alice','2024-02-20',6.98,'completed'),
  (5,'David','2024-03-05',999.99,'shipped');

INSERT INTO order_items VALUES
  (1,1,1,1,999.99),(2,1,2,1,29.99),
  (3,2,3,1,349.99),
  (4,3,4,1,199.99),(5,3,7,1,279.99),
  (6,4,5,1,4.99),(7,4,6,1,1.99),
  (8,5,1,1,999.99);

INSERT INTO students VALUES
  (1,'Liam','A',95,'liam@school.com'),
  (2,'Mia','B',82,'mia@school.com'),
  (3,'Noah','A',91,'noah@school.com'),
  (4,'Ava','C',74,'ava@school.com'),
  (5,'Ethan','B',85,'ethan@school.com');

INSERT INTO courses VALUES
  (1,'Math',1,90),(2,'Science',1,95),
  (3,'Math',2,80),(4,'English',2,84),
  (5,'Science',3,92),(6,'Math',4,70),
  (7,'English',5,88),(8,'Science',5,82);

INSERT INTO customers VALUES
  (1,'Alice Smith','New York','USA','2022-01-15'),
  (2,'Bob Jones','London','UK','2021-06-20'),
  (3,'Carol White','Paris','France','2023-03-10'),
  (4,'David Brown','Sydney','Australia','2020-11-05'),
  (5,'Eve Davis','Toronto','Canada','2022-08-18');

INSERT INTO inventory VALUES
  (1,1,50,'2024-01-01'),
  (2,2,200,'2024-01-01'),
  (3,3,30,'2024-01-01'),
  (4,4,45,'2024-01-01'),
  (5,5,500,'2024-01-01');
"""

# ── Full Curriculum ───────────────────────────────────────────────────────────
CURRICULUM = [
    {
        "id": "basics",
        "title": "SQL Basics",
        "icon": "🗄️",
        "lessons": [
            {
                "slug": "what-is-sql",
                "title": "What is SQL?",
                "theory": """
<h2>What is SQL?</h2>
<p><strong>SQL</strong> (Structured Query Language) is the language used to communicate with a relational database. Think of a database as a giant organised filing cabinet — SQL is how you search through it, add to it, change it, or remove from it.</p>
<h3>🍕 Real-world analogy</h3>
<p>Imagine a pizza restaurant's order book. SQL lets you ask:</p>
<ul>
  <li>"Show me all orders from today"</li>
  <li>"How many large pizzas did we sell this week?"</li>
  <li>"Update table 5's order to add a garlic bread"</li>
</ul>
<h3>📦 Tables, Rows & Columns</h3>
<p>Data lives in <strong>tables</strong> — just like Excel sheets. Each table has:</p>
<ul>
  <li><strong>Rows</strong> (records) — one entry per item</li>
  <li><strong>Columns</strong> (fields) — the attributes of each item</li>
</ul>
<pre><code>employees table:
┌────┬───────┬─────┬────────┐
│ id │ name  │ age │ salary │
├────┼───────┼─────┼────────┤
│  1 │ Alice │  30 │ 85000  │
│  2 │ Bob   │  28 │ 72000  │
└────┴───────┴─────┴────────┘</code></pre>
<h3>📚 Tables available in this course</h3>
<ul>
  <li><strong>employees</strong> — staff with salary, age, department, email</li>
  <li><strong>departments</strong> — dept name and city</li>
  <li><strong>products</strong> — items with price and stock</li>
  <li><strong>orders / order_items</strong> — customer orders</li>
  <li><strong>students / courses</strong> — school records</li>
  <li><strong>customers</strong> — customer info with country</li>
  <li><strong>inventory</strong> — stock levels</li>
</ul>
<h3>🔤 SQL is NOT case-sensitive</h3>
<p><code>SELECT</code> and <code>select</code> are the same. By convention, SQL keywords are written in UPPERCASE.</p>
""",
                "examples": [
                    {"title": "View all employees", "sql": "SELECT * FROM employees;"},
                    {"title": "View all tables data", "sql": "SELECT * FROM departments;"},
                    {"title": "View products", "sql": "SELECT * FROM products;"},
                ],
                "challenge": {
                    "question": "Run a query to see all rows from the <code>customers</code> table.",
                    "hint": "SELECT * FROM table_name;",
                    "answer": "SELECT * FROM customers;"
                }
            },
            {
                "slug": "select",
                "title": "SELECT Statement",
                "theory": """
<h2>SELECT Statement</h2>
<p><code>SELECT</code> is the most used SQL command — it retrieves data from a table.</p>
<h3>Syntax</h3>
<pre><code>SELECT column1, column2 FROM table_name;</code></pre>
<h3>Tips</h3>
<ul>
  <li>Use <code>*</code> to select ALL columns</li>
  <li>List specific columns to keep results clean</li>
  <li>End every statement with <code>;</code></li>
</ul>
<h3>Column Aliases (AS)</h3>
<p>Rename a column in the result using <code>AS</code>:</p>
<pre><code>SELECT name AS employee_name, salary AS pay FROM employees;</code></pre>
<h3>DISTINCT — remove duplicates</h3>
<pre><code>SELECT DISTINCT category FROM products;</code></pre>
<h3>Expressions in SELECT</h3>
<pre><code>SELECT name, salary * 12 AS annual_salary FROM employees;</code></pre>
""",
                "examples": [
                    {"title": "Select all columns", "sql": "SELECT * FROM employees;"},
                    {"title": "Select specific columns", "sql": "SELECT name, salary FROM employees;"},
                    {"title": "Column alias with AS", "sql": "SELECT name AS employee_name,\n       salary AS monthly_pay\nFROM employees;"},
                    {"title": "Math expression", "sql": "SELECT name, salary,\n       salary * 12 AS annual_salary\nFROM employees;"},
                    {"title": "DISTINCT values", "sql": "SELECT DISTINCT category FROM products;"},
                    {"title": "DISTINCT count", "sql": "SELECT COUNT(DISTINCT category) AS categories\nFROM products;"},
                ],
                "challenge": {
                    "question": "Select <code>name</code> and <code>price</code> from <code>products</code>, rename price as <code>cost</code>.",
                    "hint": "SELECT name, price AS cost FROM ...",
                    "answer": "SELECT name, price AS cost FROM products;"
                }
            },
            {
                "slug": "where",
                "title": "WHERE Clause",
                "theory": """
<h2>WHERE Clause</h2>
<p><code>WHERE</code> filters which rows you get back. Only rows matching the condition are returned.</p>
<pre><code>SELECT * FROM employees WHERE salary > 80000;</code></pre>
<h3>Comparison Operators</h3>
<table class="ops-table">
  <tr><th>Operator</th><th>Meaning</th></tr>
  <tr><td>=</td><td>Equal to</td></tr>
  <tr><td>!= or &lt;&gt;</td><td>Not equal</td></tr>
  <tr><td>&gt; / &lt;</td><td>Greater / Less than</td></tr>
  <tr><td>&gt;= / &lt;=</td><td>Greater/Less or equal</td></tr>
  <tr><td>BETWEEN a AND b</td><td>Range (inclusive)</td></tr>
  <tr><td>LIKE 'A%'</td><td>Pattern match</td></tr>
  <tr><td>IN (1,2,3)</td><td>Match a list</td></tr>
  <tr><td>IS NULL / IS NOT NULL</td><td>Check for missing value</td></tr>
</table>
<h3>Logical Operators</h3>
<ul>
  <li><strong>AND</strong> — both conditions must be true</li>
  <li><strong>OR</strong> — at least one must be true</li>
  <li><strong>NOT</strong> — reverses the condition</li>
</ul>
<h3>LIKE Wildcards</h3>
<ul>
  <li><code>%</code> — any sequence of characters (e.g. <code>'A%'</code> = starts with A)</li>
  <li><code>_</code> — exactly one character (e.g. <code>'_ob'</code> matches Bob, Rob)</li>
</ul>
""",
                "examples": [
                    {"title": "Equal filter", "sql": "SELECT * FROM employees WHERE dept_id = 1;"},
                    {"title": "Greater than", "sql": "SELECT name, salary FROM employees\nWHERE salary > 90000;"},
                    {"title": "BETWEEN range", "sql": "SELECT name, age FROM employees\nWHERE age BETWEEN 28 AND 35;"},
                    {"title": "LIKE — starts with A", "sql": "SELECT * FROM employees\nWHERE name LIKE 'A%';"},
                    {"title": "LIKE — ends with e", "sql": "SELECT * FROM employees\nWHERE name LIKE '%e';"},
                    {"title": "IN list", "sql": "SELECT * FROM employees\nWHERE dept_id IN (1, 3);"},
                    {"title": "AND condition", "sql": "SELECT name, salary FROM employees\nWHERE dept_id = 1 AND salary > 80000;"},
                    {"title": "OR condition", "sql": "SELECT * FROM products\nWHERE category = 'Electronics' OR price < 10;"},
                    {"title": "NOT condition", "sql": "SELECT * FROM products\nWHERE category NOT IN ('Electronics');"},
                ],
                "challenge": {
                    "question": "Find all products in <code>Furniture</code> category with price greater than 200.",
                    "hint": "WHERE category = '...' AND price > ...",
                    "answer": "SELECT * FROM products WHERE category = 'Furniture' AND price > 200;"
                }
            },
            {
                "slug": "order-limit",
                "title": "ORDER BY & LIMIT",
                "theory": """
<h2>ORDER BY & LIMIT</h2>
<h3>ORDER BY — Sort results</h3>
<pre><code>SELECT * FROM employees ORDER BY salary DESC;</code></pre>
<ul>
  <li><strong>ASC</strong> = smallest to largest (default)</li>
  <li><strong>DESC</strong> = largest to smallest</li>
  <li>Sort by multiple columns: <code>ORDER BY dept_id, salary DESC</code></li>
</ul>
<h3>LIMIT — cap number of rows</h3>
<pre><code>SELECT * FROM employees ORDER BY salary DESC LIMIT 5;</code></pre>
<h3>OFFSET — skip rows (pagination)</h3>
<pre><code>SELECT * FROM employees LIMIT 5 OFFSET 5; -- rows 6-10</code></pre>
<h3>TOP N pattern</h3>
<p>Combine ORDER BY + LIMIT to get top/bottom N records.</p>
""",
                "examples": [
                    {"title": "Sort by salary descending", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC;"},
                    {"title": "Sort by name A-Z", "sql": "SELECT name, age FROM employees\nORDER BY name ASC;"},
                    {"title": "Top 3 highest paid", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC LIMIT 3;"},
                    {"title": "Sort by multiple columns", "sql": "SELECT name, dept_id, salary FROM employees\nORDER BY dept_id ASC, salary DESC;"},
                    {"title": "Pagination — page 2", "sql": "SELECT * FROM employees\nLIMIT 5 OFFSET 5;"},
                    {"title": "Cheapest 3 products", "sql": "SELECT name, price FROM products\nORDER BY price ASC LIMIT 3;"},
                ],
                "challenge": {
                    "question": "Find the top 3 most expensive products. Show name and price.",
                    "hint": "ORDER BY price DESC LIMIT 3",
                    "answer": "SELECT name, price FROM products ORDER BY price DESC LIMIT 3;"
                }
            },
        ]
    },
    {
        "id": "functions",
        "title": "SQL Functions",
        "icon": "⚙️",
        "lessons": [
            {
                "slug": "char-functions",
                "title": "Character Functions",
                "theory": """
<h2>Character (String) Functions</h2>
<p>Character functions manipulate text/string values.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th><th>Example</th></tr>
  <tr><td>UPPER(s)</td><td>Convert to uppercase</td><td>UPPER('hello') → 'HELLO'</td></tr>
  <tr><td>LOWER(s)</td><td>Convert to lowercase</td><td>LOWER('HELLO') → 'hello'</td></tr>
  <tr><td>LENGTH(s)</td><td>Number of characters</td><td>LENGTH('Alice') → 5</td></tr>
  <tr><td>SUBSTR(s,start,len)</td><td>Extract part of string</td><td>SUBSTR('Alice',1,3) → 'Ali'</td></tr>
  <tr><td>TRIM(s)</td><td>Remove spaces from both ends</td><td>TRIM('  hi  ') → 'hi'</td></tr>
  <tr><td>LTRIM(s)</td><td>Remove leading spaces</td><td>LTRIM('  hi') → 'hi'</td></tr>
  <tr><td>RTRIM(s)</td><td>Remove trailing spaces</td><td>RTRIM('hi  ') → 'hi'</td></tr>
  <tr><td>REPLACE(s,old,new)</td><td>Replace substring</td><td>REPLACE('hi world','world','SQL')</td></tr>
  <tr><td>INSTR(s,sub)</td><td>Position of substring</td><td>INSTR('hello','ll') → 3</td></tr>
  <tr><td>s1 || s2</td><td>Concatenate strings</td><td>'Hello' || ' ' || 'World'</td></tr>
</table>
<h3>💡 Tip</h3>
<p>SQLite uses <code>SUBSTR</code> (1-indexed). Standard SQL uses <code>SUBSTRING(s FROM start FOR len)</code>.</p>
""",
                "examples": [
                    {"title": "UPPER & LOWER", "sql": "SELECT name,\n       UPPER(name) AS upper_name,\n       LOWER(name) AS lower_name\nFROM employees;"},
                    {"title": "LENGTH", "sql": "SELECT name, LENGTH(name) AS name_length\nFROM employees\nORDER BY name_length DESC;"},
                    {"title": "SUBSTR — first 3 chars", "sql": "SELECT name, SUBSTR(name, 1, 3) AS short_name\nFROM employees;"},
                    {"title": "REPLACE", "sql": "SELECT email,\n       REPLACE(email, '@company.com', '@corp.io') AS new_email\nFROM employees;"},
                    {"title": "Concatenate with ||", "sql": "SELECT name || ' works in dept ' || dept_id AS description\nFROM employees;"},
                    {"title": "INSTR — find position", "sql": "SELECT email,\n       INSTR(email, '@') AS at_position\nFROM employees;"},
                    {"title": "TRIM spaces", "sql": "SELECT TRIM('   Hello SQL   ') AS trimmed;"},
                    {"title": "Extract domain from email", "sql": "SELECT name,\n       SUBSTR(email, INSTR(email,'@')+1) AS domain\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Show each employee's name in UPPERCASE and the length of their name. Name the columns <code>upper_name</code> and <code>name_len</code>.",
                    "hint": "SELECT UPPER(name), LENGTH(name) ...",
                    "answer": "SELECT UPPER(name) AS upper_name, LENGTH(name) AS name_len FROM employees;"
                }
            },
            {
                "slug": "number-functions",
                "title": "Number Functions",
                "theory": """
<h2>Number Functions</h2>
<p>Number functions perform mathematical operations on numeric columns.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>ROUND(n, d)</td><td>Round to d decimal places</td></tr>
  <tr><td>CEIL(n) / CEILING(n)</td><td>Round UP to nearest integer</td></tr>
  <tr><td>FLOOR(n)</td><td>Round DOWN to nearest integer</td></tr>
  <tr><td>ABS(n)</td><td>Absolute value (removes negative sign)</td></tr>
  <tr><td>MOD(n, m)</td><td>Remainder after division (n % m)</td></tr>
  <tr><td>POWER(n, p)</td><td>n raised to power p</td></tr>
  <tr><td>SQRT(n)</td><td>Square root</td></tr>
  <tr><td>MAX(col)</td><td>Largest value</td></tr>
  <tr><td>MIN(col)</td><td>Smallest value</td></tr>
</table>
<h3>Arithmetic operators</h3>
<p>You can use <code>+  -  *  /  %</code> directly in SELECT:</p>
<pre><code>SELECT salary, salary * 1.10 AS after_raise FROM employees;</code></pre>
""",
                "examples": [
                    {"title": "ROUND", "sql": "SELECT name, salary,\n       ROUND(salary / 12, 2) AS monthly_salary\nFROM employees;"},
                    {"title": "CEIL & FLOOR", "sql": "SELECT price,\n       CEIL(price)  AS rounded_up,\n       FLOOR(price) AS rounded_down\nFROM products;"},
                    {"title": "ABS", "sql": "SELECT ABS(-250) AS absolute_value,\n       ABS(salary - 80000) AS diff_from_80k\nFROM employees;"},
                    {"title": "MOD — even/odd salary", "sql": "SELECT name, salary,\n       salary % 2 AS is_odd\nFROM employees;"},
                    {"title": "POWER & SQRT", "sql": "SELECT POWER(3, 4) AS three_to_four,\n       SQRT(144)  AS sqrt_144;"},
                    {"title": "10% salary raise", "sql": "SELECT name, salary,\n       ROUND(salary * 1.10, 2) AS new_salary\nFROM employees;"},
                    {"title": "Total inventory value", "sql": "SELECT name, price, stock,\n       ROUND(price * stock, 2) AS total_value\nFROM products\nORDER BY total_value DESC;"},
                ],
                "challenge": {
                    "question": "Show each product's name, price rounded to 1 decimal place, and the price after a 15% discount (rounded to 2 decimal places).",
                    "hint": "ROUND(price * 0.85, 2)",
                    "answer": "SELECT name, ROUND(price,1) AS price, ROUND(price*0.85,2) AS discounted FROM products;"
                }
            },
            {
                "slug": "date-functions",
                "title": "Date & Time Functions",
                "theory": """
<h2>Date & Time Functions</h2>
<p>Date functions work with date and time values. SQLite stores dates as text in <code>YYYY-MM-DD</code> format.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>DATE('now')</td><td>Today's date</td></tr>
  <tr><td>DATETIME('now')</td><td>Current date and time</td></tr>
  <tr><td>strftime('%Y', date)</td><td>Extract year from date</td></tr>
  <tr><td>strftime('%m', date)</td><td>Extract month (01-12)</td></tr>
  <tr><td>strftime('%d', date)</td><td>Extract day (01-31)</td></tr>
  <tr><td>DATE(date, '+N days')</td><td>Add N days to date</td></tr>
  <tr><td>DATE(date, '-N months')</td><td>Subtract N months</td></tr>
  <tr><td>julianday(d2)-julianday(d1)</td><td>Days between two dates</td></tr>
</table>
<h3>Common date format codes</h3>
<ul>
  <li><code>%Y</code> — 4-digit year (2024)</li>
  <li><code>%m</code> — month (01–12)</li>
  <li><code>%d</code> — day (01–31)</li>
  <li><code>%H:%M:%S</code> — time</li>
</ul>
""",
                "examples": [
                    {"title": "Today's date", "sql": "SELECT DATE('now') AS today,\n       DATETIME('now') AS now;"},
                    {"title": "Extract year & month", "sql": "SELECT name, hire_date,\n       strftime('%Y', hire_date) AS hire_year,\n       strftime('%m', hire_date) AS hire_month\nFROM employees;"},
                    {"title": "Years since hired", "sql": "SELECT name, hire_date,\n       ROUND((julianday('now') - julianday(hire_date))/365.25, 1) AS years_employed\nFROM employees\nORDER BY years_employed DESC;"},
                    {"title": "Add/subtract days", "sql": "SELECT DATE('now', '+30 days') AS thirty_days_later,\n       DATE('now', '-1 year') AS one_year_ago;"},
                    {"title": "Employees hired in 2020", "sql": "SELECT name, hire_date\nFROM employees\nWHERE strftime('%Y', hire_date) = '2020';"},
                    {"title": "Days since order", "sql": "SELECT customer, order_date,\n       ROUND(julianday('now') - julianday(order_date)) AS days_ago\nFROM orders\nORDER BY days_ago;"},
                ],
                "challenge": {
                    "question": "Show each employee's name, hire_date, and the year they were hired. Name the year column <code>hire_year</code>.",
                    "hint": "strftime('%Y', hire_date) AS hire_year",
                    "answer": "SELECT name, hire_date, strftime('%Y', hire_date) AS hire_year FROM employees;"
                }
            },
            {
                "slug": "aggregate-functions",
                "title": "Aggregate Functions",
                "theory": """
<h2>Aggregate Functions</h2>
<p>Aggregate functions calculate a <strong>single result from many rows</strong>.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>COUNT(*)</td><td>Count all rows</td></tr>
  <tr><td>COUNT(col)</td><td>Count non-NULL values</td></tr>
  <tr><td>COUNT(DISTINCT col)</td><td>Count unique values</td></tr>
  <tr><td>SUM(col)</td><td>Add up all values</td></tr>
  <tr><td>AVG(col)</td><td>Calculate average</td></tr>
  <tr><td>MAX(col)</td><td>Find biggest value</td></tr>
  <tr><td>MIN(col)</td><td>Find smallest value</td></tr>
</table>
<h3>🍕 Analogy</h3>
<p>If your table is a receipt: COUNT = how many items, SUM = total bill, AVG = average price, MAX/MIN = priciest/cheapest item.</p>
""",
                "examples": [
                    {"title": "COUNT rows", "sql": "SELECT COUNT(*) AS total_employees FROM employees;"},
                    {"title": "SUM", "sql": "SELECT SUM(salary) AS total_salary_bill FROM employees;"},
                    {"title": "AVG", "sql": "SELECT ROUND(AVG(salary), 2) AS avg_salary FROM employees;"},
                    {"title": "MAX & MIN", "sql": "SELECT MAX(salary) AS highest,\n       MIN(salary) AS lowest,\n       MAX(salary) - MIN(salary) AS range\nFROM employees;"},
                    {"title": "COUNT DISTINCT", "sql": "SELECT COUNT(DISTINCT dept_id) AS num_departments\nFROM employees;"},
                    {"title": "Multiple aggregates", "sql": "SELECT COUNT(*) AS employees,\n       ROUND(AVG(salary),0) AS avg_sal,\n       SUM(salary) AS total,\n       MAX(salary) AS top_sal\nFROM employees;"},
                ],
                "challenge": {
                    "question": "What is the total stock value across all products? (price × stock, rounded to 2 decimal places)",
                    "hint": "SUM(price * stock)",
                    "answer": "SELECT ROUND(SUM(price * stock), 2) AS total_stock_value FROM products;"
                }
            },
            {
                "slug": "conversion-functions",
                "title": "Conversion Functions",
                "theory": """
<h2>Conversion Functions</h2>
<p>Conversion functions change a value from one data type to another.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>CAST(val AS type)</td><td>Convert value to a type (INTEGER, REAL, TEXT)</td></tr>
  <tr><td>TYPEOF(val)</td><td>Returns the data type of a value</td></tr>
  <tr><td>HEX(val)</td><td>Convert to hexadecimal string</td></tr>
  <tr><td>PRINTF(fmt, val)</td><td>Format a value like C's printf</td></tr>
</table>
<h3>CAST examples</h3>
<pre><code>CAST(salary AS INTEGER)   -- removes decimal
CAST('123' AS INTEGER)    -- text to number
CAST(3.7 AS TEXT)         -- number to text</code></pre>
<h3>PRINTF for formatting</h3>
<pre><code>PRINTF('$%.2f', price)   -- formats as $999.99
PRINTF('%05d', id)        -- pads with zeros: 00001</code></pre>
""",
                "examples": [
                    {"title": "CAST — REAL to INTEGER", "sql": "SELECT name, salary,\n       CAST(salary AS INTEGER) AS salary_int,\n       TYPEOF(salary) AS type\nFROM employees;"},
                    {"title": "CAST — TEXT to INTEGER", "sql": "SELECT CAST('42' AS INTEGER) + 8 AS result;"},
                    {"title": "TYPEOF", "sql": "SELECT TYPEOF(42) AS int_type,\n       TYPEOF(3.14) AS real_type,\n       TYPEOF('hello') AS text_type,\n       TYPEOF(NULL) AS null_type;"},
                    {"title": "PRINTF — currency format", "sql": "SELECT name,\n       PRINTF('$%.2f', price) AS formatted_price\nFROM products;"},
                    {"title": "PRINTF — zero-padded ID", "sql": "SELECT PRINTF('EMP-%04d', id) AS employee_id,\n       name\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Show each product's name and price formatted as a currency string like <code>$999.99</code> using PRINTF.",
                    "hint": "PRINTF('$%.2f', price)",
                    "answer": "SELECT name, PRINTF('$%.2f', price) AS formatted_price FROM products;"
                }
            },
            {
                "slug": "null-functions",
                "title": "NULL Handling Functions",
                "theory": """
<h2>NULL Handling Functions</h2>
<p><strong>NULL</strong> means "missing" or "unknown" — it's not zero or an empty string. Special functions handle NULLs.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>COALESCE(a, b, c...)</td><td>Returns the first non-NULL value</td></tr>
  <tr><td>IFNULL(a, b)</td><td>Returns b if a is NULL, else a</td></tr>
  <tr><td>NULLIF(a, b)</td><td>Returns NULL if a = b, else returns a</td></tr>
  <tr><td>IS NULL</td><td>Test if value is NULL</td></tr>
  <tr><td>IS NOT NULL</td><td>Test if value is not NULL</td></tr>
</table>
<h3>🧠 NULL rules</h3>
<ul>
  <li>NULL = NULL is <strong>not true</strong> — use <code>IS NULL</code></li>
  <li>Any math with NULL = NULL (e.g. 5 + NULL = NULL)</li>
  <li>Aggregates like SUM/AVG <strong>ignore NULLs</strong></li>
</ul>
""",
                "examples": [
                    {"title": "COALESCE — replace NULL", "sql": "SELECT name,\n       COALESCE(phone, 'No phone') AS contact\nFROM employees;"},
                    {"title": "IFNULL", "sql": "SELECT name,\n       IFNULL(phone, 'N/A') AS phone_number\nFROM employees;"},
                    {"title": "NULLIF", "sql": "SELECT name, dept_id,\n       NULLIF(dept_id, 1) AS dept_if_not_eng\nFROM employees;"},
                    {"title": "IS NULL check", "sql": "-- Insert a test row with NULL salary\nINSERT INTO employees(name, age) VALUES('Test',30);\nSELECT name FROM employees WHERE salary IS NULL;"},
                    {"title": "IS NOT NULL", "sql": "SELECT name, salary\nFROM employees\nWHERE salary IS NOT NULL;"},
                ],
                "challenge": {
                    "question": "Use COALESCE to show each employee's phone number, and display <code>'Not provided'</code> if the phone is NULL.",
                    "hint": "COALESCE(phone, 'Not provided')",
                    "answer": "SELECT name, COALESCE(phone, 'Not provided') AS phone FROM employees;"
                }
            },
            {
                "slug": "conditional-functions",
                "title": "Conditional (CASE)",
                "theory": """
<h2>CASE Expression</h2>
<p><code>CASE</code> is SQL's way of doing <strong>if/else logic</strong> inside a query.</p>
<h3>Simple CASE</h3>
<pre><code>SELECT name,
  CASE dept_id
    WHEN 1 THEN 'Engineering'
    WHEN 2 THEN 'Marketing'
    ELSE 'Other'
  END AS department
FROM employees;</code></pre>
<h3>Searched CASE (more flexible)</h3>
<pre><code>SELECT name, salary,
  CASE
    WHEN salary > 100000 THEN 'Senior'
    WHEN salary > 75000  THEN 'Mid'
    ELSE 'Junior'
  END AS level
FROM employees;</code></pre>
<h3>IIF shorthand (SQLite)</h3>
<pre><code>IIF(condition, value_if_true, value_if_false)</code></pre>
""",
                "examples": [
                    {"title": "CASE — salary tier", "sql": "SELECT name, salary,\n  CASE\n    WHEN salary > 100000 THEN '🔴 Senior'\n    WHEN salary > 80000  THEN '🟡 Mid'\n    ELSE '🟢 Junior'\n  END AS level\nFROM employees;"},
                    {"title": "CASE — dept name", "sql": "SELECT name,\n  CASE dept_id\n    WHEN 1 THEN 'Engineering'\n    WHEN 2 THEN 'Marketing'\n    WHEN 3 THEN 'Finance'\n    ELSE 'HR'\n  END AS department\nFROM employees;"},
                    {"title": "CASE — grade label", "sql": "SELECT name, score,\n  CASE\n    WHEN score >= 90 THEN 'A'\n    WHEN score >= 80 THEN 'B'\n    WHEN score >= 70 THEN 'C'\n    ELSE 'F'\n  END AS grade\nFROM students;"},
                    {"title": "IIF shorthand", "sql": "SELECT name, stock,\n  IIF(stock < 50, 'Low Stock', 'In Stock') AS status\nFROM products;"},
                    {"title": "CASE in aggregate", "sql": "SELECT\n  COUNT(CASE WHEN salary > 90000 THEN 1 END) AS senior_count,\n  COUNT(CASE WHEN salary <= 90000 THEN 1 END) AS junior_count\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Use CASE to label each product: if price > 300 show <code>'Expensive'</code>, if price > 50 show <code>'Medium'</code>, else <code>'Cheap'</code>.",
                    "hint": "CASE WHEN price > 300 THEN ... WHEN price > 50 THEN ... ELSE ...",
                    "answer": "SELECT name, price, CASE WHEN price > 300 THEN 'Expensive' WHEN price > 50 THEN 'Medium' ELSE 'Cheap' END AS price_label FROM products;"
                }
            },
        ]
    },
    {
        "id": "grouping",
        "title": "Grouping & Filtering",
        "icon": "📦",
        "lessons": [
            {
                "slug": "group-by",
                "title": "GROUP BY",
                "theory": """
<h2>GROUP BY</h2>
<p>GROUP BY groups rows that share a value so you can run aggregates per group.</p>
<pre><code>SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id;</code></pre>
<p>Instead of "total employees", this gives "employees <strong>per department</strong>".</p>
<h3>Rules</h3>
<ul>
  <li>Every column in SELECT must either be in GROUP BY or be an aggregate</li>
  <li>You can group by multiple columns</li>
  <li>NULL values are grouped together</li>
</ul>
<h3>Execution order</h3>
<pre><code>FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT</code></pre>
""",
                "examples": [
                    {"title": "Count per department", "sql": "SELECT dept_id, COUNT(*) AS headcount\nFROM employees\nGROUP BY dept_id;"},
                    {"title": "Avg salary per dept", "sql": "SELECT dept_id,\n       ROUND(AVG(salary), 0) AS avg_salary\nFROM employees\nGROUP BY dept_id;"},
                    {"title": "Products per category", "sql": "SELECT category,\n       COUNT(*) AS count,\n       ROUND(AVG(price), 2) AS avg_price\nFROM products\nGROUP BY category;"},
                    {"title": "GROUP BY multiple columns", "sql": "SELECT dept_id, grade,\n       COUNT(*) AS count\nFROM employees e\nJOIN students s ON 1=1\nGROUP BY e.dept_id, s.grade\nLIMIT 10;"},
                    {"title": "Sales per customer", "sql": "SELECT customer,\n       COUNT(*) AS orders,\n       SUM(total) AS total_spent\nFROM orders\nGROUP BY customer\nORDER BY total_spent DESC;"},
                ],
                "challenge": {
                    "question": "Show each grade in the students table and the average score for that grade.",
                    "hint": "GROUP BY grade",
                    "answer": "SELECT grade, ROUND(AVG(score),2) AS avg_score FROM students GROUP BY grade;"
                }
            },
            {
                "slug": "having",
                "title": "HAVING Clause",
                "theory": """
<h2>HAVING Clause</h2>
<p>HAVING filters <strong>groups</strong> after GROUP BY — like WHERE but for aggregated results.</p>
<pre><code>SELECT dept_id, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
HAVING avg_sal > 80000;</code></pre>
<h3>WHERE vs HAVING</h3>
<table class="ops-table">
  <tr><th></th><th>WHERE</th><th>HAVING</th></tr>
  <tr><td>Filters</td><td>Individual rows</td><td>Groups</td></tr>
  <tr><td>When</td><td>Before grouping</td><td>After grouping</td></tr>
  <tr><td>Can use aggregates?</td><td>No</td><td>Yes</td></tr>
</table>
<h3>Both together</h3>
<pre><code>SELECT dept_id, COUNT(*) AS cnt
FROM employees
WHERE age > 30          -- filter rows first
GROUP BY dept_id
HAVING cnt > 2;         -- then filter groups</code></pre>
""",
                "examples": [
                    {"title": "HAVING — high avg salary", "sql": "SELECT dept_id, ROUND(AVG(salary),0) AS avg_sal\nFROM employees\nGROUP BY dept_id\nHAVING avg_sal > 80000;"},
                    {"title": "HAVING COUNT > 2", "sql": "SELECT dept_id, COUNT(*) AS headcount\nFROM employees\nGROUP BY dept_id\nHAVING headcount > 2;"},
                    {"title": "WHERE + GROUP BY + HAVING", "sql": "SELECT dept_id, COUNT(*) AS cnt\nFROM employees\nWHERE age > 28\nGROUP BY dept_id\nHAVING cnt >= 2;"},
                    {"title": "Categories with avg price > 100", "sql": "SELECT category, ROUND(AVG(price),2) AS avg_price\nFROM products\nGROUP BY category\nHAVING avg_price > 100;"},
                ],
                "challenge": {
                    "question": "Show grades that have more than 1 student enrolled.",
                    "hint": "GROUP BY grade HAVING COUNT(*) > 1",
                    "answer": "SELECT grade, COUNT(*) AS count FROM students GROUP BY grade HAVING COUNT(*) > 1;"
                }
            },
        ]
    },
    {
        "id": "joins",
        "title": "JOINs",
        "icon": "🔗",
        "lessons": [
            {
                "slug": "inner-join",
                "title": "INNER JOIN",
                "theory": """
<h2>INNER JOIN</h2>
<p>Returns only rows that have a <strong>match in both tables</strong>.</p>
<pre><code>SELECT e.name, d.name AS dept
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;</code></pre>
<h3>🍕 Analogy</h3>
<p>Only customers who have placed an order appear. Customers without orders and orders without customers are excluded.</p>
<h3>Table Aliases</h3>
<p>Use short aliases (<code>e</code>, <code>d</code>) so you don't have to write the full table name every time.</p>
<h3>ON clause</h3>
<p>The <code>ON</code> clause specifies which columns link the two tables (the foreign key relationship).</p>
""",
                "examples": [
                    {"title": "Employee with dept name", "sql": "SELECT e.name, e.salary,\n       d.name AS department, d.city\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id;"},
                    {"title": "JOIN with WHERE", "sql": "SELECT e.name, d.name AS dept\nFROM employees e\nJOIN departments d ON e.dept_id = d.id\nWHERE d.city = 'New York';"},
                    {"title": "JOIN with ORDER BY", "sql": "SELECT e.name, e.salary, d.name AS dept\nFROM employees e\nJOIN departments d ON e.dept_id = d.id\nORDER BY d.name, e.salary DESC;"},
                    {"title": "3-table JOIN", "sql": "SELECT o.customer, p.name AS product,\n       oi.qty, oi.unit_price\nFROM orders o\nJOIN order_items oi ON o.id = oi.order_id\nJOIN products p ON oi.product_id = p.id;"},
                ],
                "challenge": {
                    "question": "Show each student's name with their course titles and marks using an INNER JOIN.",
                    "hint": "JOIN courses c ON s.id = c.student_id",
                    "answer": "SELECT s.name, c.title, c.marks FROM students s JOIN courses c ON s.id = c.student_id;"
                }
            },
            {
                "slug": "left-right-join",
                "title": "LEFT & RIGHT JOIN",
                "theory": """
<h2>LEFT JOIN & RIGHT JOIN</h2>
<h3>LEFT JOIN</h3>
<p>Returns <strong>all rows from the left table</strong> + matching rows from the right. Non-matches show NULL.</p>
<pre><code>SELECT d.name, e.name
FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id;</code></pre>
<p>All departments appear — even those with no employees (shown as NULL).</p>
<h3>RIGHT JOIN</h3>
<p>Same but all rows from the <strong>right table</strong> are kept. SQLite doesn't support RIGHT JOIN — use LEFT JOIN with tables swapped instead.</p>
<h3>Finding unmatched rows</h3>
<pre><code>-- Departments with NO employees:
SELECT d.name FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id
WHERE e.id IS NULL;</code></pre>
""",
                "examples": [
                    {"title": "LEFT JOIN — all depts", "sql": "SELECT d.name AS department,\n       COUNT(e.id) AS employee_count\nFROM departments d\nLEFT JOIN employees e ON d.id = e.dept_id\nGROUP BY d.name;"},
                    {"title": "Show NULLs on no match", "sql": "SELECT d.name AS dept, e.name AS employee\nFROM departments d\nLEFT JOIN employees e ON d.id = e.dept_id;"},
                    {"title": "Find depts with no staff", "sql": "SELECT d.name AS dept_no_employees\nFROM departments d\nLEFT JOIN employees e ON d.id = e.dept_id\nWHERE e.id IS NULL;"},
                    {"title": "Students with no courses", "sql": "SELECT s.name, c.title\nFROM students s\nLEFT JOIN courses c ON s.id = c.student_id;"},
                ],
                "challenge": {
                    "question": "List all departments and the number of employees in each. Include departments with 0 employees.",
                    "hint": "LEFT JOIN + COUNT(e.id) + GROUP BY",
                    "answer": "SELECT d.name, COUNT(e.id) AS employees FROM departments d LEFT JOIN employees e ON d.id = e.dept_id GROUP BY d.name;"
                }
            },
            {
                "slug": "self-join",
                "title": "SELF JOIN & CROSS JOIN",
                "theory": """
<h2>SELF JOIN & CROSS JOIN</h2>
<h3>SELF JOIN</h3>
<p>A table joined with <strong>itself</strong>. Useful for comparing rows within the same table (e.g. manager–employee relationships).</p>
<pre><code>SELECT a.name AS employee, b.name AS colleague
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id
WHERE a.id != b.id;</code></pre>
<h3>CROSS JOIN</h3>
<p>Produces the <strong>Cartesian product</strong> — every row of table A combined with every row of table B. Use carefully — it multiplies row counts!</p>
<pre><code>SELECT a.name, b.name FROM employees a CROSS JOIN employees b;</code></pre>
""",
                "examples": [
                    {"title": "SELF JOIN — colleagues", "sql": "SELECT a.name AS employee,\n       b.name AS colleague\nFROM employees a\nJOIN employees b\n  ON a.dept_id = b.dept_id\n  AND a.id < b.id\nORDER BY a.name;"},
                    {"title": "Higher earner in same dept", "sql": "SELECT a.name AS emp,\n       b.name AS higher_earner\nFROM employees a\nJOIN employees b\n  ON a.dept_id = b.dept_id\n  AND b.salary > a.salary\nORDER BY a.name;"},
                    {"title": "CROSS JOIN — combinations", "sql": "SELECT p.name AS product, c.name AS customer\nFROM products p\nCROSS JOIN customers c\nLIMIT 10;"},
                ],
                "challenge": {
                    "question": "Using a SELF JOIN on employees, find pairs of employees in the same department. Show both names and their department id.",
                    "hint": "JOIN employees b ON a.dept_id = b.dept_id AND a.id < b.id",
                    "answer": "SELECT a.name AS emp1, b.name AS emp2, a.dept_id FROM employees a JOIN employees b ON a.dept_id = b.dept_id AND a.id < b.id ORDER BY a.dept_id;"
                }
            },
        ]
    },
    {
        "id": "subqueries",
        "title": "Subqueries",
        "icon": "🪆",
        "lessons": [
            {
                "slug": "subquery-where",
                "title": "Subqueries in WHERE",
                "theory": """
<h2>Subqueries in WHERE</h2>
<p>A subquery is a query <strong>inside another query</strong>. The inner query runs first.</p>
<pre><code>SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);</code></pre>
<h3>Types</h3>
<ul>
  <li><strong>Single-value subquery</strong> — returns one value, used with =, >, < etc.</li>
  <li><strong>Multi-value subquery</strong> — returns multiple rows, used with IN / NOT IN</li>
  <li><strong>Correlated subquery</strong> — references the outer query</li>
</ul>
<h3>IN with subquery</h3>
<pre><code>SELECT name FROM employees
WHERE dept_id IN (SELECT id FROM departments WHERE city='New York');</code></pre>
""",
                "examples": [
                    {"title": "Above-average salary", "sql": "SELECT name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);"},
                    {"title": "IN — NY departments", "sql": "SELECT name FROM employees\nWHERE dept_id IN (\n  SELECT id FROM departments\n  WHERE city = 'New York'\n);"},
                    {"title": "Most expensive product", "sql": "SELECT * FROM products\nWHERE price = (SELECT MAX(price) FROM products);"},
                    {"title": "NOT IN", "sql": "SELECT name FROM employees\nWHERE dept_id NOT IN (\n  SELECT id FROM departments WHERE city = 'Chicago'\n);"},
                    {"title": "Correlated subquery", "sql": "SELECT name, salary, dept_id\nFROM employees e\nWHERE salary > (\n  SELECT AVG(salary) FROM employees\n  WHERE dept_id = e.dept_id\n);"},
                ],
                "challenge": {
                    "question": "Find all students whose score is above the average score of all students.",
                    "hint": "WHERE score > (SELECT AVG(score) FROM students)",
                    "answer": "SELECT name, score FROM students WHERE score > (SELECT AVG(score) FROM students);"
                }
            },
            {
                "slug": "subquery-from",
                "title": "Subqueries in FROM & SELECT",
                "theory": """
<h2>Subqueries in FROM & SELECT</h2>
<h3>In FROM (Derived Table)</h3>
<p>Use a subquery as a temporary table inside FROM. Must be given an alias.</p>
<pre><code>SELECT dept_id, avg_sal
FROM (
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM employees
  GROUP BY dept_id
) AS dept_summary
WHERE avg_sal > 85000;</code></pre>
<h3>In SELECT (Scalar Subquery)</h3>
<p>Returns one value per row — computed alongside each row.</p>
<pre><code>SELECT name, salary,
  (SELECT AVG(salary) FROM employees) AS company_avg
FROM employees;</code></pre>
<h3>EXISTS</h3>
<p><code>EXISTS</code> checks if a subquery returns any rows at all.</p>
<pre><code>SELECT name FROM departments d
WHERE EXISTS (
  SELECT 1 FROM employees WHERE dept_id = d.id
);</code></pre>
""",
                "examples": [
                    {"title": "Derived table in FROM", "sql": "SELECT dept_id, avg_sal\nFROM (\n  SELECT dept_id, ROUND(AVG(salary),0) AS avg_sal\n  FROM employees\n  GROUP BY dept_id\n) AS ds\nWHERE avg_sal > 85000;"},
                    {"title": "Scalar subquery in SELECT", "sql": "SELECT name, salary,\n  (SELECT ROUND(AVG(salary),0) FROM employees) AS co_avg\nFROM employees;"},
                    {"title": "Compare to dept avg", "sql": "SELECT name, salary,\n  ROUND(salary - (SELECT AVG(salary) FROM employees\n    WHERE dept_id = e.dept_id), 0) AS vs_dept_avg\nFROM employees e;"},
                    {"title": "EXISTS", "sql": "SELECT name FROM departments d\nWHERE EXISTS (\n  SELECT 1 FROM employees e\n  WHERE e.dept_id = d.id\n);"},
                    {"title": "NOT EXISTS", "sql": "SELECT name FROM departments d\nWHERE NOT EXISTS (\n  SELECT 1 FROM employees e\n  WHERE e.dept_id = d.id\n);"},
                ],
                "challenge": {
                    "question": "Using a subquery in FROM, find all departments where the average salary exceeds 80000. Show dept_id and avg_salary.",
                    "hint": "SELECT ... FROM (SELECT dept_id, AVG(salary)...GROUP BY...) WHERE avg_sal > 80000",
                    "answer": "SELECT dept_id, avg_sal FROM (SELECT dept_id, ROUND(AVG(salary),0) AS avg_sal FROM employees GROUP BY dept_id) WHERE avg_sal > 80000;"
                }
            },
        ]
    },
    {
        "id": "ddl",
        "title": "DDL — Table Management",
        "icon": "🏗️",
        "lessons": [
            {
                "slug": "create-table",
                "title": "CREATE TABLE",
                "theory": """
<h2>CREATE TABLE</h2>
<p>CREATE TABLE defines a new table with its columns and data types.</p>
<h3>Syntax</h3>
<pre><code>CREATE TABLE table_name (
  column1 datatype CONSTRAINT,
  column2 datatype,
  ...
);</code></pre>
<h3>SQLite Data Types</h3>
<table class="ops-table">
  <tr><th>Type</th><th>Stores</th></tr>
  <tr><td>INTEGER</td><td>Whole numbers: 1, 42, -5</td></tr>
  <tr><td>REAL</td><td>Decimal numbers: 3.14, 999.99</td></tr>
  <tr><td>TEXT</td><td>Strings: 'Alice', 'hello'</td></tr>
  <tr><td>BLOB</td><td>Binary data (files, images)</td></tr>
  <tr><td>NUMERIC</td><td>Any numeric value</td></tr>
</table>
<h3>Common Constraints</h3>
<ul>
  <li><code>PRIMARY KEY</code> — unique identifier for each row</li>
  <li><code>NOT NULL</code> — value cannot be missing</li>
  <li><code>UNIQUE</code> — no two rows can have same value</li>
  <li><code>DEFAULT value</code> — default value if none provided</li>
  <li><code>CHECK (condition)</code> — validate data on insert</li>
  <li><code>REFERENCES table(col)</code> — foreign key</li>
</ul>
""",
                "examples": [
                    {"title": "Basic CREATE TABLE", "sql": "CREATE TABLE IF NOT EXISTS projects (\n  id      INTEGER PRIMARY KEY AUTOINCREMENT,\n  name    TEXT NOT NULL,\n  budget  REAL DEFAULT 0,\n  active  INTEGER DEFAULT 1\n);\nSELECT * FROM projects;"},
                    {"title": "With CHECK constraint", "sql": "CREATE TABLE IF NOT EXISTS salaries (\n  id      INTEGER PRIMARY KEY,\n  amount  REAL CHECK(amount >= 0),\n  level   TEXT CHECK(level IN ('Junior','Mid','Senior'))\n);\nSELECT * FROM salaries;"},
                    {"title": "With FOREIGN KEY", "sql": "CREATE TABLE IF NOT EXISTS tasks (\n  id         INTEGER PRIMARY KEY,\n  title      TEXT NOT NULL,\n  emp_id     INTEGER REFERENCES employees(id),\n  due_date   TEXT\n);\nSELECT * FROM tasks;"},
                    {"title": "CREATE TABLE AS (copy)", "sql": "CREATE TABLE IF NOT EXISTS eng_team AS\nSELECT * FROM employees WHERE dept_id = 1;\nSELECT * FROM eng_team;"},
                ],
                "challenge": {
                    "question": "Create a table called <code>feedback</code> with columns: id (PRIMARY KEY), message (TEXT NOT NULL), rating (INTEGER with CHECK rating between 1 and 5), created_at (TEXT).",
                    "hint": "CHECK(rating BETWEEN 1 AND 5)",
                    "answer": "CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, message TEXT NOT NULL, rating INTEGER CHECK(rating BETWEEN 1 AND 5), created_at TEXT);\nSELECT * FROM feedback;"
                }
            },
            {
                "slug": "alter-drop",
                "title": "ALTER & DROP TABLE",
                "theory": """
<h2>ALTER & DROP TABLE</h2>
<h3>ALTER TABLE — modify existing table</h3>
<p>SQLite supports a limited ALTER TABLE:</p>
<pre><code>-- Add a new column
ALTER TABLE employees ADD COLUMN department TEXT;

-- Rename the table
ALTER TABLE employees RENAME TO staff;

-- Rename a column (SQLite 3.25+)
ALTER TABLE employees RENAME COLUMN name TO full_name;</code></pre>
<h3>DROP TABLE — delete a table</h3>
<pre><code>DROP TABLE table_name;
DROP TABLE IF EXISTS table_name; -- safe version</code></pre>
<p>⚠️ DROP TABLE permanently deletes the table and all its data. Cannot be undone without a backup.</p>
<h3>TRUNCATE (SQLite equivalent)</h3>
<pre><code>DELETE FROM table_name; -- removes all rows, keeps structure</code></pre>
""",
                "examples": [
                    {"title": "ADD COLUMN", "sql": "-- Add a column to our temp table\nCREATE TABLE IF NOT EXISTS temp_staff AS SELECT * FROM employees LIMIT 3;\nALTER TABLE temp_staff ADD COLUMN notes TEXT DEFAULT 'No notes';\nSELECT * FROM temp_staff;"},
                    {"title": "RENAME TABLE", "sql": "CREATE TABLE IF NOT EXISTS old_name (id INTEGER, val TEXT);\nALTER TABLE old_name RENAME TO new_name;\nSELECT name FROM sqlite_master WHERE type='table' AND name='new_name';"},
                    {"title": "DROP TABLE IF EXISTS", "sql": "DROP TABLE IF EXISTS temp_staff;\nDROP TABLE IF EXISTS old_name;\nDROP TABLE IF EXISTS new_name;\nSELECT 'Tables cleaned up' AS result;"},
                ],
                "challenge": {
                    "question": "Create a table <code>temp_test</code> with one column <code>id INTEGER</code>, then add a column <code>label TEXT</code> using ALTER TABLE, then verify with SELECT *.",
                    "hint": "CREATE TABLE ... then ALTER TABLE ... ADD COLUMN ...",
                    "answer": "CREATE TABLE IF NOT EXISTS temp_test(id INTEGER);\nALTER TABLE temp_test ADD COLUMN label TEXT;\nSELECT * FROM temp_test;"
                }
            },
        ]
    },
    {
        "id": "dml",
        "title": "DML — Modifying Data",
        "icon": "✏️",
        "lessons": [
            {
                "slug": "insert",
                "title": "INSERT",
                "theory": """
<h2>INSERT — Add new rows</h2>
<pre><code>INSERT INTO table (col1, col2) VALUES (val1, val2);</code></pre>
<h3>Insert multiple rows at once</h3>
<pre><code>INSERT INTO products (name, price) VALUES
  ('Tablet', 499.99),
  ('Phone', 799.99),
  ('Watch', 299.99);</code></pre>
<h3>INSERT from SELECT</h3>
<pre><code>INSERT INTO archive_employees
SELECT * FROM employees WHERE age > 40;</code></pre>
<h3>Tips</h3>
<ul>
  <li>If a column has a DEFAULT, you can omit it</li>
  <li>AUTO INCREMENT / AUTOINCREMENT columns are auto-generated</li>
  <li>Omit the column list only if you provide values for ALL columns in order</li>
</ul>
""",
                "examples": [
                    {"title": "Basic INSERT", "sql": "INSERT INTO students (name, grade, score)\nVALUES ('Sam', 'A', 97);\nSELECT * FROM students;"},
                    {"title": "Insert multiple rows", "sql": "INSERT INTO students (name, grade, score) VALUES\n  ('Zoe', 'B', 83),\n  ('Leo', 'A', 92);\nSELECT * FROM students ORDER BY id DESC LIMIT 5;"},
                    {"title": "INSERT from SELECT", "sql": "CREATE TABLE IF NOT EXISTS top_employees AS\nSELECT * FROM employees WHERE salary > 90000;\nSELECT * FROM top_employees;"},
                    {"title": "INSERT with defaults", "sql": "INSERT INTO orders (customer, order_date, total)\nVALUES ('New Customer', DATE('now'), 150.00);\nSELECT * FROM orders ORDER BY id DESC LIMIT 3;"},
                ],
                "challenge": {
                    "question": "Insert a new product: name='Tablet', category='Electronics', price=499.99, stock=25. Then select all products ordered by id descending.",
                    "hint": "INSERT INTO products (name, category, price, stock) VALUES (...)",
                    "answer": "INSERT INTO products (name, category, price, stock) VALUES ('Tablet','Electronics',499.99,25);\nSELECT * FROM products ORDER BY id DESC LIMIT 5;"
                }
            },
            {
                "slug": "update",
                "title": "UPDATE",
                "theory": """
<h2>UPDATE — Change existing rows</h2>
<pre><code>UPDATE table SET column = value WHERE condition;</code></pre>
<p>⚠️ <strong>Always use WHERE with UPDATE!</strong> Without WHERE, every single row gets changed.</p>
<h3>Update multiple columns</h3>
<pre><code>UPDATE employees
SET salary = 95000, age = 31
WHERE name = 'Alice';</code></pre>
<h3>Update with expression</h3>
<pre><code>-- Give everyone a 10% raise
UPDATE employees SET salary = salary * 1.10;</code></pre>
<h3>Update with subquery</h3>
<pre><code>UPDATE employees
SET salary = salary * 1.15
WHERE dept_id = (SELECT id FROM departments WHERE name='Engineering');</code></pre>
""",
                "examples": [
                    {"title": "Basic UPDATE", "sql": "UPDATE employees SET salary = 90000\nWHERE name = 'Bob';\nSELECT name, salary FROM employees WHERE name='Bob';"},
                    {"title": "Update multiple columns", "sql": "UPDATE students SET grade = 'A', score = 96\nWHERE name = 'Mia';\nSELECT * FROM students WHERE name='Mia';"},
                    {"title": "10% raise for all", "sql": "UPDATE employees SET salary = ROUND(salary * 1.10, 2);\nSELECT name, salary FROM employees;"},
                    {"title": "Conditional UPDATE with CASE", "sql": "UPDATE employees\nSET salary = CASE\n  WHEN salary > 100000 THEN salary * 1.05\n  ELSE salary * 1.10\nEND;\nSELECT name, salary FROM employees;"},
                ],
                "challenge": {
                    "question": "Update all products in the <code>Electronics</code> category — increase their price by 5%. Then select all electronics.",
                    "hint": "UPDATE products SET price = price * 1.05 WHERE category = ...",
                    "answer": "UPDATE products SET price = ROUND(price * 1.05, 2) WHERE category = 'Electronics';\nSELECT * FROM products WHERE category = 'Electronics';"
                }
            },
            {
                "slug": "delete",
                "title": "DELETE",
                "theory": """
<h2>DELETE — Remove rows</h2>
<pre><code>DELETE FROM table WHERE condition;</code></pre>
<p>⚠️ <strong>Always use WHERE with DELETE!</strong> Without it, all rows are deleted permanently.</p>
<h3>Safe delete pattern</h3>
<p>Before deleting, run a SELECT with the same WHERE to preview what will be deleted:</p>
<pre><code>-- First preview:
SELECT * FROM employees WHERE age > 50;
-- Then delete:
DELETE FROM employees WHERE age > 50;</code></pre>
<h3>Delete with subquery</h3>
<pre><code>DELETE FROM order_items
WHERE order_id IN (SELECT id FROM orders WHERE status = 'cancelled');</code></pre>
<h3>TRUNCATE equivalent</h3>
<pre><code>DELETE FROM table_name; -- deletes all rows, keeps table</code></pre>
""",
                "examples": [
                    {"title": "Delete specific row", "sql": "-- First insert a test row\nINSERT INTO students(name,grade,score) VALUES('Temp',  'C', 50);\nSELECT * FROM students;\n-- Now delete it\nDELETE FROM students WHERE name='Temp';\nSELECT * FROM students;"},
                    {"title": "Delete with condition", "sql": "-- Preview first\nSELECT * FROM orders WHERE status = 'pending';"},
                    {"title": "Delete with subquery", "sql": "-- Delete items from pending orders\nSELECT * FROM order_items\nWHERE order_id IN (\n  SELECT id FROM orders WHERE status='pending'\n);"},
                ],
                "challenge": {
                    "question": "First INSERT a student named 'Test User' with grade 'F' and score 30. Then DELETE that student. Show final SELECT.",
                    "hint": "INSERT ... then DELETE ... WHERE name='Test User'",
                    "answer": "INSERT INTO students(name,grade,score) VALUES('Test User','F',30);\nDELETE FROM students WHERE name='Test User';\nSELECT * FROM students;"
                }
            },
        ]
    },
    {
        "id": "advanced",
        "title": "Advanced SQL",
        "icon": "🚀",
        "lessons": [
            {
                "slug": "cte",
                "title": "CTEs (WITH clause)",
                "theory": """
<h2>CTEs — Common Table Expressions</h2>
<p>A CTE is a <strong>named temporary result set</strong> defined with <code>WITH</code>. It makes complex queries readable and reusable within the same query.</p>
<pre><code>WITH dept_stats AS (
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM employees
  GROUP BY dept_id
)
SELECT e.name, e.salary, ds.avg_sal
FROM employees e
JOIN dept_stats ds ON e.dept_id = ds.dept_id;</code></pre>
<h3>Multiple CTEs</h3>
<pre><code>WITH
  cte1 AS (SELECT ...),
  cte2 AS (SELECT ... FROM cte1)
SELECT * FROM cte2;</code></pre>
<h3>Recursive CTEs</h3>
<p>CTEs can reference themselves to handle hierarchical data (org charts, trees).</p>
""",
                "examples": [
                    {"title": "Basic CTE", "sql": "WITH dept_avg AS (\n  SELECT dept_id, ROUND(AVG(salary),0) AS avg_sal\n  FROM employees\n  GROUP BY dept_id\n)\nSELECT e.name, e.salary, da.avg_sal\nFROM employees e\nJOIN dept_avg da ON e.dept_id = da.dept_id;"},
                    {"title": "CTE to filter", "sql": "WITH high_earners AS (\n  SELECT * FROM employees WHERE salary > 90000\n)\nSELECT h.name, h.salary, d.name AS dept\nFROM high_earners h\nJOIN departments d ON h.dept_id = d.id;"},
                    {"title": "Multiple CTEs", "sql": "WITH\n  dept_stats AS (\n    SELECT dept_id, COUNT(*) AS cnt, AVG(salary) AS avg_sal\n    FROM employees GROUP BY dept_id\n  ),\n  big_depts AS (\n    SELECT * FROM dept_stats WHERE cnt >= 2\n  )\nSELECT d.name, bd.cnt, ROUND(bd.avg_sal,0) AS avg_salary\nFROM big_depts bd\nJOIN departments d ON d.id = bd.dept_id;"},
                    {"title": "Recursive CTE — number series", "sql": "WITH RECURSIVE counter(n) AS (\n  SELECT 1\n  UNION ALL\n  SELECT n + 1 FROM counter WHERE n < 10\n)\nSELECT n FROM counter;"},
                ],
                "challenge": {
                    "question": "Write a CTE called <code>high_scores</code> that selects students with score >= 90, then query it to show their names and scores.",
                    "hint": "WITH high_scores AS (SELECT ... WHERE score >= 90) SELECT ...",
                    "answer": "WITH high_scores AS (SELECT name, score FROM students WHERE score >= 90)\nSELECT * FROM high_scores;"
                }
            },
            {
                "slug": "window-functions",
                "title": "Window Functions",
                "theory": """
<h2>Window Functions</h2>
<p>Window functions compute a value for each row <strong>using a "window" of related rows</strong>, without collapsing them like GROUP BY.</p>
<pre><code>function() OVER (PARTITION BY col ORDER BY col)</code></pre>
<h3>Ranking Functions</h3>
<table class="ops-table">
  <tr><th>Function</th><th>Behaviour on ties</th></tr>
  <tr><td>ROW_NUMBER()</td><td>Always unique (1,2,3,4)</td></tr>
  <tr><td>RANK()</td><td>Ties get same rank, gap after (1,1,3)</td></tr>
  <tr><td>DENSE_RANK()</td><td>Ties get same rank, no gap (1,1,2)</td></tr>
  <tr><td>NTILE(n)</td><td>Divide into n buckets</td></tr>
</table>
<h3>Aggregate Windows</h3>
<pre><code>SUM(salary) OVER (PARTITION BY dept_id)   -- dept total
SUM(salary) OVER (ORDER BY id)            -- running total</code></pre>
<h3>Offset Functions</h3>
<ul>
  <li><code>LAG(col, n)</code> — value from n rows before</li>
  <li><code>LEAD(col, n)</code> — value from n rows after</li>
  <li><code>FIRST_VALUE(col)</code> — first value in the window</li>
  <li><code>LAST_VALUE(col)</code> — last value in the window</li>
</ul>
""",
                "examples": [
                    {"title": "RANK by salary", "sql": "SELECT name, salary,\n  RANK() OVER (ORDER BY salary DESC) AS rank\nFROM employees;"},
                    {"title": "DENSE_RANK vs RANK", "sql": "SELECT name, salary,\n  RANK()       OVER (ORDER BY salary DESC) AS rank,\n  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank,\n  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num\nFROM employees;"},
                    {"title": "ROW_NUMBER per department", "sql": "SELECT name, dept_id, salary,\n  ROW_NUMBER() OVER (\n    PARTITION BY dept_id\n    ORDER BY salary DESC\n  ) AS rank_in_dept\nFROM employees;"},
                    {"title": "Running total", "sql": "SELECT name, salary,\n  SUM(salary) OVER (ORDER BY id) AS running_total\nFROM employees;"},
                    {"title": "Top earner per department", "sql": "SELECT name, dept_id, salary FROM (\n  SELECT name, dept_id, salary,\n    RANK() OVER (\n      PARTITION BY dept_id ORDER BY salary DESC\n    ) AS rnk\n  FROM employees\n) WHERE rnk = 1;"},
                    {"title": "LAG — previous salary", "sql": "SELECT name, salary,\n  LAG(salary) OVER (ORDER BY salary) AS prev_salary,\n  salary - LAG(salary) OVER (ORDER BY salary) AS diff\nFROM employees;"},
                    {"title": "NTILE — quartiles", "sql": "SELECT name, salary,\n  NTILE(4) OVER (ORDER BY salary) AS quartile\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Rank all students by score (highest = rank 1) using DENSE_RANK. Show name, score, and rank.",
                    "hint": "DENSE_RANK() OVER (ORDER BY score DESC)",
                    "answer": "SELECT name, score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank FROM students;"
                }
            },
            {
                "slug": "views",
                "title": "Views",
                "theory": """
<h2>Views</h2>
<p>A <strong>view</strong> is a saved SELECT query that you can treat like a table. It doesn't store data — it re-runs the query every time you access it.</p>
<pre><code>CREATE VIEW emp_dept AS
SELECT e.name, e.salary, d.name AS dept
FROM employees e
JOIN departments d ON e.dept_id = d.id;</code></pre>
<p>Then use it like a table:</p>
<pre><code>SELECT * FROM emp_dept WHERE dept = 'Engineering';</code></pre>
<h3>Why use views?</h3>
<ul>
  <li>Simplify complex queries — write once, reuse many times</li>
  <li>Hide complexity from users</li>
  <li>Security — expose only certain columns</li>
</ul>
<h3>Drop a view</h3>
<pre><code>DROP VIEW IF EXISTS emp_dept;</code></pre>
""",
                "examples": [
                    {"title": "Create a VIEW", "sql": "CREATE VIEW IF NOT EXISTS emp_dept AS\nSELECT e.name, e.salary, e.hire_date,\n       d.name AS department, d.city\nFROM employees e\nJOIN departments d ON e.dept_id = d.id;\n\nSELECT * FROM emp_dept;"},
                    {"title": "Query the VIEW", "sql": "SELECT * FROM emp_dept\nWHERE department = 'Engineering'\nORDER BY salary DESC;"},
                    {"title": "Aggregate on a VIEW", "sql": "SELECT department,\n       COUNT(*) AS headcount,\n       ROUND(AVG(salary),0) AS avg_salary\nFROM emp_dept\nGROUP BY department;"},
                    {"title": "Drop a VIEW", "sql": "DROP VIEW IF EXISTS emp_dept;\nSELECT 'View dropped' AS result;"},
                ],
                "challenge": {
                    "question": "Create a view called <code>student_summary</code> that shows each student's name, grade, and score. Then SELECT all from it.",
                    "hint": "CREATE VIEW IF NOT EXISTS student_summary AS SELECT ...",
                    "answer": "CREATE VIEW IF NOT EXISTS student_summary AS SELECT name, grade, score FROM students;\nSELECT * FROM student_summary;"
                }
            },
            {
                "slug": "indexes",
                "title": "Indexes",
                "theory": """
<h2>Indexes</h2>
<p>An index is a <strong>data structure that speeds up lookups</strong> on a column — like a book's index helping you find a page without reading every page.</p>
<pre><code>CREATE INDEX idx_emp_salary ON employees(salary);</code></pre>
<h3>When to use indexes</h3>
<ul>
  <li>Columns used frequently in WHERE clauses</li>
  <li>Columns used in JOIN conditions</li>
  <li>Columns used in ORDER BY with large tables</li>
</ul>
<h3>Tradeoff</h3>
<ul>
  <li>✅ Faster SELECT queries</li>
  <li>⚠️ Slightly slower INSERT/UPDATE/DELETE (index must be maintained)</li>
  <li>⚠️ Uses extra disk space</li>
</ul>
<h3>Unique Index</h3>
<pre><code>CREATE UNIQUE INDEX idx_email ON employees(email);
-- Ensures no two employees have the same email</code></pre>
<h3>Drop an index</h3>
<pre><code>DROP INDEX IF EXISTS idx_emp_salary;</code></pre>
""",
                "examples": [
                    {"title": "Create INDEX", "sql": "CREATE INDEX IF NOT EXISTS idx_emp_salary\nON employees(salary);\nSELECT 'Index created' AS result;"},
                    {"title": "Create UNIQUE INDEX", "sql": "CREATE UNIQUE INDEX IF NOT EXISTS idx_emp_email\nON employees(email);\nSELECT 'Unique index created' AS result;"},
                    {"title": "Composite INDEX", "sql": "CREATE INDEX IF NOT EXISTS idx_emp_dept_sal\nON employees(dept_id, salary);\nSELECT 'Composite index created' AS result;"},
                    {"title": "List indexes", "sql": "SELECT name, tbl_name, sql\nFROM sqlite_master\nWHERE type = 'index';"},
                    {"title": "DROP INDEX", "sql": "DROP INDEX IF EXISTS idx_emp_salary;\nDROP INDEX IF EXISTS idx_emp_email;\nDROP INDEX IF EXISTS idx_emp_dept_sal;\nSELECT 'Indexes dropped' AS result;"},
                ],
                "challenge": {
                    "question": "Create an index called <code>idx_product_category</code> on the <code>products</code> table for the <code>category</code> column, then list all indexes.",
                    "hint": "CREATE INDEX idx_product_category ON products(category)",
                    "answer": "CREATE INDEX IF NOT EXISTS idx_product_category ON products(category);\nSELECT name, tbl_name FROM sqlite_master WHERE type='index';"
                }
            },
            {
                "slug": "transactions",
                "title": "Transactions (TCL)",
                "theory": """
<h2>Transactions</h2>
<p>A transaction groups multiple SQL statements into a <strong>single all-or-nothing unit</strong>. Either all succeed, or none do.</p>
<h3>ACID Properties</h3>
<table class="ops-table">
  <tr><th>Property</th><th>Meaning</th></tr>
  <tr><td>Atomicity</td><td>All operations succeed or none do</td></tr>
  <tr><td>Consistency</td><td>Data remains valid before and after</td></tr>
  <tr><td>Isolation</td><td>Transactions don't interfere with each other</td></tr>
  <tr><td>Durability</td><td>Committed changes persist even after crash</td></tr>
</table>
<h3>Commands (TCL)</h3>
<pre><code>BEGIN;         -- start transaction
COMMIT;        -- save all changes
ROLLBACK;      -- undo all changes since BEGIN</code></pre>
<h3>🏦 Bank analogy</h3>
<p>Transferring $100: debit one account AND credit another. If either fails, ROLLBACK — you don't want money to disappear!</p>
""",
                "examples": [
                    {"title": "Basic COMMIT", "sql": "BEGIN;\nINSERT INTO students(name,grade,score) VALUES('TxTest','A',99);\nSELECT * FROM students WHERE name='TxTest';\nCOMMIT;\nSELECT 'Committed!' AS result;"},
                    {"title": "ROLLBACK — undo changes", "sql": "BEGIN;\nINSERT INTO students(name,grade,score) VALUES('WillBeGone','F',0);\nSELECT * FROM students WHERE name='WillBeGone';\nROLLBACK;\nSELECT * FROM students WHERE name='WillBeGone';"},
                    {"title": "SAVEPOINT", "sql": "BEGIN;\nINSERT INTO students(name,grade,score) VALUES('Step1','B',80);\nSAVEPOINT sp1;\nINSERT INTO students(name,grade,score) VALUES('Step2','C',70);\nROLLBACK TO sp1;\nSELECT name FROM students WHERE name IN ('Step1','Step2');\nCOMMIT;"},
                ],
                "challenge": {
                    "question": "Start a transaction, insert a student named 'Rollback Test', then ROLLBACK and verify they don't appear in the table.",
                    "hint": "BEGIN; INSERT...; ROLLBACK; SELECT...",
                    "answer": "BEGIN;\nINSERT INTO students(name,grade,score) VALUES('Rollback Test','D',40);\nROLLBACK;\nSELECT * FROM students WHERE name='Rollback Test';"
                }
            },
            {
                "slug": "set-operations",
                "title": "Set Operations",
                "theory": """
<h2>Set Operations</h2>
<p>Set operations combine results from two or more SELECT statements.</p>
<table class="ops-table">
  <tr><th>Operator</th><th>Returns</th></tr>
  <tr><td>UNION</td><td>All rows from both, removes duplicates</td></tr>
  <tr><td>UNION ALL</td><td>All rows from both, including duplicates</td></tr>
  <tr><td>INTERSECT</td><td>Only rows that appear in BOTH</td></tr>
  <tr><td>EXCEPT</td><td>Rows in first query but NOT in second</td></tr>
</table>
<h3>Rules</h3>
<ul>
  <li>Both queries must have the same number of columns</li>
  <li>Columns should have compatible data types</li>
  <li>Column names come from the first SELECT</li>
</ul>
<pre><code>SELECT city FROM employees
UNION
SELECT city FROM departments;</code></pre>
""",
                "examples": [
                    {"title": "UNION — combine cities", "sql": "SELECT 'Customer' AS source, city FROM customers\nUNION\nSELECT 'Department' AS source, city FROM departments;"},
                    {"title": "UNION ALL — include dupes", "sql": "SELECT name FROM employees WHERE dept_id = 1\nUNION ALL\nSELECT name FROM employees WHERE salary > 90000;"},
                    {"title": "INTERSECT", "sql": "SELECT dept_id FROM employees WHERE salary > 80000\nINTERSECT\nSELECT dept_id FROM employees WHERE age > 30;"},
                    {"title": "EXCEPT", "sql": "SELECT dept_id FROM departments\nEXCEPT\nSELECT DISTINCT dept_id FROM employees;"},
                ],
                "challenge": {
                    "question": "Use UNION to combine the names of all employees (from the employees table) and all students (from the students table) into one result column called <code>person_name</code>.",
                    "hint": "SELECT name AS person_name FROM employees UNION SELECT name FROM students",
                    "answer": "SELECT name AS person_name FROM employees UNION SELECT name AS person_name FROM students;"
                }
            },
        ]
    },
]

# ── Additional sections appended to CURRICULUM ────────────────────────────────
CURRICULUM += [
    {
        "id": "string-functions-advanced",
        "title": "Advanced String Functions",
        "icon": "🔤",
        "lessons": [
            {
                "slug": "lpad-rpad-initcap",
                "title": "LPAD, RPAD & INITCAP",
                "theory": """
<h2>LPAD, RPAD & INITCAP</h2>
<p>These functions format strings by padding or capitalising them.</p>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th><th>Example</th></tr>
  <tr><td>LPAD(s, n, pad)</td><td>Pad string from the LEFT to length n</td><td>LPAD('7', 4, '0') → '0007'</td></tr>
  <tr><td>RPAD(s, n, pad)</td><td>Pad string from the RIGHT to length n</td><td>RPAD('Hi', 5, '.') → 'Hi...'</td></tr>
  <tr><td>INITCAP(s)</td><td>Capitalise first letter of each word</td><td>INITCAP('hello world') → 'Hello World'</td></tr>
</table>
<h3>💡 Note</h3>
<p>SQLite does not have native LPAD/RPAD/INITCAP. We simulate them with <code>PRINTF</code>, <code>SUBSTR</code>, and <code>UPPER</code>/<code>LOWER</code>. In Oracle/PostgreSQL/MySQL these are built-in.</p>
<h3>LPAD in SQLite (simulate with PRINTF)</h3>
<pre><code>-- Left-pad ID to 4 digits with zeros
PRINTF('%04d', id)</code></pre>
<h3>INITCAP in SQLite (simulate)</h3>
<pre><code>UPPER(SUBSTR(name,1,1)) || LOWER(SUBSTR(name,2))</code></pre>
""",
                "examples": [
                    {"title": "LPAD — zero-pad employee ID", "sql": "SELECT name,\n       PRINTF('%05d', id) AS padded_id\nFROM employees;"},
                    {"title": "RPAD — pad with dots", "sql": "SELECT name,\n       name || SUBSTR('..........', 1, 12 - LENGTH(name)) AS padded_name\nFROM employees;"},
                    {"title": "INITCAP simulation", "sql": "SELECT name,\n       UPPER(SUBSTR(name,1,1)) || LOWER(SUBSTR(name,2)) AS title_case\nFROM employees;"},
                    {"title": "Format invoice number", "sql": "SELECT id,\n       'INV-' || PRINTF('%06d', id) AS invoice_number\nFROM orders;"},
                    {"title": "Right-align prices", "sql": "SELECT name,\n       PRINTF('%10.2f', price) AS right_aligned_price\nFROM products;"},
                ],
                "challenge": {
                    "question": "Show each product's name in Title Case (first letter upper, rest lower) and its ID zero-padded to 4 digits like <code>0001</code>.",
                    "hint": "UPPER(SUBSTR(name,1,1)) || LOWER(SUBSTR(name,2)) and PRINTF('%04d', id)",
                    "answer": "SELECT PRINTF('%04d', id) AS padded_id, UPPER(SUBSTR(name,1,1)) || LOWER(SUBSTR(name,2)) AS title_name FROM products;"
                }
            },
            {
                "slug": "ascii-chr-translate",
                "title": "ASCII, CHR & TRANSLATE",
                "theory": """
<h2>ASCII, CHR & TRANSLATE</h2>
<table class="ops-table">
  <tr><th>Function</th><th>What it does</th></tr>
  <tr><td>UNICODE(s)</td><td>Returns the ASCII/Unicode code of the first character (SQLite uses UNICODE)</td></tr>
  <tr><td>CHAR(n)</td><td>Returns the character for a given ASCII code</td></tr>
  <tr><td>HEX(s)</td><td>Returns hexadecimal representation of a string</td></tr>
</table>
<h3>ASCII codes you should know</h3>
<ul>
  <li>65–90 = A–Z (uppercase)</li>
  <li>97–122 = a–z (lowercase)</li>
  <li>48–57 = 0–9 (digits)</li>
  <li>32 = space</li>
</ul>
<h3>TRANSLATE (Oracle/PostgreSQL)</h3>
<p>Replaces individual characters one-for-one (like a character-level REPLACE). SQLite doesn't have it natively — use multiple REPLACE calls instead.</p>
<pre><code>-- Simulate: replace vowels with *
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(name,'a','*'),'e','*'),'i','*'),'o','*'),'u','*')</code></pre>
""",
                "examples": [
                    {"title": "UNICODE — char code", "sql": "SELECT UNICODE('A') AS code_A,\n       UNICODE('a') AS code_a,\n       UNICODE('0') AS code_0;"},
                    {"title": "CHAR — code to character", "sql": "SELECT CHAR(65) AS A,\n       CHAR(97) AS a,\n       CHAR(48) AS zero;"},
                    {"title": "Build alphabet", "sql": "WITH RECURSIVE nums(n) AS (\n  SELECT 65 UNION ALL SELECT n+1 FROM nums WHERE n < 90\n)\nSELECT n AS ascii_code, CHAR(n) AS letter FROM nums;"},
                    {"title": "HEX encoding", "sql": "SELECT name, HEX(name) AS hex_name FROM employees LIMIT 3;"},
                    {"title": "Translate vowels (simulate)", "sql": "SELECT name,\n  REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(\n    LOWER(name),'a','*'),'e','*'),'i','*'),'o','*'),'u','*')\n  AS masked_vowels\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Show the UNICODE (ASCII code) of the first character of every employee's name, and the CHAR of code 90.",
                    "hint": "UNICODE(name) and CHAR(90)",
                    "answer": "SELECT name, UNICODE(name) AS first_char_code, CHAR(90) AS char_90 FROM employees;"
                }
            },
            {
                "slug": "group-concat",
                "title": "GROUP_CONCAT & String Aggregation",
                "theory": """
<h2>GROUP_CONCAT</h2>
<p><code>GROUP_CONCAT</code> aggregates multiple row values into a <strong>single comma-separated string</strong>.</p>
<pre><code>SELECT dept_id,
  GROUP_CONCAT(name) AS team_members
FROM employees
GROUP BY dept_id;</code></pre>
<h3>Custom separator</h3>
<pre><code>GROUP_CONCAT(name, ' | ')</code></pre>
<h3>With ORDER BY inside</h3>
<pre><code>GROUP_CONCAT(name ORDER BY name ASC SEPARATOR ', ')
-- Note: ORDER BY inside GROUP_CONCAT is MySQL/PostgreSQL syntax
-- SQLite: use a subquery to pre-sort</code></pre>
<h3>DISTINCT inside GROUP_CONCAT</h3>
<pre><code>GROUP_CONCAT(DISTINCT category)</code></pre>
<p>In standard SQL (PostgreSQL) this is <code>STRING_AGG(name, ', ')</code>. In SQL Server it's <code>STRING_AGG</code>.</p>
""",
                "examples": [
                    {"title": "List employees per dept", "sql": "SELECT dept_id,\n       GROUP_CONCAT(name) AS team\nFROM employees\nGROUP BY dept_id;"},
                    {"title": "Custom separator", "sql": "SELECT dept_id,\n       GROUP_CONCAT(name, ' | ') AS team\nFROM employees\nGROUP BY dept_id;"},
                    {"title": "DISTINCT categories", "sql": "SELECT GROUP_CONCAT(DISTINCT category, ', ') AS all_categories\nFROM products;"},
                    {"title": "Courses per student", "sql": "SELECT s.name,\n       GROUP_CONCAT(c.title, ', ') AS courses\nFROM students s\nJOIN courses c ON s.id = c.student_id\nGROUP BY s.name;"},
                    {"title": "Tags with count", "sql": "SELECT category,\n       COUNT(*) AS count,\n       GROUP_CONCAT(name, ', ') AS products_list\nFROM products\nGROUP BY category;"},
                ],
                "challenge": {
                    "question": "Show each department id and a pipe-separated list of employee names in that department.",
                    "hint": "GROUP_CONCAT(name, ' | ') GROUP BY dept_id",
                    "answer": "SELECT dept_id, GROUP_CONCAT(name, ' | ') AS employees FROM employees GROUP BY dept_id;"
                }
            },
        ]
    },
    {
        "id": "decode-sign-trunc",
        "title": "DECODE, SIGN & TRUNC",
        "icon": "🔁",
        "lessons": [
            {
                "slug": "decode",
                "title": "DECODE Function",
                "theory": """
<h2>DECODE Function</h2>
<p><code>DECODE</code> is an Oracle/DB2 function that works like a CASE expression — it compares a value to a series of options and returns the matching result.</p>
<h3>Syntax (Oracle)</h3>
<pre><code>DECODE(expression, search1, result1, search2, result2, ..., default)</code></pre>
<h3>Equivalent CASE</h3>
<pre><code>CASE expression
  WHEN search1 THEN result1
  WHEN search2 THEN result2
  ELSE default
END</code></pre>
<p>SQLite does not have DECODE — use CASE instead. This lesson shows both so you're ready for Oracle/MySQL environments.</p>
<h3>DECODE vs CASE</h3>
<ul>
  <li>DECODE is shorter for simple equality checks</li>
  <li>CASE is more flexible (supports ranges, LIKE, IS NULL)</li>
  <li>CASE is ANSI standard — works everywhere</li>
</ul>
""",
                "examples": [
                    {"title": "DECODE — dept name (Oracle syntax shown, run CASE)", "sql": "-- DECODE syntax (Oracle):\n-- DECODE(dept_id, 1,'Engineering', 2,'Marketing', 3,'Finance','HR')\n\n-- CASE equivalent (runs in SQLite):\nSELECT name,\n  CASE dept_id\n    WHEN 1 THEN 'Engineering'\n    WHEN 2 THEN 'Marketing'\n    WHEN 3 THEN 'Finance'\n    ELSE 'HR'\n  END AS department\nFROM employees;"},
                    {"title": "DECODE — grade label", "sql": "-- DECODE(grade,'A','Excellent','B','Good','C','Average','Below Average')\n\nSELECT name, grade,\n  CASE grade\n    WHEN 'A' THEN 'Excellent'\n    WHEN 'B' THEN 'Good'\n    WHEN 'C' THEN 'Average'\n    ELSE 'Below Average'\n  END AS performance\nFROM students;"},
                    {"title": "DECODE — order status label", "sql": "SELECT customer, status,\n  CASE status\n    WHEN 'completed' THEN '✅ Done'\n    WHEN 'shipped'   THEN '🚚 On the way'\n    WHEN 'pending'   THEN '⏳ Waiting'\n    ELSE '❓ Unknown'\n  END AS status_label\nFROM orders;"},
                    {"title": "DECODE with NULL handling", "sql": "-- DECODE treats NULL = NULL (unlike =)\n-- CASE equivalent:\nSELECT name,\n  CASE\n    WHEN salary IS NULL THEN 'No salary set'\n    ELSE PRINTF('$%.0f', salary)\n  END AS salary_display\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Using CASE (DECODE equivalent), label each product: category 'Electronics' → 'Tech', 'Furniture' → 'Home', anything else → 'Other'.",
                    "hint": "CASE category WHEN 'Electronics' THEN 'Tech' ...",
                    "answer": "SELECT name, category, CASE category WHEN 'Electronics' THEN 'Tech' WHEN 'Furniture' THEN 'Home' ELSE 'Other' END AS label FROM products;"
                }
            },
            {
                "slug": "sign-trunc-mod",
                "title": "SIGN, TRUNC & MOD",
                "theory": """
<h2>SIGN, TRUNC & MOD</h2>
<h3>SIGN(n)</h3>
<p>Returns <code>-1</code> if n is negative, <code>0</code> if zero, <code>1</code> if positive.</p>
<pre><code>SIGN(-50)  → -1
SIGN(0)    →  0
SIGN(100)  →  1</code></pre>
<h3>TRUNC(n, d)</h3>
<p>Truncates (cuts off) decimal places WITHOUT rounding. Different from ROUND which rounds up/down.</p>
<pre><code>TRUNC(3.987, 2)  → 3.98   (not 3.99)
TRUNC(3.987, 0)  → 3      (integer part only)
TRUNC(-3.7, 0)   → -3     (towards zero)</code></pre>
<p>In SQLite: use <code>CAST(n AS INTEGER)</code> or arithmetic for truncation.</p>
<h3>MOD(n, m) / n % m</h3>
<p>Returns the remainder after dividing n by m.</p>
<pre><code>MOD(10, 3)  → 1    (10 = 3×3 + 1)
MOD(15, 5)  → 0    (exact division)
7 % 2       → 1    (odd number check)</code></pre>
""",
                "examples": [
                    {"title": "SIGN function", "sql": "SELECT name,\n       salary - 80000 AS diff,\n       CASE WHEN salary - 80000 < 0 THEN -1\n            WHEN salary - 80000 > 0 THEN 1\n            ELSE 0 END AS sign_val\nFROM employees;"},
                    {"title": "TRUNC — truncate salary", "sql": "-- Truncate to thousands (SQLite)\nSELECT name, salary,\n       CAST(salary/1000 AS INTEGER) * 1000 AS truncated_to_k\nFROM employees;"},
                    {"title": "TRUNC decimal places", "sql": "SELECT price,\n       ROUND(price, 1)                        AS rounded,\n       CAST(price * 10 AS INTEGER) / 10.0     AS truncated_1dp\nFROM products;"},
                    {"title": "MOD — even or odd salary", "sql": "SELECT name, salary,\n       CASE WHEN CAST(salary AS INTEGER) % 2 = 0\n            THEN 'Even' ELSE 'Odd' END AS parity\nFROM employees;"},
                    {"title": "MOD — find every 3rd employee", "sql": "SELECT id, name\nFROM employees\nWHERE id % 3 = 0;"},
                    {"title": "MOD — batch grouping", "sql": "SELECT id, name,\n       (id % 3) + 1 AS batch_number\nFROM employees\nORDER BY batch_number, id;"},
                ],
                "challenge": {
                    "question": "Show each product's price, its price truncated to the nearest integer (no rounding), and whether its id is even or odd.",
                    "hint": "CAST(price AS INTEGER) for truncate, id % 2 for even/odd",
                    "answer": "SELECT name, price, CAST(price AS INTEGER) AS truncated, CASE WHEN id % 2 = 0 THEN 'Even' ELSE 'Odd' END AS id_parity FROM products;"
                }
            },
        ]
    },
    {
        "id": "advanced-date",
        "title": "Advanced Date Functions",
        "icon": "📅",
        "lessons": [
            {
                "slug": "date-add-months",
                "title": "ADD_MONTHS, LAST_DAY & NEXT_DAY",
                "theory": """
<h2>ADD_MONTHS, LAST_DAY & NEXT_DAY</h2>
<p>These are Oracle/MySQL date functions. SQLite simulates them using <code>DATE()</code> modifiers.</p>
<table class="ops-table">
  <tr><th>Oracle Function</th><th>SQLite Equivalent</th></tr>
  <tr><td>ADD_MONTHS(date, n)</td><td>DATE(date, '+N months')</td></tr>
  <tr><td>LAST_DAY(date)</td><td>DATE(date, 'start of month', '+1 month', '-1 day')</td></tr>
  <tr><td>MONTHS_BETWEEN(d1, d2)</td><td>(julianday(d1)-julianday(d2))/30.44</td></tr>
  <tr><td>NEXT_DAY(date, weekday)</td><td>No direct equivalent — use DATE + modifiers</td></tr>
  <tr><td>SYSDATE / NOW()</td><td>DATE('now') / DATETIME('now')</td></tr>
  <tr><td>TRUNC(date, 'MM')</td><td>DATE(date, 'start of month')</td></tr>
  <tr><td>TRUNC(date, 'YYYY')</td><td>DATE(date, 'start of year')</td></tr>
</table>
""",
                "examples": [
                    {"title": "ADD_MONTHS (+3 months)", "sql": "SELECT hire_date,\n       DATE(hire_date, '+3 months') AS plus_3_months,\n       DATE(hire_date, '-6 months') AS minus_6_months\nFROM employees;"},
                    {"title": "LAST_DAY of month", "sql": "SELECT hire_date,\n       DATE(hire_date, 'start of month', '+1 month', '-1 day') AS last_day\nFROM employees;"},
                    {"title": "MONTHS_BETWEEN (approximate)", "sql": "SELECT name, hire_date,\n       ROUND((julianday('now') - julianday(hire_date)) / 30.44) AS months_employed\nFROM employees\nORDER BY months_employed DESC;"},
                    {"title": "Start of month / year", "sql": "SELECT hire_date,\n       DATE(hire_date, 'start of month') AS month_start,\n       DATE(hire_date, 'start of year')  AS year_start\nFROM employees;"},
                    {"title": "Age calculation", "sql": "SELECT name, hire_date,\n       strftime('%Y','now') - strftime('%Y', hire_date) AS approx_years\nFROM employees\nORDER BY approx_years DESC;"},
                    {"title": "Date formatting", "sql": "SELECT name,\n       strftime('%d-%m-%Y', hire_date) AS formatted_date,\n       strftime('%B', hire_date) AS month_name\nFROM employees;"},
                ],
                "challenge": {
                    "question": "For each order, show the order date and what date it would be exactly 30 days later (delivery estimate). Name it <code>delivery_date</code>.",
                    "hint": "DATE(order_date, '+30 days')",
                    "answer": "SELECT customer, order_date, DATE(order_date, '+30 days') AS delivery_date FROM orders;"
                }
            },
            {
                "slug": "to-char-to-date",
                "title": "TO_CHAR, TO_DATE & TO_NUMBER",
                "theory": """
<h2>TO_CHAR, TO_DATE & TO_NUMBER</h2>
<p>These are Oracle conversion functions for formatting and parsing dates and numbers.</p>
<table class="ops-table">
  <tr><th>Oracle Function</th><th>Purpose</th><th>SQLite Equivalent</th></tr>
  <tr><td>TO_CHAR(date, fmt)</td><td>Date → formatted string</td><td>strftime(fmt, date)</td></tr>
  <tr><td>TO_DATE(string, fmt)</td><td>String → date</td><td>dates stored as text, use direct comparison</td></tr>
  <tr><td>TO_NUMBER(string)</td><td>String → number</td><td>CAST(string AS REAL)</td></tr>
  <tr><td>TO_CHAR(number, fmt)</td><td>Number → formatted string</td><td>PRINTF(fmt, number)</td></tr>
</table>
<h3>Common TO_CHAR format codes (Oracle → strftime)</h3>
<table class="ops-table">
  <tr><th>Oracle</th><th>SQLite strftime</th><th>Output</th></tr>
  <tr><td>YYYY</td><td>%Y</td><td>2024</td></tr>
  <tr><td>MM</td><td>%m</td><td>01–12</td></tr>
  <tr><td>DD</td><td>%d</td><td>01–31</td></tr>
  <tr><td>DY</td><td>%w (0=Sun)</td><td>Day of week</td></tr>
  <tr><td>HH24:MI:SS</td><td>%H:%M:%S</td><td>14:30:00</td></tr>
</table>
""",
                "examples": [
                    {"title": "TO_CHAR date formatting", "sql": "-- TO_CHAR(hire_date, 'DD-MON-YYYY') in Oracle\n-- SQLite equivalent:\nSELECT name,\n       strftime('%d-%m-%Y', hire_date) AS formatted\nFROM employees;"},
                    {"title": "TO_CHAR number formatting", "sql": "-- TO_CHAR(salary, '$999,999') in Oracle\n-- SQLite PRINTF equivalent:\nSELECT name,\n       PRINTF('$%,.0f', salary) AS formatted_salary\nFROM employees;"},
                    {"title": "TO_NUMBER conversion", "sql": "-- TO_NUMBER('123.45') in Oracle\n-- SQLite equivalent:\nSELECT CAST('123.45' AS REAL) AS converted_number,\n       CAST('42' AS INTEGER) + 100 AS math_result;"},
                    {"title": "Extract date parts", "sql": "SELECT name, hire_date,\n       strftime('%Y', hire_date) AS year,\n       strftime('%m', hire_date) AS month,\n       strftime('%d', hire_date) AS day,\n       CASE CAST(strftime('%w', hire_date) AS INTEGER)\n         WHEN 0 THEN 'Sunday'   WHEN 1 THEN 'Monday'\n         WHEN 2 THEN 'Tuesday'  WHEN 3 THEN 'Wednesday'\n         WHEN 4 THEN 'Thursday' WHEN 5 THEN 'Friday'\n         ELSE 'Saturday'\n       END AS day_of_week\nFROM employees;"},
                ],
                "challenge": {
                    "question": "Format each employee's hire_date as <code>YYYY/MM/DD</code> and name it <code>formatted_date</code>.",
                    "hint": "strftime('%Y/%m/%d', hire_date)",
                    "answer": "SELECT name, strftime('%Y/%m/%d', hire_date) AS formatted_date FROM employees;"
                }
            },
        ]
    },
    {
        "id": "advanced-queries",
        "title": "Advanced Query Techniques",
        "icon": "⚡",
        "lessons": [
            {
                "slug": "pivot-unpivot",
                "title": "PIVOT & UNPIVOT",
                "theory": """
<h2>PIVOT & UNPIVOT</h2>
<h3>PIVOT — Rows to Columns</h3>
<p>PIVOT transforms row values into column headers — like rotating a table 90°.</p>
<p>Native PIVOT exists in SQL Server and Oracle. In SQLite/PostgreSQL we use conditional aggregation:</p>
<pre><code>SELECT dept_id,
  SUM(CASE WHEN grade='A' THEN 1 ELSE 0 END) AS grade_A,
  SUM(CASE WHEN grade='B' THEN 1 ELSE 0 END) AS grade_B
FROM students
GROUP BY dept_id;</code></pre>
<h3>UNPIVOT — Columns to Rows</h3>
<p>UNPIVOT does the reverse — turns columns into rows. Use UNION ALL to simulate in SQLite:</p>
<pre><code>SELECT name, 'salary' AS metric, salary AS value FROM employees
UNION ALL
SELECT name, 'age', age FROM employees;</code></pre>
""",
                "examples": [
                    {"title": "PIVOT — grades as columns", "sql": "SELECT\n  SUM(CASE WHEN grade='A' THEN 1 ELSE 0 END) AS grade_A,\n  SUM(CASE WHEN grade='B' THEN 1 ELSE 0 END) AS grade_B,\n  SUM(CASE WHEN grade='C' THEN 1 ELSE 0 END) AS grade_C\nFROM students;"},
                    {"title": "PIVOT — category totals as columns", "sql": "SELECT\n  SUM(CASE WHEN category='Electronics' THEN price END) AS electronics_total,\n  SUM(CASE WHEN category='Furniture'   THEN price END) AS furniture_total,\n  SUM(CASE WHEN category='Stationery'  THEN price END) AS stationery_total\nFROM products;"},
                    {"title": "PIVOT — order status counts", "sql": "SELECT\n  COUNT(CASE WHEN status='completed' THEN 1 END) AS completed,\n  COUNT(CASE WHEN status='pending'   THEN 1 END) AS pending,\n  COUNT(CASE WHEN status='shipped'   THEN 1 END) AS shipped\nFROM orders;"},
                    {"title": "UNPIVOT — employee stats as rows", "sql": "SELECT name, 'salary' AS metric, CAST(salary AS TEXT) AS value\nFROM employees\nUNION ALL\nSELECT name, 'age', CAST(age AS TEXT)\nFROM employees\nORDER BY name, metric;"},
                ],
                "challenge": {
                    "question": "PIVOT the products table: show one row with total stock for each category as separate columns: <code>electronics_stock</code>, <code>furniture_stock</code>, <code>stationery_stock</code>.",
                    "hint": "SUM(CASE WHEN category='Electronics' THEN stock ELSE 0 END)",
                    "answer": "SELECT SUM(CASE WHEN category='Electronics' THEN stock ELSE 0 END) AS electronics_stock, SUM(CASE WHEN category='Furniture' THEN stock ELSE 0 END) AS furniture_stock, SUM(CASE WHEN category='Stationery' THEN stock ELSE 0 END) AS stationery_stock FROM products;"
                }
            },
            {
                "slug": "rollup-cube",
                "title": "ROLLUP, CUBE & GROUPING SETS",
                "theory": """
<h2>ROLLUP, CUBE & GROUPING SETS</h2>
<p>These are extensions of GROUP BY that produce subtotals and grand totals automatically.</p>
<h3>ROLLUP</h3>
<p>Produces subtotals along a hierarchy (right to left) plus a grand total.</p>
<pre><code>SELECT dept_id, grade, COUNT(*)
FROM students
GROUP BY ROLLUP(dept_id, grade);</code></pre>
<p>Gives: counts per (dept+grade) → per dept → grand total</p>
<h3>CUBE</h3>
<p>Produces ALL possible subtotal combinations.</p>
<pre><code>GROUP BY CUBE(col1, col2)</code></pre>
<h3>GROUPING SETS</h3>
<p>Specify exactly which groupings you want:</p>
<pre><code>GROUP BY GROUPING SETS((col1, col2), (col1), ())</code></pre>
<h3>GROUPING() function</h3>
<p>Returns 1 when the column is a subtotal row (NULL due to ROLLUP), 0 otherwise. Helps identify which rows are subtotals.</p>
<p>Note: SQLite has limited ROLLUP support. Full support in PostgreSQL, Oracle, MySQL 8+.</p>
""",
                "examples": [
                    {"title": "ROLLUP simulation with UNION ALL", "sql": "-- Detail rows\nSELECT category, ROUND(SUM(price),2) AS total, 'detail' AS row_type\nFROM products GROUP BY category\nUNION ALL\n-- Grand total\nSELECT 'ALL CATEGORIES', ROUND(SUM(price),2), 'grand total'\nFROM products\nORDER BY row_type DESC, category;"},
                    {"title": "Subtotals by dept and overall", "sql": "SELECT dept_id, COUNT(*) AS count, ROUND(AVG(salary),0) AS avg_sal\nFROM employees\nGROUP BY dept_id\nUNION ALL\nSELECT NULL, COUNT(*), ROUND(AVG(salary),0)\nFROM employees\nORDER BY dept_id;"},
                    {"title": "GROUPING SETS simulation", "sql": "-- By category\nSELECT category, NULL AS name, COUNT(*) AS cnt\nFROM products GROUP BY category\nUNION ALL\n-- By name\nSELECT NULL, name, 1\nFROM products\nUNION ALL\n-- Grand total\nSELECT NULL, NULL, COUNT(*) FROM products\nLIMIT 15;"},
                ],
                "challenge": {
                    "question": "Show the total salary per department, then a grand total row at the bottom using UNION ALL. Label the grand total row dept_id as <code>NULL</code>.",
                    "hint": "SELECT dept_id, SUM(salary) ... UNION ALL SELECT NULL, SUM(salary)...",
                    "answer": "SELECT dept_id, SUM(salary) AS total_salary FROM employees GROUP BY dept_id UNION ALL SELECT NULL, SUM(salary) FROM employees ORDER BY dept_id;"
                }
            },
            {
                "slug": "merge-upsert",
                "title": "MERGE / UPSERT",
                "theory": """
<h2>MERGE / UPSERT</h2>
<p><strong>MERGE</strong> (also called UPSERT = UPDATE + INSERT) combines INSERT and UPDATE in one statement — insert if not exists, update if it does.</p>
<h3>Oracle / SQL Server MERGE syntax</h3>
<pre><code>MERGE INTO target_table t
USING source_table s ON (t.id = s.id)
WHEN MATCHED THEN
  UPDATE SET t.salary = s.salary
WHEN NOT MATCHED THEN
  INSERT (id, name, salary) VALUES (s.id, s.name, s.salary);</code></pre>
<h3>SQLite — INSERT OR REPLACE</h3>
<pre><code>INSERT OR REPLACE INTO employees (id, name, salary)
VALUES (1, 'Alice', 95000);</code></pre>
<h3>SQLite — INSERT OR IGNORE</h3>
<pre><code>INSERT OR IGNORE INTO employees (id, name)
VALUES (1, 'Alice');  -- skips if id=1 already exists</code></pre>
<h3>SQLite — ON CONFLICT (SQLite 3.24+)</h3>
<pre><code>INSERT INTO employees (id, name, salary)
VALUES (1, 'Alice', 95000)
ON CONFLICT(id) DO UPDATE SET salary = excluded.salary;</code></pre>
""",
                "examples": [
                    {"title": "INSERT OR IGNORE", "sql": "-- Try to insert existing ID (will be ignored)\nINSERT OR IGNORE INTO students (id, name, grade, score)\nVALUES (1, 'Liam', 'A', 95);\n\n-- Try new ID (will insert)\nINSERT OR IGNORE INTO students (id, name, grade, score)\nVALUES (99, 'NewKid', 'B', 88);\n\nSELECT * FROM students;"},
                    {"title": "INSERT OR REPLACE (UPSERT)", "sql": "-- Replaces row if id exists, inserts if not\nINSERT OR REPLACE INTO students (id, name, grade, score)\nVALUES (1, 'Liam UPDATED', 'A+', 100);\n\nSELECT * FROM students WHERE id = 1;"},
                    {"title": "ON CONFLICT DO UPDATE", "sql": "INSERT INTO students (id, name, grade, score)\nVALUES (2, 'Mia', 'A', 95)\nON CONFLICT(id)\nDO UPDATE SET score = excluded.score, grade = excluded.grade;\n\nSELECT * FROM students WHERE id = 2;"},
                    {"title": "Bulk UPSERT pattern", "sql": "INSERT OR REPLACE INTO inventory (id, product_id, quantity, updated_at)\nVALUES\n  (1, 1, 999, DATE('now')),\n  (2, 2, 888, DATE('now'));\n\nSELECT * FROM inventory;"},
                ],
                "challenge": {
                    "question": "Use INSERT OR IGNORE to try inserting a student with id=1 (already exists) and id=50 (new). Then SELECT all students to confirm only id=50 was added.",
                    "hint": "INSERT OR IGNORE INTO students ...",
                    "answer": "INSERT OR IGNORE INTO students (id,name,grade,score) VALUES (1,'Dup','A',99),(50,'Brand New','B',85);\nSELECT * FROM students ORDER BY id;"
                }
            },
            {
                "slug": "regexp-pattern",
                "title": "Pattern Matching & REGEXP",
                "theory": """
<h2>Pattern Matching & REGEXP</h2>
<h3>LIKE (recap)</h3>
<ul>
  <li><code>%</code> — any sequence of characters</li>
  <li><code>_</code> — exactly one character</li>
</ul>
<pre><code>WHERE name LIKE 'A%'   -- starts with A
WHERE name LIKE '%son'  -- ends with son
WHERE name LIKE '_ob'   -- 3 chars, ends in ob</code></pre>
<h3>GLOB (SQLite)</h3>
<p>Like LIKE but case-sensitive and uses Unix-style wildcards:</p>
<ul>
  <li><code>*</code> — any sequence of characters</li>
  <li><code>?</code> — exactly one character</li>
  <li><code>[abc]</code> — any one of a, b, c</li>
  <li><code>[a-z]</code> — range</li>
</ul>
<pre><code>WHERE name GLOB 'A*'      -- starts with A (case-sensitive)
WHERE email GLOB '*@*.com' -- email pattern</code></pre>
<h3>REGEXP (MySQL/PostgreSQL)</h3>
<pre><code>WHERE name REGEXP '^[A-E]'   -- starts with A-E
WHERE email REGEXP '@gmail'  -- contains @gmail</code></pre>
<p>SQLite supports REGEXP only if a user-defined function is registered.</p>
""",
                "examples": [
                    {"title": "LIKE patterns", "sql": "SELECT name FROM employees WHERE name LIKE 'A%';\n-- starts with A\n\nSELECT name FROM employees WHERE name LIKE '%e';\n-- ends with e"},
                    {"title": "LIKE with underscore", "sql": "SELECT name FROM employees\nWHERE name LIKE '_a%';\n-- second letter is 'a'"},
                    {"title": "GLOB — case-sensitive", "sql": "SELECT name FROM employees\nWHERE name GLOB 'A*';\n-- starts with A (case-sensitive)"},
                    {"title": "GLOB — character class", "sql": "SELECT name FROM employees\nWHERE name GLOB '[A-F]*';\n-- starts with A, B, C, D, E, or F"},
                    {"title": "GLOB — email pattern", "sql": "SELECT name, email FROM employees\nWHERE email GLOB '*@company.com';"},
                    {"title": "NOT LIKE", "sql": "SELECT name FROM employees\nWHERE name NOT LIKE '%e%';\n-- names with no 'e'"},
                ],
                "challenge": {
                    "question": "Use GLOB to find all employees whose name starts with a letter between A and F (A, B, C, D, E, or F).",
                    "hint": "GLOB '[A-F]*'",
                    "answer": "SELECT name FROM employees WHERE name GLOB '[A-F]*';"
                }
            },
            {
                "slug": "fetch-offset",
                "title": "FETCH FIRST & OFFSET ROWS",
                "theory": """
<h2>FETCH FIRST & OFFSET ROWS ONLY</h2>
<p>This is the ANSI SQL standard for pagination — an alternative to LIMIT/OFFSET (which is MySQL/SQLite syntax).</p>
<h3>Syntax (ANSI SQL — works in Oracle 12c+, PostgreSQL, SQL Server 2012+)</h3>
<pre><code>SELECT * FROM employees
ORDER BY salary DESC
OFFSET 0 ROWS FETCH FIRST 5 ROWS ONLY;</code></pre>
<h3>Page 2 (skip first 5, take next 5)</h3>
<pre><code>SELECT * FROM employees
ORDER BY salary DESC
OFFSET 5 ROWS FETCH NEXT 5 ROWS ONLY;</code></pre>
<h3>SQLite equivalent</h3>
<pre><code>SELECT * FROM employees
ORDER BY salary DESC
LIMIT 5 OFFSET 5;</code></pre>
<h3>Comparison</h3>
<table class="ops-table">
  <tr><th>Database</th><th>Syntax</th></tr>
  <tr><td>MySQL / SQLite</td><td>LIMIT n OFFSET m</td></tr>
  <tr><td>Oracle / PostgreSQL / SQL Server</td><td>OFFSET m ROWS FETCH NEXT n ROWS ONLY</td></tr>
  <tr><td>SQL Server (old)</td><td>TOP n (no offset)</td></tr>
</table>
""",
                "examples": [
                    {"title": "LIMIT equivalent (SQLite)", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC\nLIMIT 5;"},
                    {"title": "Pagination — page 1", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC\nLIMIT 3 OFFSET 0;  -- page 1"},
                    {"title": "Pagination — page 2", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC\nLIMIT 3 OFFSET 3;  -- page 2"},
                    {"title": "Pagination — page 3", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC\nLIMIT 3 OFFSET 6;  -- page 3"},
                    {"title": "FETCH FIRST (SQLite supports it too)", "sql": "SELECT name, salary FROM employees\nORDER BY salary DESC\nLIMIT 5 OFFSET 0;\n-- ANSI equivalent: OFFSET 0 ROWS FETCH FIRST 5 ROWS ONLY"},
                ],
                "challenge": {
                    "question": "Show the 4th, 5th, and 6th highest-paid employees (page 2 of a 3-per-page result) using LIMIT and OFFSET.",
                    "hint": "ORDER BY salary DESC LIMIT 3 OFFSET 3",
                    "answer": "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3 OFFSET 3;"
                }
            },
        ]
    },
    {
        "id": "constraints",
        "title": "Constraints & Integrity",
        "icon": "🔒",
        "lessons": [
            {
                "slug": "constraints-deep",
                "title": "Constraints Deep Dive",
                "theory": """
<h2>Constraints</h2>
<p>Constraints enforce rules on columns to ensure data integrity — bad data is rejected at the database level.</p>
<table class="ops-table">
  <tr><th>Constraint</th><th>Rule it enforces</th></tr>
  <tr><td>PRIMARY KEY</td><td>Unique + NOT NULL. One per table.</td></tr>
  <tr><td>NOT NULL</td><td>Column must always have a value</td></tr>
  <tr><td>UNIQUE</td><td>No duplicate values (NULLs allowed)</td></tr>
  <tr><td>CHECK(expr)</td><td>Value must pass a condition</td></tr>
  <tr><td>DEFAULT value</td><td>Auto-fills if no value provided</td></tr>
  <tr><td>FOREIGN KEY</td><td>Value must exist in another table</td></tr>
</table>
<h3>Column-level vs Table-level</h3>
<pre><code>-- Column-level (inline)
id INTEGER PRIMARY KEY

-- Table-level (at end)
CONSTRAINT pk_emp PRIMARY KEY(id, dept_id)
CONSTRAINT fk_dept FOREIGN KEY(dept_id) REFERENCES departments(id)</code></pre>
<h3>ON DELETE / ON UPDATE actions (Foreign Keys)</h3>
<table class="ops-table">
  <tr><th>Action</th><th>Behaviour</th></tr>
  <tr><td>CASCADE</td><td>Delete/update child rows automatically</td></tr>
  <tr><td>SET NULL</td><td>Set child column to NULL</td></tr>
  <tr><td>RESTRICT</td><td>Prevent deletion if child rows exist</td></tr>
  <tr><td>NO ACTION</td><td>Default — like RESTRICT</td></tr>
</table>
""",
                "examples": [
                    {"title": "All constraints together", "sql": "CREATE TABLE IF NOT EXISTS accounts (\n  id       INTEGER PRIMARY KEY AUTOINCREMENT,\n  username TEXT    NOT NULL UNIQUE,\n  email    TEXT    NOT NULL UNIQUE,\n  balance  REAL    DEFAULT 0.0 CHECK(balance >= 0),\n  status   TEXT    DEFAULT 'active' CHECK(status IN ('active','inactive'))\n);\nSELECT * FROM accounts;"},
                    {"title": "CHECK constraint rejected", "sql": "CREATE TABLE IF NOT EXISTS scores (\n  id    INTEGER PRIMARY KEY,\n  score INTEGER CHECK(score BETWEEN 0 AND 100)\n);\n-- This should succeed:\nINSERT INTO scores VALUES (1, 95);\n-- This should fail:\nINSERT INTO scores VALUES (2, 150);"},
                    {"title": "FOREIGN KEY with CASCADE", "sql": "CREATE TABLE IF NOT EXISTS parent (id INTEGER PRIMARY KEY, name TEXT);\nCREATE TABLE IF NOT EXISTS child (\n  id        INTEGER PRIMARY KEY,\n  parent_id INTEGER REFERENCES parent(id) ON DELETE CASCADE\n);\nINSERT INTO parent VALUES (1,'Alpha');\nINSERT INTO child VALUES (1,1),(2,1);\nSELECT 'parent' AS tbl, COUNT(*) FROM parent\nUNION ALL\nSELECT 'child', COUNT(*) FROM child;"},
                    {"title": "DEFAULT values", "sql": "CREATE TABLE IF NOT EXISTS tasks (\n  id         INTEGER PRIMARY KEY AUTOINCREMENT,\n  title      TEXT NOT NULL,\n  status     TEXT DEFAULT 'todo',\n  created_at TEXT DEFAULT (DATE('now'))\n);\nINSERT INTO tasks (title) VALUES ('Write SQL course');\nSELECT * FROM tasks;"},
                ],
                "challenge": {
                    "question": "Create a table <code>reviews</code> with: id (PK AUTOINCREMENT), product_id (INTEGER NOT NULL), rating (INTEGER CHECK 1-5), comment (TEXT), created_at TEXT DEFAULT today. Then insert one row.",
                    "hint": "CHECK(rating BETWEEN 1 AND 5), DEFAULT (DATE('now'))",
                    "answer": "CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL, rating INTEGER CHECK(rating BETWEEN 1 AND 5), comment TEXT, created_at TEXT DEFAULT (DATE('now')));\nINSERT INTO reviews (product_id, rating, comment) VALUES (1, 5, 'Great!');\nSELECT * FROM reviews;"
                }
            },
            {
                "slug": "sequences-autoincrement",
                "title": "Sequences & Auto-Increment",
                "theory": """
<h2>Sequences & Auto-Increment</h2>
<h3>SQLite — AUTOINCREMENT</h3>
<pre><code>id INTEGER PRIMARY KEY AUTOINCREMENT</code></pre>
<ul>
  <li><code>INTEGER PRIMARY KEY</code> — auto-assigns next rowid (reuses deleted IDs)</li>
  <li><code>AUTOINCREMENT</code> — strictly increasing, never reuses IDs</li>
</ul>
<h3>Oracle — SEQUENCE</h3>
<pre><code>CREATE SEQUENCE emp_seq START WITH 1 INCREMENT BY 1;
INSERT INTO employees (id, name)
VALUES (emp_seq.NEXTVAL, 'Alice');</code></pre>
<h3>PostgreSQL — SERIAL / GENERATED</h3>
<pre><code>id SERIAL PRIMARY KEY
-- or modern syntax:
id INTEGER GENERATED ALWAYS AS IDENTITY</code></pre>
<h3>MySQL — AUTO_INCREMENT</h3>
<pre><code>id INT AUTO_INCREMENT PRIMARY KEY</code></pre>
<h3>SQL Server — IDENTITY</h3>
<pre><code>id INT IDENTITY(1,1) PRIMARY KEY</code></pre>
""",
                "examples": [
                    {"title": "AUTOINCREMENT in action", "sql": "CREATE TABLE IF NOT EXISTS log (\n  id        INTEGER PRIMARY KEY AUTOINCREMENT,\n  message   TEXT,\n  logged_at TEXT DEFAULT (DATETIME('now'))\n);\nINSERT INTO log(message) VALUES('First entry');\nINSERT INTO log(message) VALUES('Second entry');\nINSERT INTO log(message) VALUES('Third entry');\nSELECT * FROM log;"},
                    {"title": "Check last inserted ID", "sql": "INSERT INTO log(message) VALUES('New entry');\nSELECT last_insert_rowid() AS last_id;"},
                    {"title": "Sequence simulation with max(id)", "sql": "-- Simulate sequence: next ID\nSELECT MAX(id) + 1 AS next_id FROM employees;"},
                    {"title": "Gap after delete with AUTOINCREMENT", "sql": "CREATE TABLE IF NOT EXISTS seq_test (\n  id INTEGER PRIMARY KEY AUTOINCREMENT, val TEXT\n);\nINSERT INTO seq_test(val) VALUES('a'),('b'),('c');\nDELETE FROM seq_test WHERE val='b';\nINSERT INTO seq_test(val) VALUES('d');\nSELECT * FROM seq_test; -- id 2 is skipped"},
                ],
                "challenge": {
                    "question": "Create a table <code>notifications</code> with AUTOINCREMENT id, message TEXT, and created_at defaulting to now. Insert 3 rows without specifying id. Then select all.",
                    "hint": "INTEGER PRIMARY KEY AUTOINCREMENT, DEFAULT (DATETIME('now'))",
                    "answer": "CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, created_at TEXT DEFAULT (DATETIME('now')));\nINSERT INTO notifications(message) VALUES('Alert 1'),('Alert 2'),('Alert 3');\nSELECT * FROM notifications;"
                }
            },
        ]
    },
    {
        "id": "database-objects",
        "title": "Database Objects",
        "icon": "🏛️",
        "lessons": [
            {
                "slug": "triggers",
                "title": "Triggers",
                "theory": """
<h2>Triggers</h2>
<p>A <strong>trigger</strong> is a stored procedure that runs automatically when a specific event (INSERT, UPDATE, DELETE) happens on a table.</p>
<h3>Syntax</h3>
<pre><code>CREATE TRIGGER trigger_name
AFTER INSERT ON table_name
FOR EACH ROW
BEGIN
  -- SQL statements
END;</code></pre>
<h3>Trigger events</h3>
<ul>
  <li><strong>BEFORE INSERT / UPDATE / DELETE</strong> — runs before the operation</li>
  <li><strong>AFTER INSERT / UPDATE / DELETE</strong> — runs after the operation</li>
  <li><strong>INSTEAD OF</strong> — replaces the operation (for views)</li>
</ul>
<h3>NEW and OLD</h3>
<ul>
  <li><code>NEW.column</code> — the new value being inserted/updated</li>
  <li><code>OLD.column</code> — the previous value before update/delete</li>
</ul>
<h3>Common uses</h3>
<ul>
  <li>Audit logs (record every change)</li>
  <li>Auto-update timestamps</li>
  <li>Enforce complex business rules</li>
  <li>Cascade actions manually</li>
</ul>
""",
                "examples": [
                    {"title": "Audit log trigger", "sql": "CREATE TABLE IF NOT EXISTS salary_log (\n  id         INTEGER PRIMARY KEY AUTOINCREMENT,\n  emp_id     INTEGER,\n  old_salary REAL,\n  new_salary REAL,\n  changed_at TEXT DEFAULT (DATETIME('now'))\n);\n\nCREATE TRIGGER IF NOT EXISTS log_salary_change\nAFTER UPDATE ON employees\nWHEN OLD.salary != NEW.salary\nBEGIN\n  INSERT INTO salary_log(emp_id, old_salary, new_salary)\n  VALUES(OLD.id, OLD.salary, NEW.salary);\nEND;\n\n-- Trigger it:\nUPDATE employees SET salary = 99000 WHERE name='Alice';\nSELECT * FROM salary_log;"},
                    {"title": "BEFORE INSERT validation", "sql": "CREATE TABLE IF NOT EXISTS stock_movements (\n  id       INTEGER PRIMARY KEY AUTOINCREMENT,\n  product  TEXT,\n  quantity INTEGER CHECK(quantity > 0)\n);\n\nCREATE TRIGGER IF NOT EXISTS check_positive_qty\nBEFORE INSERT ON stock_movements\nWHEN NEW.quantity <= 0\nBEGIN\n  SELECT RAISE(ABORT, 'Quantity must be positive');\nEND;\n\n-- Valid insert:\nINSERT INTO stock_movements(product, quantity) VALUES('Laptop', 5);\nSELECT * FROM stock_movements;"},
                    {"title": "List all triggers", "sql": "SELECT name, tbl_name, sql\nFROM sqlite_master\nWHERE type = 'trigger';"},
                    {"title": "Drop a trigger", "sql": "DROP TRIGGER IF EXISTS log_salary_change;\nDROP TRIGGER IF EXISTS check_positive_qty;\nSELECT 'Triggers dropped' AS result;"},
                ],
                "challenge": {
                    "question": "Create a table <code>change_log</code> (id AUTOINCREMENT, action TEXT, changed_at TEXT). Create a trigger that inserts a row into change_log with action='student_added' AFTER every INSERT on students. Then insert a student to test it.",
                    "hint": "CREATE TRIGGER ... AFTER INSERT ON students BEGIN INSERT INTO change_log...",
                    "answer": "CREATE TABLE IF NOT EXISTS change_log(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, changed_at TEXT DEFAULT(DATETIME('now')));\nCREATE TRIGGER IF NOT EXISTS trg_student_add AFTER INSERT ON students BEGIN INSERT INTO change_log(action) VALUES('student_added'); END;\nINSERT INTO students(name,grade,score) VALUES('Trigger Test','A',90);\nSELECT * FROM change_log;"
                }
            },
            {
                "slug": "stored-procedures",
                "title": "Stored Procedures & Functions",
                "theory": """
<h2>Stored Procedures & Functions</h2>
<p>Stored procedures and functions are <strong>named, reusable blocks of SQL</strong> saved in the database.</p>
<h3>Stored Procedure (Oracle/SQL Server/MySQL)</h3>
<pre><code>-- Oracle syntax:
CREATE OR REPLACE PROCEDURE give_raise(
  p_dept_id IN INTEGER,
  p_percent IN NUMBER
) AS
BEGIN
  UPDATE employees
  SET salary = salary * (1 + p_percent/100)
  WHERE dept_id = p_dept_id;
  COMMIT;
END;</code></pre>
<h3>Stored Function (Oracle)</h3>
<pre><code>CREATE OR REPLACE FUNCTION get_annual_salary(p_id INTEGER)
RETURN NUMBER AS
  v_salary NUMBER;
BEGIN
  SELECT salary * 12 INTO v_salary FROM employees WHERE id = p_id;
  RETURN v_salary;
END;</code></pre>
<h3>SQLite limitation</h3>
<p>SQLite does not support stored procedures in SQL. The logic lives in the application code (Python, Java, etc.).</p>
<h3>PostgreSQL (PL/pgSQL)</h3>
<pre><code>CREATE OR REPLACE FUNCTION get_salary(p_id INT)
RETURNS NUMERIC AS $$
  SELECT salary FROM employees WHERE id = p_id;
$$ LANGUAGE SQL;</code></pre>
""",
                "examples": [
                    {"title": "Procedure logic as a query (SQLite)", "sql": "-- Simulating a 'give_raise' procedure:\n-- Give 10% raise to dept 1\nUPDATE employees\nSET salary = ROUND(salary * 1.10, 2)\nWHERE dept_id = 1;\nSELECT name, salary FROM employees WHERE dept_id = 1;"},
                    {"title": "Function logic as a query", "sql": "-- Simulate get_annual_salary(id=1):\nSELECT name,\n       salary AS monthly,\n       salary * 12 AS annual\nFROM employees\nWHERE id = 1;"},
                    {"title": "Reusable CTE as procedure substitute", "sql": "-- CTEs can substitute simple procedures in SQLite\nWITH raise_preview AS (\n  SELECT name, salary,\n         ROUND(salary * 1.15, 2) AS new_salary\n  FROM employees\n  WHERE dept_id = 1\n)\nSELECT *, new_salary - salary AS raise_amount\nFROM raise_preview;"},
                    {"title": "View as function substitute", "sql": "CREATE VIEW IF NOT EXISTS v_annual_salaries AS\nSELECT name, salary, salary * 12 AS annual_salary,\n       ROUND(salary * 12 / 52, 2) AS weekly_salary\nFROM employees;\nSELECT * FROM v_annual_salaries;"},
                ],
                "challenge": {
                    "question": "Simulate a stored procedure: give a 20% raise to all employees in department 3. Then show the updated salaries for dept 3.",
                    "hint": "UPDATE employees SET salary = salary * 1.20 WHERE dept_id = 3",
                    "answer": "UPDATE employees SET salary = ROUND(salary * 1.20, 2) WHERE dept_id = 3;\nSELECT name, salary FROM employees WHERE dept_id = 3;"
                }
            },
            {
                "slug": "cursors",
                "title": "Cursors",
                "theory": """
<h2>Cursors</h2>
<p>A <strong>cursor</strong> is a database object used to <strong>retrieve and process rows one at a time</strong> from a result set — like a pointer that moves through rows.</p>
<h3>When to use cursors</h3>
<ul>
  <li>Row-by-row processing in stored procedures</li>
  <li>Complex logic that can't be done in a single SQL statement</li>
  <li>Iterating over results to call other procedures</li>
</ul>
<h3>⚠️ Cursor performance</h3>
<p>Cursors are usually <strong>slower</strong> than set-based SQL. Always try to solve a problem with a single SQL query first.</p>
<h3>Oracle/SQL Server cursor syntax</h3>
<pre><code>DECLARE emp_cursor CURSOR FOR
  SELECT name, salary FROM employees;

OPEN emp_cursor;

FETCH NEXT FROM emp_cursor INTO @name, @salary;

WHILE @@FETCH_STATUS = 0
BEGIN
  PRINT @name + ' earns ' + CAST(@salary AS VARCHAR)
  FETCH NEXT FROM emp_cursor INTO @name, @salary
END;

CLOSE emp_cursor;
DEALLOCATE emp_cursor;</code></pre>
<h3>SQLite equivalent</h3>
<p>SQLite processes rows through the application layer (Python, etc.) — there's no explicit cursor syntax in SQL itself.</p>
""",
                "examples": [
                    {"title": "Row-by-row logic with recursive CTE", "sql": "-- Simulate cursor: process employees one by one\nWITH RECURSIVE\n  emp_list AS (\n    SELECT id, name, salary,\n           ROW_NUMBER() OVER (ORDER BY id) AS rn\n    FROM employees\n  ),\n  processor AS (\n    SELECT id, name, salary, rn,\n           PRINTF('Processing: %s (salary $%.0f)', name, salary) AS action\n    FROM emp_list\n    WHERE rn = 1\n    UNION ALL\n    SELECT e.id, e.name, e.salary, e.rn,\n           PRINTF('Processing: %s (salary $%.0f)', e.name, e.salary)\n    FROM emp_list e\n    JOIN processor p ON e.rn = p.rn + 1\n  )\nSELECT action FROM processor;"},
                    {"title": "Running calculation (cursor-like)", "sql": "-- Running salary total (what a cursor would compute row by row)\nSELECT name, salary,\n       SUM(salary) OVER (ORDER BY id) AS running_total,\n       COUNT(*) OVER (ORDER BY id) AS row_num\nFROM employees;"},
                    {"title": "Cursor vs Set-based comparison", "sql": "-- Cursor approach: process each dept one by one\n-- Set-based approach (always prefer this):\nSELECT dept_id,\n       COUNT(*) AS headcount,\n       ROUND(AVG(salary), 0) AS avg_salary,\n       SUM(salary) AS total_cost\nFROM employees\nGROUP BY dept_id;"},
                ],
                "challenge": {
                    "question": "Using a window function (the set-based alternative to a cursor), show each employee with their salary and a running count of employees processed so far (ordered by id).",
                    "hint": "COUNT(*) OVER (ORDER BY id)",
                    "answer": "SELECT name, salary, COUNT(*) OVER (ORDER BY id) AS running_count FROM employees ORDER BY id;"
                }
            },
            {
                "slug": "synonyms-aliases",
                "title": "Synonyms & Schema Objects",
                "theory": """
<h2>Synonyms & Schema Objects</h2>
<h3>Synonyms (Oracle)</h3>
<p>A <strong>synonym</strong> is an alias for another database object (table, view, sequence). It lets you refer to an object by a different name.</p>
<pre><code>-- Oracle: Create a synonym
CREATE SYNONYM emp FOR hr.employees;
-- Now you can query: SELECT * FROM emp;

-- Public synonym (accessible to all users)
CREATE PUBLIC SYNONYM emp FOR hr.employees;

-- Drop synonym
DROP SYNONYM emp;</code></pre>
<h3>Why use synonyms?</h3>
<ul>
  <li>Hide the schema name (<code>hr.employees</code> → just <code>employees</code>)</li>
  <li>Simplify long object names</li>
  <li>Database independence — swap the underlying table without changing queries</li>
</ul>
<h3>SQLite equivalent</h3>
<p>SQLite doesn't have synonyms. Views serve a similar purpose:</p>
<pre><code>CREATE VIEW emp AS SELECT * FROM employees;</code></pre>
<h3>Schema objects overview</h3>
<table class="ops-table">
  <tr><th>Object</th><th>Purpose</th></tr>
  <tr><td>TABLE</td><td>Stores data</td></tr>
  <tr><td>VIEW</td><td>Saved query (virtual table)</td></tr>
  <tr><td>INDEX</td><td>Speeds up lookups</td></tr>
  <tr><td>SEQUENCE</td><td>Generates unique numbers</td></tr>
  <tr><td>SYNONYM</td><td>Alias for another object</td></tr>
  <tr><td>TRIGGER</td><td>Auto-runs on events</td></tr>
  <tr><td>PROCEDURE</td><td>Reusable SQL block</td></tr>
  <tr><td>FUNCTION</td><td>Returns a value</td></tr>
</table>
""",
                "examples": [
                    {"title": "View as synonym substitute", "sql": "-- Simulate synonym: short name for employees\nCREATE VIEW IF NOT EXISTS emp AS\nSELECT * FROM employees;\n\nSELECT name, salary FROM emp WHERE dept_id = 1;"},
                    {"title": "List all database objects", "sql": "SELECT type, name\nFROM sqlite_master\nWHERE type IN ('table','view','index','trigger')\nORDER BY type, name;"},
                    {"title": "Schema info for a table", "sql": "SELECT name, type, dflt_value, pk\nFROM pragma_table_info('employees');"},
                    {"title": "Drop view (synonym)", "sql": "DROP VIEW IF EXISTS emp;\nSELECT 'Synonym view dropped' AS result;"},
                ],
                "challenge": {
                    "question": "Create a view called <code>high_value_products</code> that acts as a synonym — it shows all products with price > 100. Then query it.",
                    "hint": "CREATE VIEW IF NOT EXISTS high_value_products AS SELECT ...",
                    "answer": "CREATE VIEW IF NOT EXISTS high_value_products AS SELECT * FROM products WHERE price > 100;\nSELECT * FROM high_value_products;"
                }
            },
        ]
    },
    {
        "id": "normalization",
        "title": "Normalization & Design",
        "icon": "📐",
        "lessons": [
            {
                "slug": "normalization",
                "title": "Normalization (1NF–3NF–BCNF)",
                "theory": """
<h2>Database Normalization</h2>
<p>Normalization is the process of organizing a database to <strong>reduce redundancy and improve data integrity</strong>.</p>
<h3>1NF — First Normal Form</h3>
<p>Rules:</p>
<ul>
  <li>Each column contains atomic (indivisible) values</li>
  <li>Each row is unique</li>
  <li>No repeating groups or arrays</li>
</ul>
<pre><code>❌ NOT 1NF:
| name  | phones              |
|-------|---------------------|
| Alice | 555-1001, 555-1002  |  ← multiple values

✅ 1NF:
| name  | phone    |
|-------|----------|
| Alice | 555-1001 |
| Alice | 555-1002 |</code></pre>
<h3>2NF — Second Normal Form</h3>
<p>Must be 1NF + every non-key column depends on the <strong>entire primary key</strong> (no partial dependency).</p>
<pre><code>❌ NOT 2NF (composite key: order_id + product_id):
| order_id | product_id | product_name | qty |
   ^ partial dependency: product_name depends only on product_id

✅ 2NF: split into orders and products tables</code></pre>
<h3>3NF — Third Normal Form</h3>
<p>Must be 2NF + no transitive dependencies (non-key column depending on another non-key column).</p>
<pre><code>❌ NOT 3NF:
| emp_id | dept_id | dept_name |
   dept_name depends on dept_id, not emp_id

✅ 3NF: split departments into separate table</code></pre>
<h3>BCNF — Boyce-Codd Normal Form</h3>
<p>Stricter version of 3NF — every determinant must be a candidate key.</p>
""",
                "examples": [
                    {"title": "Unnormalized → 1NF", "sql": "-- Unnormalized: student with multiple courses in one row\n-- CREATE TABLE bad (id INT, name TEXT, courses TEXT);\n-- ('Alice', 'Math, Science, English')\n\n-- 1NF version (separate rows):\nSELECT s.name, c.title\nFROM students s\nJOIN courses c ON s.id = c.student_id\nORDER BY s.name;"},
                    {"title": "Check for 2NF — no partial deps", "sql": "-- Our tables are 2NF:\n-- employees: all columns depend on id (PK)\n-- order_items: qty and unit_price depend on (order_id, product_id)\nSELECT 'employees' AS tbl,\n       'id is PK, all cols depend on it' AS note\nUNION ALL\nSELECT 'order_items',\n       'composite key: order_id + product_id';"},
                    {"title": "Check for 3NF — no transitive deps", "sql": "-- employees has dept_id (FK), not dept_name\n-- dept_name is in departments table\n-- This IS 3NF\nSELECT e.name AS employee,\n       e.dept_id,\n       d.name AS dept_name  -- from separate table\nFROM employees e\nJOIN departments d ON e.dept_id = d.id;"},
                    {"title": "Normalised schema overview", "sql": "SELECT type, name,\n       CASE type\n         WHEN 'table' THEN 'stores data'\n         WHEN 'view'  THEN 'virtual table'\n         WHEN 'index' THEN 'speeds lookups'\n       END AS purpose\nFROM sqlite_master\nWHERE type IN ('table','view','index')\nORDER BY type, name;"},
                ],
                "challenge": {
                    "question": "Our database separates employees and departments (3NF). Write a query proving dept_name is NOT stored in employees — show employees with their dept_name from the departments table.",
                    "hint": "JOIN employees with departments",
                    "answer": "SELECT e.name, e.dept_id, d.name AS dept_name FROM employees e JOIN departments d ON e.dept_id = d.id ORDER BY d.name;"
                }
            },
            {
                "slug": "query-optimization",
                "title": "Query Optimization & EXPLAIN",
                "theory": """
<h2>Query Optimization</h2>
<p>Query optimization is about writing SQL that runs fast — especially important on large datasets.</p>
<h3>EXPLAIN QUERY PLAN</h3>
<p>Shows how SQLite executes your query — which indexes it uses, whether it does a full table scan, etc.</p>
<pre><code>EXPLAIN QUERY PLAN SELECT * FROM employees WHERE salary > 80000;</code></pre>
<h3>Optimization tips</h3>
<table class="ops-table">
  <tr><th>Bad practice</th><th>Better practice</th></tr>
  <tr><td>SELECT *</td><td>SELECT only needed columns</td></tr>
  <tr><td>No index on WHERE columns</td><td>CREATE INDEX on frequently filtered columns</td></tr>
  <tr><td>Function on indexed column</td><td>Avoid wrapping indexed cols in functions</td></tr>
  <tr><td>OR in WHERE</td><td>Consider UNION instead</td></tr>
  <tr><td>Subquery in SELECT (for each row)</td><td>Use JOIN instead</td></tr>
  <tr><td>LIKE '%word%'</td><td>LIKE 'word%' (prefix match uses index)</td></tr>
</table>
<h3>Sargable predicates</h3>
<p>A WHERE clause is "SARGable" (Search ARGument ABLE) if it can use an index:</p>
<pre><code>✅ Sargable:   WHERE salary > 80000
✅ Sargable:   WHERE name = 'Alice'
❌ NOT:        WHERE UPPER(name) = 'ALICE'  -- wraps column in function</code></pre>
""",
                "examples": [
                    {"title": "EXPLAIN QUERY PLAN", "sql": "EXPLAIN QUERY PLAN\nSELECT * FROM employees WHERE salary > 80000;"},
                    {"title": "Compare with index", "sql": "CREATE INDEX IF NOT EXISTS idx_sal ON employees(salary);\n\nEXPLAIN QUERY PLAN\nSELECT * FROM employees WHERE salary > 80000;"},
                    {"title": "SELECT * vs specific columns", "sql": "-- Bad: fetches all columns\n-- SELECT * FROM employees WHERE dept_id = 1;\n\n-- Better: only what you need\nSELECT name, salary FROM employees WHERE dept_id = 1;"},
                    {"title": "Avoid function on WHERE column", "sql": "-- Bad (can't use index on name):\n-- SELECT * FROM employees WHERE UPPER(name) = 'ALICE';\n\n-- Better:\nSELECT * FROM employees WHERE name = 'Alice';"},
                    {"title": "UNION vs OR", "sql": "-- OR can be slow:\n-- SELECT * FROM employees WHERE dept_id=1 OR salary>100000;\n\n-- UNION alternative (each part can use its own index):\nSELECT * FROM employees WHERE dept_id = 1\nUNION\nSELECT * FROM employees WHERE salary > 100000;"},
                    {"title": "Check query stats", "sql": "SELECT\n  (SELECT COUNT(*) FROM employees) AS emp_rows,\n  (SELECT COUNT(*) FROM products)  AS prod_rows,\n  (SELECT COUNT(*) FROM orders)    AS order_rows;"},
                ],
                "challenge": {
                    "question": "Run EXPLAIN QUERY PLAN on a query that selects employees with salary > 90000. Then create an index on salary and run EXPLAIN again to see the difference.",
                    "hint": "EXPLAIN QUERY PLAN SELECT...; then CREATE INDEX...; then EXPLAIN again",
                    "answer": "EXPLAIN QUERY PLAN SELECT name, salary FROM employees WHERE salary > 90000;\nCREATE INDEX IF NOT EXISTS idx_opt_sal ON employees(salary);\nEXPLAIN QUERY PLAN SELECT name, salary FROM employees WHERE salary > 90000;"
                }
            },
        ]
    },
]

# ── Flatten lessons for navigation ───────────────────────────────────────────
ALL_LESSONS = []
for section in CURRICULUM:
    for lesson in section["lessons"]:
        lesson["section_id"]    = section["id"]
        lesson["section_title"] = section["title"]
        lesson["section_icon"]  = section["icon"]
        ALL_LESSONS.append(lesson)

SLUG_MAP = {l["slug"]: l for l in ALL_LESSONS}

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

# ── Google Search Console ownership verification ──────────────────────────────
@app.route("/googlec927be5152afab4b.html")
def google_verify():
    return Response(
        "google-site-verification: googlec927be5152afab4b.html",
        mimetype="text/html"
    )

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", curriculum=CURRICULUM,
                           total=len(ALL_LESSONS))

@app.route("/lesson/<slug>")
def lesson(slug):
    les = SLUG_MAP.get(slug)
    if not les:
        return "Lesson not found", 404
    uid = session.get("uid")
    if not uid:
        import uuid
        uid = str(uuid.uuid4())[:8]
        session["uid"] = uid
        init_sandbox(uid)
    idx = ALL_LESSONS.index(les)
    prev_lesson = ALL_LESSONS[idx - 1] if idx > 0 else None
    next_lesson = ALL_LESSONS[idx + 1] if idx < len(ALL_LESSONS) - 1 else None
    return render_template("lesson.html", lesson=les, curriculum=CURRICULUM,
                           all_lessons=ALL_LESSONS,
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
    blocked = ["DROP TABLE employees", "DROP TABLE departments",
               "DROP TABLE products", "ATTACH", "DETACH", ".import"]
    upper_sql = sql.upper()
    for b in blocked:
        if b.upper() in upper_sql:
            return jsonify({"error": f"'{b}' is not allowed in the sandbox."})
    try:
        conn, _ = get_sandbox_db(uid)
        results = []
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

@app.route("/sitemap.xml")
def sitemap():
    base = request.host_url.rstrip("/")
    today = datetime.utcnow().strftime("%Y-%m-%d")
    urls = [{"loc": base, "priority": "1.0", "changefreq": "weekly"}]
    for l in ALL_LESSONS:
        urls.append({"loc": f"{base}/lesson/{l['slug']}",
                     "priority": "0.9", "changefreq": "monthly"})
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append(f"""  <url>
    <loc>{u['loc']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{u['changefreq']}</changefreq>
    <priority>{u['priority']}</priority>
  </url>""")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")

@app.route("/robots.txt")
def robots():
    base = request.host_url.rstrip("/")
    return Response(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n",
                    mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
