"""add hospital insights tables

Revision ID: add_hospital_insights
Revises: db3d46e06c3d
Create Date: 2025-11-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_hospital_insights'
down_revision = 'db3d46e06c3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create hospital_budgets table
    op.create_table('hospital_budgets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('facility_id', sa.String(), nullable=False),
    sa.Column('facility_name', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('total_budget', sa.Float(), nullable=False),
    sa.Column('allocated_budget', sa.Float(), nullable=False),
    sa.Column('available_budget', sa.Float(), nullable=False),
    sa.Column('emergency_preparedness', sa.Float(), nullable=False),
    sa.Column('staff_resources', sa.Float(), nullable=False),
    sa.Column('equipment_supplies', sa.Float(), nullable=False),
    sa.Column('infrastructure', sa.Float(), nullable=False),
    sa.Column('research_development', sa.Float(), nullable=False),
    sa.Column('other', sa.Float(), nullable=False),
    sa.Column('recommended_allocation', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('risk_adjusted_budget', sa.Float(), nullable=True),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('period_start', sa.DateTime(timezone=True), nullable=False),
    sa.Column('period_end', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hospital_budgets_id'), 'hospital_budgets', ['id'], unique=False)
    op.create_index(op.f('ix_hospital_budgets_tenant_id'), 'hospital_budgets', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_hospital_budgets_facility_id'), 'hospital_budgets', ['facility_id'], unique=False)
    op.create_index(op.f('ix_hospital_budgets_timestamp'), 'hospital_budgets', ['timestamp'], unique=False)

    # Create resource_allocations table
    op.create_table('resource_allocations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('facility_id', sa.String(), nullable=False),
    sa.Column('facility_name', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('resource_type', sa.String(), nullable=False),
    sa.Column('current_capacity', sa.Float(), nullable=False),
    sa.Column('recommended_capacity', sa.Float(), nullable=False),
    sa.Column('utilization_rate', sa.Float(), nullable=False),
    sa.Column('current_allocation', sa.Float(), nullable=False),
    sa.Column('recommended_allocation', sa.Float(), nullable=False),
    sa.Column('allocation_reason', sa.Text(), nullable=True),
    sa.Column('priority_level', sa.String(), nullable=False),
    sa.Column('risk_score_id', sa.Integer(), nullable=True),
    sa.Column('risk_level', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['risk_score_id'], ['risk_scores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resource_allocations_id'), 'resource_allocations', ['id'], unique=False)
    op.create_index(op.f('ix_resource_allocations_tenant_id'), 'resource_allocations', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_resource_allocations_facility_id'), 'resource_allocations', ['facility_id'], unique=False)
    op.create_index(op.f('ix_resource_allocations_timestamp'), 'resource_allocations', ['timestamp'], unique=False)

    # Create hospital_recommendations table
    op.create_table('hospital_recommendations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('facility_id', sa.String(), nullable=False),
    sa.Column('facility_name', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('recommendation_type', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('priority', sa.String(), nullable=False),
    sa.Column('estimated_impact', sa.String(), nullable=True),
    sa.Column('estimated_cost', sa.Float(), nullable=True),
    sa.Column('estimated_savings', sa.Float(), nullable=True),
    sa.Column('implementation_steps', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('timeframe', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('risk_score_id', sa.Integer(), nullable=True),
    sa.Column('related_metrics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['risk_score_id'], ['risk_scores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hospital_recommendations_id'), 'hospital_recommendations', ['id'], unique=False)
    op.create_index(op.f('ix_hospital_recommendations_tenant_id'), 'hospital_recommendations', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_hospital_recommendations_facility_id'), 'hospital_recommendations', ['facility_id'], unique=False)
    op.create_index(op.f('ix_hospital_recommendations_timestamp'), 'hospital_recommendations', ['timestamp'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_hospital_recommendations_timestamp'), table_name='hospital_recommendations')
    op.drop_index(op.f('ix_hospital_recommendations_facility_id'), table_name='hospital_recommendations')
    op.drop_index(op.f('ix_hospital_recommendations_tenant_id'), table_name='hospital_recommendations')
    op.drop_index(op.f('ix_hospital_recommendations_id'), table_name='hospital_recommendations')
    op.drop_table('hospital_recommendations')
    op.drop_index(op.f('ix_resource_allocations_timestamp'), table_name='resource_allocations')
    op.drop_index(op.f('ix_resource_allocations_facility_id'), table_name='resource_allocations')
    op.drop_index(op.f('ix_resource_allocations_tenant_id'), table_name='resource_allocations')
    op.drop_index(op.f('ix_resource_allocations_id'), table_name='resource_allocations')
    op.drop_table('resource_allocations')
    op.drop_index(op.f('ix_hospital_budgets_timestamp'), table_name='hospital_budgets')
    op.drop_index(op.f('ix_hospital_budgets_facility_id'), table_name='hospital_budgets')
    op.drop_index(op.f('ix_hospital_budgets_tenant_id'), table_name='hospital_budgets')
    op.drop_index(op.f('ix_hospital_budgets_id'), table_name='hospital_budgets')
    op.drop_table('hospital_budgets')

