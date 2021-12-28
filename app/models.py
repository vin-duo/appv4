from app import db

class Consumo_piloto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kg_piloto = db.Column(db.Float)
    kg_piloto_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

class Consumo_rico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kg_rico = db.Column(db.Float)
    kg_rico_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

class Consumo_pobre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kg_pobre = db.Column(db.Float)
    kg_pobre_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

class Ensaios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30))
    piloto = db.Column(db.Float)
    rico = db.Column(db.Float)
    pobre = db.Column(db.Float)
    cp = db.Column(db.Float)
    pesobrita = db.Column(db.Float)
    slump = db.Column(db.Float)
    umidade = db.Column(db.Float)
    volume = db.Column(db.Float)
    dosagem_piloto = db.relationship('Dosagem_piloto', backref='ensaio')
    dosagem_rico = db.relationship('Dosagem_rico', backref='ensaio')
    dosagem_pobre = db.relationship('Dosagem_pobre', backref='ensaio')
    cp_piloto = db.relationship('Cp_piloto', backref='ensaio')
    cp_rico = db.relationship('Cp_rico', backref='ensaio')
    cp_pobre = db.relationship('Cp_pobre', backref='ensaio')
    resultados = db.relationship('Resultados', backref='ensaio')
    teste = db.relationship('Teste', backref='ensaio')
    consumo_piloto = db.relationship('Consumo_piloto', backref='ensaio')
    consumo_rico = db.relationship('Consumo_rico', backref='ensaio')
    consumo_pobre = db.relationship('Consumo_pobre', backref='ensaio')
    def __repr__(self):
        return '\n<id: {}, nome: {} piloto: {}, rico: {}, pobre: {}, cp: {}, pesobrita: {}, slump: {}, umidade: {}, relation {} >'.format(self.id, self.nome, self.piloto, self.rico, self.pobre, self.cp, self.pesobrita, self.slump, self.umidade, self.dosagem_piloto)



class Teste(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    a = db.Column(db.Float)
    cu = db.Column(db.Float)
    au = db.Column(db.Float)
    bu = db.Column(db.Float)
    cm = db.Column(db.Float)
    am = db.Column(db.Float)
    bm = db.Column(db.Float)
    cacr = db.Column(db.Float)
    aacr = db.Column(db.Float)
    teste_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))
#falta a agua


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

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Rico: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id, self.agua_cimento)


class Dosagem_pobre(db.Model):
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

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Pobre: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.a_massa_umida, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id)


class Cp_piloto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Float)
    idade = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Cp_rico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Float)
    idade = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Cp_pobre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Float)
    idade = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Resultados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    k1 = db.Column(db.Float)
    k2 = db.Column(db.Float)
    k3 = db.Column(db.Float)
    k4 = db.Column(db.Float)
    k5 = db.Column(db.Float)
    k6 = db.Column(db.Float)

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<k1 {}, k2 {}, k3 {}, k4 {}, k5 {}, k6 {}>'.format(self.k1, self.k2, self.k3, self.k4, self.k5, self.k6)


