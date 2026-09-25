// Filtros de la lista de conversaciones (por ahora solo visual: marca el
// chip activo, todavía no filtra la lista de verdad — eso necesita, o un
// campo que identifique el rol directamente en la conversación, o volver
// a pedirle la página al servidor con ese filtro por query param).
document.querySelectorAll('.chat-filter-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
        document.querySelectorAll('.chat-filter-chip').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
    });
});

// Nota: la selección de conversación (chat-list-item) ya NO se maneja acá.
// Ahora cada item es un link real (?chat_id=...) que recarga la página con
// esa conversación cargada del lado del servidor.