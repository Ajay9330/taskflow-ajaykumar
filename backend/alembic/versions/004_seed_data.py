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
        f"VALUES ('{uuid.uuid4()}', 'Setup Project Repository', 'Initialize the GitHub repository and setup CI/CD pipelines', 'done', 'high', '{PROJECT_ID_1}', '{USER_ID_1}', now() - interval '5 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Design Database Schema', 'Create ERDs and initial SQL scripts for PostgreSQL', 'done', 'high', '{PROJECT_ID_1}', '{USER_ID_2}', now() - interval '2 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Implement User Auth', 'Add JWT based authentication using FastAPI', 'in_progress', 'high', '{PROJECT_ID_1}', '{USER_ID_3}', now() + interval '2 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Create Kanban UI Component', 'Use React-beautiful-dnd or @hello-pangea/dnd for board', 'in_progress', 'medium', '{PROJECT_ID_1}', '{USER_ID_4}', now() + interval '4 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Setup Server Sent Events', 'Implement live streaming of task updates from backend to frontend', 'todo', 'high', '{PROJECT_ID_1}', '{USER_ID_5}', now() + interval '7 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Write API Documentation', 'Add docstrings and configure Swagger UI', 'todo', 'low', '{PROJECT_ID_1}', '{USER_ID_1}', now() + interval '10 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )

    # Insert tasks for Project Beta
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Market Research', 'Analyze competitor pricing and feature sets', 'done', 'medium', '{PROJECT_ID_2}', '{USER_ID_2}', now() - interval '10 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Draft Initial Pitch Deck', 'Create presentation slides for angel investors', 'in_progress', 'high', '{PROJECT_ID_2}', '{USER_ID_3}', now() + interval '1 day', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Hire Lead Designer', 'Interview candidates for UI/UX lead position', 'in_progress', 'high', '{PROJECT_ID_2}', '{USER_ID_4}', now() + interval '5 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Review Legal Contracts', 'Send incorporation documents to external counsel', 'todo', 'medium', '{PROJECT_ID_2}', '{USER_ID_5}', now() + interval '14 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Order Office Equipment', 'Purchase standing desks and dual monitors', 'todo', 'low', '{PROJECT_ID_2}', '{USER_ID_1}', now() + interval '20 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )
    op.execute(
        f"INSERT INTO tasks (id, title, description, status, priority, project_id, assignee_id, due_date, created_at, updated_at) "
        f"VALUES ('{uuid.uuid4()}', 'Finalize Brand Guidelines', 'Approve logo variants and color palettes', 'todo', 'high', '{PROJECT_ID_2}', '{USER_ID_2}', now() + interval '30 days', now(), now()) "
        f"ON CONFLICT (id) DO NOTHING"
    )

def downgrade() -> None:
    op.execute("DELETE FROM tasks")
    op.execute("DELETE FROM projects")
    op.execute("DELETE FROM users")
