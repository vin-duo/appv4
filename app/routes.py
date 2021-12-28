from flask import Flask, render_template, redirect, url_for, request
from app import app, db
from app.forms import Criar_ensaio, Alfa, Alfa_auxiliar, Calcular, Formulario_teste
from app.models import Ensaios, Dosagem_piloto, Dosagem_rico, Dosagem_pobre, Cp_piloto, Cp_rico, Cp_pobre, Resultados, Teste, Consumo_piloto, Consumo_rico, Consumo_pobre
from app.regressao import Regressao, Calculadora
from app.traco_dosagem import Ensaio

@app.route('/')
@app.route('/home')
def home():
    ensaios_registrados = Ensaios.query.all()
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
    apagar = Ensaios.query.get_or_404(id)

    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/home')

    except:
        "DEU ERRADO"


@app.route('/editar_ensaio/<int:id>', methods=['POST', 'GET'])
def editar_ensaio(id):

    form = Criar_ensaio()

    editar = Ensaios.query.get_or_404(id)
    
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

    print('Dosagem_piloto.query.order_by(Dosagem_piloto.alfa).all()')
    print(Dosagem_piloto.query.order_by(Dosagem_piloto.alfa).all()) 
    alfa_ordenado = Dosagem_piloto.query.order_by(Dosagem_piloto.alfa).all()
    if dosagens_do_ensaio_salvo != []:
        contador = 0
        indice = 0
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
    return render_template("auxiliar.html", form=form, ensaio_salvo=ensaio_salvo, id=id, m_rico=m_rico, m_pobre=m_pobre, slump=slump)





#acabou dosagem auxiliar

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
        if r_piloto != "":
            cp_piloto = Cp_piloto(resistencia=r_piloto, ensaio=ensaio_salvo)
            db.session.add(cp_piloto)
            db.session.commit()
        if r_rico != "":
            cp_rico = Cp_rico(resistencia=r_rico, ensaio=ensaio_salvo)
            db.session.add(cp_rico)
            db.session.commit()
        if r_pobre != "":
            cp_pobre = Cp_pobre(resistencia=r_pobre, ensaio=ensaio_salvo)
            db.session.add(cp_pobre)
            db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(id))
    return render_template('corpo_de_prova.html', id=id, cps_piloto=cps_piloto, cps_rico=cps_rico, cps_pobre=cps_pobre, ensaio_salvo=ensaio_salvo)




#@@@@@@@@@@@@@@@@@@@@@@

@app.route('/consumo_cimento/<int:id>', methods=['POST', 'GET'])
def consumo_cimento(id):

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    consumo_piloto_salvo = Consumo_piloto.query.filter_by(kg_piloto_id=id).first()
    consumo_pobre_salvo = Consumo_pobre.query.filter_by(kg_pobre_id=id).first()
    consumo_rico_salvo = Consumo_rico.query.filter_by(kg_rico_id=id).first()

    massa_piloto = Cp_piloto.query.all()
    massa_rico = Cp_rico.query.all()
    massa_pobre = Cp_pobre.query.all()

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
    return render_template('consumo.html', id=id, massa_piloto=massa_piloto, massa_rico=massa_rico, massa_pobre=massa_pobre, ensaio_salvo=ensaio_salvo)

#@@@@@@@@@@@@@@@@@@@@@@











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
#    print('calculo agua cimento pobre')
#    print('agua: {}'.format(d.dosagem_pobre[-1].agua))
#    print('cimento: {}'.format(d.dosagem_pobre[-1].c_massa))


#resistencias
    p = d.cp_piloto
    ri = d.cp_rico
    pb = d.cp_pobre

#    print('d.cp_piloto')
#    print(Cp_piloto.query.all())
#    print(Cp_piloto.query.count())
    print(Cp_piloto.query.filter_by(ensaio_id=id).count())#contando o numero de corpos de prova salvos para o ensaio com esse id (se eu to no ensaio id=3, conto o numero de linhas de corpo de prova do ensaio id=3)

    numero_de_cp_rico = Cp_rico.query.filter_by(ensaio_id=id).count()
    numero_de_cp_piloto = Cp_piloto.query.filter_by(ensaio_id=id).count()
    numero_de_cp_pobre = Cp_pobre.query.filter_by(ensaio_id=id).count()
#    print(numero_de_cp_rico)
#    print(numero_de_cp_piloto)
#    print(numero_de_cp_pobre)

    media_resistencia_rico = 0
    media_resistencia_piloto = 0
    media_resistencia_pobre = 0

    resistencias_piloto = Cp_piloto.query.filter_by(ensaio_id=id).all()
    resistencias_rico = Cp_rico.query.filter_by(ensaio_id=id).all()
    resistencias_pobre = Cp_pobre.query.filter_by(ensaio_id=id).all()

    for i in resistencias_piloto:
        media_resistencia_piloto = media_resistencia_piloto + i.resistencia/numero_de_cp_piloto

    for i in resistencias_rico:
        media_resistencia_rico = media_resistencia_rico + i.resistencia/numero_de_cp_rico

    for i in resistencias_pobre:
        media_resistencia_pobre = media_resistencia_pobre + i.resistencia/numero_de_cp_pobre

    print('resultados:')
    print(media_resistencia_pobre)
    print(media_resistencia_rico)
    print(media_resistencia_piloto)

    rr = [pb[0].resistencia, p[0].resistencia, ri[0].resistencia]
    ac = [acpb, acp, acr]
    m = [d.pobre, d.piloto, d.rico]
    cc = [295,371,479]
#PRECISO COLOCAR INPUT DE DADOS PARA OS VALORES DE "C"!!!!
    r = Regressao(rr, ac, m, cc)
    print('rr')
    print(rr)
    if d.resultados == []:
        resultado = Resultados(k1=r.k1(), k2=r.k2(), k3=r.k3(), k4=r.k4(), k5=r.k5(), k6=r.k6(), ensaio=d)
        db.session.add(resultado)
        db.session.commit()
    else:
        d.resultados[0].k1 = r.k1()
        d.resultados[0].k2 = r.k2()
        d.resultados[0].k3 = r.k3()
        d.resultados[0].k4 = r.k4()
        d.resultados[0].k5 = r.k5()
        d.resultados[0].k6 = r.k6()
        db.session.commit()

    return render_template('resultados.html', id=id, r=r)


@app.route('/calculadora/<int:id>', methods=['POST', 'GET'])
def calculadora(id):
    form = Calcular()
    res = request.form.get("resistencia")
    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    k = ensaio_salvo.resultados
    lista_k = [k[0].k1, k[0].k2, k[0].k3, k[0].k4, k[0].k5, k[0].k6]


    abrams = 0
    lyse = 0
    molinari = 0
    alfa_ideal = 0
    areia_unitaria = 0
    brita_unitaria = 0

    if form.validate_on_submit():
        calculo = Calculadora(lista_k, int(res))
        abrams = calculo.abrams()
        lyse = calculo.lyse()
        molinari = calculo.molinari()
        alfa_ideal = ensaio_salvo.dosagem_rico[-1].alfa
        traco = Ensaio(alfa=alfa_ideal, m=lyse, agua=abrams)
        areia_unitaria = traco.massas_unitarias()[1]
        brita_unitaria = traco.massas_unitarias()[2]

    return render_template('calculadora.html', id=id, form=form, abrams=abrams, lyse=lyse, molinari=molinari, alfa_ideal=alfa_ideal, areia_unitaria=areia_unitaria, brita_unitaria=brita_unitaria)
