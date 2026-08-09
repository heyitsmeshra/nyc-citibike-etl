from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from analysis.page_1 import get_page1_data
from analysis.page_2 import get_page2_data


def generate_report():

    page1 = get_page1_data()

    page2 = get_page2_data(
        page1["current_df"]
    )

    summary = page1["summary"]
    health = page1["health"]

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        "reports/Citi_Bike_Analytics_Report.pdf"
    )

    story = []

    # -----------------------------
    # PAGE 1
    # -----------------------------

    story.append(
        Paragraph(
            "<b>Citi Bike Analytics Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "<b>Executive Summary</b>",
            styles["Heading2"]
        )
    )

    summary_table = Table([

        ["Metric", "Value"],

        ["Stations", summary["total_stations"]],

        ["Total Capacity", summary["total_capacity"]],

        ["Available Bikes", summary["total_bikes"]],

        ["Available Docks", summary["total_docks"]],

        ["Average Capacity", summary["average_capacity"]],

        ["Bike Availability (%)",
         summary["bike_availability_ratio"]],

        ["Dock Availability (%)",
         summary["dock_availability_ratio"]]

    ])

    summary_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("ALIGN", (0, 0), (-1, -1), "CENTER")

        ])

    )

    story.append(summary_table)

    story.append(Spacer(1, 0.25 * inch))

    story.append(

        Paragraph(
            "<b>Operational Health</b>",
            styles["Heading2"]
        )

    )

    health_table = Table([

        ["Status", "Count"],

        ["Operational", health["operational"]],

        ["Partially Available",
         health["partially_available"]],

        ["Out of Service",
         health["out_of_service"]]

    ])

    health_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER")

        ])

    )

    story.append(health_table)

    story.append(Spacer(1, 0.25 * inch))

    story.append(

        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            page1["interpretation"],
            styles["BodyText"]
        )

    )

    story.append(PageBreak())
        # -----------------------------
    # PAGE 2
    # -----------------------------

    story.append(
        Paragraph(
            "<b>Visual Analysis</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Top 10 Stations by Bike Availability (%)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Image(
            page2["top_station_chart"],
            width=6.5 * inch,
            height=3.8 * inch
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    story.append(
        Paragraph(
            "<b>Distribution of Station Bike Availability (%)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Image(
            page2["distribution_chart"],
            width=6.2 * inch,
            height=3.6 * inch
        )
    )

    # -----------------------------
    # BUILD PDF
    # -----------------------------

    document.build(story)

    print(
        "PDF report generated successfully:"
    )

    print(
        "reports/Citi_Bike_Analytics_Report.pdf"
    )


if __name__ == "__main__":

    generate_report()