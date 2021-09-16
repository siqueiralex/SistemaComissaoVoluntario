from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
from openpyxl import Workbook
import xlwt
from dashboard.sheet_builder import NewSheetBuilder
from dashboard.utils import extract_list_from_sheet, controlePlanosSheetFiller, cotachSheetFiller

from .models import *


@login_required(login_url='login')
def exportarProjetosExcel(request, cron_id):
    unidades = Unidade.objects.all()
    cronograma = Cronograma.objects.get(id = cron_id)

    filename = f"Resumo Sistema - Planos de ação - {cronograma.inicio_servicos.strftime(f'%d')} a {cronograma.fim_servicos.strftime(f'%d de %B')}"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
   
    controlePlanosSheetFiller(wb.add_sheet('CONTROLE'),cronograma,unidades)
    cotachSheetFiller(wb.add_sheet("COTAxCH"), cronograma, unidades ) 
    
    wb.save(response)
    return response

@login_required(login_url='login')
def exportarVagasExcel(request, cron_id, dia):
    dia = datetime.datetime.strptime(dia, f"%Y-%m-%d").date()
    vagas = Vaga.objects.filter(dia = dia)
    
    filename = "Vagas "+dia.strftime(f"%d-%m-%Y")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

    wb = Workbook()
    sheet = wb.active
    sheet.title="Vagas"

    if not vagas.exists():
        wb.save(response)
        return response

    sb = NewSheetBuilder(sheet)
    sb.set_col_widths([10,10,35,30,10,10])

    sb.write_header([
        {'text':'DATA'},
        {'text':'UNIDADE'},
        {'text':'ATIVIDADE'},
        {'text':'RESPONSÁVEL'},
        {'text':'HORÁRIO'},
        {'text':'CH'}])
        
    sb.enter()
    for vaga in vagas:

        sb.write_cell(date_format(vaga.dia, "d-M"))
        sb.write_cell(vaga.unidade.sigla, style = sb.get_random_color_style(vaga.unidade.id))
        sb.write_cell(vaga.atividade)
        sb.write_cell(vaga.responsavel)
        sb.write_cell(vaga.horario, style=None if vaga.carga_horaria==12 else 'highlight_')
        sb.write_cell(vaga.carga_horaria, carr_ret=True)
        

    wb.save(response)
    return response