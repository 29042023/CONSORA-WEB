/* =========================
   DATOS DE EJEMPLO
   (En producción esto vendría de la API / vistas de Django)
========================= */

const REQUESTS = [
    { id: 1048, title: "Filtración en terraza", building: "palmas", buildingName: "Las Palmas", status: "En revisión", statusColor: "warning", priority: "Alta", priorityColor: "danger", date: "14/09" },
    { id: 1047, title: "Falla en tablero eléctrico", building: "belgrano", buildingName: "Belgrano", status: "Buscando proveedor", statusColor: "primary", priority: "Alta", priorityColor: "danger", date: "13/09" },
    { id: 1046, title: "Timbre de portería no funciona", building: "palmas", buildingName: "Las Palmas", status: "Presupuestos recibidos", statusColor: "info", priority: "Baja", priorityColor: "secondary", date: "12/09" },
    { id: 1045, title: "Pintura de palier 3er piso", building: "sol", buildingName: "Torres del Sol", status: "Trabajo en ejecución", statusColor: "success", priority: "Media", priorityColor: "secondary", date: "10/09" },
    { id: 1044, title: "Service de ascensor", building: "belgrano", buildingName: "Belgrano", status: "Cerrada", statusColor: "dark", priority: "Media", priorityColor: "secondary", date: "08/09" },
    { id: 1043, title: "Pérdida de agua en cochera", building: "sol", buildingName: "Torres del Sol", status: "Presupuestos recibidos", statusColor: "info", priority: "Crítica", priorityColor: "danger", date: "07/09" },
];

const PROVIDERS = [
    { name: "Servicios Integrales SRL", category: "Mantenimiento general", rating: 4.9, icon: "bi-tools", building: "palmas" },
    { name: "ElectroHogar", category: "Electricidad", rating: 4.8, icon: "bi-lightning-charge", building: "belgrano" },
    { name: "AscenSur", category: "Ascensores", rating: 4.7, icon: "bi-arrow-up-square", building: "belgrano" },
    { name: "Pinturería Centro", category: "Pintura", rating: 4.6, icon: "bi-brush", building: "sol" },
];

const ACTIVITY = [
    { icon: "bi-chat-dots", text: "Nuevo mensaje de ElectroHogar sobre la solicitud #1047", time: "Hace 20 min", building: "belgrano" },
    { icon: "bi-file-earmark-check", text: "Se recibió un presupuesto para la solicitud #1046", time: "Hace 1 h", building: "palmas" },
    { icon: "bi-check2-circle", text: "Se cerró la solicitud #1044", time: "Hace 3 h", building: "belgrano" },
    { icon: "bi-person-plus", text: "Lucía R. gestionó una nueva solicitud", time: "Ayer", building: "sol" },
    { icon: "bi-receipt", text: "Se procesó automáticamente una factura de AscenSur", time: "Ayer", building: "belgrano" },
];

const DOCUMENTS = [
    { icon: "bi-file-earmark-pdf", name: "Presupuesto_ElectroHogar.pdf", meta: "Belgrano · 320 KB", building: "belgrano" },
    { icon: "bi-file-earmark-image", name: "Foto_filtracion_terraza.jpg", meta: "Las Palmas · 1.1 MB", building: "palmas" },
    { icon: "bi-file-earmark-text", name: "Acta_asamblea_agosto.docx", meta: "Torres del Sol · 88 KB", building: "sol" },
    { icon: "bi-file-earmark-pdf", name: "Factura_service_ascensor.pdf", meta: "Belgrano · 210 KB", building: "belgrano" },
];

const ASSISTANTS = [
    { name: "Lucía R.", initial: "L", consorcios: 3, status: "Activo", statusClass: "text-bg-success" },
    { name: "Martín G.", initial: "M", consorcios: 5, status: "Activo", statusClass: "text-bg-success" },
    { name: "Sofía P.", initial: "S", consorcios: 2, status: "Suspendido", statusClass: "text-bg-secondary", muted: true },
];

const BUILDINGS = {
    todos: {
        name: "Todos los edificios",
        address: "6 consorcios bajo tu administración",
        unidades: 214,
        admin: "Vos",
        metrics: { activas: 12, presupuestos: 8, proveedores: 24, finalizados: 15 },
        pipeline: [
            { label: "En revisión", count: 4, total: 12, color: "warning" },
            { label: "Buscando proveedor", count: 3, total: 12, color: "primary" },
            { label: "Presupuestos recibidos", count: 3, total: 12, color: "info" },
            { label: "Trabajo en ejecución", count: 2, total: 12, color: "success" },
        ],
        priority: { Baja: 3, Media: 5, Alta: 3, Crítica: 1 },
    },
    palmas: {
        name: "Edificio Las Palmas",
        address: "Av. Rivadavia 4520, CABA",
        unidades: 42,
        admin: "Vos",
        metrics: { activas: 4, presupuestos: 2, proveedores: 9, finalizados: 6 },
        pipeline: [
            { label: "En revisión", count: 2, total: 4, color: "warning" },
            { label: "Buscando proveedor", count: 1, total: 4, color: "primary" },
            { label: "Presupuestos recibidos", count: 1, total: 4, color: "info" },
            { label: "Trabajo en ejecución", count: 0, total: 4, color: "success" },
        ],
        priority: { Baja: 1, Media: 2, Alta: 1, Crítica: 0 },
    },
    sol: {
        name: "Torres del Sol",
        address: "Bv. Illia 1210, Córdoba",
        unidades: 96,
        admin: "Vos",
        metrics: { activas: 3, presupuestos: 3, proveedores: 8, finalizados: 4 },
        pipeline: [
            { label: "En revisión", count: 0, total: 3, color: "warning" },
            { label: "Buscando proveedor", count: 1, total: 3, color: "primary" },
            { label: "Presupuestos recibidos", count: 1, total: 3, color: "info" },
            { label: "Trabajo en ejecución", count: 1, total: 3, color: "success" },
        ],
        priority: { Baja: 1, Media: 1, Alta: 0, Crítica: 1 },
    },
    belgrano: {
        name: "Edificio Belgrano",
        address: "Av. Cabildo 2140, CABA",
        unidades: 76,
        admin: "Vos",
        metrics: { activas: 5, presupuestos: 3, proveedores: 7, finalizados: 5 },
        pipeline: [
            { label: "En revisión", count: 2, total: 5, color: "warning" },
            { label: "Buscando proveedor", count: 1, total: 5, color: "primary" },
            { label: "Presupuestos recibidos", count: 1, total: 5, color: "info" },
            { label: "Trabajo en ejecución", count: 1, total: 5, color: "success" },
        ],
        priority: { Baja: 1, Media: 2, Alta: 2, Crítica: 0 },
    },
};

let priorityChartInstance = null;


/* =========================
   RENDER
========================= */

function renderBuildingInfo(data) {
    document.getElementById("buildingName").textContent = data.name;
    document.getElementById("buildingAddress").textContent = data.address;
    document.getElementById("buildingUnidades").textContent = data.unidades;
    document.getElementById("buildingAdmin").textContent = data.admin;
}

function renderMetrics(data) {
    document.getElementById("metricActivas").textContent = data.metrics.activas;
    document.getElementById("metricPresupuestos").textContent = data.metrics.presupuestos;
    document.getElementById("metricProveedores").textContent = data.metrics.proveedores;
    document.getElementById("metricFinalizados").textContent = data.metrics.finalizados;
}

function renderPipeline(data) {
    const container = document.getElementById("pipelineContainer");
    container.innerHTML = "";

    data.pipeline.forEach(function (item) {
        const pct = item.total ? Math.round((item.count / item.total) * 100) : 0;

        const row = document.createElement("div");
        row.className = "pipeline-item";
        row.innerHTML =
            '<div class="pipeline-item-top">' +
                "<span>" + item.label + "</span>" +
                "<span>" + item.count + "</span>" +
            "</div>" +
            '<div class="pipeline-bar">' +
                '<div class="pipeline-bar-fill bg-' + item.color + '" style="width:' + pct + '%"></div>' +
            "</div>";

        container.appendChild(row);
    });
}

function renderPriorityChart(data) {
    const labels = Object.keys(data.priority);
    const values = Object.values(data.priority);
    const colors = { Baja: "#94a3b8", Media: "#f59e0b", Alta: "#ef4444", Crítica: "#7f1d1d" };

    const ctx = document.getElementById("priorityChart");

    if (priorityChartInstance) {
        priorityChartInstance.destroy();
    }

    priorityChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: labels.map(function (l) { return colors[l]; }),
                borderWidth: 0,
            }],
        },
        options: {
            cutout: "68%",
            plugins: {
                legend: { display: false },
            },
        },
    });

    const legend = document.getElementById("priorityLegend");
    legend.innerHTML = labels.map(function (l) {
        return '<span><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:' +
            colors[l] + ';margin-right:6px;"></span>' + l + " (" + data.priority[l] + ")</span>";
    }).join("");
}

function renderRecentRequests(buildingKey) {
    const tbody = document.getElementById("recentRequestsBody");
    tbody.innerHTML = "";

    const list = REQUESTS.filter(function (r) {
        return buildingKey === "todos" || r.building === buildingKey;
    }).slice(0, 5);

    list.forEach(function (r) {
        const tr = document.createElement("tr");
        tr.innerHTML =
            "<td class='text-secondary'>#" + r.id + "</td>" +
            "<td>" +
                "<p class='req-title'>" + r.title + "</p>" +
                "<span class='req-building'>" + r.buildingName + "</span>" +
            "</td>" +
            "<td><span class='badge bg-" + r.statusColor + "-subtle text-" + r.statusColor + "-emphasis'>" + r.status + "</span></td>" +
            "<td><span class='badge bg-" + r.priorityColor + "-subtle text-" + r.priorityColor + "-emphasis'>" + r.priority + "</span></td>" +
            "<td class='text-secondary'>" + r.date + "</td>";
        tbody.appendChild(tr);
    });

    if (list.length === 0) {
        tbody.innerHTML = "<tr><td colspan='5' class='text-secondary text-center py-3'>No hay solicitudes para este edificio.</td></tr>";
    }
}

function renderProviders(buildingKey) {
    const container = document.getElementById("topProvidersContainer");
    container.innerHTML = "";

    const list = PROVIDERS.filter(function (p) {
        return buildingKey === "todos" || p.building === buildingKey;
    });

    const finalList = list.length ? list : PROVIDERS;

    finalList.forEach(function (p) {
        const row = document.createElement("div");
        row.className = "provider-row";
        row.innerHTML =
            "<div class='provider-row-info'>" +
                "<div class='provider-row-avatar'><i class='bi " + p.icon + "'></i></div>" +
                "<div class='min-w-0'>" +
                    "<p class='provider-row-name'>" + p.name + "</p>" +
                    "<span class='provider-row-category'>" + p.category + "</span>" +
                "</div>" +
            "</div>" +
            "<div class='provider-row-rating'><i class='bi bi-star-fill'></i>" + p.rating + "</div>";
        container.appendChild(row);
    });
}

function renderActivity(buildingKey) {
    const container = document.getElementById("activityContainer");
    container.innerHTML = "";

    const list = ACTIVITY.filter(function (a) {
        return buildingKey === "todos" || a.building === buildingKey;
    }).slice(0, 5);

    (list.length ? list : ACTIVITY.slice(0, 3)).forEach(function (a) {
        const row = document.createElement("div");
        row.className = "activity-item";
        row.innerHTML =
            "<div class='activity-icon'><i class='bi " + a.icon + "'></i></div>" +
            "<div>" +
                "<p class='activity-text'>" + a.text + "</p>" +
                "<span class='activity-time'>" + a.time + "</span>" +
            "</div>";
        container.appendChild(row);
    });
}

function renderDocuments(buildingKey) {
    const container = document.getElementById("documentsContainer");
    container.innerHTML = "";

    const list = DOCUMENTS.filter(function (d) {
        return buildingKey === "todos" || d.building === buildingKey;
    });

    (list.length ? list : DOCUMENTS.slice(0, 3)).forEach(function (d) {
        const row = document.createElement("div");
        row.className = "document-item";
        row.innerHTML =
            "<div class='document-icon'><i class='bi " + d.icon + "'></i></div>" +
            "<div class='min-w-0'>" +
                "<p class='document-name'>" + d.name + "</p>" +
                "<span class='document-meta'>" + d.meta + "</span>" +
            "</div>";
        container.appendChild(row);
    });
}

function renderAssistants() {
    const container = document.getElementById("assistantsContainer");
    if (!container) return;

    container.innerHTML = "";

    ASSISTANTS.forEach(function (a) {
        const row = document.createElement("div");
        row.className = "assistant-item";
        row.innerHTML =
            "<div class='d-flex align-items-center gap-3'>" +
                "<div class='assistant-avatar" + (a.muted ? " muted" : "") + "'>" + a.initial + "</div>" +
                "<div>" +
                    "<h6 class='fw-bold mb-0'>" + a.name + "</h6>" +
                    "<small class='text-secondary'>" + a.consorcios + " consorcios asignados</small>" +
                "</div>" +
            "</div>" +
            "<span class='badge " + a.statusClass + "'>" + a.status + "</span>";
        container.appendChild(row);
    });
}

function renderBuilding(key) {
    const data = BUILDINGS[key];
    if (!data) return;

    renderBuildingInfo(data);
    renderMetrics(data);
    renderPipeline(data);
    renderPriorityChart(data);
    renderRecentRequests(key);
    renderProviders(key);
    renderActivity(key);
    renderDocuments(key);
}


/* =========================
   ASISTENTE INTELIGENTE (mock)
========================= */

function answerAssistant(question, buildingKey) {
    const data = BUILDINGS[buildingKey];
    const q = question.toLowerCase();

    if (q.includes("reclamo") || q.includes("solicitud")) {
        return "Actualmente hay " + data.metrics.activas + " solicitudes activas en " +
            (buildingKey === "todos" ? "tus consorcios" : data.name) + ".";
    }

    if (q.includes("presupuesto")) {
        return "Tenés " + data.metrics.presupuestos + " presupuestos pendientes de revisión en " +
            (buildingKey === "todos" ? "tus consorcios" : data.name) + ".";
    }

    if (q.includes("proveedor")) {
        return "Contás con " + data.metrics.proveedores + " proveedores activos en " +
            (buildingKey === "todos" ? "tus consorcios" : data.name) + ".";
    }

    return "Por ahora puedo responder consultas sobre reclamos, presupuestos y proveedores. Probá reformular tu pregunta.";
}

function addChatBubble(text, from) {
    const body = document.getElementById("chatWidgetBody");
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble " + (from === "user" ? "user" : "bot");
    bubble.textContent = text;
    body.appendChild(bubble);
    body.scrollTop = body.scrollHeight;
}


/* =========================
   INIT
========================= */

document.addEventListener("DOMContentLoaded", function () {

    // --- Dashboard con datos de ejemplo ---
    const filter = document.getElementById("buildingFilter");

    if (filter) {
        renderBuilding(filter.value);
        renderAssistants();

        filter.addEventListener("change", function () {
            renderBuilding(this.value);
        });
    }

    // --- Sidebar: abrir / cerrar en mobile ---
    const sidebarToggle = document.getElementById("sidebarToggle");
    const adminSidebar = document.getElementById("adminSidebar");

    if (sidebarToggle && adminSidebar) {
        sidebarToggle.addEventListener("click", function () {
            adminSidebar.classList.toggle("open");
        });
    }

    // --- Widget de chat (asistente inteligente) ---
    const chatBtn = document.getElementById("chatWidgetBtn");
    const chatPanel = document.getElementById("chatWidgetPanel");
    const chatClose = document.getElementById("chatWidgetClose");
    const assistantForm = document.getElementById("assistantForm");
    const assistantInput = document.getElementById("assistantInput");

    function toggleChat() {
        chatPanel.classList.toggle("open");
        chatBtn.classList.toggle("active");
    }

    if (chatBtn && chatPanel) {
        chatBtn.addEventListener("click", toggleChat);
    }

    if (chatClose) {
        chatClose.addEventListener("click", toggleChat);
    }

    if (assistantForm) {
        assistantForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const question = assistantInput.value.trim();
            if (!question) return;

            const buildingKey = filter ? filter.value : "todos";

            addChatBubble(question, "user");
            addChatBubble(answerAssistant(question, buildingKey), "bot");
            assistantInput.value = "";
        });
    }

    document.querySelectorAll(".assistant-chip").forEach(function (chip) {
        chip.addEventListener("click", function () {
            const buildingKey = filter ? filter.value : "todos";
            addChatBubble(this.textContent, "user");
            addChatBubble(answerAssistant(this.textContent, buildingKey), "bot");
        });
    });

});