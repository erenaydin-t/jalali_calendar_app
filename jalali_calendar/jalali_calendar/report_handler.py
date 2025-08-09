"""
Report Integration for Jalali Calendar
مدیریت گزارش‌ها با تاریخ شمسی
"""

import frappe
from frappe import _
from .api_enhanced import convert_to_jalali, convert_to_gregorian
import json

@frappe.whitelist()
def run_report_with_jalali(report_name, filters=None):
    """اجرای گزارش با تبدیل تاریخ‌های شمسی"""
    
    # Check if jalali calendar is enabled
    if not frappe.db.get_single_value('Jalali Calendar Settings', 'enable_in_reports'):
        # Run normal report
        return frappe.desk.query_report.run(report_name, filters)
    
    # Convert jalali dates in filters to gregorian
    if filters:
        if isinstance(filters, str):
            filters = json.loads(filters)
        
        converted_filters = {}
        for key, value in filters.items():
            if isinstance(value, str) and '/' in value:
                # This might be a jalali date
                converted = convert_to_gregorian(value)
                converted_filters[key] = converted if converted != value else value
            else:
                converted_filters[key] = value
        
        filters = converted_filters
    
    # Run the report
    result = frappe.desk.query_report.run(report_name, filters)
    
    # Convert dates in result to jalali
    if result and 'result' in result:
        result['result'] = convert_report_dates(result['result'], result.get('columns', []))
    
    return result

def convert_report_dates(data, columns):
    """تبدیل تاریخ‌ها در داده‌های گزارش به شمسی"""
    
    # Find date columns
    date_columns = []
    date_fieldnames = []
    
    for i, col in enumerate(columns):
        if isinstance(col, dict):
            if col.get('fieldtype') in ['Date', 'Datetime']:
                date_columns.append(i)
                date_fieldnames.append(col.get('fieldname'))
    
    # Convert dates in data
    converted_data = []
    for row in data:
        if isinstance(row, list):
            new_row = list(row)
            for col_idx in date_columns:
                if col_idx < len(new_row) and new_row[col_idx]:
                    jalali = convert_to_jalali(new_row[col_idx])
                    if jalali:
                        new_row[col_idx] = jalali['date']
            converted_data.append(new_row)
        elif isinstance(row, dict):
            new_row = dict(row)
            for fieldname in date_fieldnames:
                if fieldname in new_row and new_row[fieldname]:
                    jalali = convert_to_jalali(new_row[fieldname])
                    if jalali:
                        new_row[fieldname] = jalali['date']
            converted_data.append(new_row)
        else:
            converted_data.append(row)
    
    return converted_data

@frappe.whitelist()
def export_report_with_jalali(report_name, file_format, filters=None):
    """Export گزارش با تاریخ‌های شمسی"""
    
    # Get report data with jalali dates
    result = run_report_with_jalali(report_name, filters)
    
    if file_format == "Excel":
        return export_to_excel(result)
    elif file_format == "CSV":
        return export_to_csv(result)
    elif file_format == "PDF":
        return export_to_pdf(result)
    else:
        return result

def export_to_excel(data):
    """Export به Excel با تاریخ شمسی"""
    from frappe.utils.xlsxutils import make_xlsx
    
    # Prepare data for excel
    xlsx_data = []
    
    # Add headers
    if data.get('columns'):
        headers = []
        for col in data['columns']:
            if isinstance(col, dict):
                headers.append(col.get('label', col.get('fieldname', '')))
            else:
                headers.append(str(col))
        xlsx_data.append(headers)
    
    # Add data rows
    if data.get('result'):
        for row in data['result']:
            if isinstance(row, list):
                xlsx_data.append(row)
            elif isinstance(row, dict):
                row_data = []
                for col in data['columns']:
                    if isinstance(col, dict):
                        fieldname = col.get('fieldname')
                        row_data.append(row.get(fieldname, ''))
                xlsx_data.append(row_data)
    
    # Create excel file
    xlsx_file = make_xlsx(xlsx_data, "Report")
    
    # Return file
    frappe.response['filename'] = f"{data.get('report_name', 'report')}_jalali.xlsx"
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'

def export_to_csv(data):
    """Export به CSV با تاریخ شمسی"""
    import csv
    from io import StringIO
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Add headers
    if data.get('columns'):
        headers = []
        for col in data['columns']:
            if isinstance(col, dict):
                headers.append(col.get('label', col.get('fieldname', '')))
            else:
                headers.append(str(col))
        writer.writerow(headers)
    
    # Add data rows
    if data.get('result'):
        for row in data['result']:
            if isinstance(row, list):
                writer.writerow(row)
            elif isinstance(row, dict):
                row_data = []
                for col in data['columns']:
                    if isinstance(col, dict):
                        fieldname = col.get('fieldname')
                        row_data.append(row.get(fieldname, ''))
                writer.writerow(row_data)
    
    # Return CSV
    frappe.response['filename'] = f"{data.get('report_name', 'report')}_jalali.csv"
    frappe.response['filecontent'] = output.getvalue()
    frappe.response['type'] = 'download'

def export_to_pdf(data):
    """Export به PDF با تاریخ شمسی"""
    # Generate HTML for PDF
    html = generate_report_html(data)
    
    # Convert to PDF
    pdf = frappe.utils.pdf.get_pdf(html)
    
    # Return PDF
    frappe.response['filename'] = f"{data.get('report_name', 'report')}_jalali.pdf"
    frappe.response['filecontent'] = pdf
    frappe.response['type'] = 'pdf'

def generate_report_html(data):
    """تولید HTML برای گزارش"""
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Vazir', Tahoma, Arial; direction: rtl; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
            th { background-color: #f2f2f2; }
            .date { direction: ltr; text-align: left; }
        </style>
    </head>
    <body>
        <h2>{title}</h2>
        <table>
            <thead>
                <tr>
    """.format(title=data.get('report_name', 'گزارش'))
    
    # Add headers
    if data.get('columns'):
        for col in data['columns']:
            if isinstance(col, dict):
                html += f"<th>{col.get('label', col.get('fieldname', ''))}</th>"
            else:
                html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
    
    # Add data rows
    if data.get('result'):
        for row in data['result']:
            html += "<tr>"
            if isinstance(row, list):
                for cell in row:
                    # Check if it's a date
                    cell_class = "date" if isinstance(cell, str) and '/' in cell else ""
                    html += f'<td class="{cell_class}">{cell}</td>'
            elif isinstance(row, dict):
                for col in data['columns']:
                    if isinstance(col, dict):
                        fieldname = col.get('fieldname')
                        value = row.get(fieldname, '')
                        cell_class = "date" if isinstance(value, str) and '/' in value else ""
                        html += f'<td class="{cell_class}">{value}</td>'
            html += "</tr>"
    
    html += """
        </tbody>
        </table>
    </body>
    </html>
    """
    
    return html
