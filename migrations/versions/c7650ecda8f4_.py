"""empty message

Revision ID: c7650ecda8f4
Revises: 
Create Date: 2021-12-26 18:47:59.110632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7650ecda8f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ensaios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=30), nullable=True),
    sa.Column('piloto', sa.Float(), nullable=True),
    sa.Column('rico', sa.Float(), nullable=True),
    sa.Column('pobre', sa.Float(), nullable=True),
    sa.Column('cp', sa.Float(), nullable=True),
    sa.Column('pesobrita', sa.Float(), nullable=True),
    sa.Column('slump', sa.Float(), nullable=True),
    sa.Column('umidade', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cp_piloto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resistencia', sa.Float(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cp_pobre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resistencia', sa.Float(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cp_rico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resistencia', sa.Float(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dosagem_piloto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alfa', sa.Float(), nullable=True),
    sa.Column('c_unitario', sa.Float(), nullable=True),
    sa.Column('a_unitario', sa.Float(), nullable=True),
    sa.Column('b_unitario', sa.Float(), nullable=True),
    sa.Column('c_massa', sa.Float(), nullable=True),
    sa.Column('a_massa', sa.Float(), nullable=True),
    sa.Column('b_massa', sa.Float(), nullable=True),
    sa.Column('c_acr', sa.Float(), nullable=True),
    sa.Column('a_acr', sa.Float(), nullable=True),
    sa.Column('a_massa_umida', sa.Float(), nullable=True),
    sa.Column('umidade_agregado', sa.Float(), nullable=True),
    sa.Column('agua', sa.Float(), nullable=True),
    sa.Column('agua_cimento', sa.Float(), nullable=True),
    sa.Column('indice', sa.Integer(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dosagem_pobre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alfa', sa.Float(), nullable=True),
    sa.Column('c_unitario', sa.Float(), nullable=True),
    sa.Column('a_unitario', sa.Float(), nullable=True),
    sa.Column('b_unitario', sa.Float(), nullable=True),
    sa.Column('c_massa', sa.Float(), nullable=True),
    sa.Column('a_massa', sa.Float(), nullable=True),
    sa.Column('b_massa', sa.Float(), nullable=True),
    sa.Column('c_acr', sa.Float(), nullable=True),
    sa.Column('a_acr', sa.Float(), nullable=True),
    sa.Column('a_massa_umida', sa.Float(), nullable=True),
    sa.Column('umidade_agregado', sa.Float(), nullable=True),
    sa.Column('agua', sa.Float(), nullable=True),
    sa.Column('agua_cimento', sa.Float(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dosagem_rico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alfa', sa.Float(), nullable=True),
    sa.Column('c_unitario', sa.Float(), nullable=True),
    sa.Column('a_unitario', sa.Float(), nullable=True),
    sa.Column('b_unitario', sa.Float(), nullable=True),
    sa.Column('c_massa', sa.Float(), nullable=True),
    sa.Column('a_massa', sa.Float(), nullable=True),
    sa.Column('b_massa', sa.Float(), nullable=True),
    sa.Column('c_acr', sa.Float(), nullable=True),
    sa.Column('a_acr', sa.Float(), nullable=True),
    sa.Column('a_massa_umida', sa.Float(), nullable=True),
    sa.Column('umidade_agregado', sa.Float(), nullable=True),
    sa.Column('agua', sa.Float(), nullable=True),
    sa.Column('agua_cimento', sa.Float(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resultados',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('k1', sa.Float(), nullable=True),
    sa.Column('k2', sa.Float(), nullable=True),
    sa.Column('k3', sa.Float(), nullable=True),
    sa.Column('k4', sa.Float(), nullable=True),
    sa.Column('k5', sa.Float(), nullable=True),
    sa.Column('k6', sa.Float(), nullable=True),
    sa.Column('ensaio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ensaio_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teste',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('a', sa.Float(), nullable=True),
    sa.Column('cu', sa.Float(), nullable=True),
    sa.Column('au', sa.Float(), nullable=True),
    sa.Column('bu', sa.Float(), nullable=True),
    sa.Column('teste_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teste_id'], ['ensaios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teste')
    op.drop_table('resultados')
    op.drop_table('dosagem_rico')
    op.drop_table('dosagem_pobre')
    op.drop_table('dosagem_piloto')
    op.drop_table('cp_rico')
    op.drop_table('cp_pobre')
    op.drop_table('cp_piloto')
    op.drop_table('ensaios')
    # ### end Alembic commands ###