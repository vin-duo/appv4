from app import db

class Ensaios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30))
    piloto = db.Column(db.Integer)
    rico = db.Column(db.Integer)
    pobre = db.Column(db.Integer)
    cp = db.Column(db.Integer)
    pesobrita = db.Column(db.Integer)
    slump = db.Column(db.Integer)
    umidade = db.Column(db.Integer)
    dosagem_piloto = db.relationship('Dosagem_piloto', backref='ensaio')
    dosagem_rico = db.relationship('Dosagem_rico', backref='ensaio')
    dosagem_pobre = db.relationship('Dosagem_pobre', backref='ensaio')
    cp_piloto = db.relationship('Cp_piloto', backref='ensaio')
    cp_rico = db.relationship('Cp_rico', backref='ensaio')
    cp_pobre = db.relationship('Cp_pobre', backref='ensaio')
    resultados = db.relationship('Resultados', backref='ensaio')

    def __repr__(self):
        return '\n<id: {}, nome: {} piloto: {}, rico: {}, pobre: {}, cp: {}, pesobrita: {}, slump: {}, umidade: {}, relation {} >'.format(self.id, self.nome, self.piloto, self.rico, self.pobre, self.cp, self.pesobrita, self.slump, self.umidade, self.dosagem_piloto)


class Dosagem_piloto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alfa = db.Column(db.Float)

    c_unitario = db.Column(db.Float)
    a_unitario = db.Column(db.Float)
    b_unitario = db.Column(db.Float)
    
    c_massa = db.Column(db.Float)
    a_massa = db.Column(db.Float)
    b_massa = db.Column(db.Float)
    
    c_acr = db.Column(db.Float)
    a_acr= db.Column(db.Float)

    a_massa_umida = db.Column(db.Float)    
    umidade_agregado = db.Column(db.Float)
    agua = db.Column(db.Float)
    agua_cimento = db.Column(db.Float)

    indice = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Piloto: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.agua_cimento, self.indice, self.ensaio_id)


class Dosagem_rico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alfa = db.Column(db.Integer)

    c_unitario = db.Column(db.Integer)
    a_unitario = db.Column(db.Integer)
    b_unitario = db.Column(db.Integer)

    c_massa = db.Column(db.Integer)
    a_massa = db.Column(db.Integer)
    b_massa = db.Column(db.Integer)
    
    c_acr = db.Column(db.Integer)
    a_acr= db.Column(db.Integer)
    
    a_massa_umida = db.Column(db.Integer)    
    umidade_agregado = db.Column(db.Integer)
    agua = db.Column(db.Integer)
    agua_cimento = db.Column(db.Integer)

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Rico: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id, self.agua_cimento)


class Dosagem_pobre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alfa = db.Column(db.Integer)

    c_unitario = db.Column(db.Integer)
    a_unitario = db.Column(db.Integer)
    b_unitario = db.Column(db.Integer)
    
    c_massa = db.Column(db.Integer)
    a_massa = db.Column(db.Integer)
    b_massa = db.Column(db.Integer)
    
    c_acr = db.Column(db.Integer)
    a_acr= db.Column(db.Integer)
    
    a_massa_umida = db.Column(db.Integer)
    umidade_agregado = db.Column(db.Integer)
    agua = db.Column(db.Integer)
    agua_cimento = db.Column(db.Integer)

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Pobre: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.a_massa_umida, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id)


class Cp_piloto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Cp_rico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Cp_pobre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Resultados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    k1 = db.Column(db.Integer)
    k2 = db.Column(db.Integer)
    k3 = db.Column(db.Integer)
    k4 = db.Column(db.Integer)
    k5 = db.Column(db.Integer)
    k6 = db.Column(db.Integer)

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<k1 {}, k2 {}, k3 {}, k4 {}, k5 {}, k6 {}>'.format(self.k1, self.k2, self.k3, self.k4, self.k5, self.k6)


