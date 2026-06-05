from django.shortcuts import render, redirect
from . import basedados


# Página Inicial 
def index(request):
    try:
        conformidade = basedados.clientes_por_conformidade_nis2()
    except Exception:
        conformidade = []
    try:
        top_incidentes = basedados.top5_clientes_mais_incidentes()
    except Exception:
        top_incidentes = []
    try:
        docs_por_mes = basedados.documentos_por_cliente_e_mes()
    except Exception:
        docs_por_mes = []
    try:
        utilizadores = basedados.distribuicao_utilizadores_por_perfil()
    except Exception:
        utilizadores = []
    try:
        pedidos_estado = basedados.estado_pedidos_e_tempo_medio()
    except Exception:
        pedidos_estado = []

    return render(request, 'clinica/index.html', {
        'conformidade': conformidade,
        'top_incidentes': top_incidentes,
        'docs_por_mes': docs_por_mes,
        'utilizadores': utilizadores,
        'pedidos_estado': pedidos_estado,
    })


# Clientes
def clientes_list_create(request):
    if request.method == "POST":
        basedados.criar_cliente(
            request.POST.get('nome'),
            request.POST.get('email'),
            request.POST.get('telefone'),
            request.POST.get('password', 'changeme'),
        )
        return redirect('clientes_list_create')
    return render(request, 'clinica/clientes.html', {
        'clientes': basedados.listar_clientes()
    })


# Ativos Tecnológicos
def ativos_list_create(request):
    if request.method == "POST":
        basedados.criar_ativo_tecnologico(
            request.POST.get('cliente_id'),
            request.POST.get('nome'),
            request.POST.get('tipo'),
            request.POST.get('criticidade'),
            request.POST.get('descricao', ''),
        )
        return redirect('ativos_list_create')
    return render(request, 'clinica/ativos.html', {
        'ativos': basedados.listar_ativos_tecnologicos(),
        'clientes': basedados.listar_clientes(),
    })


# Documentação
def documentacao_list_create(request):
    if request.method == "POST":
        basedados.criar_documento(
            request.POST.get('cliente_id'),
            request.POST.get('nome'),
            request.POST.get('tipo'),
            request.POST.get('descricao', ''),
        )
        return redirect('documentacao_list_create')
    return render(request, 'clinica/documentos.html', {
        'documentos': basedados.listar_documentos(),
        'clientes': basedados.listar_clientes(),
    })


# Incidentes
def incidentes_list_create(request):
    if request.method == "POST":
        basedados.criar_incidente(
            request.POST.get('cliente_id'),
            request.POST.get('tipo'),
            request.POST.get('data_ocorrencia'),
            request.POST.get('impacto'),
            request.POST.get('descricao'),
            request.POST.get('acoes_imediatas', ''),
        )
        return redirect('incidentes_list_create')
    return render(request, 'clinica/incidentes.html', {
        'incidentes': basedados.listar_incidentes(),
        'clientes': basedados.listar_clientes(),
    })


# Pedidos / Tickets de Suporte
def pedidos_list_create(request):
    if request.method == "POST":
        basedados.criar_pedido(
            request.POST.get('cliente_id'),
            request.POST.get('titulo'),
            request.POST.get('descricao'),
        )
        return redirect('pedidos_list_create')
    return render(request, 'clinica/pedidos.html', {
        'pedidos': basedados.listar_pedidos(),
        'clientes': basedados.listar_clientes(),
    })
