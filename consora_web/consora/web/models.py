from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.rol


class EstadoCuenta(models.Model):
    id_estado_cuenta = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)
    motivo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'estados_cuenta'

    def __str__(self):
        return self.estado


class Usuario(models.Model):
    id_user = models.AutoField(primary_key=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    name_surname = models.CharField(max_length=150)
    password = models.CharField(max_length=255)  # se guarda el hash, nunca texto plano
    mail = models.EmailField(max_length=150, unique=True)
    rol = models.ForeignKey(
        Rol, on_delete=models.PROTECT, related_name='usuarios', db_column='role',
    )
    dni = models.CharField(max_length=20, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    date_nacimiento = models.DateField(blank=True, null=True)
    estado_cuenta = models.ForeignKey(
        EstadoCuenta, on_delete=models.PROTECT, related_name='usuarios',
        blank=True, null=True, db_column='id_estado_cuenta',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def iniciales(self):
        partes = self.name_surname.split()[:2]
        return "".join(p[0] for p in partes).upper() if partes else "?"

    def __str__(self):
        return f"{self.name_surname} ({self.mail})"


class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='administrador', db_column='id_user',
    )
    matricula = models.CharField(max_length=50, unique=True)
    fecha_alta_matricula = models.DateField(blank=True, null=True)
    ente_otorgante = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'administrador'

    def __str__(self):
        return f"Administrador: {self.usuario.name_surname}"


class Asistente(models.Model):
    id_asistente = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='asistente', db_column='id_user',
    )
    admin = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='asistentes_a_cargo', db_column='id_admin',
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = 'asistente'

    def __str__(self):
        return f"Asistente: {self.usuario.name_surname}"


class Consorcio(models.Model):
    id_consorcio = models.AutoField(primary_key=True)
    representante = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, related_name='consorcios_administrados',
        db_column='representante',
    )
    name_consorcio = models.CharField(max_length=150)
    img_consorcio = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=255)

    class Meta:
        db_table = 'consorcio'

    def __str__(self):
        return self.name_consorcio


class AsistenteConsorcio(models.Model):
    """Qué consorcios puede gestionar cada asistente, y si ese acceso puntual está habilitado."""
    id_asistente_consorcio = models.AutoField(primary_key=True)
    asistente = models.ForeignKey(
        Asistente, on_delete=models.CASCADE, related_name='consorcios_asignados',
    )
    consorcio = models.ForeignKey(
        Consorcio, on_delete=models.CASCADE, related_name='asistentes_asignados',
    )
    habilitado = models.BooleanField(default=True)
    asignado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asistente_consorcio'
        constraints = [
            models.UniqueConstraint(fields=['asistente', 'consorcio'], name='uq_asistente_consorcio'),
        ]

    def __str__(self):
        return f"{self.asistente.usuario.name_surname} → {self.consorcio.name_consorcio}"


class MotivoHistorial(models.Model):
    """Catálogo de motivos posibles de un evento de historial, agrupados por categoría
    (la categoría es lo que se usa para el filtro por tipo en la interfaz)."""
    id_motivo_historial = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=30)  # 'acceso' | 'mensaje' | 'solicitud' | 'presupuesto' | ...
    motivo = models.CharField(max_length=150)

    class Meta:
        db_table = 'motivo_historial'

    def __str__(self):
        return f"[{self.categoria}] {self.motivo}"


class Historial(models.Model):
    id_historial = models.AutoField(primary_key=True)
    motivo = models.ForeignKey(
        MotivoHistorial, on_delete=models.PROTECT, related_name='eventos',
        db_column='id_motivo_historial',
    )
    descripcion = models.CharField(max_length=255)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='historial_generado', db_column='id_user',
    )
    usuario_involucrado = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, related_name='historial_involucrado',
        db_column='id_user_involucrado', blank=True, null=True,
    )
    # No se usa auto_now_add a propósito: así el seed_data puede cargar eventos
    # con fecha pasada para tener datos de ejemplo realistas. Si no se especifica
    # al crear un evento nuevo, toma la fecha/hora actual igual.
    creado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'historial'
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.descripcion} ({self.creado_en:%d/%m/%Y})"


class HistorialDoc(models.Model):
    id_historial_doc = models.AutoField(primary_key=True)
    historial = models.ForeignKey(
        Historial, on_delete=models.CASCADE, related_name='documentos', db_column='id_historial',
    )
    doc = models.CharField(max_length=255)

    class Meta:
        db_table = 'historial_doc'

    def __str__(self):
        return self.doc


class TipoChat(models.Model):
    id_tipo_chat = models.AutoField(primary_key=True)
    name_chat = models.CharField(max_length=50)  # 'Individual' | 'Grupal'

    class Meta:
        db_table = 'tipo_chat'

    def __str__(self):
        return self.name_chat


class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    tipo_chat = models.ForeignKey(
        TipoChat, on_delete=models.PROTECT, related_name='chats', db_column='id_tipo_chat',
    )

    class Meta:
        db_table = 'chat'

    def __str__(self):
        return f"Chat #{self.id_chat}"


class MiembroChat(models.Model):
    id_miembro = models.AutoField(primary_key=True)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='miembros', db_column='id_chat',
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='chats_de_los_que_participa', db_column='id_user',
    )

    class Meta:
        db_table = 'miembros_chat'
        constraints = [
            models.UniqueConstraint(fields=['chat', 'usuario'], name='uq_miembro_por_chat'),
        ]

    def __str__(self):
        return f"{self.usuario.name_surname} en chat #{self.chat_id}"


class MensajeChat(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='mensajes', db_column='id_chat',
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados', db_column='id_user',
    )
    mensaje = models.TextField()
    # DATETIME en vez de TIME: con solo la hora se pierde la fecha del mensaje.
    # default=timezone.now (no auto_now_add) para que el seed_data pueda cargar
    # mensajes con fecha pasada, igual que hicimos con Historial.
    enviado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'mensaje_chat'
        ordering = ['enviado_en']

    def __str__(self):
        return f"{self.usuario.name_surname}: {self.mensaje[:30]}"