/**
 * Admin Panel JavaScript
 */

// ── Sidebar mobile toggle ────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // Range input live value display
    document.querySelectorAll('input[type="range"]').forEach(range => {
        const display = document.getElementById(range.id + '_display');
        if (display) {
            display.textContent = range.value + '%';
            range.addEventListener('input', () => {
                display.textContent = range.value + '%';
            });
        }
    });

    // Auto-hide alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // Image file preview
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function () {
            const preview = document.getElementById(this.id + '_preview');
            if (preview && this.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
});

// ── Inline skill edit ────────────────────────────────────
function editSkill(id) {
    const rows = document.querySelectorAll('.skill-edit-row');
    rows.forEach(r => {
        if (r.dataset.id != id) r.style.display = 'none';
    });
    const row = document.querySelector(`.skill-edit-row[data-id="${id}"]`);
    if (row) row.style.display = row.style.display === 'table-row' ? 'none' : 'table-row';
}

function saveSkill(id) {
    const name = document.getElementById(`skill_name_${id}`).value.trim();
    const level = document.getElementById(`skill_level_${id}`).value;
    const category = document.getElementById(`skill_category_${id}`).value.trim();

    fetch(`/admin/skills/edit/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `name=${encodeURIComponent(name)}&level=${level}&category=${encodeURIComponent(category)}`
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showToast('Ko\'nikma yangilandi!', 'success');
            setTimeout(() => location.reload(), 800);
        }
    })
    .catch(() => showToast('Xatolik yuz berdi', 'error'));
}

// ── Delete confirmation ──────────────────────────────────
function confirmDelete(formId, msg) {
    if (confirm(msg || 'O\'chirishni tasdiqlaysizmi?')) {
        document.getElementById(formId).submit();
    }
}

// ── Toast notification ───────────────────────────────────
function showToast(message, type = 'success') {
    const colors = {
        success: { bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.3)', color: '#00ff88' },
        error:   { bg: 'rgba(255,0,128,0.1)', border: 'rgba(255,0,128,0.3)', color: '#ff0080' },
        info:    { bg: 'rgba(0,245,255,0.1)', border: 'rgba(0,245,255,0.3)', color: '#00f5ff' },
    };
    const c = colors[type] || colors.info;
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
        padding: 0.9rem 1.5rem; border-radius: 8px;
        background: ${c.bg}; border: 1px solid ${c.border}; color: ${c.color};
        font-family: 'Share Tech Mono', monospace; font-size: 0.85rem;
        backdrop-filter: blur(15px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        animation: slideInRight 0.3s ease;
    `;
    toast.textContent = message;

    const style = document.createElement('style');
    style.textContent = `@keyframes slideInRight { from { transform: translateX(120%); opacity: 0; } to { transform: none; opacity: 1; } }`;
    document.head.appendChild(style);

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.4s';
        setTimeout(() => toast.remove(), 400);
    }, 2500);
}
