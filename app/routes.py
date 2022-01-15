from flask import Flask, render_template, redirect, url_for, request
from app import app, db
from app.forms import Criar_ensaio, Alfa, Alfa_auxiliar, Calcular, Formulario_teste
from app.models import Ensaios, Dosagem_piloto, Dosagem_rico, Dosagem_pobre, Cp_piloto, Cp_rico, Cp_pobre, Resultados, Teste, Consumo_piloto, Consumo_rico, Consumo_pobre
from app.regressao import Regressao, Calculadora
from app.traco_dosagem import Ensaio

@app.route('/')
@app.route('/home')
def home():
    ensaios_registrados = Ensaios.query.order_by(Ensaios.id).all()
    return render_template('home.html', ensaios_registrados=ensaios_registrados)


#TESTE
@app.route('/teste/<int:id>', methods=['POST', 'GET'])
def teste(id):

    form = Formulario_teste()
    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    dosagens_do_ensaio_salvo = ensaio_salvo.teste

    m = ensaio_salvo.piloto
    pesobrita = ensaio_salvo.pesobrita
    slump = ensaio_salvo.slump

    mensagem = 'nada'
    if dosagens_do_ensaio_salvo != []:
        mensagem = 'dosagens_do_ensaio_salvo nao esta vazio'
        contador = 0
        indice = 0

        for i in dosagens_do_ensaio_salvo:
            alfa = i.a

            if contador == 0:
                alfaantigo = 0
            else:
                alfaantigo = dosagens_do_ensaio_salvo[contador-1].a

            traco = Ensaio(
                m = m,
                alfa = alfa, 
                pesobrita = pesobrita,
                alfaantigo = alfaantigo)
            i.a = alfa
            i.cu = traco.massas_unitarias()[0]
            i.au = traco.massas_unitarias()[1]
            i.bu = traco.massas_unitarias()[2]

            i.cm = traco.massas_iniciais()[0]
            i.am = traco.massas_iniciais()[1]
            i.bm = traco.massas_iniciais()[2]
            
            i.cacr = traco.quantidades_adicionar()[0]
            i.aacr = traco.quantidades_adicionar()[1]

            i.ensaio = ensaio_salvo

            db.session.commit()
            contador = contador + 1
            indice = indice + 1


    if form.validate_on_submit():
        testando = Teste(a=form.valor.data, ensaio=ensaio_salvo)
        db.session.add(testando)
        db.session.commit()
        return redirect('/teste/{}'.format(id))
    return render_template('teste.html', form=form, id=id, m=m, pesobrita=pesobrita, slump=slump, mensagem=mensagem, dosagens_do_ensaio_salvo=dosagens_do_ensaio_salvo)
#TESTE


@app.route('/user/<name>')
def user(name):
    return render_template('user.html')


@app.route('/criar', methods=['POST', 'GET'])
def criar():

    form = Criar_ensaio()
    if form.validate_on_submit():

        novo_ensaio = Ensaios(
        nome = form.nome.data,
        piloto = form.piloto.data,
        rico = form.rico.data,
        pobre = form.pobre.data,
        pesobrita = form.pesobrita.data,
        slump = form.slump.data,
        volume = form.volume_recipiente.data)
        db.session.add(novo_ensaio)
        db.session.commit()

        return redirect('/home')
    return render_template('criar.html', form=form)


@app.route('/home/<int:id>')
def apagar_ensaio(id):

    apagar_ensaio = Ensaios.query.get_or_404(id)

    def objetos_para_deletar(obj):
        for i in obj:
            db.session.delete(i)

    try:
        objetos_para_deletar(Resultados.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Consumo_piloto.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Consumo_rico.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Consumo_pobre.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Cp_piloto.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Cp_rico.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Cp_pobre.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Dosagem_rico.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Dosagem_pobre.query.filter_by(ensaio_id=id).all())
        objetos_para_deletar(Dosagem_piloto.query.filter_by(ensaio_id=id).all())
        db.session.delete(apagar_ensaio)
        db.session.commit()
        return redirect('/home')

    except:
        "DEU ERRADO"


@app.route('/editar_ensaio/<int:id>', methods=['POST', 'GET'])
def editar_ensaio(id):

    form = Criar_ensaio()

    editar = Ensaios.query.get_or_404(id)
    print(editar.volume)
    if form.validate_on_submit():
        editar.nome = form.nome.data
        editar.piloto = form.piloto.data
        editar.rico = form.rico.data
        editar.pobre = form.pobre.data
#        editar.cp = form.cp.data
        editar.pesobrita = form.pesobrita.data
        editar.slump = form.slump.data
#        editar.umidade = form.umidade.data
        editar.volume = form.volume_recipiente.data
        db.session.commit()
        return redirect('/home')
    return render_template('editar_ensaio.html', form=form, editar=editar)


@app.route('/dosagem/<int:id>', methods=['POST', 'GET'])
def dosagem(id):
    form = Alfa()

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    dosagens_do_ensaio_salvo = ensaio_salvo.dosagem_piloto
    m = ensaio_salvo.piloto
#    cp = ensaio_salvo.cp
    pesobrita = ensaio_salvo.pesobrita
    slump = ensaio_salvo.slump
#    umidade = ensaio_salvo.umidade

    alfa_ordenado = Dosagem_piloto.query.filter_by(ensaio_id=id).order_by(Dosagem_piloto.alfa).all()
    if dosagens_do_ensaio_salvo != []:
        contador = 0
        indice = 1
        for i in alfa_ordenado:
            alfa = i.alfa
            if contador == 0:
                alfaantigo = 0
            else:
                alfaantigo = alfa_ordenado[contador-1].alfa

            traco = Ensaio(
                m = m,
                alfa = alfa, 
                pesobrita = pesobrita,
                alfaantigo = alfaantigo)

            i.alfa = alfa
            i.c_unitario = traco.massas_unitarias()[0]
            i.a_unitario = traco.massas_unitarias()[1]
            i.b_unitario = traco.massas_unitarias()[2]

            i.c_massa = traco.massas_iniciais()[0]
            i.a_massa = traco.massas_iniciais()[1]
            i.b_massa = traco.massas_iniciais()[2]
            
            i.c_acr = traco.quantidades_adicionar()[0]
            i.a_acr = traco.quantidades_adicionar()[1]

            i.a_massa_umida = traco.umidade_agregado()[0]
            i.umidade_agregado = traco.umidade_agregado()[1]

            i.ensaio = ensaio_salvo
            i.indice = indice

            db.session.commit()
            contador = contador + 1
            indice = indice + 1

    if form.validate_on_submit():
        add_no_db = Dosagem_piloto(alfa=form.alfa.data, agua=0, ensaio=ensaio_salvo)
        db.session.add(add_no_db)
        db.session.commit()
        return redirect ('/dosagem/{}'.format(id))
    return render_template("dosagem.html", form=form, id=id, dosagens_do_ensaio_salvo=dosagens_do_ensaio_salvo, m=m, slump=slump, pesobrita=pesobrita, alfa_ordenado=alfa_ordenado)


@app.route("/agua", methods=["POST"])
def update_agua():#o nome "valor_alfa" é o nome dado no html para um elemento na tabela do db. Quando cria uma linha no db, a tabela chama essa linha de "valor_alfa", que tem as propriedades "id", "alfa", "agua"......
    i_id = request.form.get("i_id")
    valor_agua_novo = request.form.get("valor_agua_novo")
    nova_agua = Dosagem_piloto.query.filter_by(id=i_id).first()
    nova_agua.agua = valor_agua_novo
    db.session.commit()
    a = nova_agua.ensaio.id
    return redirect("/dosagem/{}".format(a))


@app.route("/agua_rico", methods=["POST"])
def update_agua_rico():#o nome "valor_alfa" é o nome dado no html para um elemento na tabela do db. Quando cria uma linha no db, a tabela chama essa linha de "valor_alfa", que tem as propriedades "id", "alfa", "agua"......
    i_id = request.form.get("i_id")
    valor_agua_novo = request.form.get("valor_agua_novo")
    nova_agua = Dosagem_rico.query.filter_by(id=i_id).first()
    nova_agua.agua = valor_agua_novo
    db.session.commit()
    a = nova_agua.ensaio.id
    return redirect("/auxiliar/{}".format(a))


@app.route("/agua_pobre", methods=["POST"])
def update_agua_pobre():#o nome "valor_alfa" é o nome dado no html para um elemento na tabela do db. Quando cria uma linha no db, a tabela chama essa linha de "valor_alfa", que tem as propriedades "id", "alfa", "agua"......
    i_id = request.form.get("i_id")
    valor_agua_novo = request.form.get("valor_agua_novo")
    nova_agua = Dosagem_pobre.query.filter_by(id=i_id).first()
    nova_agua.agua = valor_agua_novo
    db.session.commit()
    a = nova_agua.ensaio.id
    return redirect("/auxiliar/{}".format(a))


@app.route('/auxiliar/<int:id>', methods=['POST', 'GET'])
def dosagem_auxiliar(id):

    form = Alfa_auxiliar()
    ensaio_salvo = Ensaios.query.filter_by(id=id).first()

    m = ensaio_salvo.piloto
    mp = ensaio_salvo.pobre
    mr = ensaio_salvo.rico
    if m % 1 == 0:
        m = int(m)
    if mp % 1 == 0:
        mp = int(mp)
    if mr % 1 == 0:
        mr = int(mr)

    m_rico = ensaio_salvo.rico
    m_pobre = ensaio_salvo.pobre
#    cp = ensaio_salvo.cp
    alfa = form.alfa_auxiliar.data
    pesobrita = ensaio_salvo.pesobrita
    slump = ensaio_salvo.slump

    if form.validate_on_submit():
        if ensaio_salvo.dosagem_rico == []:
            traco = Ensaio(
                m = m_rico,
                alfa = form.alfa_auxiliar.data, 
                pesobrita = pesobrita)

            add_no_db_rico = Dosagem_rico(
                alfa = form.alfa_auxiliar.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)

            traco = Ensaio(
                m = m_pobre,
                alfa = form.alfa_auxiliar.data, 
                pesobrita = pesobrita)

            add_no_db_pobre = Dosagem_pobre(
                alfa = form.alfa_auxiliar.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)

            db.session.add(add_no_db_rico)
            db.session.add(add_no_db_pobre)
            db.session.commit()

        else:
            rico_velho = ensaio_salvo.dosagem_rico[0]
            pobre_velho = ensaio_salvo.dosagem_pobre[0]
            db.session.delete(rico_velho)
            db.session.delete(pobre_velho)
            db.session.commit()

            traco = Ensaio(
                m = m_rico,
                alfa = form.alfa_auxiliar.data, 
                pesobrita = pesobrita)

            add_no_db_rico = Dosagem_rico(
                alfa = form.alfa_auxiliar.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)

            traco = Ensaio(
                m = m_pobre,
                alfa = form.alfa_auxiliar.data, 
                pesobrita = pesobrita)

            add_no_db_pobre = Dosagem_pobre(
                alfa = form.alfa_auxiliar.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)
            db.session.add(add_no_db_rico)
            db.session.add(add_no_db_pobre)
            db.session.commit()
        return redirect('/auxiliar/{}'.format(id))
    return render_template("auxiliar.html", form=form, ensaio_salvo=ensaio_salvo, id=id, m_rico=m_rico, m_pobre=m_pobre, slump=slump, m=m, mp=mp, mr=mr)


@app.route('/dosagem/delete/<int:id>')#esse id é da linha na tabela Dosagem_piloto
def delete(id):
    #linha da dosagem a ser deletara
    dosagem_deletada = Dosagem_piloto.query.filter_by(id=id).first()
    #id do ensaio que essa dosagem pertence (.ensaio é o backref pra achar o o elemento "pai")
    dosagem_deletada.ensaio.id

    db.session.delete(dosagem_deletada)
    db.session.commit()

    return redirect('/dosagem/{}'.format(dosagem_deletada.ensaio.id))


@app.route('/dosagem_auxiliar/delete/<int:id>')#esse id é da linha na tabela Dosagem_piloto
def delete_auxiliar(id):
    #linha da dosagem a ser deletada
    dosagem_deletada_rico = Dosagem_rico.query.filter_by(id=id).first()
    dosagem_deletada_pobre = Dosagem_pobre.query.filter_by(id=id).first()

    id_do_ensaio = dosagem_deletada_rico.ensaio.id

    #id do ensaio que essa dosagem pertence (.ensaio é o backref pra achar o o elemento "pai")
#    dosagem_deletada_pobre.ensaio.id
#    dosagem_deletada_pobre.ensaio.id

    db.session.delete(dosagem_deletada_rico)
    db.session.delete(dosagem_deletada_pobre)
    db.session.commit()

    return redirect('/auxiliar/{}'.format(id_do_ensaio))


@app.route('/corpo_de_prova/<int:id>', methods=['POST', 'GET'])
def corpo_de_prova(id):

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    cps_piloto = Cp_piloto.query.all()
    cps_rico = Cp_rico.query.all()
    cps_pobre = Cp_pobre.query.all()
    r_piloto = request.form.get("resistencia_piloto")
    r_rico = request.form.get("resistencia_rico")
    r_pobre = request.form.get("resistencia_pobre")

    if request.method == 'POST':
        age = request.form.get("selectfield")
        if r_piloto != "":
            cp_piloto = Cp_piloto(resistencia=r_piloto, idade=age, ensaio=ensaio_salvo)
            db.session.add(cp_piloto)
            db.session.commit()
        if r_rico != "":
            cp_rico = Cp_rico(resistencia=r_rico, idade=age, ensaio=ensaio_salvo)
            db.session.add(cp_rico)
            db.session.commit()
        if r_pobre != "":
            cp_pobre = Cp_pobre(resistencia=r_pobre, idade=age, ensaio=ensaio_salvo)
            db.session.add(cp_pobre)
            db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(id))
    return render_template('corpo_de_prova.html', id=id, cps_piloto=cps_piloto, cps_rico=cps_rico, cps_pobre=cps_pobre, ensaio_salvo=ensaio_salvo)


@app.route('/consumo_cimento/<int:id>', methods=['POST', 'GET'])
def consumo_cimento(id):

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    consumo_piloto_salvo = Consumo_piloto.query.filter_by(ensaio_id=id).first()
    consumo_pobre_salvo = Consumo_pobre.query.filter_by(ensaio_id=id).first()
    consumo_rico_salvo = Consumo_rico.query.filter_by(ensaio_id=id).first()

    recipiente = ensaio_salvo.volume
    '''
    massa_piloto = consumo_piloto_salvo.kg_piloto
    massa_rico = consumo_pobre_salvo.kg_rico
    massa_pobre = consumo_rico_salvo.kg_pobre
    '''
    m_piloto = request.form.get("massa_piloto")
    m_rico = request.form.get("massa_rico")
    m_pobre = request.form.get("massa_pobre")

    if request.method == 'POST':
        if m_piloto != "":
            if consumo_piloto_salvo == None:
                kg_piloto = Consumo_piloto(kg_piloto=m_piloto, ensaio=ensaio_salvo)
                db.session.add(kg_piloto)
                db.session.commit()
            else:
                consumo_piloto_salvo.kg_piloto = m_piloto
                db.session.commit()
        if m_rico != "":
            if consumo_rico_salvo == None:
                kg_rico = Consumo_rico(kg_rico=m_rico, ensaio=ensaio_salvo)
                db.session.add(kg_rico)
                db.session.commit()
            else:
                consumo_rico_salvo.kg_rico = m_rico
                db.session.commit()
        if m_pobre != "":
            if consumo_pobre_salvo == None:
                kg_pobre = Consumo_pobre(kg_pobre=m_pobre, ensaio=ensaio_salvo)
                db.session.add(kg_pobre)
                db.session.commit()
            else:
                consumo_pobre_salvo.kg_pobre = m_pobre
                db.session.commit()
        return redirect('/consumo_cimento/{}'.format(id))
    return render_template('consumo.html', id=id, consumo_piloto_salvo=consumo_piloto_salvo, consumo_pobre_salvo=consumo_pobre_salvo, consumo_rico_salvo=consumo_rico_salvo, ensaio_salvo=ensaio_salvo, recipiente=recipiente)


@app.route('/corpo_de_prova/deletar_piloto/<int:id>')
def deletar_corpo_de_prova_piloto(id):
    apagar = Cp_piloto.query.get_or_404(id)#CRIAR A TABELA DO CORPO DE PROVA
    a = apagar.ensaio.id
    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(a))
    except:
        "DEU ERRADO"


@app.route('/corpo_de_prova/deletar_rico/<int:id>')
def deletar_corpo_de_prova_rico(id):
    apagar = Cp_rico.query.get_or_404(id)#CRIAR A TABELA DO CORPO DE PROVA
    a = apagar.ensaio.id
    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(a))
    except:
        "DEU ERRADO"


@app.route('/corpo_de_prova/deletar_pobre/<int:id>')
def deletar_corpo_de_prova_pobre(id):
    apagar = Cp_pobre.query.get_or_404(id)#CRIAR A TABELA DO CORPO DE PROVA
    a = apagar.ensaio.id
    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(a))
    except:
        "DEU ERRADO"


@app.route('/resultados/<int:id>', methods=['POST', 'GET'])
def resultados(id):

#    print(d.dosagem_piloto)#lista de elementos na tabela dosagem_piloto relacionada com Ensaios.
#    print(d.dosagem_piloto[2].agua)#valor de agua  do elemento 2 da lista acima.
    d = Ensaios.query.filter_by(id=id).first()

#calculo do agua cimento certo.
    a = []
    for i in range(len(d.dosagem_piloto)):
        a.append(d.dosagem_piloto[i].agua)
    acp = sum(a)/d.dosagem_piloto[-1].c_massa
    acr = d.dosagem_rico[-1].agua/d.dosagem_rico[-1].c_massa
    acpb = d.dosagem_pobre[-1].agua/d.dosagem_pobre[-1].c_massa

    kgp = Consumo_piloto.query.filter_by(ensaio_id=id).first().kg_piloto
    kgr = Consumo_rico.query.filter_by(ensaio_id=id).first().kg_rico
    kgpb = Consumo_pobre.query.filter_by(ensaio_id=id).first().kg_pobre

    recipiente = d.volume
    gamap = kgp/recipiente
    gamar = kgr/recipiente
    gamapb = kgpb/recipiente
    consumop = gamap / (1+d.piloto+acp)
    consumor = gamar / (1+d.piloto+acr)
    consumopb = gamapb / (1+d.piloto+acpb)


#resistencias
    p = d.cp_piloto
    ri = d.cp_rico
    pb = d.cp_pobre

    numero_de_cp_rico7 = Cp_rico.query.filter_by(ensaio_id=id, idade=7).count()
    numero_de_cp_piloto7 = Cp_piloto.query.filter_by(ensaio_id=id, idade=7).count()
    numero_de_cp_pobre7 = Cp_pobre.query.filter_by(ensaio_id=id, idade=7).count()

    numero_de_cp_rico14 = Cp_rico.query.filter_by(ensaio_id=id, idade=14).count()
    numero_de_cp_piloto14 = Cp_piloto.query.filter_by(ensaio_id=id, idade=14).count()
    numero_de_cp_pobre14 = Cp_pobre.query.filter_by(ensaio_id=id, idade=14).count()

    numero_de_cp_rico28 = Cp_rico.query.filter_by(ensaio_id=id, idade=28).count()
    numero_de_cp_piloto28 = Cp_piloto.query.filter_by(ensaio_id=id, idade=28).count()
    numero_de_cp_pobre28 = Cp_pobre.query.filter_by(ensaio_id=id, idade=28).count()

    media_resistencia_rico7 = 0
    media_resistencia_piloto7 = 0
    media_resistencia_pobre7 = 0

    media_resistencia_rico14 = 0
    media_resistencia_piloto14 = 0
    media_resistencia_pobre14 = 0

    media_resistencia_rico28 = 0
    media_resistencia_piloto28 = 0
    media_resistencia_pobre28 = 0

    resistencias_piloto7 = Cp_piloto.query.filter_by(ensaio_id=id, idade=7).all()
    resistencias_rico7 = Cp_rico.query.filter_by(ensaio_id=id, idade=7).all()
    resistencias_pobre7 = Cp_pobre.query.filter_by(ensaio_id=id, idade=7).all()

    resistencias_piloto14 = Cp_piloto.query.filter_by(ensaio_id=id, idade=14).all()
    resistencias_rico14 = Cp_rico.query.filter_by(ensaio_id=id, idade=14).all()
    resistencias_pobre14 = Cp_pobre.query.filter_by(ensaio_id=id, idade=14).all()

    resistencias_piloto28 = Cp_piloto.query.filter_by(ensaio_id=id, idade=28).all()
    resistencias_rico28 = Cp_rico.query.filter_by(ensaio_id=id, idade=28).all()
    resistencias_pobre28 = Cp_pobre.query.filter_by(ensaio_id=id, idade=28).all()

    for i in resistencias_piloto7:
        media_resistencia_piloto7 = media_resistencia_piloto7 + i.resistencia/numero_de_cp_piloto7
    for i in resistencias_rico7:
        media_resistencia_rico7 = media_resistencia_rico7 + i.resistencia/numero_de_cp_rico7
    for i in resistencias_pobre7:
        media_resistencia_pobre7 = media_resistencia_pobre7 + i.resistencia/numero_de_cp_pobre7

    for i in resistencias_piloto14:
        media_resistencia_piloto14 = media_resistencia_piloto14 + i.resistencia/numero_de_cp_piloto14
    for i in resistencias_rico14:
        media_resistencia_rico14 = media_resistencia_rico14 + i.resistencia/numero_de_cp_rico14
    for i in resistencias_pobre14:
        media_resistencia_pobre14 = media_resistencia_pobre14 + i.resistencia/numero_de_cp_pobre14

    for i in resistencias_piloto28:
        media_resistencia_piloto28 = media_resistencia_piloto28 + i.resistencia/numero_de_cp_piloto28
    for i in resistencias_rico28:
        media_resistencia_rico28 = media_resistencia_rico28 + i.resistencia/numero_de_cp_rico28
    for i in resistencias_pobre28:
        media_resistencia_pobre28 = media_resistencia_pobre28 + i.resistencia/numero_de_cp_pobre28

#resistencias
    rr7 = [media_resistencia_pobre7, media_resistencia_piloto7, media_resistencia_rico7]
    rr14 = [media_resistencia_pobre14, media_resistencia_piloto14, media_resistencia_rico14]
    rr28 = [media_resistencia_pobre28, media_resistencia_piloto28, media_resistencia_rico28]
    ac = [acpb, acp, acr]
    m = [d.pobre, d.piloto, d.rico]
    cc = [consumopb,consumop,consumor]

    teste7 = 1
    teste14 = 1
    teste28 = 1


    for i in rr7:
        if i == 0:
            teste7 = 0

    for i in rr14:
        if i == 0:
            teste14 = 0

    for i in rr28:
        if i == 0:
            teste28 = 0

    if teste7 == 1:
        r7 = Regressao(rr7, ac, m, cc)
    else:
        r7 = None


    if teste14 == 1:
        r14 = Regressao(rr14, ac, m, cc)
    else:
        r14 = None

    if teste28 == 1:
        r28 = Regressao(rr28, ac, m, cc)
    else:
        r28 = None



    d7 = Resultados.query.filter_by(ensaio_id=id, idade=7).first()
    d14 = Resultados.query.filter_by(ensaio_id=id, idade=14).first()
    d28 = Resultados.query.filter_by(ensaio_id=id, idade=28).first()
    print('d28')
    print(d28)
    if d7 == None:
        if r7:
            resultado7 = Resultados(k1=r7.k1(), k2=r7.k2(), k3=r7.k3(), k4=r7.k4(), k5=r7.k5(), k6=r7.k6(), idade=7, ensaio=d)
            db.session.add(resultado7)
            db.session.commit()
    elif r7:
        d7.k1 = r7.k1()
        d7.k2 = r7.k2()
        d7.k3 = r7.k3()
        d7.k4 = r7.k4()
        d7.k5 = r7.k5()
        d7.k6 = r7.k6()
        db.session.commit()
    else:
        db.session.delete(d7)
        db.session.commit()


    if d14 == None:
        if r14:
            resultado14 = Resultados(k1=r14.k1(), k2=r14.k2(), k3=r14.k3(), k4=r14.k4(), k5=r14.k5(), k6=r14.k6(), idade=14, ensaio=d)
            db.session.add(resultado14)
            db.session.commit()
    elif r14:
        d14.k1 = r14.k1()
        d14.k2 = r14.k2()
        d14.k3 = r14.k3()
        d14.k4 = r14.k4()
        d14.k5 = r14.k5()
        d14.k6 = r14.k6()
        db.session.commit()
    else:
        db.session.delete(d14)
        db.session.commit()

    if d28 == None:
        if r28:
            resultado28 = Resultados(k1=r28.k1(), k2=r28.k2(), k3=r28.k3(), k4=r28.k4(), k5=r28.k5(), k6=r28.k6(), idade=28, ensaio=d)
            db.session.add(resultado28)
            db.session.commit()
    elif r28:
        d28.k1 = r28.k1()
        d28.k2 = r28.k2()
        d28.k3 = r28.k3()
        d28.k4 = r28.k4()
        d28.k5 = r28.k5()
        d28.k6 = r28.k6()
        db.session.commit()
    else:
        db.session.delete(d28)
        db.session.commit()

    return render_template('resultados.html', id=id, r7=r7,  r14=r14, r28=r28, p=p, ri=ri, pb=pb, d=d, acp=round(acp,2), acpb=round(acpb,2), acr=round(acr,2))


@app.route('/calculadora/<int:id>', methods=['POST', 'GET'])
def calculadora(id):
    form = Calcular()
    res = request.form.get("resistencia")
    ensaio_salvo = Ensaios.query.filter_by(id=id).first()

    ki7 = Resultados.query.filter_by(ensaio_id=id, idade=7).first()
    ki14 = Resultados.query.filter_by(ensaio_id=id, idade=14).first()
    ki28 = Resultados.query.filter_by(ensaio_id=id, idade=28).first()

    lista_k = []
    idades = []
    abrams = []
    lyse = []
    molinari = []
    alfa_ideal = []
    areia_unitaria = []
    brita_unitaria = []


    if ki28:
        lista_ki28 = [ki28.k1, ki28.k2, ki28.k3, ki28.k4, ki28.k5, ki28.k6]
        lista_k.append(lista_ki28)
        idades.append(ki28.idade)
    if ki14:
        lista_ki14 = [ki14.k1, ki14.k2, ki14.k3, ki14.k4, ki14.k5, ki14.k6]
        lista_k.append(lista_ki14)
        idades.append(ki14.idade)
    if ki7:
        lista_ki7 = [ki7.k1, ki7.k2, ki7.k3, ki7.k4, ki7.k5, ki7.k6]
        lista_k.append(lista_ki7)
        idades.append(ki7.idade)
    '''
    lista_k = [
    [ki7.k1, ki7.k2, ki7.k3, ki7.k4, ki7.k5, ki7.k6],
    [ki14.k1, ki14.k2, ki14.k3, ki14.k4, ki14.k5, ki14.k6],
    [ki28.k1, ki28.k2, ki28.k3, ki28.k4, ki28.k5, ki28.k6]
    ]
    '''

    if form.validate_on_submit():
        contador = 0
        for i in lista_k:
            calculo = Calculadora(i, float(res))
            abrams.append(calculo.abrams())
            lyse.append(calculo.lyse())
            molinari.append(calculo.molinari())
            alfa_ideal = ensaio_salvo.dosagem_rico[-1].alfa
            traco = Ensaio(alfa=alfa_ideal, m=lyse[contador], agua=abrams[contador])
            areia_unitaria.append(traco.massas_unitarias()[1])
            brita_unitaria.append(traco.massas_unitarias()[2])
            contador = contador + 1

    return render_template('calculadora.html', id=id, form=form, abrams=abrams, lyse=lyse, molinari=molinari, alfa_ideal=alfa_ideal, areia_unitaria=areia_unitaria, brita_unitaria=brita_unitaria, res=res, idades=idades)
