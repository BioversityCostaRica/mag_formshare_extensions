import xlsxwriter
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def generate_sheet_8(settings, schema, output_file):
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

    # configurations
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
    # writte
    # pagine.set_row(0, 70)
    pagine.set_column("A:Q", 13)
    pagine.set_row(0, 35)
    pagine.merge_range(
        "A1:Q1",
        "FORMULARIO N 8: AGROPECUARIO: SUBSECTOR AGRICOLA; ASENTAMIENTOS CAMPESINOS, INFRAESTRUCTURA DE RIEGO",
        formattitle,
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
    pagine.merge_range("L4:Q4", "Fecha: xx-xx-xxxx", formatdirection)

    pagine.set_row(5, 25)
    pagine.set_row(6, 45)
    pagine.merge_range("A6:A7", "Cantones", formatvariable)
    pagine.merge_range("B6:B7", "Distrito", formatvariable)
    pagine.merge_range("C6:C7", "Poblado", formatvariable)

    pagine.merge_range("D6:K6", "Afectación", formatvariablegray)

    pagine.write("D7", "Actividad o Productos", formatvariable_afe)
    pagine.write("E7", "N° de Fincas o Productores", formatvariable_afe)
    pagine.write("F7", "Área Afectada (Ha.)", formatvariable_afe)
    pagine.write(
        "G7", "Cantidades Estimadas (volumen producido ton.)", formatvariable_afe
    )
    pagine.write("H7", "Insumos / cantidad", formatvariable_afe2)
    pagine.write("I7", "Infraestructura Agrícola (m2, metros)", formatvariable_afe2)
    pagine.write("J7", "Naturaleza de Daños", formatvariable_afe)
    pagine.write("K7", "Monto Estimado de Pérdidas", formatvariable_afe2)

    pagine.merge_range(
        "L6:Q6",
        "PLAN DE ATENCIÓN, REHABILITACIÓN Y RECONSTRUCCIÓN ",
        formatvariablegray,
    )

    pagine.write("L7", "Nivel de Prioridad", formatvariable_afe2)
    pagine.write("M7", "Fase", formatvariable_afe2)
    pagine.write("N7", "Programas, Proyectos,  Acciones, Obras", formatvariable_afe2)
    pagine.write("O7", "Instituciones Involucradas", formatvariable_afe)
    pagine.write("P7", "Plazo", formatvariable_afe2)
    pagine.write("Q7", "Monto Estimado", formatvariable_afe2)

    # PRIMARIAS
    sql = (
        "select "
        "    M.id_formulario,"
        "    C.canton2_des,"
        "    actividad_label,"
        "    sum((IFNULL(area_arrasada_prin,0) + IFNULL(area_anegada_prin,0) + IFNULL(area_volcamiento_plantas_prin,0) + IFNULL(area_exceso_lluvia_prin,0) ) ) as area_afectada,"
        "	 sum(((IFNULL(area_arrasada_prin,0) * IFNULL((select i_p_arrasada from formshare.cne_cultivos where Nombre = actividad_label),0) )+ (IFNULL(area_anegada_prin,0) * IFNULL((select i_p_anegada from formshare.cne_cultivos where Nombre = actividad_label),0) ) + (IFNULL(area_volcamiento_plantas_prin,0) * IFNULL((select i_p_volcamiento from formshare.cne_cultivos where Nombre = actividad_label),0) ) + (IFNULL(area_exceso_lluvia_prin,0) ) * IFNULL((select i_p_excesolluvia from formshare.cne_cultivos where Nombre = actividad_label),0) ) ) as area_establecimiento, "
        "    sum(((IFNULL(area_arrasada_prin,0) * IFNULL((select i_c_arrasada from formshare.cne_cultivos where Nombre = actividad_label),0) )+ (IFNULL(area_anegada_prin,0) * IFNULL((select i_c_anegado from formshare.cne_cultivos where Nombre = actividad_label),0) ) + (IFNULL(area_volcamiento_plantas_prin,0) * IFNULL((select i_c_volcamiento from formshare.cne_cultivos where Nombre = actividad_label),0) ) + (IFNULL(area_exceso_lluvia_prin,0) ) * IFNULL((select i_c_excesolluvia from formshare.cne_cultivos where Nombre = actividad_label),0) ) ) as area_costo, "
        "    D.distrito2_des"
        " from "
        "	maintable M, "
        "    repite_para_saber_fechas_distintas_prin RPSFDP, "
        "    lkpcanton2 C,"
        "    lkpdistrito2 D"
        " where "
        "	M.sector_productivo in (1,3) AND "
        "    M.id_formulario = RPSFDP.id_formulario AND "
        "    M.canton2 = C.canton2_cod AND"
        "    M.distrito2 = D.distrito2_cod "
        " group by"
        "    M.id_formulario,"
        "    C.canton2_des,"
        "    actividad_label, "
        "    D.distrito2_des"
    )

    queryResults = engine.execute(sql).fetchall()

    summaryInformationForTable8 = []

    for result in queryResults:
        if result[3] > 0:
            summaryInformationForTable8.append(
                [
                    result[1],
                    result[2],
                    result[3],
                    result[6],
                    result[4],
                    "prin",
                    result[5],
                ]
            )

    # SECUNDARIAS
    secondaryProductsQuery = (
        "select "
        "	M.id_formulario,"
        "    C.canton2_des,"
        "    cultivo_preguntando,"
        "    sum((IFNULL(area_arrasada,0) + IFNULL(area_anegada,0) + IFNULL(area_volcamiento_plantas,0) + IFNULL(area_exceso_lluvia,0) ) ) as area_afectada,"
        "	 sum(((IFNULL(area_arrasada,0) * IFNULL((select i_p_arrasada from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) )+ (IFNULL(area_anegada,0) * IFNULL((select i_p_anegada from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) ) + (IFNULL(area_volcamiento_plantas,0) * IFNULL((select i_p_volcamiento from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) ) + (IFNULL(area_exceso_lluvia,0) ) * IFNULL((select i_p_excesolluvia from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) ) ) as area_establecimiento, "
        "    sum(((IFNULL(area_arrasada,0) * IFNULL((select i_c_arrasada from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) )+ (IFNULL(area_anegada,0) * IFNULL((select i_c_anegado from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) ) + (IFNULL(area_volcamiento_plantas,0) * IFNULL((select i_c_volcamiento from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) ) + (IFNULL(area_exceso_lluvia,0) ) * IFNULL((select i_c_excesolluvia from formshare.cne_cultivos where Nombre = cultivo_preguntando),0) ) ) as area_costo,"
        "    D.distrito2_des"
        " from "
        "	maintable M, "
        "    cuadro_de_perdida_de_plantaciones CDPDP,"
        "    repite_para_saber_fechas_distintas RPSFD, "
        "    lkpcanton2 C,"
        "    lkpdistrito2 D"
        " where "
        "	M.sector_productivo in (1,3) AND "
        "    M.id_formulario = CDPDP.id_formulario AND"
        "    CDPDP.id_formulario = RPSFD.id_formulario AND"
        "    CDPDP.cuadro_de_perdida_de_plantaciones_rowid = RPSFD.cuadro_de_perdida_de_plantaciones_rowid AND"
        "    M.canton2 = C.canton2_cod AND"
        "    M.distrito2 = D.distrito2_cod "
        " group by"
        "	M.id_formulario,"
        "    C.canton2_des,"
        "    cultivo_preguntando,"
        "    D.distrito2_des"
    )

    queryResults = engine.execute(sql).fetchall()

    for result in queryResults:
        if result[3] > 0:
            summaryInformationForTable8.append(
                [
                    result[1],
                    result[2],
                    result[3],
                    result[6],
                    result[4],
                    "secun",
                    result[5],
                ]
            )

    products = []
    rowInExcell = 8

    for data in summaryInformationForTable8:
        products.append(data[1])
        products = list(set(products))
        products.sort()

    counterProducts = 0
    generalFarms = 0
    generalArea = 0
    generalCost = 0

    for producto in products:
        totalAreaAffected = 0
        totalForCalculate = 0
        totalForCalculate2 = 0
        totalOfFarms = 0
        conty = []
        district = []

        for data in summaryInformationForTable8:

            if data[1] == producto:

                totalAreaAffected = totalAreaAffected + data[2]

                if data[5] == "prin":
                    totalOfFarms = totalOfFarms + 1

                totalForCalculate = totalForCalculate + data[4]
                totalForCalculate2 = totalForCalculate2 + data[6]

                conty.append(data[0])
                district.append(data[3])

        # Empezamos a escribir en el documento de excell
        generalFarms = generalFarms + totalOfFarms
        generalArea = generalArea + totalAreaAffected
        if totalAreaAffected > 0:

            contys = ""
            districts = ""
            for con in list(set(conty)):
                contys = contys + con + "\n"

            for dis in list(set(district)):
                districts = districts + dis + "\n"

            pagine.write("A" + str(rowInExcell), contys)
            pagine.write("B" + str(rowInExcell), districts)
            pagine.write("D" + str(rowInExcell), producto)
            pagine.write("E" + str(rowInExcell), totalOfFarms)
            pagine.write("F" + str(rowInExcell), totalAreaAffected)
            pagine.write("G" + str(rowInExcell), totalForCalculate)
            pagine.write("H" + str(rowInExcell), totalForCalculate2)

            queryForProductCost = (
                "SELECT IFNULL(costoestablecimiento,0), IFNULL(costocosecha,0) "
                "FROM formshare.cne_cultivos WHERE Nombre = '{}';".format(producto)
            )

            queryResultsOfCost = engine.execute(queryForProductCost).fetchone()

            costoEstablecimiento = 0
            costoCosecha = 0

            if queryResultsOfCost:
                costoEstablecimiento = queryResultsOfCost[0]
                costoCosecha = queryResultsOfCost[1]

            calculo = float(totalForCalculate) * float(costoEstablecimiento)
            calculo2 = float(totalForCalculate2) * float(costoCosecha)

            pagine.write("K" + str(rowInExcell), calculo + calculo2)
            generalCost = generalCost + calculo + calculo2

        rowInExcell = rowInExcell + 1

    pagine.write("A" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("B" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("C" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("D" + str(rowInExcell), "Total", formatvariable_afe2)
    pagine.write("E" + str(rowInExcell), generalFarms, formatvariable_afe2)
    pagine.write("F" + str(rowInExcell), generalArea, formatvariable_afe2)
    pagine.write("G" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("H" + str(rowInExcell), "Total", formatvariable_afe2)
    pagine.write("I" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("J" + str(rowInExcell), "Total", formatvariable_afe2)
    pagine.write("K" + str(rowInExcell), generalCost, formatvariable_afe2)
    pagine.write("L" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("M" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("N" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("O" + str(rowInExcell), "", formatvariable_afe2)
    pagine.write("P" + str(rowInExcell), "Total", formatvariable_afe2)
    pagine.write("Q" + str(rowInExcell), "", formatvariable_afe2)

    archive.close()
    engine.dispose()
