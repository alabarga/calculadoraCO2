# -*- coding: utf-8 -*-

import calendar
from datetime import date, datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User 
from django.contrib.sites.models import get_current_site

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django.template import Context, loader
from django.db.models import Avg, Max, Min, Count, Sum

from django.views.generic import CreateView

from chartit import DataPool, Chart, PivotDataPool, PivotChart

from co2.models import *
from co2.forms import EntidadForm, ConsumosFormSet

import csv
from pyvttbl import DataFrame
from django.db.models import Max, Sum, Avg


def entidades(request):
    entidades = Entidad.objects.all()

    return render_to_response("entidades.html", {"entidades":entidades})    

def get_year():
    a = Consumo.objects.all().aggregate(year=Max('ano'))
    return a['year']

def ordenar(x):
    return (int(x[1][0]),)

def month_name(*t):
    names ={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    month_num = t[0]
    return (names[month_num], )

def monthname(month_num):
    names ={'1': 'Ene', '2': 'Feb', '3': 'Mar', '4': 'Abr', '5': 'May', '6': 'Jun',
            '7': 'Jul', '8': 'Ago', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'}
    return (names[month_num[0]],)

def meses(month_num):
    names ={1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    return names[month_num]

def calcular_acumulado(ano):

    Acumulado.objects.filter(ano=ano).delete()

    from django.db import connection, transaction
    cursor = connection.cursor()

    cursor.execute('''select t1.ano, t1.mes, Avg(t1.co2) co2, Sum(t2.co2) acumulado
                    FROM
                    (select ano, mes, Sum(co2) co2 
                     from co2_consumo
                     WHERE ano = %s
                     GROUP BY ano, mes) t1
                     INNER JOIN
                    (select mes, Sum(co2) co2
                     from co2_consumo
                     WHERE ano = %s
                     GROUP BY mes) t2
                     ON t2.mes <= t1.mes
                     GROUP BY t1.mes''' % (ano, ano))

    rows = cursor.fetchall()
    for row in rows:
        print row
        a = Acumulado()
        a.ano = row[0]
        a.mes = row[1]
        a.co2 = row[2]
        a.acumulado = row[3]
        a.save()

def g_mensual(entidad,ano,tipo=None,id=1):

    if tipo:
        dataSource = Consumo.objects.filter(ano = int(ano), entidad__id=entidad, content_type__name = tipo, object_id=id).order_by('mes')
    else:
        dataSource = Consumo.objects.filter(ano = int(ano), entidad__id=entidad).order_by('mes')

    datos = PivotDataPool(
      series= [
       {'options':{
          'source': dataSource,
          'categories': ['mes',],
          'legend_by': 'medida__recurso__denominacion'},
        'terms': {
          'consumo':Sum('co2'),
        }}],
      sortf_mapf_mts = (ordenar , monthname, True))

    # datos.series["consumo"]["_cv_lv_dfv"][('1',)]

    chart = PivotChart(
          datasource = datos, 
          series_options = [
            {'options': {
               'type': 'column',
               'stacking': True},
             'terms': [
                'consumo',
                ]}],
          chart_options = {
            'title': {'text': 'Evolución de las emisiones de CO2 en %s' % ano},
            'yAxis': {'title': {'text': 'Kg CO2'},
                      'plotLines' : [{
                    'value' : 1500,
                    'color' : 'green',
                    'dashStyle' : 'shortdash',
                    'width' : 2,
                    'label' : {
                        'text' : 'Objetivo %s' % ano
                    }
                }]
            },
            'xAxis': {'title': {'text': 'Mes'},}
          },
          )
 
    return chart

def g_compare(entidad, ano=None):

    if ano is None:
        ano = get_year()

    datos = PivotDataPool(
      series= [
       {'options':{
          'source': Consumo.objects.filter(ano = int(ano)-1).order_by('mes'),
          'categories': ['mes',],
          },
        'terms': {
          'consumo %d' % (int(ano)-1):Sum('co2'),
        }},
        {'options':{
          'source': Consumo.objects.filter(ano = int(ano)).order_by('mes'),
          'categories': ['mes',],
          },
        'terms': {
          'consumo %d' % (int(ano)):Sum('co2'),
        }}],
      sortf_mapf_mts = (ordenar , monthname, True))

    chart = PivotChart(
          datasource = datos, 
          series_options = [
            {'options': {
               'type':'column',
               'stacking': False},
             'terms': [
                'consumo %d' % (int(ano) - 1), 'consumo %d' % (int(ano))
                ]}],
          chart_options = {
            'title': {'text': 'Evolucion del consumo en %s' % ano},
            'yAxis': [{}, {'opposite': True}],
            'xAxis': {'title': {'text': 'Mes'}}},
          )
    return chart

def g_acumulado(entidad, ano = None):

    if ano is None:
        ano = get_year()

    calcular_acumulado(ano)

    #Step 1: Create a DataPool with the data we want to retrieve.
    datos = \
        DataPool(
           series=
            [{'options': {
               'source': Acumulado.objects.filter(ano=ano)},
              'terms': [
                'mes',
                'acumulado',
                'co2']}
             ])

    #Step 2: Create the Chart object
    chart = Chart(
            datasource = datos,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'mes': ['acumulado']
                  }
                },
                {'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':{
                  'mes': ['co2']
                  }
                }

              ],
            chart_options =
              {'title': {
                   'text': 'Evolución de las emisiones de CO2 en %s' % str(ano)},
               'xAxis': {
                    'title': {'text': 'Mes'}
                },
                'yAxis': {'title': {'text': 'Kg CO2'},
                      'plotLines' : [{
                    'value' : 15000,
                    'color' : 'green',
                    'dashStyle' : 'shortdash',
                    'width' : 2,
                    'label' : {
                        'text' : 'Objetivo %s' % ano
                    }
                }]
            },
          }, x_sortf_mapf_mts = (None, meses, False))
    
    return chart  

@login_required
def userprofile(request):
    profile = request.user.get_profile()
    entidad = 1
    return HttpResponseRedirect("/%d/" % entidad)

def home(request):
    entidad = Entidad.objects.get(pk=1)
    acumulado = g_acumulado('1',get_year()) 
    comparacion = g_compare('1',get_year())
    consumos = Consumo.objects.all()
    return render_to_response("index.html", 
                              {"page":"home","consumos":consumos,"charts":[acumulado,comparacion]},
                              context_instance=RequestContext(request))

def main(request, entidad=1, ano=None):

    if ano is None:
        ano = get_year()

    consumos = Consumo.objects.filter(entidad__pk=entidad, ano=ano)  
    entidad = Entidad.objects.get(pk=entidad)
    acumulado = g_acumulado(entidad,ano) 
    comparacion = g_compare(entidad,ano)
  
    return render_to_response("index.html", 
                               {"page":"home","consumos":consumos,"entidad":entidad, "charts":[acumulado,comparacion]},
                               context_instance=RequestContext(request))

def detalle_local(request, entidad = 1, id=1, ano=None):

    local = Local.objects.get(id=id)
    if ano is None:
        ano = local.get_years()[0]

    consumos = Consumo.objects.filter(entidad__pk=entidad, ano=ano)  
    chart = g_mensual(entidad,ano,tipo='Local',id=id) 
    entidad = Entidad.objects.get(pk=entidad)    
    comparacion = g_compare(entidad,ano)
    years = local.get_years()
    return render_to_response("detalle.html", 
                              {"page":"locales","years":years,"consumos":consumos,"entidad":entidad, "chart":[chart]},
                              context_instance=RequestContext(request))

def detalle_vehiculo(request, entidad = 1, id=1, ano=None):

    vehiculo = Vehiculo.objects.get(id=id)
    if ano is None:
        ano = vehiculo.get_years()[0]

    consumos = Consumo.objects.filter(entidad__pk=entidad, ano=ano)  
    chart = g_mensual(entidad,ano,tipo='Vehiculo',id=id) 
    entidad = Entidad.objects.get(pk=entidad)
    comparacion = g_compare(entidad,ano)
    years = vehiculo.get_years()

    return render_to_response("detalle.html", 
                              {"page":"vehiculos","years":years,"consumos":consumos,"entidad":entidad, "chart":[chart]},
                              context_instance=RequestContext(request))

def info_vehiculos(request, entidad=1):
    entidad = Entidad.objects.get(pk=entidad)
    locales =  entidad.locales.all()
    vehiculos = entidad.vehiculos.all()
    return render_to_response("info_vehiculos.html", 
                              {"page":"vehiculos","entidad":entidad, "locales":locales,"vehiculos":vehiculos},
                              context_instance=RequestContext(request))

def info_locales(request, entidad=1):
    entidad = Entidad.objects.get(pk=entidad)
    locales =  entidad.locales.all()
    vehiculos = entidad.vehiculos.all()
    return render_to_response("info_locales.html", 
                              {"page":"locales","entidad":entidad, "locales":locales,"vehiculos":vehiculos},

                              context_instance=RequestContext(request))
    
def historico(request,entidad):

    aa = list(set(Consumo.objects.all().values_list('ano', flat=True).distinct()))
    aa.reverse()

    charts = [g_anual(entidad)]
    years = ["Anual"]
    consumos = {}
    for a in aa:
        charts.append(g_mensual(entidad,a))
        years.append(str(a)) 
        consumos[str(a)] = (Consumo.objects.filter(entidad=entidad, ano = a))

    # Send the chart object to the template.   
    return render_to_response("charts.html", 
                              {"page":"charts","charts":charts,"years":years,"consumos":consumos,"container":",".join(years)},
                              context_instance=RequestContext(request))    

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

class AddConsumoView(CreateView):
    template_name = 'co2/consumos.html'
    model = Consumo
    success_url = '/'

    def get_context_data(self, **kwargs):

        context = super(AddConsumoView, self).get_context_data(**kwargs)
        entidad_id = self.kwargs['entidad']
        context['locales'] = Local.objects.filter(entidad__id=entidad_id)
        context['vehiculos'] = Vehiculo.objects.filter(entidad__id=entidad_id)
        context['entidad'] = Entidad.objects.get(id=entidad_id)
        context['page'] = 'consumos'
        return context

######################################################################

    
######################################################################

def test(request):

    #Step 1: Create a DataPool with the data we want to retrieve.
    datos = \
        DataPool(
           series=
            [{'options': {
               'source': Consumo.objects.filter(ano=2012)},
              'terms': [
                'mes',
                'valor']}
             ])

    #Step 2: Create the Chart object
    linechart = Chart(
            datasource = datos,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'mes': [
                    'valor', ]
                  }}],
            chart_options =
              {'title': {
                   'text': 'Evolucion del consumo en 2012'},
               'xAxis': {
                    'title': {
                       'text': 'Mes'}}})

    #Step 2: Create the Chart object
    barchart = Chart(
            datasource = datos,
           
            series_options =
              [{'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':{
                  'mes': [
                    'valor', ]
                  }}],
            chart_options =
              {'title': {
                   'text': 'Evolucion del consumo en 2012'},
               'xAxis': {
                    'title': {
                       'text': 'Mes'}}})

    #Step 3: Send the chart object to the template.
    
    return render_to_response("co2/test.html", {"chart":[linechart,barchart]})    

def acumulado(request,entidad,ano):
   #Step 3: Send the chart object to the template.   
    chart = g_acumulado(entitad,ano)
    return render_to_response("co2/grafico.html", {"chart":chart})    

def g_anual(entidad):

    #Step 1: Create a DataPool with the data we want to retrieve.

    datos = PivotDataPool(
      series= [
        {'options':{
          'source': Consumo.objects.filter(entidad__id=entidad),
          'categories':'ano',
          },
         'terms': {
          'consumo':Sum('co2'),
          }
        }])

    chart = PivotChart(
          datasource = datos, 
          series_options = [
            {'options': {
               'type':'column'
              },
             'terms': ['consumo']
            } 
            ],
            chart_options = {
            'title': {'text': 'Evolucion del consumo'},
            'xAxis': {'title': {'text': 'Año'}}}            
            )

    return chart

def anual(request):
    chart = g_anual(1)
    return render_to_response("co2/grafico.html", {"chart":chart})

def locales(request,entidad,ano):

    datos = PivotDataPool(
      series= [
       {'options':{
          'source': Consumo.objects.filter(ano = int(ano),content_type__id=16),
          'categories': ['object_id'],
          'legend_by': 'medida__recurso__denominacion'},
        'terms': {
          'consumo':Sum('co2'),
        }}],
      sortf_mapf_mts = (None , None, True))

    chart = PivotChart(
          datasource = datos, 
          series_options = [
            {'options': {
               'type': 'column',
               'stacking': True},
             'terms': [
                'consumo',
                ]}],
          chart_options = {
            'title': {'text': 'Reparto del consumo en %s' % ano},
            'yAxis': [{}, {'opposite': True}],
            'xAxis': {'title': {'text': 'Mes'}}},
          )
  
    return render_to_response("co2/grafico.html", {"chart":chart}, context_instance=RequestContext(request))

  
def evolucion(request,entidad):

    datos = PivotDataPool(
      series= [
       {'options':{
          'source': Consumo.objects.all(),
          'categories': ['ano',],
          'legend_by': 'recurso__denominacion'},
        'terms': {
          'consumo':Sum('co2'),
        }}],
      sortf_mapf_mts = (None , None, True))

    chart = PivotChart(
          datasource = datos, 
          series_options = [
            {'options': {
               'type': 'column',
               'stacking': True},
             'terms': [
                'consumo',
                ]}],
          chart_options = {
            'title': {'text': 'Evolucion del consumo de %s' % entidad},
            'yAxis': {'title': {'text': 'Kg CO2'},
                      'plotLines' : [{
                    'value' : 1500,
                    'color' : 'green',
                    'dashStyle' : 'shortdash',
                    'width' : 2,
                    'label' : {
                        'text' : 'Objetivo' 
                    }
                }]
            },
            'xAxis': {'title': {'text': 'Año'},}
          },
          )


    return render_to_response("co2/grafico.html", {"chart":chart}, context_instance=RequestContext(request))


def compare(request,entidad,ano=None):

    if ano is None:
        ano = get_year()

    chart = g_compare(entidad,ano)
    return render_to_response("co2/grafico.html", {"chart":chart}, context_instance=RequestContext(request))

class AddConsumoView2(CreateView):
    template_name = 'co2/consumos.html'
    form_class = EntidadForm

    def get_context_data(self, **kwargs):
        context = super(AddConsumoView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ConsumosFormSet(self.request.POST)
        else:
            context['formset'] = ConsumosFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())  # assuming your model has ``get_absolute_url`` defined.
        else:
            return self.render_to_response(self.get_context_data(form=form))

def export_to_csv(request):
    # get the response object, this can be used as a stream.
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    qs = request.session['queryset']
    for cdr in qs:
        writer.writerow([cdr['calldate'], cdr['src'], cdr['dst'], ])
    return response

def export_csv(request, entidad=1, ano=None):

    if ano is None:
        ano = get_year()

    consumos = Consumo.objects.filter(entidad__pk=entidad, ano=ano)  
    # get the response object, this can be used as a stream.
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = "attachment;filename=export.csv"
    # the csv writer
    writer = csv.writer(response)
    writer.writerow(["Año", "Mes", "Consumo", "Valor", "CO2"])
    for c in consumos:
        writer.writerow([c.ano, c.mes, c.medida, c.valor, c.co2])
    return response

def export_csv_pivot(request, entidad=1, ano=str(date.today().year)):

    consumos = Consumo.objects.filter(entidad__pk=entidad, ano=ano)
    
    from collections import namedtuple
    LineaDetalle = namedtuple('LineaDetalle',[u'Año', "Mes", 'Local_o_Vehiculo', "Consumo", "Valor"])

    df = DataFrame()    
    
    for c in consumos:

        if c.content_type.id == 16:
            denominacion = Local.objects.get(pk=c.object_id).denominacion
        else:
            denominacion = Vehiculo.objects.get(pk=c.object_id).denominacion

        df.insert(LineaDetalle(c.ano, c.mes, denominacion.encode("utf-8"), c.medida.denominacion.encode("utf-8"), c.valor)._asdict())

    pt = df.pivot("Valor", ['Local_o_Vehiculo','Consumo'], ['Mes'])

    # get the response object, this can be used as a stream.
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'

    response.write(pt)

    return response

def informe_local(request,entidad,ano):
    total = []
    locales = Local.objects.all()
    for l in locales:
        consumos = l.consumos().filter(ano=ano).values('mes').annotate(total=Sum('co2'))
        ll = {'Row':l.denominacion}
        for c in consumos:
          ll[meses(c['mes'])] = c['total']
        total.append(ll)

    return render_to_response("informe.html", {"page":"informes","total":total,"tipo":"Local"})

def informe_anual(request,entidad,ano):
    total = []
    for l in list(set(Consumo.objects.values_list('medida__recurso__denominacion',flat=True))):
        consumos = Consumo.objects.filter(ano=ano,medida__recurso__denominacion=l).values('mes').annotate(total=Sum('co2'))
        ll = {'Row':l}
        for c in consumos:
            ll[meses(c['mes'])] = c['total']
        total.append(ll)

    return render_to_response("informe.html", {"page":"informes","total":total,"tipo":"Recurso"}, context_instance=RequestContext(request))


