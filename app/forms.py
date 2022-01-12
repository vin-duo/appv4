from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired


class Formulario_teste(FlaskForm):
    valor = FloatField('Valor teste')
    selection = SelectField('Selecione: ', choices=[('7', '7'),('20', '20'),('28','28')])
    enviar = SubmitField('enviar para teste')

class Criar_ensaio(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired(message='Campo necessario')])
    piloto = FloatField('Traço Piloto', validators=[InputRequired(message='Campo necessario')])
    rico = FloatField('Traço Rico', validators=[InputRequired(message='Campo necessario')])
    pobre = FloatField('Traço Pobre', validators=[InputRequired(message='Campo necessario')])
#    cp = FloatField('cp')
    pesobrita = FloatField('Brita (kg)', validators=[InputRequired(message='Campo necessario')])
    slump = FloatField('slump (mm)', validators=[InputRequired(message='Campo necessario')])
#    umidade = FloatField('umidade (%)')
    volume_recipiente = FloatField('Volume do recipiente (m3)', validators=[InputRequired(message='Campo necessario')])
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

