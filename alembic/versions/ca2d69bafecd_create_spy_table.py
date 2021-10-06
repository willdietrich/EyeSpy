"""create spy table

Revision ID: ca2d69bafecd
Revises: 
Create Date: 2021-10-01 10:24:08.973713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca2d69bafecd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'DiscordSpys',
        sa.Column('DiscordSpyId',
                  sa.INTEGER,
                  primary_key=True),
        sa.Column('DiscordName',
                  sa.TEXT,
                  nullable=False)
    )

    op.create_table(
        'DiscordSpyTargets',
        sa.Column('DiscordSpyTargetId',
                  sa.INTEGER,
                  primary_key=True),
        sa.Column('DiscordSpyId',
                  sa.INTEGER,
                  sa.ForeignKey('DiscordSpys.DiscordSpyId', name='fk_discordspytargets_discordspyid_discordspys'),
                  nullable=False),
        sa.Column('DiscordName',
                  sa.TEXT,
                  nullable=False)
    )

    op.create_table(
        'discord_status',
        sa.Column('username',
                  sa.TEXT,
                  nullable=False),
        sa.Column('status',
                  sa.TEXT),
        sa.Column('activity',
                  sa.TEXT),
        sa.Column('timestamp',
                  sa.INTEGER)
    )


def downgrade():
    op.drop_table('DiscordSpys')
    op.drop_table('DiscordSpyTargets')
