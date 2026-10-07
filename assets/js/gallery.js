/**
 * ARRUDA CHUDZY ADVOGADAS - Dynamic Events & Content Gallery
 * Features:
 * - Visual Showcases for Curso 1 and Curso 2
 * - Cards sem fotos das advogadas (foco estrito no conteúdo textual e técnico)
 * - Dynamic Category Filtering
 * - Native <dialog> Modal Viewer com Light-Dismiss Fallback
 */

// Events and Training Programs Repository
const EVENTS_DATA = [
  {
    id: 'secretarias-360',
    category: 'cursos',
    categoryLabel: 'Treinamento Prático',
    title: 'Treinamento Secretárias 360º',
    date: 'Para Secretárias, Recepcionistas e Atendimento',
    image: null,
    excerpt: 'Capacitação da equipe de atendimento de clínicas e hospitais para atuar de forma estratégica, reduzindo riscos jurídicos e proporcionando uma experiência de excelência ao paciente.',
    fullDescription: 'PÚBLICO-ALVO:\nSecretárias, recepcionistas e profissionais de atendimento que atuam em clínicas e hospitais.\n\nOBJETIVO:\nCapacitar a equipe para atuar de forma estratégica, reduzindo riscos jurídicos, otimizando processos internos e proporcionando uma experiência de excelência ao paciente.\n\nSOBRE O TREINAMENTO:\nCom uma abordagem prática e completa, o treinamento desenvolve competências essenciais para uma atuação segura, organizada e eficiente, fortalecendo o papel da secretária como peça-chave para o sucesso e blindagem da clínica.'
  },
  {
    id: 'canetinhas',
    category: 'cursos',
    categoryLabel: 'Treinamento Especializado',
    title: 'Treinamento "Canetinhas" — Tratamentos Injetáveis',
    date: 'Para Médicos Prescritores',
    image: null,
    excerpt: 'Segurança jurídica e ética na prescrição de tratamentos injetáveis, com foco nas normas do CFM, elaboração de prescrições, prontuários, TCLE e comunicação.',
    fullDescription: 'PÚBLICO-ALVO:\nMédicos que prescrevem tratamentos injetáveis e desejam atuar com maior segurança jurídica e ética em sua prática profissional.\n\nOBJETIVO:\nCapacitar os profissionais para prevenir riscos jurídicos, assegurar a conformidade com as normas do CFM e fortalecer a segurança na prescrição, documentação e comunicação com os pacientes.\n\nSOBRE O TREINAMENTO:\nO treinamento apresenta as principais normas do CFM e as orientações dos CRMs aplicáveis à prescrição de tratamentos injetáveis. São abordados aspectos relacionados à adequada elaboração de prescrições, prontuários e TCLE, bem como boas práticas de comunicação com o paciente.'
  },
  {
    id: 'publicidade-medica',
    category: 'cursos',
    categoryLabel: 'Publicidade Médica',
    title: 'Curso de Ética & Publicidade Médica',
    date: 'Resolução CFM nº 2.336/2023',
    image: null,
    excerpt: 'Treinamento prático voltado à aplicação da Resolução CFM nº 2.336/2023, abordando limites e possibilidades da publicidade médica e redes sociais.',
    fullDescription: 'PÚBLICO-ALVO:\nMédicos, equipes e empresas de marketing que atuam ou prestam serviços para a área da saúde.\n\nOBJETIVO:\nCapacitar os participantes para compreender e aplicar corretamente as disposições do Código de Ética Médica e as regras de publicidade médica.\n\nSOBRE O TREINAMENTO:\nTreinamento prático voltado à interpretação e aplicação do Código de Ética Médica e da Resolução CFM nº 2.336/2023, abordando os limites e possibilidades da publicidade médica, divulgação de serviços, uso das redes sociais e comunicação com pacientes.'
  },
  {
    id: 'estatuto-paciente',
    category: 'cursos',
    categoryLabel: 'Legislação em Saúde',
    title: 'Curso Estatuto do Paciente',
    date: 'Lei Federal nº 15.378/2026',
    image: null,
    excerpt: 'Diretrizes, direitos e garantias fundamentais previstos na Lei nº 15.378/2026 para conduzir atendimentos em total conformidade jurídica.',
    fullDescription: 'PÚBLICO-ALVO:\nProfissionais da saúde que desejam fortalecer a relação com os pacientes e atuar em conformidade com as normas que regem os direitos dos pacientes.\n\nOBJETIVO:\nCapacitar os participantes para conduzir atendimentos alinhados às disposições da Lei nº 15.378/2026.\n\nSOBRE O TREINAMENTO:\nApresenta os principais direitos, garantias e diretrizes previstos no Estatuto dos Direitos do Paciente, prevenindo conflitos e estabelecendo rotinas assistenciais seguras.'
  },
  {
    id: 'ia-medicina',
    category: 'cursos',
    categoryLabel: 'Inovação & CFM',
    title: 'Treinamento Inteligência Artificial na Medicina',
    date: 'Resolução CFM nº 2.454/2026',
    image: null,
    excerpt: 'Aspectos da Resolução CFM nº 2.454/2026: limites, responsabilidades, deveres e vedações relacionados ao uso de IA na prática médica.',
    fullDescription: 'PÚBLICO-ALVO:\nMédicos e profissionais da saúde que utilizam ou pretendem utilizar ferramentas de Inteligência Artificial.\n\nOBJETIVO:\nCapacitar os participantes para utilizar recursos de Inteligência Artificial em conformidade com a Resolução CFM nº 2.454/2026.\n\nSOBRE O TREINAMENTO:\nApresenta os principais aspectos da Resolução CFM nº 2.454/2026, abordando limites, responsabilidades, deveres e vedações relacionados ao uso da Inteligência Artificial na medicina e na assistência à saúde.'
  },
  {
    id: 'telemedicina',
    category: 'cursos',
    categoryLabel: 'Telemedicina',
    title: 'Treinamento Telemedicina',
    date: 'Resolução CFM nº 2.314/2022',
    image: null,
    excerpt: 'Requisitos legais para atendimentos remotos: documentação, termos de consentimento, segurança da informação e responsabilidade médica.',
    fullDescription: 'PÚBLICO-ALVO:\nMédicos e profissionais da saúde que realizam ou pretendem realizar atendimentos por telemedicina.\n\nOBJETIVO:\nCapacitar os participantes para conduzir consultas e acompanhamentos remotos em conformidade com a Resolução CFM nº 2.314/2022, reduzindo riscos éticos e jurídicos.\n\nSOBRE O TREINAMENTO:\nAborda os principais requisitos para a prática da telemedicina, incluindo documentação, consentimento, documentos digitais e responsabilidade, proporcionando maior segurança jurídica na prestação de serviços de saúde a distância.'
  },
  {
    id: 'compliance-tcle',
    category: 'cursos',
    categoryLabel: 'Compliance & Gestão',
    title: 'Workshop de Compliance Médico e Validade do TCLE',
    date: 'Prontuários & Gestão de Riscos',
    image: null,
    excerpt: 'Elaboração e implementação prática de Termos de Consentimento (TCLE) personalizados e conformidade à LGPD na rotina de clínicas.',
    fullDescription: 'Elaboração e implementação prática do Termo de Consentimento Livre e Esclarecido (TCLE) personalizado para procedimentos invasivos e cirúrgicos. Aborda as teses do STJ sobre suficiência de informação e estruturação de prontuários médicos seguros.'
  },
  {
    id: 'sindicancias-crm',
    category: 'cursos',
    categoryLabel: 'Defesa Ética',
    title: 'Assessoria em Sindicâncias e Processos Éticos no CRM',
    date: 'Conselhos Profissionais & CFM',
    image: null,
    excerpt: 'Atuação estratégica em sindicâncias e processos ético-disciplinares em conselhos de classe da medicina e áreas afins.',
    fullDescription: 'Acompanhamento rigoroso em todas as fases de sindicâncias e Processos Ético-Profissionais (PEP) perante o CRM e CFM. Defesas preliminares, oitivas e recursos com total confidencialidade e técnica jurídica apurada.'
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

      // Render image if present (Course 1 or Course 2), otherwise render clean text header (no lawyer photos)
      const visualHeader = item.image
        ? `
          <div class="event-thumb-wrap">
            <img src="${item.image}" alt="${item.title}" loading="lazy" width="600" height="340">
            <span class="event-category-badge">${item.categoryLabel}</span>
          </div>
        `
        : `
          <div class="event-card-header-clean">
            <span class="event-category-badge static">${item.categoryLabel}</span>
          </div>
        `;

      card.innerHTML = `
        ${visualHeader}
        <div class="event-body">
          <div class="event-meta-info">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            <span>${item.date}</span>
          </div>
          <h3 class="event-title">${item.title}</h3>
          <p class="event-description">${item.excerpt}</p>
          <div class="event-card-action">
            <button type="button" class="event-view-details-btn" data-event-id="${item.id}">
              <span>Ver detalhes do treinamento</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
          </div>
        </div>
      `;
      galleryContainer.appendChild(card);
    });

    // Add in-company consultation card
    const placeholderCard = document.createElement('div');
    placeholderCard.className = 'event-card-add-future reveal is-visible';
    placeholderCard.innerHTML = `
      <div class="future-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
      </div>
      <h4 style="font-family: var(--font-serif); font-size: 1.4rem; color: var(--color-primary-dark); margin-bottom: 8px;">Treinamento In Company</h4>
      <p style="font-size: 0.9rem; color: var(--color-text-muted); line-height: 1.5; margin-bottom: 18px;">
        Capacitações personalizadas e exclusivas para o corpo clínico e equipe de sua clínica, hospital ou empresa de saúde.
      </p>
      <a href="https://wa.me/5549999370099?text=Ol%C3%A1!%20Gostaria%20de%20solicitar%20um%20treinamento%20in%20company%20para%20minha%20cl%C3%ADnica." target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="padding: 10px 22px; font-size: 0.86rem; background: var(--color-primary); color: #fff;">
        Solicitar Proposta
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

  // Light-Dismiss Fallback
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    dialog.addEventListener('click', (event) => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      const isDialogContent = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      );
      if (isDialogContent) return;
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

  if (imgEl) {
    if (eventItem.image) {
      imgEl.src = eventItem.image;
      imgEl.style.display = 'block';
    } else {
      imgEl.style.display = 'none';
    }
  }

  if (catEl) catEl.textContent = eventItem.categoryLabel;
  if (titleEl) titleEl.textContent = eventItem.title;
  if (dateEl) dateEl.textContent = eventItem.date;
  if (descEl) {
    // Preserve linebreaks
    descEl.innerText = eventItem.fullDescription;
  }

  if (typeof dialog.showModal === 'function') {
    dialog.showModal();
  }
}

// Global modal trigger for Curso 1 and Curso 2 image viewing
window.openCourseViewer = function(courseNumber) {
  const dialog = document.getElementById('eventDetailsModal');
  if (!dialog) return;

  const imgEl = dialog.querySelector('.modal-header-image');
  const catEl = dialog.querySelector('.modal-category-tag');
  const titleEl = dialog.querySelector('.modal-event-title');
  const dateEl = dialog.querySelector('.modal-event-date');
  const descEl = dialog.querySelector('.modal-event-desc');

  if (courseNumber === 1) {
    if (imgEl) {
      imgEl.src = 'assets/images/curso-1.jpg';
      imgEl.style.display = 'block';
    }
    if (catEl) catEl.textContent = 'Cursos & Treinamentos';
    if (titleEl) titleEl.textContent = 'Cursos & Treinamentos (Direito Médico e da Saúde) — Módulo I';
    if (dateEl) dateEl.textContent = 'Secretárias 360º • Treinamento "Canetinhas" • Ética & Publicidade Médica';
    if (descEl) descEl.innerText = 'Programa de capacitação prática contemplando:\n\n1. Treinamento Secretárias 360º: Preparação completa da equipe de atendimento para redução de riscos jurídicos.\n2. Treinamento "Canetinhas": Prescrição de tratamentos injetáveis com segurança ética e conformidade às resoluções do CFM.\n3. Curso de Ética & Publicidade Médica: Aplicação prática da Resolução CFM nº 2.336/2023 para médicos e equipes de marketing.';
  } else {
    if (imgEl) {
      imgEl.src = 'assets/images/curso-2.jpg';
      imgEl.style.display = 'block';
    }
    if (catEl) catEl.textContent = 'Cursos & Treinamentos';
    if (titleEl) titleEl.textContent = 'Cursos & Treinamentos (Direito Médico e da Saúde) — Módulo II';
    if (dateEl) dateEl.textContent = 'Estatuto do Paciente • Inteligência Artificial • Telemedicina';
    if (descEl) descEl.innerText = 'Programa de capacitação contemporâneo contemplando:\n\n1. Curso Estatuto do Paciente: Alinhamento às disposições da Lei Federal nº 15.378/2026.\n2. Treinamento Inteligência Artificial: Diretrizes da Resolução CFM nº 2.454/2026 para uso de IA na medicina.\n3. Treinamento Telemedicina: Requisitos da Resolução CFM nº 2.314/2022 para consultas a distância com total segurança jurídica.';
  }

  if (typeof dialog.showModal === 'function') {
    dialog.showModal();
  }
};
