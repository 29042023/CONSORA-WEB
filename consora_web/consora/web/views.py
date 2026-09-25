from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Usuario, Asistente, Consorcio, Chat, MensajeChat


def index(request):
    return render(request, 'index.html')


def login_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        usuario = Usuario.objects.filter(mail__iexact=email).first()

        if usuario is None or not usuario.check_password(password):
            error = 'Email o contraseña incorrectos.'
        elif usuario.estado_cuenta and usuario.estado_cuenta.estado != 'Activa':
            error = 'Tu cuenta no está activa. Contactá al soporte.'
        else:
            request.session['usuario_id'] = usuario.pk
            return redirect('dashboard')

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def _get_logged_usuario(request):
    """Devuelve el Usuario logueado (con rol/estado_cuenta) o None si no hay sesión válida."""
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return None

    usuario = Usuario.objects.select_related('rol', 'estado_cuenta').filter(pk=usuario_id).first()

    if usuario is None:
        request.session.flush()
        return None

    return usuario


def dashboard(request):
    usuario = _get_logged_usuario(request)

    if usuario is None:
        return redirect('login')

    return render(request, 'admin/dashboard.html', {
        'page_title': 'Dashboard',
        'page_subtitle': 'Resumen general de tus consorcios',
        'usuario': usuario,
    })


def asistentes(request):
    usuario = _get_logged_usuario(request)

    if usuario is None:
        return redirect('login')

    lista_asistentes = list(
        Asistente.objects
        .select_related('usuario', 'usuario__estado_cuenta')
        .filter(admin=usuario)
        .prefetch_related('consorcios_asignados__consorcio')
        .order_by('usuario__name_surname')
    )

    ahora = timezone.now()

    # Para cada asistente, traemos su historial (más reciente primero) y le
    # calculamos "hace cuántos días" pasó, así el filtro de período del
    # modal (Últimos 7/30 días) puede compararlo del lado del cliente.
    for asistente in lista_asistentes:
        eventos = list(
            asistente.usuario.historial_generado
            .select_related('motivo', 'usuario_involucrado')
            .prefetch_related('documentos')
            .order_by('-creado_en')[:15]
        )
        for evento in eventos:
            evento.dias_ago = (ahora - evento.creado_en).days
        asistente.historial_list = eventos

    total_asistentes = len(lista_asistentes)
    asistentes_activos = sum(1 for a in lista_asistentes if a.habilitado)
    consorcios_delegados = (
        Consorcio.objects
        .filter(asistentes_asignados__asistente__admin=usuario)
        .distinct()
        .count()
    )

    return render(request, 'admin/asistentes.html', {
        'page_title': 'Asistentes',
        'page_subtitle': 'Gestioná las cuentas de tu equipo y sus permisos',
        'usuario': usuario,
        'lista_asistentes': lista_asistentes,
        'total_asistentes': total_asistentes,
        'asistentes_activos': asistentes_activos,
        'consorcios_delegados': consorcios_delegados,
    })


def chat(request):
    usuario = _get_logged_usuario(request)

    if usuario is None:
        return redirect('login')

    # Todos los chats individuales/grupales donde participa este usuario,
    # con el último mensaje de cada uno para armar la lista de la izquierda.
    chats_usuario = (
        Chat.objects
        .filter(miembros__usuario=usuario)
        .prefetch_related('miembros__usuario', 'mensajes')
        .distinct()
    )

    conversaciones = []
    for c in chats_usuario:
        otro_miembro = next(
            (m.usuario for m in c.miembros.all() if m.usuario_id != usuario.pk),
            None,
        )
        ultimo_mensaje = c.mensajes.order_by('-enviado_en').first()

        conversaciones.append({
            'chat': c,
            'otro_usuario': otro_miembro,
            'ultimo_mensaje': ultimo_mensaje,
        })

    # Más reciente primero
    conversaciones.sort(
        key=lambda x: x['ultimo_mensaje'].enviado_en if x['ultimo_mensaje'] else timezone.datetime.min,
        reverse=True,
    )

    # ¿Qué conversación mostrar del lado derecho? La que venga por
    # ?chat_id=, o si no la más reciente de la lista.
    chat_id_param = request.GET.get('chat_id')
    chat_activo = None
    otro_usuario_activo = None
    mensajes_activos = []

    if conversaciones:
        seleccionada = None
        if chat_id_param:
            seleccionada = next(
                (conv for conv in conversaciones if str(conv['chat'].id_chat) == chat_id_param),
                None,
            )
        if seleccionada is None:
            seleccionada = conversaciones[0]

        chat_activo = seleccionada['chat']
        otro_usuario_activo = seleccionada['otro_usuario']
        mensajes_activos = list(
            MensajeChat.objects.filter(chat=chat_activo).select_related('usuario').order_by('enviado_en')
        )

    return render(request, 'chat.html', {
        'page_title': 'Chat',
        'page_subtitle': 'Comunicate con propietarios, proveedores y tu equipo',
        'usuario': usuario,
        'conversaciones': conversaciones,
        'chat_activo': chat_activo,
        'otro_usuario_activo': otro_usuario_activo,
        'mensajes_activos': mensajes_activos,
    })