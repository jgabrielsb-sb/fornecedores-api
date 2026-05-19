"""adding logs table

Revision ID: e7f8a9b0c1d2
Revises: f1e2d3c4b5a6
Create Date: 2026-05-18 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'e7f8a9b0c1d2'
down_revision: Union[str, Sequence[str], None] = 'f1e2d3c4b5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trace_id', sa.String(), nullable=False),
        sa.Column('execution_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('process_name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_logs_id'), 'logs', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_logs_id'), table_name='logs')
    op.drop_table('logs')
