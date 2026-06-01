// Email Signature Manager - App Logic
// Controlador principal: eventos, validação, atualização de UI

// ============================================================
// Constantes de região
// ============================================================

const REGION_DEFAULTS = {
  brasil: { instagram: 'doitsistema', website: 'www.doit.com.br' },
  usa: { instagram: 'doit.systems', website: 'www.doiterp.com' }
};

// ============================================================
// Funções de validação
// ============================================================

/**
 * Validates email format: must contain @ with text before and after, and a . after @
 * @param {string} email
 * @returns {boolean}
 */
function validateEmail(email) {
  if (!email) return true; // empty is valid (optional field)
  const atIndex = email.indexOf('@');
  if (atIndex < 1) return false; // must have text before @
  const afterAt = email.slice(atIndex + 1);
  if (!afterAt || afterAt.length === 0) return false; // must have text after @
  const dotIndex = afterAt.indexOf('.');
  if (dotIndex < 1) return false; // must have a . after @ with text before it
  if (dotIndex === afterAt.length - 1) return false; // must have text after the .
  return true;
}

/**
 * Validates phone: only digits, parentheses, spaces, hyphens, and optionally + at start
 * @param {string} phone
 * @returns {boolean}
 */
function validatePhone(phone) {
  if (!phone) return true; // empty is valid (optional field)
  // Optional + at start, then only digits, parentheses, spaces, hyphens
  const pattern = /^\+?[\d()\s-]+$/;
  return pattern.test(phone);
}

/**
 * Validates photo URL: must start with "https://"
 * @param {string} url
 * @returns {boolean}
 */
function validatePhotoUrl(url) {
  if (!url) return true; // empty is valid (optional field)
  return url.startsWith('https://');
}

// ============================================================
// Lógica de região
// ============================================================

/**
 * Updates instagram and website fields with region defaults, then triggers preview update.
 * @param {string} region - 'brasil' or 'usa'
 */
function handleRegionChange(region) {
  const defaults = REGION_DEFAULTS[region];
  if (!defaults) return;

  const instagramInput = document.getElementById('instagram');
  const websiteInput = document.getElementById('website');

  if (instagramInput) instagramInput.value = defaults.instagram;
  if (websiteInput) websiteInput.value = defaults.website;

  handleFormInput();
}

// ============================================================
// Atualização do preview e validação
// ============================================================

/**
 * Collects form values, generates signature, updates preview and code output,
 * and runs field validation with visual feedback.
 */
function handleFormInput() {
  // Collect form values
  const data = {
    name: document.getElementById('name').value.trim(),
    role: document.getElementById('role').value.trim(),
    photoUrl: document.getElementById('photoUrl').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    instagram: document.getElementById('instagram').value.trim(),
    website: document.getElementById('website').value.trim()
  };

  // Generate signature HTML
  const html = generateSignature(data);

  // Update preview (rendered HTML)
  const preview = document.getElementById('preview');
  if (preview) {
    const hasData = data.name || data.role || data.photoUrl || data.email || data.phone || data.instagram || data.website;
    if (hasData) {
      preview.innerHTML = html;
    } else {
      preview.innerHTML = '<p style="color: #9ca3af; text-align: center; margin: 40px 0;">Preencha os campos para visualizar a assinatura</p>';
    }
  }

  // Update code output (as text)
  const codeOutput = document.getElementById('code-output');
  if (codeOutput) codeOutput.textContent = html;

  // Run validation
  validateAndShowErrors(data);
}

/**
 * Validates fields and shows/hides error messages with appropriate CSS classes.
 * @param {Object} data - The collected form data
 */
function validateAndShowErrors(data) {
  // Email validation
  const emailInput = document.getElementById('email');
  const emailError = document.getElementById('email-error');
  if (emailInput && emailError) {
    if (data.email && !validateEmail(data.email)) {
      emailError.textContent = 'Formato de e-mail inválido';
      emailInput.classList.add('invalid');
      emailInput.classList.remove('valid');
    } else {
      emailError.textContent = '';
      emailInput.classList.remove('invalid');
      if (data.email) {
        emailInput.classList.add('valid');
      } else {
        emailInput.classList.remove('valid');
      }
    }
  }

  // Phone validation
  const phoneInput = document.getElementById('phone');
  const phoneError = document.getElementById('phone-error');
  if (phoneInput && phoneError) {
    if (data.phone && !validatePhone(data.phone)) {
      phoneError.textContent = 'Telefone contém caracteres inválidos';
      phoneInput.classList.add('invalid');
      phoneInput.classList.remove('valid');
    } else {
      phoneError.textContent = '';
      phoneInput.classList.remove('invalid');
      if (data.phone) {
        phoneInput.classList.add('valid');
      } else {
        phoneInput.classList.remove('valid');
      }
    }
  }

  // Photo URL validation
  const photoInput = document.getElementById('photoUrl');
  const photoError = document.getElementById('photoUrl-error');
  if (photoInput && photoError) {
    if (data.photoUrl && !validatePhotoUrl(data.photoUrl)) {
      photoError.textContent = 'URL deve iniciar com https://';
      photoInput.classList.add('invalid');
      photoInput.classList.remove('valid');
    } else {
      photoError.textContent = '';
      photoInput.classList.remove('invalid');
      if (data.photoUrl) {
        photoInput.classList.add('valid');
      } else {
        photoInput.classList.remove('valid');
      }
    }
  }
}

// ============================================================
// Cópia para clipboard
// ============================================================

/**
 * Copies the generated HTML code to clipboard with fallback for older browsers.
 * Shows visual feedback on success.
 */
async function copyToClipboard() {
  const codeOutput = document.getElementById('code-output');
  if (!codeOutput) return;

  const text = codeOutput.textContent;

  try {
    // Try modern clipboard API first
    await navigator.clipboard.writeText(text);
    showCopyFeedback();
  } catch {
    // Fallback: create temporary textarea
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();

    try {
      document.execCommand('copy');
      showCopyFeedback();
    } catch {
      // Keep text selected for manual copy
      textarea.style.position = 'static';
      textarea.style.opacity = '1';
      textarea.focus();
      textarea.select();
      return; // Don't remove textarea so user can copy manually
    }

    document.body.removeChild(textarea);
  }
}

/**
 * Shows the copy feedback message temporarily.
 */
function showCopyFeedback() {
  const feedback = document.getElementById('copy-feedback');
  if (!feedback) return;

  feedback.removeAttribute('hidden');
  setTimeout(() => {
    feedback.setAttribute('hidden', '');
  }, 2000);
}

// ============================================================
// Inicialização
// ============================================================

/**
 * Initializes the application: registers event listeners and sets initial state.
 */
function init() {
  // Register 'input' event listeners on all text/email/tel inputs
  const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"]');
  inputs.forEach(input => {
    input.addEventListener('input', handleFormInput);
  });

  // Register 'change' event listener on region select
  const regionSelect = document.getElementById('region');
  if (regionSelect) {
    regionSelect.addEventListener('change', (e) => {
      handleRegionChange(e.target.value);
    });
  }

  // Register 'click' event listener on copy button
  const copyBtn = document.getElementById('copy-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', copyToClipboard);
  }

  // Pre-fill fields with initial region value
  const initialRegion = regionSelect ? regionSelect.value : 'brasil';
  handleRegionChange(initialRegion);

  // Generate initial state (handleRegionChange already calls handleFormInput)
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', init);
