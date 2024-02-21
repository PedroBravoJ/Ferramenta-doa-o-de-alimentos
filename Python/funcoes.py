from db.config import *
from excecoes import ComandoInvalido, SenhaInvalida, EmailJaCadastrado, SiglaEstadoIncorreta, IdNaoEncontrado, ErroMes

# Menu, onde para acessar cadastro de pedidos, entregas, configuração de conta, deve estar logado como ong ou estab


def chamar_menu(sessao):
    print('----- MENU -----\n')
    if sessao == '':
        print('-> LOGIN [L] \n'
              '-> CADASTRO [C]')
        func = '[L/C/R/S]'
    else:
        print('-> CONFIGURAR CONTA [CO]')
        if sessao['ong_estab'] == 'ONG':
            print('-> CADASTRAR PEDIDOS [CP] \n'
                  '-> CONFIGURAR PEDIDOS [COP]')
            func = '[CO/CP/COP/LO/R/S]'
        else:
            print('-> CADASTRAR ENTREGAS [CE] \n'
                  '-> CONFIGURAR ENTREGAS [COE]')
            func = '[CO/CE/COE/LO/R/S]'
        print("-> LOGOUT [LO]")
    print("-> RELATÓRIOS [R]\n"
          "-> SAIR [S] \n")
    menu = input(f"Digite a funcionalidade que deseja utilizar: {func} ").upper()

    return menu

# FUNCOES PESQUISA

# ong_estab = True > ONG
# ong_estab = False > ESTAB


def pesquisa_id(id: int, ong_estab: bool):

    if ong_estab:
        search = session.query(TOng).filter_by(id_ong=id).first()
    else:
        search = session.query(TEstabelecimento).filter_by(id_estab=id).first()

    return search


def pesquisa_email(email: str, ong_estab: bool):
    if ong_estab:
        search = session.query(TOng).filter_by(email_ong=email).first()
    else:
        search = session.query(TEstabelecimento).filter_by(email_estab=email).first()

    return search


# MÉTODO = define se a pesquisa sera por um endereco especifico ou por todos os enderecos de um(a) estab/ong
def pesquisa_endereco(id: int, ong_estab: bool, metodo: bool):
    if metodo:
        if ong_estab:
            adress_search = session.query(TEnderecoOng).filter_by(id_ong=id).all()
        else:
            adress_search = session.query(TEnderecoEstab).filter_by(id_estab=id).all()
    else:
        if ong_estab:
            adress_search = session.query(TEnderecoOng).filter_by(id_endereco_ong=id).first()
        else:
            adress_search = session.query(TEnderecoEstab).filter_by(id_endereco_estab=id).first()
    return adress_search


def pesquisa_pedidos(id: int, ong_estab: bool, metodo: bool):
    if metodo:
        pedido_search = session.query(TPedidos).filter_by(id_pedidos=id).first()
    else:
        if ong_estab:
            pedido_search = session.query(TPedidos).filter_by(id_ong=id).all()
        else:
            pedido_search = session.query(TPedidos).filter_by(id_estab=id).all()

    return pedido_search


def pesquisa_entrega(id):
    entrega_search = session.query(TEntrega).filter_by(id_pedidos=id).first()
    return entrega_search


def print_all(tabela):
    if tabela == 1:
        resultados = session.query(TOng).all()
    elif tabela == 2:
        resultados = session.query(TEstabelecimento).all()
    elif tabela == 3:
        resultados = session.query(TPedidos).all()

    for resultado in resultados:
        print(resultado)

# CADASTRO


def cadastro_estab_ong():
    while True:
        ong_estab = input("Deseja cadastrar uma ONG ou um estabelecimento? [O/E]").upper()
        if ong_estab == 'O':
            ong_estab = True
        elif ong_estab == 'E':
            ong_estab = False
        else:
            raise ComandoInvalido
        nome = input("Digite o nome: ")
        email = input("Digite o e-mail: ").lower()
        if ong_estab:
            email_validation = pesquisa_email(email, True)
        else:
            email_validation = pesquisa_email(email, False)
        if email_validation is not None:
            raise EmailJaCadastrado

        pw = input("Digite sua senha: (Mín. 6 caracteres, números e letras, maiúsculas e minúsculas) ")
        pw_validation = validar_senha(pw)
        if len(pw) < 6 or pw_validation[0] == 0 or pw_validation[1] == 0 or pw_validation[2] == 0:
            raise SenhaInvalida

        cnpj = input("Digite o CNPJ: XX.XXX.XXX/0001-XX ")
        id = insert_ong_estab(nome, email, pw, cnpj, ong_estab)

        numero_enderecos = int(input("Quantos endereços possui? "))
        if numero_enderecos <= 0:
            raise ValueError

        for endereco in range(0, numero_enderecos):
            endereco = input("Digite seu endereço: [Rua], [numero] ")
            cidade = input("Digite a cidade: ")
            estado = input("Digite a sigla do estado: (Ex.: SP, MG, PA)  ").upper()
            if len(estado) != 2:
                raise SiglaEstadoIncorreta
            insert_endereco(id, endereco, cidade, estado, ong_estab)

        break


def cadastro_pedido(sessao):
    id_ong = sessao['id']
    item = input("Digite o produto que deseja pedir: ")
    quantidade = input("Digite a quantidade e a medida: (Ex: 20kg, 500g) ")

    insert_pedido(id_ong, item, quantidade)


def cadastrar_entrega(sessao):
    print_all(3)
    while True:
        id_pedido = int(input("Digite o ID do pedido que deseja atender: "))
        pedido = pesquisa_pedidos(id_pedido, False, True)
        if pedido is None:
            raise IdNaoEncontrado

        if pedido.id_estab is None:
            enderecos = pesquisa_endereco(pedido.id_ong, True, True)
            for endereco in enderecos:
                print(endereco)
            id_endereco = int(input("Digite o id do endereço mais próximo ao seu estabelecimento: "))
            endereco_search = pesquisa_endereco(id_endereco, True, False)
            endereco_entrega = endereco_search.endereco_ong

            data_entrega = input("Digite a data na qual será realizada a entrega: [DD/M/AAAA] ")
            data_entrega = format_data(data_entrega)
            obs = input("Se necessário, informe as observações da entrega: ")

            insert_entrega(id_pedido, data_entrega, endereco_entrega, obs)
            pedido.status_pedidos = 'Processando'
            pedido.id_estab = sessao['id']
            session.commit()
            break
        else:
            print("Pedido selecionado já está em andamento!")
            continue


# FUNÇÕES INSERT


def insert_ong_estab(nome: str, email: str, pw: str, cnpj: str, ong_estab: bool):
    if ong_estab:
        ong = TOng(nome_ong=nome, email_ong=email, senha_ong=pw, cnpj_ong=cnpj)
        session.add(ong)
        session.commit()

        return ong.id_ong

    else:
        estab = TEstabelecimento(nome_estab=nome, email_estab=email, senha_estab=pw, cnpj_estab=cnpj)
        session.add(estab)
        session.commit()

        return estab.id_estab


def insert_endereco(id_ong_estab: int, endereco: str, cidade: str, estado: str, ong_estab: bool):
    if ong_estab:
        endereco = TEnderecoOng(id_ong=id_ong_estab, endereco_ong=endereco,
                                cidade_ong=cidade, estado_ong=estado)
        session.add(endereco)
        session.commit()
    else:
        endereco = TEnderecoEstab(id_estab=id_ong_estab, endereco_estab=endereco,
                                  cidade_estab=cidade, estado_estab=estado)
        session.add(endereco)
        session.commit()


def insert_pedido(id_ong: int, item: str, quantidade: str):
    pedido = TPedidos(id_ong=id_ong, item_pedidos=item, quantidade_pedidos=quantidade,
                      status_pedidos="Pendente")
    session.add(pedido)
    session.commit()


def insert_entrega(id_pedidos: int, data: str, endereco: str, obs: str):
    entrega = TEntrega(id_pedidos=id_pedidos, data_entrega=data, endereco_entrega=endereco, observacoes_entrega=obs)

    session.add(entrega)
    session.commit()

# FUNCOES DELETE


def delete_ong_estab(sessao):
    if sessao != '':
        if sessao['ong_estab'] == 'ONG':
            conta = pesquisa_id(sessao['id'], True)
        else:
            conta = pesquisa_id(sessao['id'], False)
        print(conta)
        confirm_delete = input("Tem certeza que deseja deletar sua conta? (Todos os pedidos, entregas e endereços "
                               "relacionados a esta conta serão excluídos) [S/N] ").upper()
        if confirm_delete == 'S':
            session.delete(conta)
            session.commit()
            print("Conta deletada com sucesso!")
            sessao = ''
        else:
            print("Exclusão de conta cancelada...")
    else:
        print("Você deve estar logado para deletar sua conta!")

    return sessao


def delete_pedido(sessao: dict):
    pedidos = pesquisa_pedidos(sessao['id'], True, False)
    for pedido in pedidos:
        print(pedido)

    id_pedido = int(input('Digite o id do pedido que deseja deletar: '))
    pedido = pesquisa_pedidos(id_pedido, True, True)
    if pedido is None:
        raise IdNaoEncontrado
    print(pedido)
    confirm_delete = input("Tem certeza que deseja deletar o pedido acima? [S/N] ").upper()
    if confirm_delete == 'S':
        session.delete(pedido)
        session.commit()
        print("Pedido deletado com sucesso!")
    else:
        print("Exclusão de pedido cancelada...")


def delete_entrega(sessao: dict):
    pedidos = pesquisa_pedidos(sessao['id'], False, False)
    for pedido in pedidos:
        print(pedido)
    id_pedido = int(input("Digite o id do pedido que deseja deletar a entrega: "))
    entrega = pesquisa_entrega(id_pedido)
    pedido = pesquisa_pedidos(id_pedido, False, True)
    if entrega is None:
        raise IdNaoEncontrado
    print(entrega)
    confirm_delete = input("Tem certeza que deseja deletar a entrega acima? [S/N] ").upper()
    if confirm_delete == 'S':
        session.delete(entrega)
        pedido.id_estab = None
        session.commit()
        print("Entrega deletada com sucesso!")
    else:
        print("Exclusão de entrega cancelada...")


def delete_endereco(sessao):
    if sessao['ong_estab'] == 'ONG':
        enderecos = pesquisa_endereco(sessao['id'], True, True)
    else:
        enderecos = pesquisa_endereco(sessao['id'], False, True)

    for endereco in enderecos:
        print(endereco)
    id_endereco_delete = int(input('Digite o id do endereço que deseja deletar: '))
    if sessao['ong_estab'] == 'ONG':
        endereco_delete = pesquisa_endereco(id_endereco_delete, True, False)
    else:
        endereco_delete = pesquisa_endereco(id_endereco_delete, False, False)

    if endereco_delete is None:
        raise IdNaoEncontrado

    print(endereco_delete)
    confirm_delete = input("Tem certeza que deseja deletar o endereço acima? [S/N] ").upper()
    if confirm_delete == 'S':
        session.delete(endereco_delete)
        session.commit()
        print("Endereço deletado com sucesso!")
    else:
        print("Exclusão de endereço cancelada...")


# FUNCOES UPDATE


def update_ong_estab(sessao):
    if sessao != '':
        if sessao['ong_estab'] == 'ONG':
            ong_estab = True
        else:
            ong_estab = False
        while True:
            conta = pesquisa_id(sessao['id'], ong_estab)
            print(conta)
            alteracao = input("Deseja alterar nome ou senha(email e cnpj não podem ser alterados) [N/S] ").upper()
            if alteracao == 'N':
                novo_nome = input("Digite o novo nome: ")
                if ong_estab:
                    conta.nome_ong = novo_nome
                else:
                    conta.nome_estab = novo_nome
            if alteracao == 'S':
                nova_senha = input("Digite sua nova senha: (Mín. 6 caracteres, números e letras, "
                                   "maiúsculas e minúsculas) ")
                pw_validation = validar_senha(nova_senha)
                if len(nova_senha) < 6 or pw_validation[0] == 0 or pw_validation[1] == 0 or pw_validation[2] == 0:
                    raise SenhaInvalida

                if ong_estab:
                    conta.senha_ong = nova_senha
                else:
                    conta.senha_estab = nova_senha
            session.commit()
            continuar = input("Deseja alterar mais informações? [S/N] ").upper()
            if continuar == 'S':
                continue
            else:
                break


def update_endereco(sessao):
    if sessao != '':
        if sessao['ong_estab'] == 'ONG':
            ong_estab = True
        else:
            ong_estab = False
        while True:
            enderecos = pesquisa_endereco(sessao['id'], ong_estab, True)
            for endereco in enderecos:
                print(endereco)
            id_endereco = int(input('Digite o id do endereco que deseja alterar: '))
            endereco_update = pesquisa_endereco(id_endereco, ong_estab, False)
            if endereco_update is None:
                raise IdNaoEncontrado

            novo_endereco = input('Digite o novo endereço: [Rua], [numero] ')
            nova_cidade = input('Digite a nova cidade: ')
            novo_estado = input('Digite a sigla do novo estado: (Ex.: SP, MG, PA)  ').upper()
            if len(novo_estado) != 2:
                raise SiglaEstadoIncorreta

            if ong_estab:
                endereco_update.endereco_ong = novo_endereco
                endereco_update.cidade_ong = nova_cidade
                endereco_update.estado_ong = novo_estado
            else:
                endereco_update.endereco_estab = novo_endereco
                endereco_update.cidade_estab = nova_cidade
                endereco_update.estado_estab = novo_estado
            session.commit()

            continuar = input('Deseja alterar outro endereço? [S/N] ').upper()
            if continuar == 'S':
                continue
            else:
                break


def update_pedido(sessao):
    if sessao != '':
        pedidos = pesquisa_pedidos(sessao['id'], True, False)
        for pedido in pedidos:
            print(pedido)
        while True:
            id_pedido = int(input("Digite o id do pedido que deseja alterar: "))
            pedido_update = pesquisa_pedidos(id_pedido, True, True)

            if pedido_update is None:
                raise IdNaoEncontrado

            alteracao = input("Deseja alterar o item ou quantidade? [I/Q] ").upper()
            if alteracao == 'I':
                novo_item = input("Digite o novo item: ")
                pedido_update.item_pedidos = novo_item
            else:
                nova_quantidade = input("Digite a nova quantidade: (Ex.: 20kg, 300g) ")
                pedido_update.quantidade_pedidos = nova_quantidade
            session.commit()

            continuar = input('Deseja alterar mais pedidos? [S/N] ').upper()
            if continuar == 'S':
                continue
            else:
                break


def update_entrega(sessao):
    if sessao != '':
        pedidos = pesquisa_pedidos(sessao['id'], False, False)
        for pedido in pedidos:
            print(pedido)

        while True:
            id_pedido = int(input("Digite o id do pedido que deseja configurar a entrega: "))
            entrega = pesquisa_entrega(id_pedido)

            if entrega is None:
                raise IdNaoEncontrado

            print(entrega)
            alteracao = input("Deseja alterar a data ou as observações? [D/O] ").upper()
            if alteracao != 'D' and alteracao != 'O':
                raise ComandoInvalido

            if alteracao == 'D':
                nova_data = input("Digite a nova data: [DD/MM/AAAA] ")
                nova_data = format_data(nova_data)
                entrega.data_entrega = nova_data
                session.commit()
            elif alteracao == 'O':
                nova_obs = input("Digite a nova observação: ")
                entrega.observacoes_entrega = nova_obs
                session.commit()

            continuar = input('Deseja alterar mais entregas? [S/N] ').upper()
            if continuar == 'S':
                continue
            else:
                break

# RELATORIOS


def menu_relatorio():
    menu = input("Pesquisar por:\n"
                 "-> Ong ou Estabelecimento [OE]\n"
                 "-> Endereço [E]\n"
                 "-> Pedidos [P]\n"
                 "-> Entregas [EN]\n").upper()
    return menu


def relatorios():
    menu = menu_relatorio()
    if menu == 'E':
        relatorio_endereco()
    elif menu == 'P':
        try:
            relatorio_pedidos()
        except ValueError:
            print("O ID deve ser um valor númerico inteiro!")
    elif menu == 'EN':
        relatorio_entrega()


def relatorio_entrega():
    data = input("Digite a data que deseja pesquisar: [DD/MM/AAAA] ")
    data = format_data(data)
    entregas = session.query(TEntrega).filter_by(data_entrega=data).all()
    if len(entregas) > 0:
        for entrega in entregas:
            print(entrega)
    else:
        print("\nNenhum resultado encontrado!")


def relatorio_pedidos():
    pesquisa = input("Pesquisar por ong, estab, item ou status? [O/E/I/S] ").upper()
    if pesquisa == 'O':
        id = int(input("Digite o ID que deseja pesquisar: "))
        pedidos = pesquisa_pedidos(id, True, False)
    elif pesquisa == 'E':
        id = int(input("Digite o ID que deseja pesquisar: "))
        pedidos = pesquisa_pedidos(id, False, False)
    elif pesquisa == 'I':
        item = input("Digite o item que deseja pesquisar: ")
        pedidos = session.query(TPedidos).filter_by(item_pedidos=item).all()
    elif pesquisa == 'S':
        status = input("Digite o status que deseja pesquisar: [Pendente/Processando/Entregue/Cancelado] ")
        pedidos = session.query(TPedidos).filter_by(status_pedidos=status).all()
    if len(pedidos) > 0:
        for pedido in pedidos:
            print(pedido)
    else:
        print("\nNenhum resultado encontrado!")


def relatorio_endereco():
    oe = input("Pesquisar por endereços de ongs ou estabelecimentos? [O/E] ").upper()
    ce = input("Pesquisar por cidade ou estado? [C/E] ").upper()

    if oe == 'O':
        ong_estab = True
    elif oe == 'E':
        ong_estab = False
    else:
        print("Comando inválido!")
    if ce == 'C':
        cidade_estado = True
    elif ce == 'E':
        cidade_estado = False
    else:
        print("Comando inválido!")

    if cidade_estado:
        cidade = input("Digite a cidade que deseja pesquisar: ")
        if ong_estab:
            resultados = session.query(TEnderecoOng).filter_by(cidade_ong=cidade).all()
        else:
            resultados = session.query(TEnderecoEstab).filter_by(cidade_estab=cidade).all()
    else:
        estado = input("Digite o estado que deseja pesquisar: ")
        if ong_estab:
            resultados = session.query(TEnderecoOng).filter_by(estado_ong=estado).all()
        else:
            resultados = session.query(TEnderecoEstab).filter_by(estado_estab=estado).all()
    if len(resultados) > 0:
        if ong_estab:
            for resultado in resultados:
                ong = session.query(TOng).filter_by(id_ong=resultado.id_ong).first()
                print(ong)
                print(resultado)
                print('-------///-------')
        else:
            for resultado in resultados:
                estab = session.query(TEstabelecimento).filter_by(id_estab=resultado.id_estab).first()
                print(estab)
                print(resultado)
                print('-------///-------')
    else:
        print("\nNenhum resultado encontrado!")

# CONFIGURAÇAO


def configurar_conta(sessao):
    menu_co = input("Deseja configurar informações da conta ou de endereço? [C/E] ").upper()
    if menu_co == 'C':
        upd_or_del = input("Deseja deletar a conta ou atualizar informações? [D/A] ").upper()
        if upd_or_del == 'D':
            sessao = delete_ong_estab(sessao)
        elif upd_or_del == 'A':
            update_ong_estab(sessao)
    if menu_co == 'E':
        upd_or_del = input("Deseja deletar um endereço ou atualizar informações? [D/A] ").upper()
        if upd_or_del == 'D':
            try:
                delete_endereco(sessao)
            except ValueError:
                print("ERRO: O ID deve ser um número inteiro! ")
            except IdNaoEncontrado:
                print("ERRO: O id digitado não foi encontrado no sistema!")
        elif upd_or_del == 'A':
            update_endereco(sessao)
    if menu_co != 'C' and menu_co != 'E':
        raise ComandoInvalido
    if upd_or_del != 'D' and upd_or_del != 'A':
        raise ComandoInvalido

    return sessao


def configurar_pedidos(sessao):
    upd_or_del = input('Deseja deletar um pedido ou atualizar informações? [D/A] ').upper()
    if upd_or_del == 'D':
        try:
            delete_pedido(sessao)
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro! ")
        except IdNaoEncontrado:
            print("ERRO: O id digitado não foi encontrado no sistema!")

    elif upd_or_del == 'A':
        try:
            update_pedido(sessao)
        except IdNaoEncontrado:
            print("ERRO: O id digitado não foi encontrado no sistema!")
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro! ")
    if upd_or_del != 'D' and upd_or_del != 'A':
        raise ComandoInvalido


def configurar_entrega(sessao):
    upd_or_del = input('Deseja deletar uma entrega ou atualizar informações? [D/A] ').upper()
    if upd_or_del == 'D':
        try:
            delete_entrega(sessao)
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro! ")
        except IdNaoEncontrado:
            print("ERRO: O id digitado não foi encontrado no sistema!")

    elif upd_or_del == 'A':
        try:
            update_entrega(sessao)
        except IdNaoEncontrado:
            print("ERRO: O id digitado não foi encontrado no sistema!")
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro! ")
    if upd_or_del != 'D' and upd_or_del != 'A':
        raise ComandoInvalido


# LOGIN


def login_ong_estab(sessao, ong_estab: bool):
    if sessao != '':
        print("Você já está logado em uma conta! ")
    else:
        while True:
            email = input("Digite o email: ").lower()
            pw = input("Digite a senha: ")
            if ong_estab:
                login = pesquisa_email(email, True)
            else:
                login = pesquisa_email(email, False)
            if login is not None:
                if ong_estab:
                    if login.senha_ong == pw:
                        sessao = {
                            'id': login.id_ong,
                            'nome': login.nome_ong,
                            'email': login.email_ong,
                            'ong_estab': 'ONG'
                        }
                        print(f"\nSeja bem-vindo(a), {sessao['nome']}!")
                        break
                else:
                    if login.senha_estab == pw:
                        sessao = {
                            'id': login.id_estab,
                            'nome': login.nome_estab,
                            'email': login.email_estab,
                            'ong_estab': 'ESTAB',
                        }
                        print(f"\nSeja bem-vindo(a), {sessao['nome']}!")
                        break
            if sessao == '':
                retry_login = input("Email e/ou senha incorretos!! Deseja tentar novamente? [S/N]").upper()
                if retry_login != 'S':
                    break
                else:
                    continue
        return sessao


# Validação


def validar_senha(pw: str):
    pw_numeros = 0
    pw_letras_min = 0
    pw_letras_mai = 0

    for x in range(0, len(pw) - 1):
        if pw[x] == "0" or pw[x] == "1" or pw[x] == "2" or pw[x] == "3" or pw[x] == "4" or pw[x] == "5" or \
                pw[x] == "6" or pw[x] == "7" \
                or pw[x] == "8" or pw[x] == "9":
            pw_numeros += 1
        elif pw[x] == "a" or pw[x] == "b" or pw[x] == "c" or pw[x] == "d" or pw[x] == "e" or pw[x] == "f" \
                or pw[x] == "g" or pw[x] == "h" or pw[x] == "i" or pw[x] == "j" or pw[x] == "k" or pw[x] == "l" \
                or pw[x] == "m" or pw[x] == "n" or pw[x] == "o" or pw[x] == "p" or pw[x] == "q" or pw[x] == "r" \
                or pw[x] == "s" or pw[x] == "t" or pw[x] == "u" or pw[x] == "v" or pw[x] == "w" or pw[x] == "x" \
                or pw[x] == "y" or pw[x] == "z":
            pw_letras_min += 1
        elif pw[x] == "A" or pw[x] == "B" or pw[x] == "C" or pw[x] == "D" or pw[x] == "E" or pw[x] == "F" \
                or pw[x] == "G" or pw[x] == "H" or pw[x] == "I" or pw[x] == "J" or pw[x] == "K" or pw[x] == "L" \
                or pw[x] == "M" or pw[x] == "N" or pw[x] == "O" or pw[x] == "P" or pw[x] == "Q" or pw[x] == "R" \
                or pw[x] == "S" or pw[x] == "T" or pw[x] == "U" or pw[x] == "V" or pw[x] == "W" or pw[x] == "X" \
                or pw[x] == "Y" or pw[x] == "Z":
            pw_letras_mai += 1

    return [pw_numeros, pw_letras_mai, pw_letras_min]


# FUNCOES FORMATAÇAO


def format_endereco(endereco, ong_estab: bool):
    if ong_estab:
        return f"{endereco.endereco_ong} - {endereco.cidade_ong}, {endereco.estado_ong}"
    else:
        return f"{endereco.endereco_estab} - {endereco.cidade_estab}, {endereco.estado_estab}"


def format_data(data: str):
    data = data.split('/')
    dia = data[0]
    mes = int(data[1])
    ano = data[2]

    if mes < 1 or mes > 12:
        raise ErroMes

    if mes == 1:
        mes_format = 'JAN'
    elif mes == 2:
        mes_format = 'FEB'
    elif mes == 3:
        mes_format = 'MAR'
    elif mes == 4:
        mes_format = 'APR'
    elif mes == 5:
        mes_format = 'MAY'
    elif mes == 6:
        mes_format = 'JUN'
    elif mes == 7:
        mes_format = 'JUL'
    elif mes == 8:
        mes_format = 'AUG'
    elif mes == 9:
        mes_format = 'SEP'
    elif mes == 10:
        mes_format = 'OCT'
    elif mes == 11:
        mes_format = 'NOV'
    elif mes == 12:
        mes_format = 'DEC'

    return f'{dia}-{mes_format}-{ano}'
