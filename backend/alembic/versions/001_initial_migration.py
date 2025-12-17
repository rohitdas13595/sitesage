"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-12-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create seo_reports table
    op.create_table(
        'seo_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('h1_tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('h2_tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('images', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('load_time', sa.Float(), nullable=True),
        sa.Column('seo_score', sa.Float(), nullable=True),
        sa.Column('missing_alt_tags', sa.Integer(), server_default='0'),
        sa.Column('broken_links', sa.Integer(), server_default='0'),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('ai_suggestions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('full_report', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_seo_reports_id'), 'seo_reports', ['id'], unique=False)
    op.create_index(op.f('ix_seo_reports_url'), 'seo_reports', ['url'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_seo_reports_url'), table_name='seo_reports')
    op.drop_index(op.f('ix_seo_reports_id'), table_name='seo_reports')
    op.drop_table('seo_reports')
