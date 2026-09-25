from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from web.models import (
    Rol, EstadoCuenta, Usuario, Administrador, Asistente,
    Consorcio, AsistenteConsorcio, MotivoHistorial, Historial, HistorialDoc,
    TipoChat, Chat, MiembroChat, MensajeChat,
)


class Command(BaseCommand):
    help = "Carga los datos de ejemplo de CONSORA (roles, estados, usuarios, asistentes, consorcios, historial)."

    def handle(self, *args, **options):

        # --- Roles ---
        roles = {}
        for nombre in [
            'Administrador del sistema',
            'Administrador/a',
            'Propietario/Residente',
            'Proveedor',
            'Asistente',
        ]:
            rol, created = Rol.objects.get_or_create(rol=nombre)
            roles[nombre] = rol
            self.stdout.write(self.style.SUCCESS(f"Rol: {nombre}") if created else f"Rol ya existía: {nombre}")

        # --- Estados de cuenta ---
        estado_activa, _ = EstadoCuenta.objects.get_or_create(estado='Activa', defaults={'motivo': None})
        EstadoCuenta.objects.get_or_create(estado='Suspendida', defaults={'motivo': 'Pago pendiente'})
        EstadoCuenta.objects.get_or_create(estado='Baja', defaults={'motivo': 'Solicitada por el usuario'})

        # --- Usuarios de ejemplo (todos con la misma contraseña de prueba) ---
        PASSWORD_PRUEBA = 'consora123'

        usuarios_data = [
            dict(mail='maria.gonzalez@consora.com', name_surname='María González',
                 rol=roles['Administrador/a'], dni='30111222', phone='+5491111111111',
                 date_nacimiento='1985-03-12'),
            dict(mail='lucia.r@consora.com', name_surname='Lucía Ramírez',
                 rol=roles['Asistente'], dni='35222333', phone='+5491122222222',
                 date_nacimiento='1996-07-01'),
            dict(mail='martin.g@consora.com', name_surname='Martín Gómez',
                 rol=roles['Asistente'], dni='34333444', phone='+5491133333333',
                 date_nacimiento='1994-11-20'),
            dict(mail='sofia.p@consora.com', name_surname='Sofía Pérez',
                 rol=roles['Asistente'], dni='36444555', phone='+5491144444444',
                 date_nacimiento='1998-02-15'),
            dict(mail='carlos.perez@mail.com', name_surname='Carlos Pérez',
                 rol=roles['Propietario/Residente'], dni='28444555', phone='+5491144444444',
                 date_nacimiento='1978-05-05'),
            dict(mail='ana.fernandez@mail.com', name_surname='Ana Fernández',
                 rol=roles['Propietario/Residente'], dni='31555666', phone='+5491155555555',
                 date_nacimiento='1990-09-18'),
            dict(mail='contacto@electrohogar.com', name_surname='ElectroHogar SRL',
                 rol=roles['Proveedor'], dni=None, phone='+5491166666666',
                 date_nacimiento=None),
        ]

        usuarios = {}
        for data in usuarios_data:
            usuario, created = Usuario.objects.get_or_create(
                mail=data['mail'],
                defaults={
                    'name_surname': data['name_surname'],
                    'rol': data['rol'],
                    'dni': data['dni'],
                    'phone': data['phone'],
                    'date_nacimiento': data['date_nacimiento'],
                    'estado_cuenta': estado_activa,
                },
            )
            if created:
                usuario.set_password(PASSWORD_PRUEBA)
                usuario.save()
                self.stdout.write(self.style.SUCCESS(f"Usuario creado: {data['mail']}"))
            else:
                self.stdout.write(f"Usuario ya existía: {data['mail']}")

            usuarios[data['mail']] = usuario

        # --- Administrador (María) ---
        Administrador.objects.get_or_create(
            usuario=usuarios['maria.gonzalez@consora.com'],
            defaults={
                'matricula': 'RPA-12345',
                'fecha_alta_matricula': '2015-02-10',
                'ente_otorgante': 'Registro Público de Administradores - GCBA',
            },
        )

        # --- Asistentes (Lucía y Martín activos, Sofía suspendida) ---
        asistentes = {}

        asistente_lucia, _ = Asistente.objects.get_or_create(
            usuario=usuarios['lucia.r@consora.com'],
            defaults={'admin': usuarios['maria.gonzalez@consora.com'], 'habilitado': True},
        )
        asistentes['lucia'] = asistente_lucia

        asistente_martin, _ = Asistente.objects.get_or_create(
            usuario=usuarios['martin.g@consora.com'],
            defaults={'admin': usuarios['maria.gonzalez@consora.com'], 'habilitado': True},
        )
        asistentes['martin'] = asistente_martin

        asistente_sofia, _ = Asistente.objects.get_or_create(
            usuario=usuarios['sofia.p@consora.com'],
            defaults={'admin': usuarios['maria.gonzalez@consora.com'], 'habilitado': False},
        )
        asistentes['sofia'] = asistente_sofia

        # --- Consorcios (todos administrados por María) ---
        consorcios_data = [
            dict(nombre='Edificio Las Palmas', direccion='Av. Rivadavia 4520, CABA',
                 descripcion='Edificio de 42 unidades en Av. Rivadavia'),
            dict(nombre='Torres del Sol', direccion='Bv. Illia 1210, Córdoba',
                 descripcion='Complejo de 96 unidades en Córdoba'),
            dict(nombre='Edificio Belgrano', direccion='Av. Cabildo 2140, CABA',
                 descripcion='Edificio de 76 unidades en Belgrano'),
            dict(nombre='Edificio San Martín', direccion='San Martín 850, CABA',
                 descripcion='Edificio de 30 unidades'),
            dict(nombre='Edificio Norte', direccion='Av. del Libertador 6200, CABA',
                 descripcion='Edificio de 54 unidades'),
        ]

        consorcios = {}
        for data in consorcios_data:
            consorcio, created = Consorcio.objects.get_or_create(
                name_consorcio=data['nombre'],
                defaults={
                    'representante': usuarios['maria.gonzalez@consora.com'],
                    'direccion': data['direccion'],
                    'descripcion': data['descripcion'],
                },
            )
            consorcios[data['nombre']] = consorcio
            if created:
                self.stdout.write(self.style.SUCCESS(f"Consorcio creado: {data['nombre']}"))

        # --- Asignaciones asistente ↔ consorcio ---
        asignaciones = [
            ('lucia', 'Edificio Las Palmas', True),
            ('lucia', 'Torres del Sol', True),
            ('lucia', 'Edificio Belgrano', True),

            ('martin', 'Edificio Las Palmas', True),
            ('martin', 'Torres del Sol', True),
            ('martin', 'Edificio Belgrano', False),
            ('martin', 'Edificio San Martín', True),
            ('martin', 'Edificio Norte', True),

            ('sofia', 'Torres del Sol', False),
            ('sofia', 'Edificio Belgrano', False),
        ]

        for clave_asistente, nombre_consorcio, habilitado in asignaciones:
            AsistenteConsorcio.objects.get_or_create(
                asistente=asistentes[clave_asistente],
                consorcio=consorcios[nombre_consorcio],
                defaults={'habilitado': habilitado},
            )

        # --- Motivos de historial (agrupados por categoría) ---
        motivos_data = [
            ('mensaje', 'Mensaje con cliente'),
            ('mensaje', 'Archivo enviado a cliente'),
            ('mensaje', 'Archivo recibido'),
            ('presupuesto', 'Presupuesto cargado'),
            ('factura', 'Factura cargada'),
            ('solicitud', 'Solicitud creada'),
            ('solicitud', 'Solicitud actualizada'),
            ('solicitud', 'Solicitud cerrada'),
            ('acceso', 'Consorcio asignado'),
            ('acceso', 'Consorcio deshabilitado'),
            ('acceso', 'Cuenta suspendida'),
            ('acceso', 'Cuenta reactivada'),
        ]

        motivos = {}
        for categoria, motivo in motivos_data:
            obj, created = MotivoHistorial.objects.get_or_create(categoria=categoria, motivo=motivo)
            motivos[motivo] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Motivo creado: [{categoria}] {motivo}"))

        # --- Eventos de historial de ejemplo (con fechas pasadas, para tener datos realistas) ---
        ahora = timezone.now()

        def hace(dias, horas=0):
            return ahora - timedelta(days=dias, hours=horas)

        eventos = [
            # Lucía
            dict(usuario='lucia.r@consora.com', motivo='Mensaje con cliente',
                 descripcion='Respondió al mensaje de ElectroHogar (solicitud #1047)',
                 involucrado='contacto@electrohogar.com', cuando=hace(0, 2)),
            dict(usuario='lucia.r@consora.com', motivo='Solicitud actualizada',
                 descripcion='Cambió la solicitud #1046 a "Presupuestos recibidos"',
                 involucrado=None, cuando=hace(1)),
            dict(usuario='lucia.r@consora.com', motivo='Archivo enviado a cliente',
                 descripcion='Envió el reglamento de copropiedad a Carlos Pérez',
                 involucrado='carlos.perez@mail.com', cuando=hace(2),
                 docs=['reglamento_copropiedad.pdf']),
            dict(usuario='lucia.r@consora.com', motivo='Presupuesto cargado',
                 descripcion='Cargó un presupuesto de Servicios Integrales SRL',
                 involucrado=None, cuando=hace(5),
                 docs=['presupuesto_servicios_integrales.pdf']),
            dict(usuario='lucia.r@consora.com', motivo='Solicitud creada',
                 descripcion='Creó la solicitud #1041 (filtración en cochera)',
                 involucrado='carlos.perez@mail.com', cuando=hace(9),
                 docs=['foto_filtracion_cochera.jpg', 'foto_filtracion_cochera_2.jpg']),
            dict(usuario='lucia.r@consora.com', motivo='Mensaje con cliente',
                 descripcion='Envió un mensaje a un propietario de Las Palmas',
                 involucrado='carlos.perez@mail.com', cuando=hace(14)),
            dict(usuario='lucia.r@consora.com', motivo='Factura cargada',
                 descripcion='Cargó la factura de expensas de septiembre de Las Palmas',
                 involucrado=None, cuando=hace(4),
                 docs=['factura_expensas_las_palmas_09_2026.pdf']),
            dict(usuario='lucia.r@consora.com', motivo='Consorcio asignado',
                 descripcion='Se le asignó el consorcio Torres del Sol',
                 involucrado=None, cuando=hace(90)),

            # Martín
            dict(usuario='martin.g@consora.com', motivo='Factura cargada',
                 descripcion='Cargó la factura de AscenSur por el service del mes',
                 involucrado=None, cuando=hace(6),
                 docs=['factura_ascensur_09_2026.pdf']),
            dict(usuario='martin.g@consora.com', motivo='Presupuesto cargado',
                 descripcion='Cargó un presupuesto de Pinturería Centro',
                 involucrado=None, cuando=hace(3),
                 docs=['presupuesto_pintureria_centro.pdf']),
            dict(usuario='martin.g@consora.com', motivo='Solicitud cerrada',
                 descripcion='Cerró la solicitud #1044 (service de ascensor)',
                 involucrado=None, cuando=hace(7)),
            dict(usuario='martin.g@consora.com', motivo='Archivo recibido',
                 descripcion='Recibió el certificado de service de AscenSur',
                 involucrado='ana.fernandez@mail.com', cuando=hace(8),
                 docs=['certificado_service_ascensor.pdf']),
            dict(usuario='martin.g@consora.com', motivo='Consorcio deshabilitado',
                 descripcion='Se le deshabilitó el acceso al consorcio Belgrano',
                 involucrado=None, cuando=hace(20)),
            dict(usuario='martin.g@consora.com', motivo='Solicitud creada',
                 descripcion='Creó la solicitud #1038 (luces de emergencia)',
                 involucrado=None, cuando=hace(35)),
            dict(usuario='martin.g@consora.com', motivo='Consorcio asignado',
                 descripcion='Se le asignó el consorcio Edificio Norte',
                 involucrado=None, cuando=hace(135)),

            # Sofía
            dict(usuario='sofia.p@consora.com', motivo='Cuenta suspendida',
                 descripcion='Cuenta suspendida por María González',
                 involucrado='maria.gonzalez@consora.com', cuando=hace(45)),
            dict(usuario='sofia.p@consora.com', motivo='Mensaje con cliente',
                 descripcion='Respondió una consulta de un propietario',
                 involucrado='ana.fernandez@mail.com', cuando=hace(49)),
            dict(usuario='sofia.p@consora.com', motivo='Solicitud actualizada',
                 descripcion='Cambió la solicitud #1030 a "En revisión"',
                 involucrado=None, cuando=hace(60)),
            dict(usuario='sofia.p@consora.com', motivo='Consorcio asignado',
                 descripcion='Se le asignó el consorcio Torres del Sol',
                 involucrado=None, cuando=hace(238)),
        ]

        creados = 0
        docs_creados = 0
        for ev in eventos:
            evento, created = Historial.objects.get_or_create(
                usuario=usuarios[ev['usuario']],
                descripcion=ev['descripcion'],
                defaults={
                    'motivo': motivos[ev['motivo']],
                    'usuario_involucrado': usuarios[ev['involucrado']] if ev['involucrado'] else None,
                    'creado_en': ev['cuando'],
                },
            )
            if created:
                creados += 1

            # Los documentos se aseguran siempre, exista o no el evento de antes
            # (si ya corriste seed_data una vez sin esta parte, esto la completa).
            for nombre_doc in ev.get('docs', []):
                _, doc_creado = HistorialDoc.objects.get_or_create(historial=evento, doc=nombre_doc)
                if doc_creado:
                    docs_creados += 1

        self.stdout.write(self.style.SUCCESS(f"Eventos de historial cargados: {creados}"))
        self.stdout.write(self.style.SUCCESS(f"Documentos adjuntos cargados: {docs_creados}"))

        # --- Tipos de chat ---
        tipo_individual, _ = TipoChat.objects.get_or_create(name_chat='Individual')
        TipoChat.objects.get_or_create(name_chat='Grupal')

        def crear_chat_individual(usuario_a, usuario_b, mensajes):
            """Busca un chat individual ya existente entre estos dos usuarios
            por email, o crea uno nuevo."""

            usuario_a = usuarios[usuario_a]
            usuario_b = usuarios[usuario_b]

            chat_existente = (
                Chat.objects
                .filter(tipo_chat=tipo_individual, miembros__usuario=usuario_a)
                .filter(miembros__usuario=usuario_b)
                .first()
            )

            if chat_existente:
                chat = chat_existente
            else:
                chat = Chat.objects.create(tipo_chat=tipo_individual)
                MiembroChat.objects.create(chat=chat, usuario=usuario_a)
                MiembroChat.objects.create(chat=chat, usuario=usuario_b)

            creados_msj = 0

            for autor, texto, cuando in mensajes:
                _, creado = MensajeChat.objects.get_or_create(
                    chat=chat,
                    usuario=usuarios[autor],
                    mensaje=texto,
                    defaults={'enviado_en': cuando},
                )

                if creado:
                    creados_msj += 1

            return chat, creados_msj

            if chat_existente:
                chat = chat_existente
            else:
                chat = Chat.objects.create(tipo_chat=tipo_individual)
                MiembroChat.objects.create(chat=chat, usuario=usuario_a)
                MiembroChat.objects.create(chat=chat, usuario=usuario_b)

            creados_msj = 0
            for autor, texto, cuando in mensajes:
                _, creado = MensajeChat.objects.get_or_create(
                    chat=chat, usuario=usuarios[autor], mensaje=texto,
                    defaults={'enviado_en': cuando},
                )
                if creado:
                    creados_msj += 1

            return chat, creados_msj

        # Chat María <-> Carlos (mismo contenido que el mockup de la página de Chat)
        _, n1 = crear_chat_individual(
            'maria.gonzalez@consora.com', 'carlos.perez@mail.com',
            [
                ('carlos.perez@mail.com', 'Hola, quería consultar por el estado de mi reclamo de la filtración en la terraza.', hace(0, 3)),
                ('maria.gonzalez@consora.com', 'Hola Carlos, ya estamos esperando el presupuesto de Servicios Integrales SRL. Apenas lo tengamos te aviso.', hace(0, 3) ),
                ('carlos.perez@mail.com', 'Te mando una foto más, se nota mejor la humedad en la esquina.', hace(0, 2)),
                ('maria.gonzalez@consora.com', 'Perfecto, la sumo a la solicitud. En cuanto tengamos el presupuesto te contactamos para coordinar.', hace(0, 2)),
                ('carlos.perez@mail.com', 'Perfecto, quedo atento a la respuesta', hace(0, 1)),
            ],
        )

        # Chat María <-> Ana
        _, n2 = crear_chat_individual(
            'maria.gonzalez@consora.com', 'ana.fernandez@mail.com',
            [
                ('ana.fernandez@mail.com', '¿Ya se coordinó la visita técnica?', hace(1)),
                ('maria.gonzalez@consora.com', 'Todavía no, estamos comparando presupuestos. Te confirmo esta semana.', hace(1)),
            ],
        )

        # Chat María <-> ElectroHogar
        _, n3 = crear_chat_individual(
            'maria.gonzalez@consora.com', 'contacto@electrohogar.com',
            [
                ('maria.gonzalez@consora.com', 'Hola, ¿cómo va el presupuesto para la solicitud #1047?', hace(1, 2)),
                ('contacto@electrohogar.com', 'Envío el presupuesto en breve', hace(1)),
            ],
        )

        # Chat María <-> Lucía (asistente)
        _, n4 = crear_chat_individual(
            'maria.gonzalez@consora.com', 'lucia.r@consora.com',
            [
                ('lucia.r@consora.com', 'Ya avisé a Carlos sobre el reclamo', hace(4)),
            ],
        )

        self.stdout.write(self.style.SUCCESS(f"Mensajes de chat cargados: {n1 + n2 + n3 + n4}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nListo. Todos los usuarios de ejemplo tienen la contraseña: {PASSWORD_PRUEBA}"
        ))