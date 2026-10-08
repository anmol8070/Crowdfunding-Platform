# Architecture
BackerWave follows the standard Django Model-View-Template (MVT) architecture.
- **Models**: Defines database schema (SQLite in development, PostgreSQL ready).
- **Views**: Business logic, filtering, sorting, permissions.
- **Templates**: Bootstrap 5 with server-side rendered HTML.
- **Apps**: `accounts`, `core`, `campaigns`, `contributions`.
