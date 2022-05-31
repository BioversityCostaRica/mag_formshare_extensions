import xlsxwriter
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def generate_sheet_9(settings, schema, output_file):
    engine = create_engine(
        "mysql+mysqlconnector://{}:{}@{}/{}?"
        "charset=utf8mb4&ssl_disabled=True".format(
            settings["mysql.user"],
            settings["mysql.password"],
            settings["mysql.host"],
            schema,
        ),
        poolclass=NullPool,
    )
    archive = xlsxwriter.Workbook(output_file)
    pagine = archive.add_worksheet()

    formattitle = archive.add_format(
        {"bold": True, "font_size": 20, "font_name": "Arial"}
    )
    formattitle.set_align("center")
    formattitle.set_align("vcenter")

    formatdirection = archive.add_format(
        {"bold": True, "font_size": 16, "font_name": "Arial", "align": "left"}
    )
    formatdirection.set_text_wrap()

    formatvariable = archive.add_format(
        {
            "bold": True,
            "font_size": 16,
            "font_name": "Arial",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "fg_color": "yellow",
        }
    )
    formatvariable.set_text_wrap()

    formatvariablegray = archive.add_format(
        {
            "bold": True,
            "font_size": 16,
            "font_name": "Arial",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "fg_color": "gray",
        }
    )

    formatvariable_afe = archive.add_format(
        {
            "bold": True,
            "font_size": 10,
            "font_name": "Arial",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "fg_color": "yellow",
        }
    )
    formatvariable_afe.set_text_wrap()

    formatvariable_afe2 = archive.add_format(
        {
            "bold": True,
            "font_size": 10,
            "font_name": "Arial",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "fg_color": "gray",
        }
    )
    formatvariable_afe2.set_text_wrap()

    formatrow = archive.add_format({"border": 1, "font_size": 16, "font_name": "Arial"})

    pagine.set_column("A:Q", 13)
    pagine.set_row(0, 35)
    pagine.merge_range(
        "A1:Q1", "FORMULARIO N 9: AGROPECUARIO: SUBSECTOR PECUARIO", formattitle
    )
    pagine.set_row(1, 35)
    pagine.merge_range(
        "A2:Q2",
        "DAÑOS, PÉRDIDAS Y PROPUESTAS DE ATENCIÓN,  REHABILITACIÓN Y RECONSTRUCCIÓN",
        formattitle,
    )
    pagine.set_row(2, 35)
    pagine.merge_range("A3:Q3", "NOMBRE DEL EVENTO - MES - 2022", formattitle)
    pagine.set_row(3, 50)
    pagine.merge_range("A4:K4", "Institución Informante: ", formatdirection)
    pagine.merge_range("L4:Q4", "Fecha: ", formatdirection)

    pagine.set_row(5, 25)
    pagine.set_row(6, 45)
    pagine.merge_range("A6:A7", "Cantones", formatvariable)
    pagine.merge_range("B6:B7", "Distrito", formatvariable)
    pagine.merge_range("C6:C7", "Poblado", formatvariable)

    pagine.merge_range("D6:I6", "Afectación", formatvariablegray)

    pagine.write("D7", "Actividad", formatvariable_afe)
    pagine.write("E7", "N° de Fincas o Productores", formatvariable_afe)
    pagine.write("F7", "Cantidad (N° Animales)", formatvariable_afe)
    pagine.write("G7", "", formatvariable_afe)
    pagine.write("H7", "Naturaleza de Daños", formatvariable_afe2)
    pagine.write("I7", "Monto Estimado de Pérdidas", formatvariable_afe2)

    pagine.merge_range("J6:O6", "PROPUESTAS", formatvariablegray)

    pagine.write("J7", "Nivel de Prioridad", formatvariable_afe2)
    pagine.write("K7", "Fase", formatvariable_afe2)
    pagine.write("L7", "Programas, Proyectos,  Acciones, Obras", formatvariable_afe2)
    pagine.write("M7", "Instituciones Involucradas", formatvariable_afe)
    pagine.write("N7", "Plazo", formatvariable_afe2)
    pagine.write("O7", "Monto Estimado", formatvariable_afe2)

    # PECUARIOS
    sqlPecuarios = (
        "SELECT "
        "	M.id_formulario,"
        "    pecuaria_preguntando, "
        "    sum(ap_numero_animales_muertos) as animalesmuertos,"
        "    C.canton2_des,"
        "    D.distrito2_des "
        "FROM "
        "	maintable M,"
        "    cuadro_de_afectacion_pecuaria CDAP,"
        "    lkpcanton2 C,"
        "    lkpdistrito2 D "
        "WHERE "
        "	M.sector_productivo in (2,3) AND"
        "    M.id_formulario = CDAP.id_formulario AND"
        "    M.canton2 = C.canton2_cod AND"
        "    M.distrito2 = D.distrito2_cod  AND"
        "    ap_numero_animales_muertos > 0 "
        "group by"
        "	M.id_formulario,"
        "    pecuaria_preguntando,"
        "    C.canton2_des,"
        "    D.distrito2_des"
    )

    queryResults = engine.execute(sqlPecuarios).fetchall()

    summaryInformationForTable9 = []

    for result in queryResults:
        if result[2] > 0:
            summaryInformationForTable9.append(
                [result[1], result[2], 1, result[3], result[4]]
            )

    # PATIO
    sqlPatio = (
        "SELECT "
        "	M.id_formulario,"
        "	animales_de_patio_preguntando,"
        "    sum(numero_animales_de_patio_muertos) as animalesmuertos,"
        "    C.canton2_des,"
        "    D.distrito2_des "
        "FROM "
        "	maintable M,"
        "    cuadro_de_animales_de_patio CDADP,"
        "    lkpcanton2 C,"
        "    lkpdistrito2 D "
        "WHERE "
        "	M.sector_productivo in (2,3) AND"
        "    M.id_formulario = CDADP.id_formulario AND"
        "    M.canton2 = C.canton2_cod AND"
        "    M.distrito2 = D.distrito2_cod  AND"
        "    numero_animales_de_patio_muertos > 0 "
        "group by"
        "	M.id_formulario,"
        "    animales_de_patio_preguntando,"
        "    C.canton2_des,"
        "    D.distrito2_des"
    )

    queryResults = engine.execute(sqlPatio).fetchall()

    for result in queryResults:
        if result[2] > 0:
            summaryInformationForTable9.append(
                [result[1], result[2], 1, result[3], result[4]]
            )

    activities = []
    rowExcell = 8

    for data in summaryInformationForTable9:
        activities.append(data[0])
        activities = list(set(activities))
        activities.sort()

    generalNum_Farms = 0
    generalNum_Anim = 0
    generalTot = 0

    for activity in activities:
        totalNumberOfAnimalsAffected = 0
        totalOfFarms = 0
        conty = []
        district = []

        for data in summaryInformationForTable9:

            if data[0] == activity:
                totalOfFarms = totalOfFarms + 1
                totalNumberOfAnimalsAffected = totalNumberOfAnimalsAffected + data[1]
                conty.append(data[3])
                district.append(data[4])

        if totalNumberOfAnimalsAffected > 0:

            contys = ""
            districts = ""
            for con in list(set(conty)):
                contys = contys + con + "\n"

            for dis in list(set(district)):
                districts = districts + dis + "\n"

            queryForProductCost = "SELECT IFNULL(costo,0) FROM formshare.cne_pecuario WHERE actividad = '{}';".format(
                activity
            )

            queryResultsOfCost = engine.execute(queryForProductCost).fetchone()

            costoEstablecimiento = 0
            if queryResultsOfCost:
                costoEstablecimiento = queryResultsOfCost[0]

            costoDeLaActividad = float(totalNumberOfAnimalsAffected) * float(
                costoEstablecimiento
            )
            generalTot += costoDeLaActividad

            pagine.write("A" + str(rowExcell), contys)
            pagine.write("B" + str(rowExcell), districts)
            pagine.write("D" + str(rowExcell), activity)
            pagine.write("E" + str(rowExcell), totalOfFarms)
            pagine.write("F" + str(rowExcell), totalNumberOfAnimalsAffected)
            pagine.write("I" + str(rowExcell), costoDeLaActividad)

            generalNum_Farms += totalOfFarms
            generalNum_Anim += totalNumberOfAnimalsAffected

            rowExcell = rowExcell + 1

    pagine.write("A" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("B" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("C" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("D" + str(rowExcell), "Total", formatvariable_afe2)
    pagine.write("E" + str(rowExcell), generalNum_Farms, formatvariable_afe2)
    pagine.write("F" + str(rowExcell), generalNum_Anim, formatvariable_afe2)
    pagine.write("G" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("H" + str(rowExcell), "Total", formatvariable_afe2)
    pagine.write("I" + str(rowExcell), generalTot, formatvariable_afe2)
    pagine.write("J" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("K" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("L" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("M" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("N" + str(rowExcell), "", formatvariable_afe2)
    pagine.write("O" + str(rowExcell), "", formatvariable_afe2)

    archive.close()
    engine.dispose()
