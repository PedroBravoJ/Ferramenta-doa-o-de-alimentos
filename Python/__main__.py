from funcoes import chamar_menu, cadastro_estab_ong, cadastro_pedido, cadastrar_entrega,\
    login_ong_estab, configurar_entrega, configurar_conta, configurar_pedidos, relatorios
from excecoes import ComandoInvalido, SenhaInvalida, EmailJaCadastrado, SiglaEstadoIncorreta, IdNaoEncontrado


sessao = ''

while True:
    menu = chamar_menu(sessao)
    if menu == 'C':
        try:
            cadastro_estab_ong()
        except ValueError:
            print("ERRO: O número de endereços deve ser um valor númerico inteiro maior que 0!")
        except ComandoInvalido:
            print("ERRO: Comando digitado é inválido!")
        except SenhaInvalida:
            print("ERRO: Sua senha deve ter letras maiúsculas, minúsculas, números e no mínimo 6 dígitos!")
        except EmailJaCadastrado:
            print("ERRO: O email digitado já está cadastrado no sistema!")
        except SiglaEstadoIncorreta:
            print("ERRO: O estado deve ser representado por sua sigla (Ex.: SP, RS, RJ, BA etc.)")
        else:
            print("Cadastro realizado com sucesso!")

    elif menu == 'L':
        ong_estab = input("Deseja se realizar login em uma conta de estabelecimento ou ONG? [O/E] ").upper()
        if ong_estab == "O":
            ong_estab = True
        else:
            ong_estab = False
        sessao = login_ong_estab(sessao, ong_estab)
    elif menu == 'CO':
        try:
            sessao = configurar_conta(sessao)
        except ComandoInvalido:
            print("ERRO: Comando digitado é inválido!")
        else:
            print("A configuração foi um sucesso!")
    elif menu == 'CP':
        cadastro_pedido(sessao)

    elif menu == 'COP':
        try:
            configurar_pedidos(sessao)
        except ComandoInvalido:
            print("ERRO: Comando digitado é inválido!")
        else:
            print("A configuração foi um sucesso!")
    elif menu == 'CE':
        try:
            cadastrar_entrega(sessao)
        except IdNaoEncontrado:
            print("ERRO: ID não encontrado!")
        else:
            print("Entrega cadastrada com sucesso.")
    elif menu == 'COE':
        try:
            configurar_entrega(sessao)
        except ComandoInvalido:
            print("ERRO: Comando digitado é inválido!")
        else:
            print("A configuração foi um sucesso!")
    elif menu == 'R':
        relatorios()
    elif menu == 'LO':
        print("Logout realizado!")
        sessao = ''
    elif menu == 'S':
        print("Obrigado por utilizar nosso sistema, volte sempre! ")
        break
    else:
        print("Comando inválido!")
        continue
