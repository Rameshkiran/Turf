from django.contrib import admin
from .models import *
from django.http import HttpResponse
import csv
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Define a custom admin action to export the report as CSV
def export_report_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="turfbooked_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Amount', 'Selected Date', 'Current Date', 'Booking Time', 'Slots'])

    for obj in queryset:
        writer.writerow([obj.name, obj.email, obj.amount, obj.selected_date, obj.current_date, obj.booking_time, obj.slots])

    return response

export_report_csv.short_description = 'Export Report as CSV'

# Define a custom admin action to export the report as Excel
def export_report_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="turfbooked_report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('TurfBooked Report')

    row_num = 0
    columns = ['Name', 'Email', 'Amount', 'Selected Date', 'Current Date', 'Booking Time', 'Slots']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    for obj in queryset:
        row_num += 1
        row = [obj.name, obj.email, obj.amount, obj.selected_date, obj.current_date, obj.booking_time, obj.slots]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response

export_report_excel.short_description = 'Export Report as Excel'

# Define a custom admin action to export the report as PDF
def export_report_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="turfbooked_report.pdf"'

    # Create a PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    data = []
    
    data.append(['Name', 'Email', 'Amount', 'Selected Date', 'Current Date', 'Booking Time', 'Slots'])
    for obj in queryset:
        data.append([obj.name, obj.email, str(obj.amount), obj.selected_date, obj.current_date, obj.booking_time, ', '.join(obj.slots)])

    table = Table(data)

    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add table to the PDF
    doc.build([table])
    return response

export_report_pdf.short_description = 'Export Report as PDF'

# Define a custom admin class for TurfBooked model
class TurfBookedAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin list view
    list_display = ('name', 'email', 'amount', 'selected_date', 'current_date', 'booking_time', 'slots')

    # Register the export_report actions
    actions = [export_report_csv, export_report_excel, export_report_pdf]

    # Override get_actions to add buttons for exporting report
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions



# Register your models here.
admin.site.register(Contact)
admin.site.register(turfBooking)
admin.site.register(bookslot)
admin.site.register(TurfBooked, TurfBookedAdmin)

