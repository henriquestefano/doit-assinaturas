// Email Signature Manager - Módulo Gerador de Assinatura
// Responsável por gerar o HTML da assinatura de e-mail com estilos inline

/**
 * Formata um número de telefone para uso na URL da API do WhatsApp.
 */
function formatPhoneForWhatsApp(phone) {
  if (phone.startsWith('+')) {
    // Número com código de país explícito: remover '+' e não-numéricos
    const digits = phone.slice(1).replace(/\D/g, '');
    return `%2B${digits}`;
  }
  // Número sem código de país: assumir Brasil (+55)
  const digits = phone.replace(/\D/g, '');
  return `%2B55${digits}`;
}

/**
 * Escapa caracteres especiais de HTML para prevenir XSS e quebra de estrutura.
 *
 * @param {string} str - String bruta do usuário
 * @returns {string} String segura para inserção em HTML
 */
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * Gera o HTML completo da assinatura de e-mail com estilos inline.
 */
function generateSignature(data) {
  const { name, role, photoUrl, email, phone, instagram, website } = data;

  // Construir conteúdo da coluna esquerda (foto, nome, cargo)
  let leftColumnContent = '';

  if (photoUrl) {
    const altText = name ? escapeHtml(name) : 'Foto';
    leftColumnContent += `<img src="${escapeHtml(photoUrl)}" alt="${altText}" style="width: 200px; display: block;" />`;
  }

  if (name) {
    leftColumnContent += `<p style="margin: 5px 0 0 0; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size: 14px;">${escapeHtml(name)}</p>`;
  }

  if (role) {
    leftColumnContent += `<p style="margin: 2px 0 0 0; font-family: Arial, Helvetica, sans-serif; font-size: 12px;">${escapeHtml(role)}</p>`;
  }

  // Construir conteúdo da coluna direita (links de contato)
  const contactStyle = 'margin: 1px; font-size: 12px; font-family: Arial, Helvetica, sans-serif; line-height: 18px;';
  const linkStyle = 'color: black; text-decoration: none';
  let rightColumnContent = '';

  if (instagram) {
    rightColumnContent += `<div style="${contactStyle}"><a href="https://www.instagram.com/${instagram}/" target="_blank" style="${linkStyle}">${escapeHtml(instagram)}</a></div>`;
  }

  if (phone) {
    const encodedPhone = formatPhoneForWhatsApp(phone);
    rightColumnContent += `<div style="${contactStyle}"><a href="https://api.whatsapp.com/send/?phone=${encodedPhone}" target="_blank" style="${linkStyle}">${escapeHtml(phone)}</a></div>`;
  }

  if (email) {
    rightColumnContent += `<div style="${contactStyle}"><a href="mailto:${escapeHtml(email)}" target="_blank" style="${linkStyle}">${escapeHtml(email)}</a></div>`;
  }

  if (website) {
    rightColumnContent += `<div style="${contactStyle}"><a href="https://${website}/" target="_blank" style="${linkStyle}">${escapeHtml(website)}</a></div>`;
  }

  // Montar a tabela completa
  const html = `<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td style="width: 225px; vertical-align: top; padding: 10px;">${leftColumnContent}</td><td style="vertical-align: top; padding-top: 20px;">${rightColumnContent}</td></tr></tbody></table>`;

  return html;
}
