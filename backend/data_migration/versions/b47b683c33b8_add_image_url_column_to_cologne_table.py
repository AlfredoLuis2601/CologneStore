"""add image_url column to cologne table

Revision ID: b47b683c33b8
Revises: 
Create Date: 2026-08-03 14:33:06.510598

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b47b683c33b8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    target_table = None
    for table in existing_tables:
        if table.lower() in ("cologneinfo", "cologne_info", "cologne"):
            target_table = table
            break
    if target_table:
        existing_columns = [col['name'] for col in inspector.get_columns(target_table)]
        if 'image_url' not in existing_columns:
            table_name_to_use = f'"{target_table}"' if any(c.isupper() for c in target_table) else target_table
            op.add_column(
                table_name_to_use, 
                sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True)
            )
    else:
        op.create_table(
            'cologneinfo',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('price', sa.Float(), nullable=False),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )

def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    for table in existing_tables:
        if table.lower() in ("cologneinfo", "cologne_info", "cologne"):
            table_name_to_use = f'"{table}"' if any(c.isupper() for c in table) else table
            op.drop_column(table_name_to_use, 'image_url')
            break