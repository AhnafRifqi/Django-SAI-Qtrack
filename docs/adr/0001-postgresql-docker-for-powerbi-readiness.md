# 0001. Use PostgreSQL in Docker Instead of SQLite

Django defaults to SQLite for local development. For SAI-Qtrack, we use PostgreSQL running in a Docker container because PT SAI requires integration with analytics tools (PowerBI) and strict relational concurrency matching production manufacturing execution systems. Direct ODBC/PostgreSQL connectors allow PowerBI to query shopfloor scrap tables without altering the web app runtime.
