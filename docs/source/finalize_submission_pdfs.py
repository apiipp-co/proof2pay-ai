"""Put the current implementation boundary in front of older concept PDFs.

Run with the bundled Python runtime that includes reportlab and pypdf.
The status page is replaced on rerun, so the script is idempotent.
"""

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
NAVY = colors.HexColor("#172B45")
TEAL = colors.HexColor("#087E83")
GRAY = colors.HexColor("#526174")
LIGHT = colors.HexColor("#EEF5F5")
MARKER = "SUBMISSION STATUS | 2 OCT 2026"

styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=TEAL, spaceAfter=14),
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=NAVY, spaceAfter=12),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11, leading=16, textColor=GRAY, spaceAfter=18),
    "heading": ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=NAVY, spaceBefore=15, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15, textColor=NAVY, spaceAfter=7),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=GRAY),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=13, textColor=NAVY),
    "cellhead": ParagraphStyle("cellhead", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=NAVY),
}


def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor("#D7E3E8"))
    canvas.line(54, 46, doc.pagesize[0] - 54, 46)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(54, 32, "PROOF2PAY AI  |  Hackathon Stage 1")
    canvas.drawRightString(doc.pagesize[0] - 54, 32, "2 October 2026")


def make_pdf(story, pagesize=letter):
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=pagesize, rightMargin=54, leftMargin=54,
        topMargin=55, bottomMargin=62,
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buf.seek(0)
    return PdfReader(buf)


def p(text, style="body"):
    return Paragraph(text, styles[style])


def status_page(name):
    story = [
        p(MARKER, "eyebrow"),
        p(name, "title"),
        p("Current implementation boundary for the technical concept pages that follow.", "subtitle"),
        HRFlowable(width="100%", thickness=1.2, color=TEAL),
        p("Verified local demo", "heading"),
        p("The browser prototype assesses a synthetic AC work order. Four deterministic Langflow flows handle analysis, evidence validation, a guarded completion pack, and a combined review. Direct MCP calls to those four tools pass. A separate local IBM Granite Agent graph runs through Ollama; a deterministic guard supplies its final source-linked answer."),
        p("The 2 October checks passed: browser 4/4, Langflow API 13/13, direct MCP 5/5, and guarded Agent output 5/5. Three genuine NYC Parks work-order records remain insufficient for a billing decision."),
        p("Limits that matter", "heading"),
        p("IBM Bob displayed the local MCP server as Connected, but no successful tool call through Bob has been verified. The public static browser demo does not call Langflow. The Agent check does not measure interpretation accuracy for photos or documents. No customer pilot, hosted backend, invoice, or payment action exists."),
        p("How to read the following pages", "heading"),
        p("They describe the intended product workflow and technical design. Treat AI extraction, retrieval, customer data integration, Bob-led orchestration, and external follow-up as planned capabilities unless a current run report proves them."),
        Spacer(1, 14),
        p('Current source of truth: <link href="https://github.com/apiipp-co/proof2pay-ai/blob/main/IMPLEMENTATION_STATUS.md" color="#087E83">IMPLEMENTATION_STATUS.md</link> and <link href="https://github.com/apiipp-co/proof2pay-ai/tree/main/langflow/runs" color="#087E83">run reports</link>.', "small"),
    ]
    return make_pdf(story)


def prepend_status(filename, title):
    path = DOCS / filename
    reader = PdfReader(path)
    pages = list(reader.pages)
    if pages and MARKER in (pages[0].extract_text() or ""):
        pages = pages[1:]
    writer = PdfWriter()
    writer.add_page(status_page(title).pages[0])
    for page in pages:
        writer.add_page(page)
    writer.add_metadata({"/Title": f"PROOF2PAY AI - {title} (current status + concept)"})
    tmp = path.with_suffix(".tmp.pdf")
    with tmp.open("wb") as stream:
        writer.write(stream)
    tmp.replace(path)


def one_pager():
    story = [
        p("STAGE 1 JUDGE BRIEF  |  2 OCT 2026", "eyebrow"),
        p("PROOF2PAY AI", "title"),
        p("Evidence review for B2B field-service billing handoff", "subtitle"),
        HRFlowable(width="100%", thickness=1.2, color=TEAL),
        p("The problem", "heading"),
        p("A technician can report an AC service job complete while the operations team still lacks the reading, customer acknowledgement, or final report needed to prepare billing. PROOF2PAY shows exactly which requirement lacks proof and who should act next."),
        p("What the MVP demonstrates", "heading"),
    ]
    rows = [
        [p("Surface", "cellhead"), p("Observed result", "cellhead")],
        [p("Synthetic work order WO-1028", "cell"), p("Starts BLOCKED with three unresolved requirements. A source-linked demo pack requires complete evidence and named human approval.", "cell")],
        [p("Three public NYC Parks records", "cell"), p("Genuine source metadata is shown, but a Completed field remains INSUFFICIENT_EVIDENCE for billing.", "cell")],
        [p("Langflow and MCP", "cell"), p("Four deterministic flows run locally and are exposed as MCP tools. API checks passed 13/13; direct MCP checks passed 5/5.", "cell")],
        [p("Local Granite Agent", "cell"), p("The Agent graph runs through Ollama. Its final answer is source-linked by a deterministic output guard; guarded-output checks passed 5/5.", "cell")],
    ]
    table = Table(rows, colWidths=[145, 340], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("LINEBELOW", (0, 0), (-1, -1), 0.35, colors.HexColor("#D8E5E8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([
        table,
        p("Safety and current limits", "heading"),
        p("A claim is not treated as proof. Conflicts require human review; missing critical evidence blocks the pack. Bob connected to the local MCP server, but a Bob tool call is unverified. The public static browser demo and local Langflow are separate surfaces. No customer pilot, measured business uplift, invoice, or payment action is claimed."),
        p("Business hypothesis", "heading"),
        p("B2B SaaS for field-service operations teams, beginning with AC/HVAC. Pricing, demand, and the best first vertical still require customer interviews."),
        Spacer(1, 7),
        p('<link href="https://apiipp-co.github.io/proof2pay-ai/app/" color="#087E83">Open browser demo</link>  |  <link href="https://github.com/apiipp-co/proof2pay-ai/blob/main/demo/proof2pay-demo-stage1-final.mp4" color="#087E83">76-second video</link>  |  <link href="https://github.com/apiipp-co/proof2pay-ai" color="#087E83">Repository and evidence</link>', "small"),
    ])
    path = DOCS / "09-judge-one-pager.pdf"
    pdf = make_pdf(story, pagesize=A4)
    if len(pdf.pages) != 1:
        raise RuntimeError(f"Judge brief must stay one page; got {len(pdf.pages)}")
    writer = PdfWriter()
    writer.add_page(pdf.pages[0])
    writer.add_metadata({"/Title": "PROOF2PAY AI - Stage 1 Judge Brief"})
    with path.open("wb") as stream:
        writer.write(stream)


if __name__ == "__main__":
    for filename, title in [
        ("03-technical-documentation.pdf", "Technical documentation"),
        ("05-system-architecture.pdf", "System architecture"),
        ("06-user-flow.pdf", "User flow"),
    ]:
        prepend_status(filename, title)
    one_pager()
