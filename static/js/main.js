/**
 * Portfolio Main JavaScript
 * Matrix rain, typewriter, scroll animations, contact form
 */

// ── Matrix Canvas Animation ──────────────────────────────
(function initMatrix() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノABCDEFGHIJKLMNOPQRSTUVWXYZ<>{}[]()';
    const fontSize = 13;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = Array(columns).fill(1);

    function drawMatrix() {
        ctx.fillStyle = 'rgba(5, 8, 16, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00f5ff';
        ctx.font = `${fontSize}px 'Share Tech Mono', monospace`;

        for (let i = 0; i < drops.length; i++) {
            const char = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillStyle = Math.random() > 0.98 ? '#ffffff' : '#00f5ff';
            ctx.globalAlpha = Math.random() * 0.5 + 0.2;
            ctx.fillText(char, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
        ctx.globalAlpha = 1;
    }

    setInterval(drawMatrix, 50);
    window.addEventListener('resize', () => {
        columns = Math.floor(canvas.width / fontSize);
        drops = Array(columns).fill(1);
    });
})();

// ── Typewriter Effect ────────────────────────────────────
(function initTypewriter() {
    const el = document.getElementById('typewriter');
    if (!el) return;

    const phrases = [
        'Full Stack Developer',
        'Python & Flask Expert',
        'UI/UX Enthusiast',
        'Problem Solver',
        'Open Source Contributor'
    ];

    let phraseIndex = 0, charIndex = 0, deleting = false;
    let speed = 100;

    function type() {
        const current = phrases[phraseIndex];
        if (deleting) {
            el.textContent = current.slice(0, --charIndex);
            speed = 60;
        } else {
            el.textContent = current.slice(0, ++charIndex);
            speed = 100;
        }

        if (!deleting && charIndex === current.length) {
            speed = 2000;
            deleting = true;
        } else if (deleting && charIndex === 0) {
            deleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            speed = 400;
        }
        setTimeout(type, speed);
    }
    setTimeout(type, 1000);
})();

// ── Navbar Scroll Effect ─────────────────────────────────
(function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });

    // Active link highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    function updateActiveLink() {
        let current = '';
        sections.forEach(sec => {
            if (window.scrollY >= sec.offsetTop - 100) current = sec.id;
        });
        navLinks.forEach(link => {
            link.classList.toggle('active', link.dataset.section === current);
        });
    }
    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();
})();

// ── Mobile Hamburger Menu ────────────────────────────────
(function initHamburger() {
    const btn = document.getElementById('hamburger');
    const links = document.querySelector('.nav-links');
    if (!btn || !links) return;

    btn.addEventListener('click', () => {
        links.classList.toggle('open');
    });

    // Close on link click
    links.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => links.classList.remove('open'));
    });
})();

// ── Scroll Reveal Animation ──────────────────────────────
(function initReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                // Stagger effect
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, i * 80);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    elements.forEach(el => observer.observe(el));
})();

// ── Skill Bar Animation ──────────────────────────────────
(function initSkillBars() {
    const bars = document.querySelectorAll('.skill-fill');
    if (!bars.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target.dataset.target;
                entry.target.style.width = target + '%';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    bars.forEach(bar => observer.observe(bar));
})();

// ── Contact Form ─────────────────────────────────────────
(function initContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('submitBtn');
        const msgEl = document.getElementById('formMessage');
        const data = new FormData(form);

        // Loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yuborilmoqda...';
        msgEl.className = 'form-message';
        msgEl.style.display = 'none';

        try {
            const res = await fetch('/contact', { method: 'POST', body: data });
            const json = await res.json();

            if (json.success) {
                msgEl.textContent = json.message;
                msgEl.className = 'form-message success';
                msgEl.style.display = 'block';
                form.reset();
            } else {
                throw new Error(json.message);
            }
        } catch (err) {
            msgEl.textContent = err.message || 'Xatolik yuz berdi. Qayta urinib ko\'ring.';
            msgEl.className = 'form-message error';
            msgEl.style.display = 'block';
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Yuborish';
        }
    });
})();

// ── Smooth scroll for anchor links ──────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ── Cursor glow effect ───────────────────────────────────
(function initCursorGlow() {
    const glow = document.createElement('div');
    glow.style.cssText = `
        position: fixed; pointer-events: none; z-index: 9999;
        width: 300px; height: 300px; border-radius: 50%;
        background: radial-gradient(circle, rgba(0,245,255,0.04) 0%, transparent 70%);
        transform: translate(-50%, -50%); transition: opacity 0.3s;
        mix-blend-mode: screen;
    `;
    document.body.appendChild(glow);

    document.addEventListener('mousemove', (e) => {
        glow.style.left = e.clientX + 'px';
        glow.style.top = e.clientY + 'px';
    });

    document.addEventListener('mouseleave', () => glow.style.opacity = '0');
    document.addEventListener('mouseenter', () => glow.style.opacity = '1');
})();
