"""Initial tables

Revision ID: 0001
Revises: 
Create Date: 2024-06-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('provider', sa.String, nullable=False),
        sa.Column('collection', sa.String, nullable=False),
        sa.Column('product_id', sa.String, unique=True, nullable=False),
        sa.Column('acquisition_time', sa.DateTime, nullable=False),
        sa.Column('cloud_pct', sa.Float),
        sa.Column('properties', sa.JSON),
        sa.Column('footprint', geoalchemy2.types.Geometry('POLYGON', srid=4326)),
    )
    op.create_table(
        'assets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('kind', sa.String, nullable=False),
        sa.Column('uri', sa.String, nullable=False),
        sa.Column('checksum', sa.String),
        sa.Column('mime', sa.String),
        sa.Column('bytes', sa.Integer),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_table(
        'stats',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('aoi_geom', geoalchemy2.types.Geometry('POLYGON', srid=4326)),
        sa.Column('ndvi_mean', sa.Float),
        sa.Column('ndvi_std', sa.Float),
        sa.Column('px_count', sa.Integer),
        sa.Column('pct_cloud', sa.Float),
        sa.Column('bands', sa.JSON),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kind', sa.String),
        sa.Column('status', sa.String),
        sa.Column('started_at', sa.DateTime),
        sa.Column('finished_at', sa.DateTime),
        sa.Column('log_uri', sa.String),
        sa.Column('params', sa.JSON),
    )

def downgrade():
    op.drop_table('jobs')
    op.drop_table('stats')
    op.drop_table('assets')
    op.drop_table('products')
