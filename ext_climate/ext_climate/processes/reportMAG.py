"""
  @author : bmadriz acoto
  @since : 25/11/19
  @Description : 
"""
# - *- coding: utf- 8 - *-

####################pip install xlsxwriter###############
import xlsxwriter
import csv
import random
import MySQLdb
import json
import decimal
import sys

# reload(sys)
# sys.setdefaultencoding("utf8")
jsonForReport = {}


def createTableNumber8(month):

    data=[]
    """
    archive = xlsxwriter.Workbook('./cuadro_for_month_' + str(month) + '.xlsx')
    pagine = archive.add_worksheet("Reporte-CNE")

    columnsFormat = archive.add_format(
        {
            'bold': True,
            'font_size': 16,
            'font_name': 'Arial',
            'border': 1,
            'fg_color': 'gray'
        })

    rowNumbers = archive.add_format(
        {
            'align': 'center',
        })

    columnsFormat.set_align('center')
    columnsFormat.set_align('vcenter')

    pagine.set_column('A1:A1', 10)
    pagine.set_column('B1:C1', 23)
    pagine.set_column('D1:D1', 20)
    pagine.set_column('E1:E1', 15)
    pagine.set_column('F1:F1', 30)
    pagine.set_column('G1:G1', 40)
    pagine.set_row(0, 38)
    pagine.write('A1', 'Cantón', columnsFormat)
    pagine.write('B1', 'Número de\nfamilias afectadas', columnsFormat)
    pagine.write('C1', 'Número de\nfamilias atendidas', columnsFormat)
    pagine.write('D1', 'Área\n(hectáreas)', columnsFormat)
    pagine.write('E1', 'Actividad', columnsFormat)
    pagine.write('F1', 'Animales afectados', columnsFormat)
    pagine.write('G1', 'Estimación de afectación\n(Millones CRC)', columnsFormat)
    """
    row = 2

    for province in jsonForReport:
        rows=[]
        cantons = ""
        for canton in jsonForReport[province]["Cantons"]:
            if cantons == "":
                cantons += canton
            else:
                cantons += "</br>" + canton

        #pagine.write('A' + str(row), cantons)
        #pagine.write('B' + str(row), str(jsonForReport[province]["AffectedFamilies"]), rowNumbers)
        #pagine.write('C' + str(row), str(jsonForReport[province]["AffectedFamilies"]), rowNumbers)
        #pagine.write('D' + str(row), str(jsonForReport[province]["Area"]), rowNumbers)
        rows.append(cantons)
        rows.append(str(jsonForReport[province]["AffectedFamilies"]))
        rows.append(str(jsonForReport[province]["AffectedFamilies"]))
        rows.append(str(jsonForReport[province]["Area"]))
        activities = ""
        for activity in jsonForReport[province]["Activities"]:
            if activities == "":
                activities += activity["activity"] + ": " + str(activity["area"]) + " ha"
            else:
                activities += "</br>" + activity["activity"] + ": " + str(activity["area"]) + " ha"

        #pagine.write('E' + str(row), activities)
        rows.append(activities)
        costs = ""
        for activity in jsonForReport[province]["Cost"]:
            if costs == "":
                costs += activity["activity"] + ": " + str(activity["cost"]) + " "
            else:
                costs += "\n" + activity["activity"] + ": " + str(activity["cost"]) + " "

        #pagine.write('G' + str(row), costs)

        animals = ""
        # print jsonForReport[province]["AffectedAnimals"]
        for animal in jsonForReport[province]["AffectedAnimals"]:
            # print animal
            if animals == "":
                animals += animal["animal"] + ": " + str(animal["quantity"])
            else:
                animals += "\n" + animal["animal"] + ": " + str(animal["quantity"])

        #pagine.write('F' + str(row), animals)
        rows.append(animals)
        rows.append(costs)
        #pagine.write('G' + str(row), "")
        row = row + 1
        if (rows[0]!=""):
            data.append(rows)
    print(len(data))
    return data


def getProvinces(self, prj_id, startTime, finishTime):
    sql = "select distinct(P.provincia_des) from %s.maintable M, %s.lkpprovincia P, %s.lkpcanton C where  M.canton = C.canton_cod and C.provincia_cod = P.provincia_cod and MONTH(M.starttime_auto) between '%s' and '%s'" % (
        prj_id, prj_id, prj_id, startTime, finishTime)

    result = self.request.dbsession.execute(sql).fetchall()

    for province in result:
        jsonForReport[province[0]] = {}


def getCantons(self, prj_id, startTime, finishTime):
    sql = "select P.provincia_des, C.canton_des, count(*) as Cantidad, sum(M.landcultivated * if(M.unitland = 'mz',0.7,if(M.unitland='hectare',1,if(M.unitland='m2',0.0001,1)))) + IFNULL((select sum(pasto_total * if(pasto_total_unit = 'mz',0.7,if(pasto_total_unit='hectare',1,if(pasto_total_unit='m2',0.0001,1)))) from %s.livestock_repeat where i_d in (select i_d from %s.maintable W where W.canton = M.canton and MONTH(W.starttime_auto) between '%s' and '%s')),0) as Total  from %s.maintable M, %s.lkpprovincia P, %s.lkpcanton C  where  M.canton = C.canton_cod and C.provincia_cod = P.provincia_cod and MONTH(M.starttime_auto) between %s and %s group by P.provincia_des, C.canton_des, M.canton;" % (
        prj_id, prj_id, startTime, finishTime, prj_id, prj_id, prj_id, startTime, finishTime)

    result = self.request.dbsession.execute(sql).fetchall()

    for province in jsonForReport.keys():

        DetailsByCanton = {}
        DetailsByCanton["Cantons"] = []
        DetailsByCanton["Area"] = 0
        DetailsByCanton["AffectedFamilies"] = 0
        DetailsByCanton["Activities"] = []
        DetailsByCanton["Cost"] = []
        DetailsByCanton["AffectedAnimals"] = []

        for data in result:
            if data[0] == province:
                DetailsByCanton["Cantons"].append(data[1])
                DetailsByCanton["Area"] = DetailsByCanton["Area"] + round(data[3], 3)
                DetailsByCanton["AffectedFamilies"] = DetailsByCanton["AffectedFamilies"] + data[2]

        jsonForReport[province] = DetailsByCanton


def getActivities(self, prj_id, startTime, finishTime, month):
    sql = "(select P.provincia_des,K.crop_list_des, sum(C.crop_planted * if(C.crop_yield_units = 'mz',0.7,if(C.crop_yield_units='ha',1,if(C.crop_yield_units='m2',0.0001,1)))) as Total from %s.maintable T, %s.crop_repeat C, %s.lkpcrop_list K, %s.lkpprovincia P, %s.lkpcanton Ca where T.canton = Ca.canton_cod and Ca.provincia_cod = P.provincia_cod and T.i_d = C.i_d and C.crop_name = K.crop_list_cod and MONTH(T.starttime_auto) between '%s' and '%s' group by P.provincia_des, C.crop_name ) union all ( select provincia,pasto,sum(total) as total from ( ( select P.provincia_des provincia,'Pasto de piso' as pasto,(select sum(I.pasto_piso * if(I.pasto_piso_unit = 'mz',0.7,if(I.pasto_piso_unit='hectare',1,if(I.pasto_piso_unit='m2',0.0001,1)))) from %s.livestock_repeat I where I.i_d = M.i_d) as total  FROM %s.maintable M, %s.lkpprovincia P, %s.lkpcanton Ca where M.canton = Ca.canton_cod and Ca.provincia_cod = P.provincia_cod and MONTH(M.starttime_auto) between '%s' and '%s') Union all ( select P.provincia_des provincia,'Pasto mejorado' as pasto,(select sum(I.pasto_mejorado * if(I.pasto_mejorado_unit = 'mz',0.7,if(I.pasto_mejorado_unit='hectare',1,if(I.pasto_mejorado_unit='m2',0.0001,1)))) from %s.livestock_repeat I where I.i_d = M.i_d) as total FROM %s.maintable M, %s.lkpprovincia P, %s.lkpcanton Ca where M.canton = Ca.canton_cod and Ca.provincia_cod = P.provincia_cod and MONTH(M.starttime_auto) between '%s' and '%s') Union all  ( select P.provincia_des provincia,'Pasto de corte' as pasto,(select sum(I.pasto_corte * if(I.pasto_corte_unit = 'mz',0.7,if(I.pasto_corte_unit='hectare',1,if(I.pasto_corte_unit='m2',0.0001,1)))) from %s.livestock_repeat I where I.i_d = M.i_d) as total FROM %s.maintable M, %s.lkpprovincia P, %s.lkpcanton Ca where M.canton = Ca.canton_cod and Ca.provincia_cod = P.provincia_cod and MONTH(M.starttime_auto) between '%s' and '%s') ) as TiposDePastos  where TiposDePastos.total IS NOT NULL group by provincia, pasto)" %(prj_id,prj_id,prj_id,prj_id,prj_id,startTime, finishTime,prj_id,prj_id,prj_id,prj_id,startTime,finishTime,prj_id,prj_id,prj_id,prj_id,startTime,finishTime,prj_id,prj_id,prj_id,prj_id,startTime,finishTime )

    result = self.request.dbsession.execute(sql).fetchall()

    for province in jsonForReport.keys():
        for activity in result:
            if activity[0] == province:
                if round(activity[2], 3) != 0.0:
                    DetailsByactivity = {"activity": "", "area": 0}
                    DetailsByactivity["activity"] = activity[1]
                    DetailsByactivity["area"] = round(activity[2], 3)
                    jsonForReport[province]["Activities"].append(DetailsByactivity)


def getEstablecimiento(self, prj_id, startTime, finishTime, month):
    sql = "select provincia_des, cultivo, sum(costoestablecimiento) as establecimiento from (select P.provincia_des, K.crop_list_des as cultivo, (sum(C.crop_planted * if(C.crop_yield_units = 'mz',0.7,if(C.crop_yield_units='ha',1,if(C.crop_yield_units='m2',0.0001,1)))) * (select if(H.classCode = 4, 0,if(H.classCode = 3, 0.33,if(H.classCode = 2, 0.66,if(H.classCode = 1, 1,1)))) as porcentaje from ndvibioversity.hazardRainCanton H where H.canton_cod = T.canton and H.nmonth = %s ) ) * (ifnull(K.costperha,0) ) as costoestablecimiento from %s.maintable T, %s.crop_repeat C, %s.lkpcrop_list K, %s.lkpprovincia P, %s.lkpcanton Ca " \
          " where T.canton = Ca.canton_cod and Ca.provincia_cod = P.provincia_cod and T.i_d = C.i_d and C.crop_name = K.crop_list_cod and MONTH(T.starttime_auto) between '%s' and '%s' group by P.provincia_des,T.canton,C.crop_name) as selectTable group by provincia_des,cultivo;" % (
          month, prj_id, prj_id, prj_id, prj_id, prj_id, startTime, finishTime)
    result = self.request.dbsession.execute(sql).fetchall()

    for province in jsonForReport.keys():
        for activity in result:
            if activity[0] == province:
                if round(activity[2], 3) != 0.0:
                    DetailsByestablishment = {"activity": "", "area": 0}
                    DetailsByestablishment["activity"] = activity[1]
                    DetailsByestablishment["cost"] = str(round(activity[2], 3))+"</br>"
                    jsonForReport[province]["Cost"].append(DetailsByestablishment)


def defaultencode(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)


def getAffectedAnimals(self, prj_id,startTime, finishTime):
    sql = "select P.provincia_des,concat(LL.livestock_list_des,' ',if(LR.live_name='cattle',LR.tipo_ganaderia,if(LR.live_name='chicken',LR.tipo_aves,''))) as live, if(LR.live_name='bees', sum(LR.bee_number),sum(LR.live_number)) as total FROM %s.maintable M, %s.livestock_repeat LR, %s.lkpprovincia P, %s.lkpcanton Ca, %s.lkplivestock_list  LL  where LR.live_name = LL.livestock_list_cod and M.canton = Ca.canton_cod and Ca.provincia_cod = P.provincia_cod and M.i_d = LR.i_d and MONTH(M.starttime_auto) between '%s' and '%s' group by P.provincia_des,concat(LL.livestock_list_des,' ',if(LR.live_name='cattle',LR.tipo_ganaderia,if(LR.live_name='chicken',LR.tipo_aves,''))), LR.live_name"%(prj_id,prj_id,prj_id,prj_id,prj_id,startTime,finishTime)

    result = self.request.dbsession.execute(sql).fetchall()

    for province in jsonForReport.keys():
        for activity in result:
            if activity[0] == province:
                DetailsByanimal = {"animal": "", "quantity": 0}
                DetailsByanimal["animal"] = activity[1]
                DetailsByanimal["quantity"] = str(activity[2]) +"</br>"
                jsonForReport[province]["AffectedAnimals"].append(DetailsByanimal)


def main(self, prj_id,start, end):
    # datos = ["localhost", "root", "inspinia4", "FS_7b758deb_6f36_424c_9db8_5e566a1fef9a"]
    # connection = MySQLdb.connect(*datos, charset='utf8')

    month = start
    startTime = str(start)
    finishTime = str(end)

    getProvinces(self, prj_id, startTime, finishTime)
    getCantons(self, prj_id, startTime, finishTime)
    getActivities(self, prj_id, startTime, finishTime, month)
    getAffectedAnimals(self, prj_id, startTime, finishTime)
    getEstablecimiento(self, prj_id,startTime, finishTime, month)

    #createTableNumber8(month)

    return createTableNumber8(month)
