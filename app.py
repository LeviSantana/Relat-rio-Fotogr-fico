import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from PIL import Image as PILImage
import io
from datetime import datetime

st.set_page_config(page_title="Relatório Fotográfico",
                   page_icon="📸", layout="wide")

st.title("📸 Gerador de Relatório Fotográfico")
st.markdown("Preencha as informações abaixo, adicione as fotos e gere o PDF.")

# ─── DADOS DO RELATÓRIO ───────────────────────────────────────────────────────
st.header("📋 Dados do Relatório")

col1, col2 = st.columns(2)
with col1:
    empresa = st.text_input("Nome da Empresa / Responsável",
                            placeholder="Ex: Construtora ABC Ltda")
    responsavel = st.text_input(
        "Responsável Técnico", placeholder="Ex: João Silva")
    obra = st.text_input("Nome da Obra / Serviço",
                         placeholder="Ex: Reforma Fachada - Bloco A")

with col2:
    contrato = st.text_input("OM", placeholder="Ex: OM-2026000000")
    local = st.text_input("Local / Endereço",
                          placeholder="Ex: Rua das Flores, 123 - São Paulo/SP")
    data_relatorio = st.date_input("Data do Relatório", value=datetime.today())

observacoes_gerais = st.text_area("Observações Gerais (opcional)",
                                  placeholder="Descreva informações gerais sobre o serviço executado...")

st.divider()

# ─── UPLOAD DE FOTOS ──────────────────────────────────────────────────────────
st.header("🖼️ Fotos")

uploaded_files = st.file_uploader(
    "Faça o upload das fotos (até 30 imagens)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} foto(s) carregada(s).")

    st.subheader("Adicione legendas para cada foto:")
    legendas = []

    cols_per_row = 2
    for i in range(0, len(uploaded_files), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(uploaded_files):
                with col:
                    st.image(uploaded_files[idx], use_container_width=True)
                    legenda = st.text_input(
                        f"Legenda da foto {idx + 1}",
                        placeholder=f"Descreva o que mostra a foto {idx + 1}",
                        key=f"legenda_{idx}"
                    )
                    legendas.append(legenda)

    st.divider()

    # ─── GERAR PDF ────────────────────────────────────────────────────────────
    if st.button("📄 Gerar Relatório PDF", type="primary", use_container_width=True):

        if not empresa:
            st.error("Por favor, preencha o nome da empresa/responsável.")
        elif not obra:
            st.error("Por favor, preencha o nome da obra/serviço.")
        else:
            with st.spinner("Gerando PDF..."):

                buffer = io.BytesIO()
                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=A4,
                    rightMargin=2*cm,
                    leftMargin=2*cm,
                    topMargin=2*cm,
                    bottomMargin=2*cm
                )

                styles = getSampleStyleSheet()
                story = []

                # Estilos personalizados
                style_title = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Title'],
                    fontSize=18,
                    textColor=colors.HexColor('#1a1a2e'),
                    spaceAfter=6,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold'
                )
                style_subtitle = ParagraphStyle(
                    'CustomSubtitle',
                    parent=styles['Normal'],
                    fontSize=11,
                    textColor=colors.HexColor('#16213e'),
                    spaceAfter=4,
                    alignment=TA_CENTER,
                    fontName='Helvetica'
                )
                style_section = ParagraphStyle(
                    'SectionHeader',
                    parent=styles['Heading2'],
                    fontSize=12,
                    textColor=colors.white,
                    backColor=colors.HexColor('#1a1a2e'),
                    spaceBefore=12,
                    spaceAfter=8,
                    leftIndent=6,
                    fontName='Helvetica-Bold'
                )
                style_label = ParagraphStyle(
                    'Label',
                    parent=styles['Normal'],
                    fontSize=9,
                    textColor=colors.HexColor('#555555'),
                    fontName='Helvetica-Bold'
                )
                style_value = ParagraphStyle(
                    'Value',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.HexColor('#1a1a2e'),
                    fontName='Helvetica'
                )
                style_caption = ParagraphStyle(
                    'Caption',
                    parent=styles['Normal'],
                    fontSize=9,
                    textColor=colors.HexColor('#333333'),
                    alignment=TA_CENTER,
                    fontName='Helvetica-Oblique',
                    spaceAfter=10
                )
                style_obs = ParagraphStyle(
                    'Obs',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.HexColor('#333333'),
                    fontName='Helvetica',
                    leading=14
                )

                # ── CABEÇALHO ─────────────────────────────────────────────────
                story.append(Spacer(1, 0.3*cm))
                story.append(Paragraph("RELATÓRIO FOTOGRÁFICO", style_title))
                story.append(
                    Paragraph("Evidências de Execução de Serviços", style_subtitle))
                story.append(HRFlowable(width="100%", thickness=2,
                             color=colors.HexColor('#1a1a2e'), spaceAfter=12))

                # ── DADOS DO RELATÓRIO ─────────────────────────────────────────
                story.append(Paragraph("  DADOS DO RELATÓRIO", style_section))

                data_table = [
                    [Paragraph("EMPRESA / RESPONSÁVEL", style_label), Paragraph(empresa, style_value),
                     Paragraph("DATA", style_label), Paragraph(data_relatorio.strftime("%d/%m/%Y"), style_value)],
                    [Paragraph("OBRA / SERVIÇO", style_label), Paragraph(obra, style_value),
                     Paragraph("CONTRATO / OS", style_label), Paragraph(contrato or "—", style_value)],
                    [Paragraph("RESPONSÁVEL TÉCNICO", style_label), Paragraph(responsavel or "—", style_value),
                     Paragraph("LOCAL", style_label), Paragraph(local or "—", style_value)],
                ]

                t = Table(data_table, colWidths=[4*cm, 6.5*cm, 3.5*cm, 3.5*cm])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1),
                     [colors.white, colors.HexColor('#f0f4f8')]),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                    ('INNERGRID', (0, 0), (-1, -1),
                     0.3, colors.HexColor('#dddddd')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(t)

                # Observações gerais
                if observacoes_gerais:
                    story.append(Spacer(1, 0.3*cm))
                    story.append(
                        Paragraph("  OBSERVAÇÕES GERAIS", style_section))
                    story.append(Paragraph(observacoes_gerais, style_obs))

                # ── REGISTRO FOTOGRÁFICO ───────────────────────────────────────
                story.append(
                    Paragraph("  REGISTRO FOTOGRÁFICO", style_section))

                fotos_por_linha = 2
                img_width = 8.5*cm
                img_height = 6.5*cm

                for i in range(0, len(uploaded_files), fotos_por_linha):
                    row_images = []
                    row_captions = []

                    for j in range(fotos_por_linha):
                        idx = i + j
                        if idx < len(uploaded_files):
                            # Processar imagem
                            img_file = uploaded_files[idx]
                            img_file.seek(0)
                            pil_img = PILImage.open(img_file)

                            # Converter para RGB se necessário
                            if pil_img.mode in ('RGBA', 'P'):
                                pil_img = pil_img.convert('RGB')

                            # Redimensionar mantendo proporção
                            pil_img.thumbnail((800, 600), PILImage.LANCZOS)
                            img_buffer = io.BytesIO()
                            pil_img.save(img_buffer, format='JPEG', quality=85)
                            img_buffer.seek(0)

                            rl_img = Image(
                                img_buffer, width=img_width, height=img_height)
                            rl_img.hAlign = 'CENTER'

                            num_label = Paragraph(f"<b>Foto {idx + 1}</b>", ParagraphStyle(
                                'PhotoNum', parent=styles['Normal'],
                                fontSize=8, textColor=colors.white,
                                backColor=colors.HexColor('#1a1a2e'),
                                alignment=TA_CENTER, fontName='Helvetica-Bold'
                            ))

                            caption_text = legendas[idx] if legendas[idx] else f"Foto {
                                idx + 1}"
                            caption = Paragraph(caption_text, style_caption)

                            cell_content = Table(
                                [[num_label], [rl_img], [caption]],
                                colWidths=[img_width]
                            )
                            cell_content.setStyle(TableStyle([
                                ('BOX', (0, 0), (-1, -1), 0.5,
                                 colors.HexColor('#cccccc')),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('TOPPADDING', (0, 0), (-1, -1), 4),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                            ]))
                            row_images.append(cell_content)
                        else:
                            row_images.append("")

                    photo_row = Table([row_images], colWidths=[
                                      img_width + 0.5*cm] * fotos_por_linha)
                    photo_row.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 4),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ]))
                    story.append(photo_row)

                # ── RODAPÉ ────────────────────────────────────────────────────
                story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor('#cccccc'), spaceBefore=10))
                footer_text = f"Relatório gerado em {datetime.now().strftime(
                    '%d/%m/%Y às %H:%M')}  |  {empresa}  |  Total de fotos: {len(uploaded_files)}"
                story.append(Paragraph(footer_text, ParagraphStyle(
                    'Footer', parent=styles['Normal'],
                    fontSize=8, textColor=colors.HexColor('#888888'),
                    alignment=TA_CENTER, fontName='Helvetica'
                )))

                # Gerar PDF
                doc.build(story)
                buffer.seek(0)

            st.success("✅ Relatório gerado com sucesso!")
            nome_arquivo = f"relatorio_{obra.replace(' ', '_').lower()}_{
                data_relatorio.strftime('%d%m%Y')}.pdf"
            st.download_button(
                label="⬇️ Baixar Relatório PDF",
                data=buffer,
                file_name=nome_arquivo,
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

else:
    st.info("📁 Faça o upload das fotos para continuar.")
