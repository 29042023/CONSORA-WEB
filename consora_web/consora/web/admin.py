from django.contrib import admin
from .models import (
    Rol, EstadoCuenta, Usuario, Administrador, Asistente, Consorcio,
    AsistenteConsorcio, MotivoHistorial, Historial, HistorialDoc,
    TipoChat, Chat, MiembroChat, MensajeChat,
)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'rol')


@admin.register(EstadoCuenta)
class EstadoCuentaAdmin(admin.ModelAdmin):
    list_display = ('id_estado_cuenta', 'estado', 'motivo')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'name_surname', 'mail', 'rol', 'estado_cuenta', 'created_at')
    search_fields = ('name_surname', 'mail', 'dni')
    list_filter = ('rol', 'estado_cuenta')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('id_administrador', 'usuario', 'matricula', 'fecha_alta_matricula')


@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ('id_asistente', 'usuario', 'admin', 'habilitado', 'creado_en')


@admin.register(Consorcio)
class ConsorcioAdmin(admin.ModelAdmin):
    list_display = ('id_consorcio', 'name_consorcio', 'representante', 'direccion')
    search_fields = ('name_consorcio', 'direccion')


@admin.register(AsistenteConsorcio)
class AsistenteConsorcioAdmin(admin.ModelAdmin):
    list_display = ('id_asistente_consorcio', 'asistente', 'consorcio', 'habilitado', 'asignado_en')
    list_filter = ('habilitado',)


@admin.register(MotivoHistorial)
class MotivoHistorialAdmin(admin.ModelAdmin):
    list_display = ('id_motivo_historial', 'categoria', 'motivo')
    list_filter = ('categoria',)


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('id_historial', 'usuario', 'motivo', 'descripcion', 'usuario_involucrado', 'creado_en')
    list_filter = ('motivo__categoria',)
    search_fields = ('descripcion',)


@admin.register(HistorialDoc)
class HistorialDocAdmin(admin.ModelAdmin):
    list_display = ('id_historial_doc', 'historial', 'doc')


@admin.register(TipoChat)
class TipoChatAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_chat', 'name_chat')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id_chat', 'tipo_chat')


@admin.register(MiembroChat)
class MiembroChatAdmin(admin.ModelAdmin):
    list_display = ('id_miembro', 'chat', 'usuario')


@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    list_display = ('id_mensaje', 'chat', 'usuario', 'mensaje', 'enviado_en')
    search_fields = ('mensaje',)