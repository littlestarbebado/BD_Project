from django.db import connection

# ===========================================================
# OPERAÇÕES DE CLIENTES 
# ===========================================================

def listar_clientes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, telefone, score, status
            FROM public."Clientes"
            ORDER BY id DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_cliente(nome, email, telefone, password):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO public."Clientes" (nome, email, telefone, password, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, NOW(), NOW());
        """, [nome, email, telefone, password])

def obter_cliente(cliente_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, telefone, score, status
            FROM public."Clientes"
            WHERE id = %s;
        """, [cliente_id])
        colunas = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(colunas, row)) if row else None

def atualizar_cliente(cliente_id, nome, email, telefone):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE public."Clientes"
            SET nome=%s, email=%s, telefone=%s, "updatedAt"=NOW()
            WHERE id=%s;
        """, [nome, email, telefone, cliente_id])

def eliminar_cliente(cliente_id):
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM public."Clientes" WHERE id=%s;""", [cliente_id]) 

# 1. Número de clientes por estado de conformidade NIS2
def clientes_por_conformidade_nis2():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                CASE
                    WHEN score >= 75 THEN 'Conforme'
                    WHEN score >= 40 THEN 'Em avaliação'
                    ELSE 'Com pendências'
                END AS estado_conformidade,
                COUNT(*) AS total_clientes
            FROM public."Clientes"
            GROUP BY estado_conformidade
            ORDER BY total_clientes DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]


# ===========================================================
# OPERAÇÕES DE ATIVOS TECNOLÓGICOS 
# ===========================================================

def listar_ativos_tecnologicos():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id, a.nome, a.tipo, a.criticidade, a.descricao, c.nome AS nome_cliente
            FROM public."AtivoTecnologicos" a
            LEFT JOIN public."Clientes" c ON a."ClienteId" = c.id
            ORDER BY a.id DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_ativo_tecnologico(cliente_id, nome, tipo, criticidade, descricao=''):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO public."AtivoTecnologicos" ("ClienteId", nome, tipo, criticidade, descricao, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
        """, [cliente_id, nome, tipo, criticidade, descricao])

def obter_ativo(ativo_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, tipo, criticidade, descricao, "ClienteId"
            FROM public."AtivoTecnologicos" WHERE id=%s;
        """, [ativo_id])
        colunas = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(colunas, row)) if row else None

def atualizar_ativo(ativo_id, nome, tipo, criticidade, descricao):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE public."AtivoTecnologicos"
            SET nome=%s, tipo=%s, criticidade=%s, descricao=%s, "updatedAt"=NOW()
            WHERE id=%s;
        """, [nome, tipo, criticidade, descricao, ativo_id])

def eliminar_ativo(ativo_id):
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM public."AtivoTecnologicos" WHERE id=%s;""", [ativo_id])


# ===========================================================
# OPERAÇÕES DE DOCUMENTOS 
# ===========================================================

def listar_documentos():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT d.id, d.nome, d.tipo, d.descricao, d."createdAt", c.nome AS nome_cliente
            FROM public."Documentos" d
            LEFT JOIN public."Clientes" c ON d."ClienteId" = c.id
            ORDER BY d."createdAt" DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_documento(cliente_id, nome, tipo, descricao=''):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO public."Documentos" ("ClienteId", nome, tipo, descricao, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, NOW(), NOW());
        """, [cliente_id, nome, tipo, descricao])

def obter_documento(doc_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, tipo, descricao, "ClienteId"
            FROM public."Documentos" WHERE id=%s;
        """, [doc_id])
        colunas = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(colunas, row)) if row else None

def atualizar_documento(doc_id, nome, tipo, descricao):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE public."Documentos"
            SET nome=%s, tipo=%s, descricao=%s, "updatedAt"=NOW()
            WHERE id=%s;
        """, [nome, tipo, descricao, doc_id])

def eliminar_documento(doc_id):
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM public."Documentos" WHERE id=%s;""", [doc_id])
        
# 3. Total de documentos submetidos por cliente e por mês
def documentos_por_cliente_e_mes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                c.nome AS nome_cliente,
                TO_CHAR(d."createdAt", 'YYYY-MM') AS mes,
                COUNT(d.id) AS total_documentos
            FROM public."Documentos" d
            LEFT JOIN public."Clientes" c ON d."ClienteId" = c.id
            GROUP BY c.id, c.nome, TO_CHAR(d."createdAt", 'YYYY-MM')
            ORDER BY mes DESC, total_documentos DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]



# ===========================================================
# OPERAÇÕES DE INCIDENTES 
# ===========================================================

def listar_incidentes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT i.id, i.tipo, i."dataOcorrencia", i.impacto, i.descricao, i.estado, c.nome AS nome_cliente
            FROM public."Incidentes" i
            LEFT JOIN public."Clientes" c ON i."ClienteId" = c.id
            ORDER BY i."dataOcorrencia" DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_incidente(cliente_id, tipo, data_ocorrencia, impacto, descricao, acoes_imediatas=''):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO public."Incidentes" ("ClienteId", tipo, "dataOcorrencia", impacto, descricao, "acoesImediatas", estado, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, 'Pendente', NOW(), NOW());
        """, [cliente_id, tipo, data_ocorrencia, impacto, descricao, acoes_imediatas])

def obter_incidente(incidente_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, tipo, "dataOcorrencia", impacto, descricao, "acoesImediatas", estado, "ClienteId"
            FROM public."Incidentes" WHERE id=%s;
        """, [incidente_id])
        colunas = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(colunas, row)) if row else None

def atualizar_incidente(incidente_id, tipo, impacto, descricao, estado):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE public."Incidentes"
            SET tipo=%s, impacto=%s, descricao=%s, estado=%s, "updatedAt"=NOW()
            WHERE id=%s;
        """, [tipo, impacto, descricao, estado, incidente_id])

def eliminar_incidente(incidente_id):
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM public."Incidentes" WHERE id=%s;""", [incidente_id])
        
        
# 2. Top 5 clientes com mais incidentes de segurança registados
def top5_clientes_mais_incidentes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.nome AS nome_cliente, COUNT(i.id) AS total_incidentes
            FROM public."Clientes" c
            LEFT JOIN public."Incidentes" i ON i."ClienteId" = c.id
            GROUP BY c.id, c.nome
            ORDER BY total_incidentes DESC
            LIMIT 5;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]


# ===========================================================
# OPERAÇÕES DE PEDIDOS/TICKETS 
# ===========================================================

def listar_pedidos():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.titulo, p.descricao, p.estado, p."createdAt", p."updatedAt", c.nome AS nome_cliente
            FROM public."Pedidos" p
            LEFT JOIN public."Clientes" c ON p."ClienteId" = c.id
            ORDER BY p."createdAt" DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_pedido(cliente_id, titulo, descricao):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO public."Pedidos" ("ClienteId", titulo, descricao, estado, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, 'Pendente', NOW(), NOW());
        """, [cliente_id, titulo, descricao])

def obter_pedido(pedido_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, titulo, descricao, estado, "createdAt", "updatedAt", "ClienteId"
            FROM public."Pedidos" WHERE id=%s;
        """, [pedido_id])
        colunas = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(colunas, row)) if row else None

def atualizar_pedido(pedido_id, titulo, descricao, estado):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE public."Pedidos"
            SET titulo=%s, descricao=%s, estado=%s, "updatedAt"=NOW()
            WHERE id=%s;
        """, [titulo, descricao, estado, pedido_id])

def eliminar_pedido(pedido_id):
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM public."Pedidos" WHERE id=%s;""", [pedido_id])
        
        
# 5. Estado dos pedidos/tickets e tempo médio de resolução (em dias)
def estado_pedidos_e_tempo_medio():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                estado,
                COUNT(*) AS total_pedidos,
                ROUND(
                    AVG(
                        EXTRACT(EPOCH FROM ("updatedAt" - "createdAt")) / 86400.0
                    )::numeric, 1
                ) AS tempo_medio_dias
            FROM public."Pedidos"
            GROUP BY estado
            ORDER BY total_pedidos DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]



# ===========================================================
# OPERAÇÕES DE ADMINS 
# ===========================================================

def listar_admins():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, telefone, role
            FROM public."Admins"
            ORDER BY id DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_admin(nome, email, password, telefone='', role='Gestor'):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO public."Admins" (nome, email, password, telefone, role, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
        """, [nome, email, password, telefone, role])

def obter_admin(admin_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, telefone, role
            FROM public."Admins" WHERE id=%s;
        """, [admin_id])
        colunas = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(colunas, row)) if row else None

def atualizar_admin(admin_id, nome, email, telefone, role):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE public."Admins"
            SET nome=%s, email=%s, telefone=%s, role=%s, "updatedAt"=NOW()
            WHERE id=%s;
        """, [nome, email, telefone, role, admin_id])

def eliminar_admin(admin_id):
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM public."Admins" WHERE id=%s;""", [admin_id])


# 4. Distribuição de utilizadores por perfil
#    (Administrador, Colaborador/Gestor, Cliente)
def distribuicao_utilizadores_por_perfil():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT role AS perfil, COUNT(*) AS total
            FROM public."Admins"
            GROUP BY role
            UNION ALL
            SELECT 'Cliente' AS perfil, COUNT(*) AS total
            FROM public."Clientes"
            ORDER BY total DESC;
        """)
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]


