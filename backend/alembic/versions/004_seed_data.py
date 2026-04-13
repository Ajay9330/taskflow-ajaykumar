"""seed initial data

Revision ID: 004
Revises: 003
Create Date: 2026-04-10 12:00:03.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

USER_ID_1 = uuid.uuid4()
USER_ID_2 = uuid.uuid4()
USER_ID_3 = uuid.uuid4()
USER_ID_4 = uuid.uuid4()
USER_ID_5 = uuid.uuid4()

PROJECT_ID_1 = uuid.uuid4()
PROJECT_ID_2 = uuid.uuid4()

# Hash for password: 'password123'
HASH = "$2b$12$4pAiQvTnKjLA3/1Cu/jAJu6Gjq0VeN0.GpF.4l893JgJMtGMyr1SK"

def upgrade() -> None:
    # Insert users
    op.execute(
        f"INSERT INTO users (id, name, email, password, created_at, updated_at) "
        f"VALUES ('{USER_ID_1}', 'Test User', 'test1@example.com', '{HASH}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO users (id, name, email, password, created_at, updated_at) "
        f"VALUES ('{USER_ID_2}', 'Test User 2', 'test2@example.com', '{HASH}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO users (id, name, email, password, created_at, updated_at) "
        f"VALUES ('{USER_ID_3}', 'Test User 3', 'test3@example.com', '{HASH}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO users (id, name, email, password, created_at, updated_at) "
        f"VALUES ('{USER_ID_4}', 'Test User 4', 'test4@example.com', '{HASH}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO users (id, name, email, password, created_at, updated_at) "
        f"VALUES ('{USER_ID_5}', 'Test User 5', 'test5@example.com', '{HASH}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )

    # Insert projects
    op.execute(
        f"INSERT INTO projects (id, name, description, owner_id, created_at, updated_at) "
        f"VALUES ('{PROJECT_ID_1}', 'Project Alpha', 'First project', '{USER_ID_1}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO projects (id, name, description, owner_id, created_at, updated_at) "
        f"VALUES ('{PROJECT_ID_2}', 'Project Beta', 'Second project', '{USER_ID_2}', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )

    # Insert tasks for Project Alpha
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 1', 'Description for task 1', 'todo', 'low', '{PROJECT_ID_1}', '{USER_ID_1}', now() + interval '1 day', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 2', 'Description for task 2', 'in_progress', 'medium', '{PROJECT_ID_1}', '{USER_ID_2}', now() + interval '2 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 3', 'Description for task 3', 'done', 'high', '{PROJECT_ID_1}', '{USER_ID_3}', now() + interval '3 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 4', 'Description for task 4', 'todo', 'high', '{PROJECT_ID_1}', '{USER_ID_4}', now() + interval '1 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 5', 'Description for task 5', 'in_progress', 'low', '{PROJECT_ID_1}', '{USER_ID_5}', now() + interval '4 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 6', 'Description for task 6', 'done', 'medium', '{PROJECT_ID_1}', '{USER_ID_1}', now() + interval '2 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )

    # Insert tasks for Project Beta
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 7', 'Description for task 7', 'todo', 'medium', '{PROJECT_ID_2}', '{USER_ID_2}', now() + interval '3 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 8', 'Description for task 8', 'in_progress', 'high', '{PROJECT_ID_2}', '{USER_ID_3}', now() + interval '1 day', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 9', 'Description for task 9', 'done', 'low', '{PROJECT_ID_2}', '{USER_ID_4}', now() + interval '5 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 10', 'Description for task 10', 'todo', 'low', '{PROJECT_ID_2}', '{USER_ID_5}', now() + interval '2 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 11', 'Description for task 11', 'in_progress', 'medium', '{PROJECT_ID_2}', '{USER_ID_1}', now() + interval '1 day', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Task 12', 'Description for task 12', 'done', 'high', '{PROJECT_ID_2}', '{USER_ID_2}', now() + interval '4 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )

def downgrade() -> None:
    op.execute("DELETE FROM tasks")
    op.execute("DELETE FROM projects")
    op.execute("DELETE FROM users")
