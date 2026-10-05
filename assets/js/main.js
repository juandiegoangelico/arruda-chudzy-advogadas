/**
 * ARRUDA CHUDZY ADVOGADAS - Main Interactive Logic
 * Modern, accessible, lightweight vanilla JS
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeaderScroll();
  initMobileMenu();
  initScrollSpy();
  initScrollReveal();
  initContactForm();
});

/**
 * Header shrinking on scroll with modern fallback
 * Checks CSS.supports for scroll-driven animations; if not supported, applies fallback.
 */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const supportsScrollTimeline = 'CSS' in window &&
    CSS.supports('(animation-timeline: scroll()) and (animation-range: 0% 100%)');

  if (!supportsScrollTimeline) {
    let ticking = false;
    const threshold = 60;

    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (window.scrollY > threshold) {
            header.classList.add('shrunk');
          } else {
            header.classList.remove('shrunk');
          }
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // initial check
  }
}

/**
 * Mobile Navigation Menu & ARIA management
 */
function initMobileMenu() {
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (!menuToggle || !navMenu) return;

  const toggleMenu = (open) => {
    const shouldOpen = open !== undefined ? open : !navMenu.classList.contains('is-open');
    menuToggle.classList.toggle('is-active', shouldOpen);
    navMenu.classList.toggle('is-open', shouldOpen);
    menuToggle.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false');
    document.body.style.overflow = shouldOpen ? 'hidden' : '';
  };

  menuToggle.addEventListener('click', () => toggleMenu());

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (navMenu.classList.contains('is-open')) {
        toggleMenu(false);
      }
    });
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu.classList.contains('is-open')) {
      toggleMenu(false);
    }
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (navMenu.classList.contains('is-open') &&
        !navMenu.contains(e.target) &&
        !menuToggle.contains(e.target)) {
      toggleMenu(false);
    }
  });
}

/**
 * Active navigation link updater based on visible section
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  if (!sections.length || !navLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          const href = link.getAttribute('href');
          if (href === '#' + id) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach(sec => observer.observe(sec));
}

/**
 * Scroll Reveal Animations via IntersectionObserver
 */
function initScrollReveal() {
  const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (!revealElements.length) return;

  // If user prefers reduced motion, show immediately
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealElements.forEach(el => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.1
  });

  revealElements.forEach(el => observer.observe(el));
}

/**
 * Contact Form submission & WhatsApp bridge
 */
function initContactForm() {
  const form = document.getElementById('contactForm');
  const feedback = document.getElementById('formFeedback');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = form.querySelector('[name="nome"]').value.trim();
    const phone = form.querySelector('[name="telefone"]').value.trim();
    const email = form.querySelector('[name="email"]').value.trim();
    const area = form.querySelector('[name="area"]').value;
    const message = form.querySelector('[name="mensagem"]').value.trim();

    if (!name || !phone) {
      alert('Por favor, preencha seu nome e telefone para contato.');
      return;
    }

    // Format message for WhatsApp
    const lines = [
      '*Novo Contato via Site - Arruda Chudzy Advogadas*',
      '',
      `*Nome:* ${name}`,
      `*Telefone:* ${phone}`,
      `*E-mail:* ${email || 'Não informado'}`,
      `*Área de Interesse:* ${area}`,
      `*Mensagem:* ${message || 'Solicitação de atendimento personalizado.'}`
    ];
    const waText = encodeURIComponent(lines.join('\n'));
    const waUrl = `https://wa.me/5549999370099?text=${waText}`;

    if (feedback) {
      feedback.className = 'form-feedback success';
      feedback.innerHTML = `
        <strong>Mensagem preparada com sucesso!</strong><br>
        Você será redirecionado para o WhatsApp do escritório para concluir seu atendimento personalizado com nossas advogadas.
      `;
      feedback.style.display = 'block';
    }

    setTimeout(() => {
      window.open(waUrl, '_blank', 'noopener,noreferrer');
      form.reset();
    }, 1200);
  });
}
