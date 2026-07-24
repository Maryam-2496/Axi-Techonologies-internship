## Schema Definition

### users table
| Column        | Type         | Constraints                |
|---------------|--------------|-----------------------------|
| id            | INTEGER      | PRIMARY KEY                |
| username      | VARCHAR(80)  | UNIQUE, NOT NULL           |
| email         | VARCHAR(120) | UNIQUE, NOT NULL           |
| password_hash | VARCHAR(255) | NOT NULL                   |

### posts table
| Column      | Type         | Constraints                                  |
|-------------|--------------|-----------------------------------------------|
| id          | INTEGER      | PRIMARY KEY                                  |
| title       | VARCHAR(150) | NOT NULL                                     |
| content     | TEXT         | NOT NULL                                     |
| created_at  | DATETIME     | DEFAULT current time                        |
| updated_at  | DATETIME     | DEFAULT current time, updates on change      |
| user_id     | INTEGER      | FOREIGN KEY → users.id, ON DELETE CASCADE, NOT NULL |

## Migrations Note

`db.create_all()` only creates NEW tables — it does not modify existing tables
if their structure changes later (e.g. adding a new column). This works fine
 since we're creating fresh tables.

In a real production project, you'd use **Flask-Migrate** (built on Alembic) instead:
- `flask db init`     → sets up a migrations/ folder (one-time)
- `flask db migrate -m "add posts table"`  → auto-generates a migration script by
  comparing your models to the current DB schema
- `flask db upgrade`  → actually applies that script to the database

This lets you evolve your schema safely over time without dropping/recreating
tables and losing existing data — something create_all() can't do.