

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    m_rico = ensaio_salvo.rico
    m_pobre = ensaio_salvo.pobre
#    cp = ensaio_salvo.cp
    alfa = form.alfa_auxiliar.data
    pesobrita = ensaio_salvo.pesobrita
    slump = ensaio_salvo.slump





    m_rico = ensaio_salvo.rico
    m_pobre = ensaio_salvo.pobre
#    alfa = form.alfa_auxiliar.data

if form.validate_on_submit():
    if ensaio_salvo.dosagem_rico == []:
        traco = Ensaio(
            m = m_rico,
            alfa = novo_alfa_ideal, 
            pesobrita = pesobrita)

        add_no_db_rico = Dosagem_rico(
            alfa = novo_alfa_ideal,
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
            alfa = novo_alfa_ideal, 
            pesobrita = pesobrita)

        add_no_db_pobre = Dosagem_pobre(
            alfa = novo_alfa_ideal,
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

    elif ensaio_salvo.dosagem_rico[0].alfa < novo_alfa_ideal:
        rico_velho = ensaio_salvo.dosagem_rico[0]
        pobre_velho = ensaio_salvo.dosagem_pobre[0]
        db.session.delete(rico_velho)
        db.session.delete(pobre_velho)
        db.session.commit()

        traco = Ensaio(
            m = m_rico,
            alfa = novo_alfa_ideal, 
            pesobrita = pesobrita)

        add_no_db_rico = Dosagem_rico(
            alfa = novo_alfa_ideal,
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
            alfa = novo_alfa_ideal, 
            pesobrita = pesobrita)

        add_no_db_pobre = Dosagem_pobre(
            alfa = novo_alfa_ideal,
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




sesson.delete
session.commit

#se for o ultimo
se delete.alfa == auxiliar.alfa:
	deleta o auxiliar
	commit
	se tiver alfa em piloto:
		ordenar pelo alfa
		pegar o ultimo alfa
		calcular novo auxiliar
		session.add
		session.commit










@app.route('/pobre/<int:id>', methods=['POST', 'GET'])
def rico(id):

        return redirect('/auxiliar/{}'.format(id))
return render_template("auxiliar.html", form=form, ensaio_salvo=ensaio_salvo, id=id, m_rico=m_rico, m_pobre=m_pobre, slump=slump, m=m, mp=mp, mr=mr)




@app.route('/pobre/<int:id>', methods=['POST', 'GET'])
def pobre(id):

        return redirect('/auxiliar/{}'.format(id))
return render_template("auxiliar.html", form=form, ensaio_salvo=ensaio_salvo, id=id, m_rico=m_rico, m_pobre=m_pobre, slump=slump, m=m, mp=mp, mr=mr)

