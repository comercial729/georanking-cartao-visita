/* ============================================================
 * GeoRanking API — Adaptador da Presença Digital
 * ------------------------------------------------------------
 * Contrato REAL levantado do backend (Spring Boot, app.jar) em 23/07/2026:
 *   Base:    https://api.georanking.com.br/api/v1
 *   Auth:    POST /auth  (login; o front usa Bearer token)
 *   Perfil:  GET  /business-profiles/{businessProfileId}/details
 *            -> ResponseDTO { data: BusinessProfileResponse }
 *            campos: publicId, name, description, website, whatsappNumber,
 *                    email, facebookUrl, instagramUrl, linkedinUrl, address,
 *                    categories[], keywords[], hours{}, serviceOptions, latLong
 *            (mainPhone existe no UpdateContactDataRequest — confirmar se o
 *             details expõe; o adapter tenta mainPhone e phoneNumber)
 *   Updates: PUT/PATCH /business-profiles/{id}/... (contactData, location,
 *            schedule, description, extras, categories, changeTracking)
 *   Reviews: GET /reviews/profile/{businessProfileId}
 *
 * USO (teste local — NADA disso toca produção em escrita):
 *   GeoAPI.config({ profileId:'...', token:'...' });
 *   const perfil = await GeoAPI.carregarPerfil();  // modelo da Presença
 *   -> se a API falhar (sem token, CORS, offline), cai no MOCK (CSA)
 *      e o resultado vem com fonte:'mock' para a UI sinalizar.
 * ============================================================ */
(function (global) {
  const LS_KEY = 'geo_api_cfg';

  const state = {
    baseUrl: 'https://api.georanking.com.br/api/v1',
    token: null,
    profileId: null,
  };

  // carrega config persistida (localStorage) e via querystring (?profileId=&token=&apiBase=)
  try {
    const saved = JSON.parse(localStorage.getItem(LS_KEY) || '{}');
    Object.assign(state, saved);
    const q = new URLSearchParams(location.search);
    if (q.get('apiBase')) state.baseUrl = q.get('apiBase');
    if (q.get('profileId')) state.profileId = q.get('profileId');
    if (q.get('token')) state.token = q.get('token');
  } catch (e) { /* ambiente sem localStorage */ }

  function config(opts) {
    Object.assign(state, opts || {});
    try { localStorage.setItem(LS_KEY, JSON.stringify({ baseUrl: state.baseUrl, token: state.token, profileId: state.profileId })); } catch (e) {}
    return { ...state, token: state.token ? '***' : null };
  }

  // ---- MOCK (fallback para desenvolvimento sem API) ----
  const MOCK = {
    fonte: 'mock',
    profileId: 'mock-csa',
    nome: 'CSA Casa da Segurança Eletrônica',
    iniciais: 'CSA',
    categoria: 'Segurança Eletrônica',
    descricao: 'Instalação e monitoramento de câmeras, alarmes e cerca elétrica para residências e empresas em Rio Verde.',
    telefone: '(64) 3620-1090',
    whatsapp: '(64) 99226-1090',
    email: 'contato@csaseguranca.com.br',
    site: 'www.csaseguranca.com.br',
    endereco: 'Rua 16, 81A — Rio Verde, GO',
    cidade: 'Rio Verde, GO',
    redes: { instagram: '@csaseguranca', facebook: '/csaseguranca', linkedin: null },
    horarios: {},
    keywords: [],
    latLong: null,
  };

  function iniciaisDe(nome) {
    if (!nome) return '?';
    const sig = (nome.match(/\b[A-ZÀ-Ú]{2,}\b/g) || []).find(w => w.length <= 4);
    if (sig) return sig; // sigla explícita no nome (ex.: CSA)
    return nome.split(/\s+/).filter(w => w.length > 2).slice(0, 2).map(w => w[0].toUpperCase()).join('');
  }

  function cidadeDe(address) {
    if (!address) return '';
    // address vem como string "Rua X, N - Bairro, Cidade - UF" (ou objeto; tenta os dois)
    if (typeof address === 'object') {
      const c = address.city || address.locality || '';
      const uf = address.state || address.administrativeArea || '';
      return c ? (uf ? c + ', ' + uf : c) : '';
    }
    const parts = String(address).split(',').map(s => s.trim());
    return parts.length >= 2 ? parts.slice(-2).join(', ').replace(/\s*-\s*/g, ', ') : String(address);
  }

  // mapeia BusinessProfileResponse -> modelo da Presença Digital
  function mapearPerfil(d) {
    const cat = Array.isArray(d.categories) && d.categories.length
      ? (typeof d.categories[0] === 'string' ? d.categories[0] : (d.categories[0].name || d.categories[0].displayName || ''))
      : '';
    return {
      fonte: 'api',
      profileId: d.publicId || state.profileId,
      nome: d.name || '',
      iniciais: iniciaisDe(d.name),
      categoria: cat,
      descricao: d.description || '',
      telefone: d.mainPhone || d.phoneNumber || d.phone || '',
      whatsapp: d.whatsappNumber || '',
      email: d.email || (d.customer && d.customer.email) || '',
      site: d.website || '',
      endereco: typeof d.address === 'string' ? d.address : (d.address ? [d.address.street, d.address.city].filter(Boolean).join(' — ') : ''),
      cidade: cidadeDe(d.address),
      redes: { instagram: d.instagramUrl || null, facebook: d.facebookUrl || null, linkedin: d.linkedinUrl || null },
      horarios: d.hours || {},
      keywords: d.keywords || [],
      latLong: d.latLong || null,
      _raw: d,
    };
  }

  async function chamar(path) {
    const headers = { 'Accept': 'application/json' };
    if (state.token) headers['Authorization'] = 'Bearer ' + state.token;
    const r = await fetch(state.baseUrl + path, { headers });
    if (!r.ok) throw new Error('HTTP ' + r.status + ' em ' + path);
    const j = await r.json();
    return j && j.data !== undefined ? j.data : j; // ResponseDTO { data } ou payload direto
  }

  async function carregarPerfil() {
    if (!state.profileId) return { ...MOCK, _motivo: 'profileId não configurado' };
    try {
      const d = await chamar('/business-profiles/' + encodeURIComponent(state.profileId) + '/details');
      return mapearPerfil(d);
    } catch (e) {
      return { ...MOCK, _motivo: 'falha na API: ' + e.message + ' (CORS? token? offline?)' };
    }
  }

  async function carregarReviews() {
    if (!state.profileId) return { fonte: 'mock', reviews: [], _motivo: 'profileId não configurado' };
    try {
      const d = await chamar('/reviews/profile/' + encodeURIComponent(state.profileId));
      return { fonte: 'api', reviews: Array.isArray(d) ? d : (d.reviews || d.content || []), _raw: d };
    } catch (e) {
      return { fonte: 'mock', reviews: [], _motivo: 'falha na API: ' + e.message };
    }
  }

  global.GeoAPI = { config, carregarPerfil, carregarReviews, _state: () => ({ ...state, token: state.token ? '***' : null }), MOCK };
})(window);
