from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3dc958093cec'
down_revision = None  # Since you've reset the migrations
branch_labels = None
depends_on = None

def upgrade():
    # Drop foreign key constraints in child tables
    op.drop_constraint('projects_OrgID_fkey', 'projects', type_='foreignkey')
    op.drop_constraint('resources_OrgID_fkey', 'resources', type_='foreignkey')
    op.drop_constraint('teams_OrgID_fkey', 'teams', type_='foreignkey')

    # Alter OrgID column type in parent table 'organizations'
    with op.batch_alter_table('organizations') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.Integer(),
                              type_=sa.String(),
                              nullable=False)

    # Alter OrgID column type in child tables
    with op.batch_alter_table('projects') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.Integer(),
                              type_=sa.String(),
                              nullable=False)

    with op.batch_alter_table('resources') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.Integer(),
                              type_=sa.String(),
                              nullable=False)

    with op.batch_alter_table('teams') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.Integer(),
                              type_=sa.String(),
                              nullable=False)

    # Recreate foreign key constraints with updated types
    op.create_foreign_key(
        'projects_OrgID_fkey',
        'projects', 'organizations',
        ['OrgID'], ['OrgID'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'resources_OrgID_fkey',
        'resources', 'organizations',
        ['OrgID'], ['OrgID'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'teams_OrgID_fkey',
        'teams', 'organizations',
        ['OrgID'], ['OrgID'],
        ondelete='CASCADE'
    )

def downgrade():
    # Drop foreign key constraints in child tables
    op.drop_constraint('projects_OrgID_fkey', 'projects', type_='foreignkey')
    op.drop_constraint('resources_OrgID_fkey', 'resources', type_='foreignkey')
    op.drop_constraint('teams_OrgID_fkey', 'teams', type_='foreignkey')

    # Revert OrgID column type in child tables
    with op.batch_alter_table('teams') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.String(),
                              type_=sa.Integer(),
                              nullable=False)

    with op.batch_alter_table('resources') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.String(),
                              type_=sa.Integer(),
                              nullable=False)

    with op.batch_alter_table('projects') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.String(),
                              type_=sa.Integer(),
                              nullable=False)

    # Revert OrgID column type in parent table 'organizations'
    with op.batch_alter_table('organizations') as batch_op:
        batch_op.alter_column('OrgID',
                              existing_type=sa.String(),
                              type_=sa.Integer(),
                              nullable=False)

    # Recreate foreign key constraints with original types
    op.create_foreign_key(
        'projects_OrgID_fkey',
        'projects', 'organizations',
        ['OrgID'], ['OrgID'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'resources_OrgID_fkey',
        'resources', 'organizations',
        ['OrgID'], ['OrgID'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'teams_OrgID_fkey',
        'teams', 'organizations',
        ['OrgID'], ['OrgID'],
        ondelete='CASCADE'
    )
