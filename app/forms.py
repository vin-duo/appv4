from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired



class Formulario_teste(FlaskForm):
    valor = FloatField('Valor teste')
    enviar = SubmitField('enviar para teste')


    # FORMS

class Criar_ensaio(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    piloto = FloatField('Traço Piloto')
    rico = FloatField('Traço Rico')
    pobre = FloatField('Traço Pobre')
#    cp = FloatField('cp')
    pesobrita = FloatField('Brita (kg)')
    slump = FloatField('slump (mm)')
#    umidade = FloatField('umidade (%)')

    submit = SubmitField('Registrar')

class Alfa(FlaskForm):
    alfa = FloatField('Alfa:')
    submit = SubmitField('Registrar')

class Alfa_auxiliar(FlaskForm):
    alfa_auxiliar = FloatField('Alfa:')
    submit = SubmitField('Registrar')

class Calcular(FlaskForm):
    resistencia = FloatField('Resistencia')
    calcular = SubmitField('Calcular')




'''
class Alfa_ideal(FlaskForm):
    alfa_ideal = QuerySelectField(allow_blank=True, get_label='id')
'''
