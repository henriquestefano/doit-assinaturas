import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
import re

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Gerador de Assinatura - DOit",
    page_icon="✉️",
    layout="wide",
)

# ========== CONSTANTS ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "assinaturas", "Imagens")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

TEMPLATE_BR_PATH = os.path.join(TEMPLATES_DIR, "Template Assinatura BR.png")
TEMPLATE_USA_PATH = os.path.join(TEMPLATES_DIR, "Template Assinatura USA.png")

# Canvas size (template images are 1200x600)
CANVAS_W = 1200
CANVAS_H = 600

# Positions in 1200x600 scale (400x200 * 3)
MEMOJI_X = 164       # 54.5 * 3
MEMOJI_Y = 99        # 32.9 * 3
MEMOJI_SIZE = 304    # 101.2 * 3

NAME_X = 612         # 203.8 * 3
NAME_Y = 120         # ajustado para baixo
NAME_FONT_SIZE = 54
NAME_COLOR = "#000000"

ROLE_X = 612         # 203.8 * 3
ROLE_Y = 185         # ajustado para baixo
ROLE_FONT_SIZE = 36
ROLE_COLOR = "#333333"

REGION_DEFAULTS = {
    "Brasil": {
        "instagram": "doitsistema",
        "website": "www.doit.com.br",
        "template": TEMPLATE_BR_PATH,
    },
    "USA": {
        "instagram": "doit.systems",
        "website": "www.doiterp.com",
        "template": TEMPLATE_USA_PATH,
    },
}


# ========== FONT LOADING ==========
def load_font(font_name: str, size: int):
    """Try to load a font from the fonts directory, fallback to default."""
    font_paths = {
        "league_spartan_bold": [
            os.path.join(FONTS_DIR, "LeagueSpartan-Bold.ttf"),
            os.path.join(FONTS_DIR, "LeagueSpartan-Bold.otf"),
        ],
        "open_sans": [
            os.path.join(FONTS_DIR, "OpenSans-Regular.ttf"),
            os.path.join(FONTS_DIR, "OpenSans-Regular.otf"),
        ],
    }

    paths = font_paths.get(font_name, [])
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (IOError, OSError):
                continue

    # Fallback: try common system font paths
    system_fallbacks = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]

    for fallback in system_fallbacks:
        if os.path.exists(fallback):
            try:
                return ImageFont.truetype(fallback, size)
            except (IOError, OSError):
                continue

    # Last resort: Pillow default with size
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except (IOError, OSError):
        return ImageFont.load_default()


# ========== IMAGE GENERATION ==========
def generate_signature_image(
    template_path: str,
    memoji_file,
    name: str,
    role: str,
):
    """Generate the composite signature image."""
    if not os.path.exists(template_path):
        st.error(f"Template não encontrado: {template_path}")
        return None

    # Load template
    template = Image.open(template_path).convert("RGBA")

    # Create composite on top of template
    composite = template.copy()

    # Draw memoji if provided
    if memoji_file is not None:
        memoji = Image.open(memoji_file).convert("RGBA")
        memoji = memoji.resize((MEMOJI_SIZE, MEMOJI_SIZE), Image.LANCZOS)

        # Create circular mask
        mask = Image.new("L", (MEMOJI_SIZE, MEMOJI_SIZE), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, MEMOJI_SIZE - 1, MEMOJI_SIZE - 1], fill=255)

        # Paste memoji with circular mask
        composite.paste(memoji, (MEMOJI_X, MEMOJI_Y), mask)

    # Draw text
    draw = ImageDraw.Draw(composite)

    if name:
        name_font = load_font("league_spartan_bold", NAME_FONT_SIZE)
        draw.text((NAME_X, NAME_Y), name, fill=NAME_COLOR, font=name_font)

    if role:
        role_font = load_font("open_sans", ROLE_FONT_SIZE)
        draw.text((ROLE_X, ROLE_Y), role, fill=ROLE_COLOR, font=role_font)

    return composite


# ========== PHONE ENCODING ==========
def encode_phone(phone: str) -> str:
    """Encode phone number for WhatsApp link."""
    if not phone:
        return ""
    if phone.startswith("+"):
        digits = re.sub(r"\D", "", phone[1:])
        return f"%2B{digits}"
    else:
        digits = re.sub(r"\D", "", phone)
        return f"%2B55{digits}"


# ========== HTML GENERATION ==========
def generate_html(
    image_base64: str,
    instagram: str,
    phone: str,
    email: str,
    website: str,
) -> str:
    """Generate the signature HTML code."""
    image_url = f"data:image/png;base64,{image_base64}"

    link_style = "color: black; text-decoration: none;"
    div_style = "margin: 1px; font-size: 12px; font-family: Arial, Helvetica, sans-serif; line-height: 18px;"

    links = ""
    if instagram:
        links += f'<div style="{div_style}"><a href="https://www.instagram.com/{instagram}/" target="_blank" style="{link_style}">{instagram}</a></div>\n      '
    if phone:
        phone_encoded = encode_phone(phone)
        links += f'<div style="{div_style}"><a href="https://api.whatsapp.com/send/?phone={phone_encoded}" target="_blank" style="{link_style}">{phone}</a></div>\n      '
    if email:
        links += f'<div style="{div_style}"><a href="mailto:{email}" target="_blank" style="{link_style}">{email}</a></div>\n      '
    if website:
        links += f'<div style="{div_style}"><a href="https://{website}/" target="_blank" style="{link_style}">{website}</a></div>\n      '

    html = f"""<table border="0" cellpadding="0" cellspacing="0" style="background: url('{image_url}') no-repeat top / 100% auto; font-size: 15px; font-family: 'Open Sauce', sans-serif; height: 200px; padding: 10px 20px 40px 225px; table-layout: fixed; width: 400px;">
  <tbody>
    <tr><td style="padding-top: 35px;"><div style="margin: -25px 0 0 0;"></div></td></tr>
    <tr><td height="0" style="padding-top: 24px;">
      {links.strip()}
    </td></tr>
  </tbody>
</table>"""

    return html


# ========== IMAGE TO BASE64 ==========
def image_to_base64(img: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


# ========== STREAMLIT UI ==========
def main():
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e5e7eb;
            margin-bottom: 1.5rem;
        }
        .main-header h1 {
            font-size: 1.8rem;
            margin-bottom: 0.2rem;
        }
        .main-header p {
            color: #6b7280;
            font-size: 0.95rem;
        }
        </style>
        <div class="main-header">
            <h1>✉️ Gerador de Assinatura de E-mail</h1>
            <p>DOit — Crie sua assinatura profissional</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Layout: sidebar for inputs, main area for preview
    col_form, col_preview = st.columns([1, 2])

    with col_form:
        st.subheader("Dados da Assinatura")

        # Region selection
        region = st.radio(
            "Região",
            options=["Brasil", "USA"],
            horizontal=True,
            index=0,
        )

        defaults = REGION_DEFAULTS[region]

        # Memoji upload
        memoji_file = st.file_uploader(
            "Memoji (PNG com fundo transparente)",
            type=["png", "jpg", "jpeg", "webp"],
            help="Arraste ou selecione a imagem do memoji",
        )

        # Form fields
        nome = st.text_input("Nome", placeholder="Nome completo")
        cargo = st.text_input("Cargo", placeholder="Cargo / Função")
        email = st.text_input("E-mail", placeholder="email@doit.com.br")
        telefone = st.text_input("Telefone", placeholder="(11) 91305-2222")

        # Instagram and Website with region defaults
        if f"instagram_{region}" not in st.session_state:
            st.session_state[f"instagram_{region}"] = defaults["instagram"]
        if f"website_{region}" not in st.session_state:
            st.session_state[f"website_{region}"] = defaults["website"]

        instagram = st.text_input(
            "Instagram",
            value=st.session_state[f"instagram_{region}"],
            key=f"ig_input_{region}",
        )
        website = st.text_input(
            "Website",
            value=st.session_state[f"website_{region}"],
            key=f"web_input_{region}",
        )

        # Update session state
        st.session_state[f"instagram_{region}"] = instagram
        st.session_state[f"website_{region}"] = website

    with col_preview:
        st.subheader("Preview da Assinatura")

        has_data = any([nome, cargo, email, telefone, instagram, website, memoji_file])

        if has_data:
            # Generate composite image
            signature_img = generate_signature_image(
                template_path=defaults["template"],
                memoji_file=memoji_file,
                name=nome,
                role=cargo,
            )

            if signature_img:
                # Show preview image
                st.image(signature_img, caption="Imagem da assinatura", use_container_width=True)

                # Generate base64 and HTML
                img_b64 = image_to_base64(signature_img)
                html_code = generate_html(
                    image_base64=img_b64,
                    instagram=instagram,
                    phone=telefone,
                    email=email,
                    website=website,
                )

                # Show rendered HTML preview
                st.markdown("---")
                st.markdown("**Preview renderizado (como aparece no e-mail):**")
                st.components.v1.html(html_code, height=230, scrolling=False)

                # HTML code section
                st.markdown("---")
                st.subheader("Código HTML")
                st.code(html_code, language="html")

                # Copy button info
                st.info(
                    "💡 **Para copiar:** Selecione o código acima e copie (Ctrl+C / Cmd+C), "
                    "ou use o botão de copiar no canto superior direito do bloco de código. "
                    "Cole nas configurações de assinatura do seu cliente de e-mail."
                )

                # Download image option
                img_buffer = io.BytesIO()
                signature_img.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                st.download_button(
                    label="⬇️ Baixar imagem da assinatura",
                    data=img_buffer,
                    file_name=f"assinatura_{nome or 'doit'}.png",
                    mime="image/png",
                )
        else:
            st.markdown(
                '<p style="color: #aaa; text-align: center; margin: 60px 0;">'
                "Preencha os campos ao lado para gerar a assinatura</p>",
                unsafe_allow_html=True,
            )

    # Footer with font instructions
    st.markdown("---")
    with st.expander("ℹ️ Sobre as fontes"):
        st.markdown(
            f"""
            Para melhor resultado visual, adicione os arquivos de fonte na pasta `fonts/`:

            - **League Spartan Bold** → `fonts/LeagueSpartan-Bold.ttf`
            - **Open Sans Regular** → `fonts/OpenSans-Regular.ttf`

            Você pode baixá-las do [Google Fonts](https://fonts.google.com/).

            Caminho esperado: `{FONTS_DIR}`

            Se as fontes não estiverem disponíveis, o app usará fontes do sistema como fallback.
            """
        )


if __name__ == "__main__":
    main()
