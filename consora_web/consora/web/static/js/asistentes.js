// Filtros del historial de actividad dentro de cada modal de detalle de asistente.
// Recuerda el estado de filtro (tipo, período, texto, solo-con-documentos) por cada lista.
const activityFilterState = {};

function filterActivity(listId, changes) {
    const state = activityFilterState[listId] || { tipo: 'todos', dias: 'todo', texto: '', soloDocs: false };
    Object.assign(state, changes);
    activityFilterState[listId] = state;

    const list = document.getElementById(listId);
    if (!list) return;

    const items = list.querySelectorAll('.activity-item');
    const textoLower = state.texto.trim().toLowerCase();
    let visibles = 0;

    items.forEach(function (item) {
        const matchTipo = state.tipo === 'todos' || item.dataset.type === state.tipo;
        const matchDias = state.dias === 'todo' || parseInt(item.dataset.dias, 10) <= parseInt(state.dias, 10);
        const matchTexto = !textoLower || item.textContent.toLowerCase().includes(textoLower);
        const matchDocs = !state.soloDocs || item.dataset.hasDocs === '1';

        const visible = matchTipo && matchDias && matchTexto && matchDocs;
        item.classList.toggle('hidden', !visible);
        if (visible) visibles++;
    });

    const emptyMsg = document.getElementById(listId + 'Empty');
    if (emptyMsg) emptyMsg.style.display = visibles === 0 ? 'block' : 'none';
}

// Abre la modal compartida de vista previa de documento.
function showDoc(nombre) {
    const nameEl = document.getElementById('docViewerName');
    if (nameEl) nameEl.textContent = nombre;

    const modalEl = document.getElementById('docViewerModal');
    if (!modalEl || !window.bootstrap) return;

    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
}