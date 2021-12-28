from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired



class Formulario_teste(FlaskForm):
    valor = FloatField('Valor teste')
    selection = SelectField('Selecione: ', choices=[('7', '7'),('20', '20'),('28','28')])
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
    volume_recipiente = FloatField('Volume do recipiente (m3)')
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
