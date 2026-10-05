/**
 * ARRUDA CHUDZY ADVOGADAS - Dynamic Events & Content Gallery
 * Features:
 * - Dynamic Category Filtering
 * - Native <dialog> Modal Viewer
 * - Mandatory Light-Dismiss Fallback (Modern Web Guidance)
 * - Extensible Data Architecture for future events, courses, and publications
 */

// Events Data Repository
const EVENTS_DATA = [
  {
    id: 'summit-saude-2026',
    category: 'palestras',
    categoryLabel: 'Palestra',
    title: 'Summit Saúde: Secretárias 360º — Treinamento Jurídico',
    date: 'Florianópolis / SC',
    image: 'assets/images/events-lecture.jpg',
    excerpt: 'Treinamento jurídico intensivo para equipes de atendimento e secretárias em clínicas e consultórios médicos, minimizando riscos civis e éticos.',
    fullDescription: 'Participação de destaque no Summit Saúde apresentando a palestra "Secretárias 360º — treinamento jurídico para a equipe que atende o paciente". Foco na primeira linha de acolhimento e proteção de clínicas, conformidade com a LGPD em dados sensíveis de saúde, gestão de prontuários e prevenção estratégica de reclamações ético-profissionais perante o CRM.'
  },
  {
    id: 'tcle-compliance-medico',
    category: 'cursos',
    categoryLabel: 'Curso / Workshop',
    title: 'Workshop de Compliance Médico e Validade do TCLE',
    date: 'Lages / SC',
    image: 'assets/images/contracts-desk.jpg',
    excerpt: 'Elaboração e implementação prática do Termo de Consentimento Livre e Esclarecido (TCLE) personalizado para procedimentos invasivos e cirúrgicos.',
    fullDescription: 'Workshop exclusivo direcionado a cirurgiões, dermatologistas e gestores de clínicas. Abordou as mais recentes teses do Superior Tribunal de Justiça (STJ) sobre o dever de informação, a insuficiência de termos genéricos padronizados e as melhores práticas na personalização do TCLE para respaldar a prática médica e evitar indenizações.'
  },
  {
    id: 'blindagem-contratual-clinicas',
    category: 'publicacoes',
    categoryLabel: 'Publicação Especializada',
    title: 'Guia de Contratos Médicos e Sociedades em Saúde',
    date: 'Artigo & E-book Jurídico',
    image: 'assets/images/office-consultation.jpg',
    excerpt: 'Análise minuciosa das cláusulas essenciais em contratos de prestação de serviços médicos, locação de consultórios e acordos de sócios.',
    fullDescription: 'Publicação técnica de autoria das sócias detalhando os principais erros contratuais em sociedades de saúde e parcerias médicas. Traz orientações preventivas sobre cláusulas de não concorrência, sigilo profissional, divisão de responsabilidades civis e estratégias para mitigar conflitos societários antes que atinjam esferas judiciais.'
  },
  {
    id: 'defesa-etica-crm',
    category: 'institucional',
    categoryLabel: 'Atuação Institucional',
    title: 'Assessoria Consultiva e Ético-Profissional em Sindicâncias',
    date: 'Atuação Regional',
    image: 'assets/images/hero-advocacia-saude.jpg',
    excerpt: 'Acompanhamento rigoroso e técnico de sindicâncias e processos ético-disciplinares em conselhos de classe de medicina e áreas afins.',
    fullDescription: 'Atuação especializada e personalizada em todas as fases de sindicâncias e Processos Ético-Profissionais (PEP) perante o Conselho Regional de Medicina. Elaboração de defesas preliminares, acompanhamento em oitivas e recursos no Conselho Federal de Medicina (CFM), resguardando o histórico e o livre exercício da profissão médica com sigilo e excelência técnica.'
  }
];

document.addEventListener('DOMContentLoaded', () => {
  initEventsGallery();
  initEventModal();
});

/**
 * Renders gallery cards and binds category filters
 */
function initEventsGallery() {
  const galleryContainer = document.getElementById('eventsGalleryGrid');
  const filterButtons = document.querySelectorAll('.filter-btn');

  if (!galleryContainer) return;

  const renderCards = (filterCategory = 'todos') => {
    galleryContainer.innerHTML = '';

    const filtered = filterCategory === 'todos'
      ? EVENTS_DATA
      : EVENTS_DATA.filter(item => item.category === filterCategory);

    filtered.forEach(item => {
      const card = document.createElement('article');
      card.className = 'event-card reveal is-visible';
      card.setAttribute('data-category', item.category);
      card.innerHTML = `
        <div class="event-thumb-wrap">
          <img src="${item.image}" alt="${item.title}" loading="lazy" width="600" height="340">
          <span class="event-category-badge">${item.categoryLabel}</span>
        </div>
        <div class="event-body">
          <div class="event-meta-info">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            <span>${item.date}</span>
          </div>
          <h3 class="event-title">${item.title}</h3>
          <p class="event-description">${item.excerpt}</p>
          <div class="event-card-action">
            <button type="button" class="event-view-details-btn" data-event-id="${item.id}">
              <span>Conhecer detalhes</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
          </div>
        </div>
      `;
      galleryContainer.appendChild(card);
    });

    // Add future event card placeholder for ongoing scalability
    const placeholderCard = document.createElement('div');
    placeholderCard.className = 'event-card-add-future reveal is-visible';
    placeholderCard.innerHTML = `
      <div class="future-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"></path></svg>
      </div>
      <h4 style="font-family: var(--font-serif); font-size: 1.4rem; color: var(--color-primary-dark); margin-bottom: 8px;">Novas Edições em Breve</h4>
      <p style="font-size: 0.9rem; color: var(--color-text-muted); line-height: 1.5; margin-bottom: 18px;">
        Acompanhe nossos próximos eventos, treinamentos in company para equipes de saúde e artigos em primeira mão.
      </p>
      <a href="https://www.instagram.com/arrudachudzy/" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="padding: 10px 22px; font-size: 0.86rem; color: var(--color-primary-dark); border-color: var(--color-primary);">
        Seguir no Instagram
      </a>
    `;
    galleryContainer.appendChild(placeholderCard);

    // Bind click events on detail buttons
    galleryContainer.querySelectorAll('.event-view-details-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const eventId = btn.getAttribute('data-event-id');
        openEventModal(eventId);
      });
    });
  };

  // Initial render
  renderCards('todos');

  // Filter button clicks
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const category = btn.getAttribute('data-filter');
      renderCards(category);
    });
  });
}

/**
 * Native <dialog> Modal Viewer with Mandatory Light-Dismiss Fallback
 */
function initEventModal() {
  const dialog = document.getElementById('eventDetailsModal');
  if (!dialog) return;

  const closeBtn = dialog.querySelector('.modal-close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => dialog.close());
  }

  // MANDATORY: Light-Dismiss Fallback from Modern Web Guidance
  // For browsers that do not yet support closedBy, check if click occurred outside content box
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    dialog.addEventListener('click', (event) => {
      // 1. When clicking backdrop, target is the dialog element itself
      if (event.target !== dialog) return;

      // 2. Check if click coordinates fall within dialog's content box
      const rect = dialog.getBoundingClientRect();
      const isDialogContent = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      );

      if (isDialogContent) return;

      // 3. Click was outside content area (on backdrop), close dialog
      dialog.close();
    });
  }
}

/**
 * Open and populate modal with event details
 */
function openEventModal(eventId) {
  const dialog = document.getElementById('eventDetailsModal');
  const eventItem = EVENTS_DATA.find(e => e.id === eventId);
  if (!dialog || !eventItem) return;

  const imgEl = dialog.querySelector('.modal-header-image');
  const catEl = dialog.querySelector('.modal-category-tag');
  const titleEl = dialog.querySelector('.modal-event-title');
  const dateEl = dialog.querySelector('.modal-event-date');
  const descEl = dialog.querySelector('.modal-event-desc');

  if (imgEl) imgEl.src = eventItem.image;
  if (catEl) catEl.textContent = eventItem.categoryLabel;
  if (titleEl) titleEl.textContent = eventItem.title;
  if (dateEl) dateEl.textContent = eventItem.date;
  if (descEl) descEl.textContent = eventItem.fullDescription;

  if (typeof dialog.showModal === 'function') {
    dialog.showModal();
  }
}

// Global hook for adding events dynamically in future modules
window.ArrudaEvents = {
  data: EVENTS_DATA,
  addEvent: function(item) {
    EVENTS_DATA.push(item);
    initEventsGallery();
  }
};
