"""
Equivalencias y normalización de cargos.

Este archivo transforma las diferentes formas de escribir
un cargo en un nombre estándar antes de aplicar las reglas.

Ejemplos:

    "Op. Campo" -> "OPERADOR DE CAMPO"
    "Ing. Mantenimiento" -> "INGENIERO DE MANTENIMIENTO"
    "Operadora" -> "OPERADOR"
    "Supervisor Coque 2" -> "SUPERVISOR"
"""

import re
import unicodedata


# ============================================================
# NORMALIZACIÓN GENERAL
# ============================================================

def normalizar_texto_cargo(valor) -> str:
    """
    Limpia un cargo para poder compararlo.

    - Elimina tildes.
    - Convierte a mayúsculas.
    - Reemplaza signos por espacios.
    - Elimina espacios repetidos.
    """
    if valor is None:
        return ""

    texto = str(valor).strip()

    texto = unicodedata.normalize(
        "NFKD",
        texto,
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = texto.upper()

    texto = re.sub(
        r"[^A-Z0-9]+",
        " ",
        texto,
    )

    return re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()


# ============================================================
# EQUIVALENCIAS EXACTAS
# ============================================================

EQUIVALENCIAS_EXACTAS = {
    # --------------------------------------------------------
    # OPERADOR GENERAL
    # --------------------------------------------------------
    "OPERADOR": "OPERADOR",
    "OPERADORA": "OPERADOR",
    "OP": "OPERADOR",

    # --------------------------------------------------------
    # OPERADOR DE CAMPO
    # --------------------------------------------------------
    "OP CAMPO": "OPERADOR DE CAMPO",
    "OP DE CAMPO": "OPERADOR DE CAMPO",
    "OP CAMPO FCC": "OPERADOR DE CAMPO",
    "OP CAMPO FCC2": "OPERADOR DE CAMPO",
    "OPERADOR CAMPO": "OPERADOR DE CAMPO",
    "OPERADOR DE CAMPO": "OPERADOR DE CAMPO",
    "OPERADORA DE CAMPO": "OPERADOR DE CAMPO",
    "AUXILIAR CAMPO": "AUXILIAR DE CAMPO",
    "AUXILIAR DE CAMPO": "AUXILIAR DE CAMPO",

    # --------------------------------------------------------
    # OPERADOR DE CONSOLA
    # --------------------------------------------------------
    "OP DE CONSOLA": "OPERADOR DE CONSOLA",
    "OP CONSOLA": "OPERADOR DE CONSOLA",
    "OPERADOR CONSOLA": "OPERADOR DE CONSOLA",
    "OPERADOR DE CONSOLA": "OPERADOR DE CONSOLA",
    "OPERADORA DE CONSOLA": "OPERADOR DE CONSOLA",
    "OPERADOR DE CONSOLA COMPLEJA": "OPERADOR DE CONSOLA",
    "OPERADOR CONSOLA COMPLEJA": "OPERADOR DE CONSOLA",
    "OPERADOR DE CONSOLA SIMPLE": "OPERADOR DE CONSOLA",
    "OPERADOR CONSOLA SIMPLE": "OPERADOR DE CONSOLA",
    "OPERADOR CONSOLA SIMPLE CLAUS": "OPERADOR DE CONSOLA",
    "OPERADOR DE CONSOLA CLAUS": "OPERADOR DE CONSOLA",
    "OPERADOR DE CLAUS": "OPERADOR DE CONSOLA",
    "OPERADOR CLAUS": "OPERADOR DE CONSOLA",

    # --------------------------------------------------------
    # SUBESTACIONES Y DISTRIBUCIÓN ELÉCTRICA
    # --------------------------------------------------------
    "OPERADOR DE SUBESTACION": "OPERADOR DE SUBESTACION",
    "OPERADOR DE SUBESTACIONES": "OPERADOR DE SUBESTACION",
    "OPERADOR SUBESTACION": "OPERADOR DE SUBESTACION",
    "OPERADOR DE SUBESTACION ELECTRICA": "OPERADOR DE SUBESTACION",
    "OPERADOR DE SUBESTACIONES ELECTRICAS": "OPERADOR DE SUBESTACION",
    "DISTRIBUCION ELECTRICA": "DISTRIBUCION ELECTRICA",
    "OPERADOR DE DISTRIBUCION ELECTRICA": "DISTRIBUCION ELECTRICA",

    # --------------------------------------------------------
    # SUPERVISIÓN GENERAL
    # --------------------------------------------------------
    "SUPERVISOR": "SUPERVISOR",
    "SUPERVISORA": "SUPERVISOR",
    "SUPERVISION": "SUPERVISOR",
    "SUPERVIDOR": "SUPERVISOR",
    "SUPERVISOR DE PRODUCCION": "SUPERVISOR DE PRODUCCION",
    "SUPERVISOR PRODUCCION": "SUPERVISOR DE PRODUCCION",
    "SUP PRODUCCION": "SUPERVISOR DE PRODUCCION",
    "SUPERVISOR DE INSTRUMENTOS": "SUPERVISOR DE INSTRUMENTOS",
    "SUPERVISOR INSTRUMENTOS": "SUPERVISOR DE INSTRUMENTOS",
    "SUP INSTRUMENTOS": "SUPERVISOR DE INSTRUMENTOS",
    "SUPERVISOR TRATAMIENTO DE AGUAS": "SUPERVISOR",
    "SUPERVISOR DE TRATAMIENTO DE AGUAS": "SUPERVISOR",
    "SUPERVISOR COQUE 2": "SUPERVISOR",
    "SUPERVISOR COQUE II": "SUPERVISOR",
    "SUPERVISOR BOMBERO": "SUPERVISOR",
    "SUPERVISOR CONTROL EMERGENCIAS": "SUPERVISOR",

    # --------------------------------------------------------
    # SUPERVISIÓN DE MANTENIMIENTO
    # --------------------------------------------------------
    "SUP MANT": "SUPERVISOR DE MANTENIMIENTO",
    "SUP MTTO": "SUPERVISOR DE MANTENIMIENTO",
    "SUP MTO": "SUPERVISOR DE MANTENIMIENTO",
    "SUPERVISOR MANTENIMIENTO": "SUPERVISOR DE MANTENIMIENTO",
    "SUPERVISOR DE MANTENIMIENTO": "SUPERVISOR DE MANTENIMIENTO",
    "SUPERVISORA DE MANTENIMIENTO": "SUPERVISOR DE MANTENIMIENTO",
    "MECANICA": "MECANICA",
    "SOLICITANTE": "SOLICITANTE",
    "OBRA CIVIL": "OBRA CIVIL",
    "ADMINISTRADOR DE OBRA": "ADMINISTRADOR DE OBRA",
    "ADMINISTRADOR OBRA": "ADMINISTRADOR DE OBRA",

    # --------------------------------------------------------
    # INGENIERÍA Y PROYECTOS
    # --------------------------------------------------------
    "INGENIERO DE PROYECTO": "INGENIERO DE PROYECTO",
    "INGENIERO DE PROYECTOS": "INGENIERO DE PROYECTO",
    "ING DE PROYECTO": "INGENIERO DE PROYECTO",
    "ING PROYECTO": "INGENIERO DE PROYECTO",
    "INGENIERA DE PROYECTO": "INGENIERO DE PROYECTO",

    "LIDER PROYECTO": "LIDER DE PROYECTO",
    "LIDER PROYECTOS": "LIDER DE PROYECTO",
    "LIDER DE PROYECTO": "LIDER DE PROYECTO",
    "LIDER DE PROYECTOS": "LIDER DE PROYECTO",

    "COORDINADOR DE PROYECTO": "COORDINADOR",
    "COORDINADOR DE PROYECTOS": "COORDINADOR",
    "COORDINADORA DE PROYECTO": "COORDINADOR",
    "COORDINADORA DE PROYECTOS": "COORDINADOR",
    "COORDINADOR DE OBRAS": "COORDINADOR",
    "COORDINADOR DE OBRA": "COORDINADOR",
    "COORDINADOR PERFORACIONES CILC": "COORDINADOR",
    "COORDINADOR MAS": "COORDINADOR",

    "ING MANTENIMIENTO": "INGENIERO DE MANTENIMIENTO",
    "ING DE MANTENIMIENTO": "INGENIERO DE MANTENIMIENTO",
    "INGENIERO MANTENIMIENTO": "INGENIERO DE MANTENIMIENTO",
    "INGENIERO DE MANTENIMIENTO": "INGENIERO DE MANTENIMIENTO",
    "INGENIERA DE MANTENIMIENTO": "INGENIERO DE MANTENIMIENTO",

    "INGENIERIA": "INGENIERIA",
    "INGENIERIA DE PROCESOS": "INGENIERIA",
    "ING PROCESOS": "INGENIERIA",
    "INGENIERO DE PROCESOS": "INGENIERIA",

    # --------------------------------------------------------
    # OPERACIONES
    # --------------------------------------------------------
    "ANALISTA DE OPERACIONES": "ANALISTA DE OPERACIONES",
    "ANALISTA OPERACIONES": "ANALISTA DE OPERACIONES",

    # --------------------------------------------------------
    # ANALISTA DE GASES
    # --------------------------------------------------------
    "ANALISTA DE GAS": "ANALISTA DE GASES",
    "ANALISTA DE GASES": "ANALISTA DE GASES",
    "ANALISTA GASES": "ANALISTA DE GASES",
    "ANALG": "ANALISTA DE GASES",
    "ANALISTA MEDIO AMBIENTE": "ANALISTA DE SEGURIDAD",
    "ANALISTA AMBIENTAL": "ANALISTA DE SEGURIDAD",

    # --------------------------------------------------------
    # PAROS
    # --------------------------------------------------------
    "INSPECTOR PAROS": "INSPECTOR DE PAROS",
    "INSPECTOR DE PAROS": "INSPECTOR DE PAROS",
    "ANALISTA DE PAROS": "INSPECTOR DE PAROS",
    "ANALISTA PAROS": "INSPECTOR DE PAROS",
    "PROGRAMADOR DE PAROS": "INSPECTOR DE PAROS",
    "PROGRAMADOR DE PARO": "INSPECTOR DE PAROS",
    "PROGRAMADOR PARO": "INSPECTOR DE PAROS",
    "INSPECTOR DE PARO": "INSPECTOR DE PAROS",

    # --------------------------------------------------------
    # INSPECCIÓN DE OBRAS
    # --------------------------------------------------------
    "INSPECTOR OBRAS": "INSPECTOR DE OBRAS",
    "INSPECTOR DE OBRAS": "INSPECTOR DE OBRAS",
    "INSPECTOR DE OBRA": "INSPECTOR DE OBRAS",
    "INSPECTOR DE OBRAD": "INSPECTOR DE OBRAS",
    "INSPECCION Y OBRAS": "INSPECTOR DE OBRAS",

    # --------------------------------------------------------
    # PLANIFICACIÓN Y MANTENIMIENTO
    # --------------------------------------------------------
    "PLANIFICADOR MTTO RUTINARIO": "PLANIFICADOR DE MANTENIMIENTO",
    "PLANIFICADOR MTO": "PLANIFICADOR DE MANTENIMIENTO",
    "PLANIFICADOR MTTO": "PLANIFICADOR DE MANTENIMIENTO",
    "PLANIFICADOR DE MANTENIMIENTO": "PLANIFICADOR DE MANTENIMIENTO",
    "PLANIFICADOR MECANICA": "PLANIFICADOR DE MANTENIMIENTO",
    "PROGRAMADOR DE MANTENIMIENTO DIARIO": "PLANIFICADOR DE MANTENIMIENTO",
    "ANALISTA PLANIFICACION DE RUTINA": "PLANIFICADOR DE MANTENIMIENTO",
    "ANALISTA PLANIFICADOR MANTENIMIENTO MECANICO": "PLANIFICADOR DE MANTENIMIENTO",
    "ANALISTA DE PLANIFICACION DE MANTENIMIENTO": "PLANIFICADOR DE MANTENIMIENTO",

    "INSPECTOR DE MANTENIMIENTO": "INSPECTOR DE MANTENIMIENTO",
    "INSPECTOR MANTENIMIENTO": "INSPECTOR DE MANTENIMIENTO",

    "INSTRUMENTOS": "SUPERVISOR DE MANTENIMIENTO",
    "MTO ELECTRICO": "SUPERVISOR DE MANTENIMIENTO",
    "MTTO ELECTRICO": "SUPERVISOR DE MANTENIMIENTO",
    "SUP ESTATICOS": "SUPERVISOR DE MANTENIMIENTO",
    "JEFE MANTENIMIENTO DE ESTATICOS": "SUPERVISOR DE MANTENIMIENTO",
    "JEFE DE EQUIPOS DINAMICOS": "SUPERVISOR DE MANTENIMIENTO",

    # --------------------------------------------------------
    # JEFATURAS
    # --------------------------------------------------------
    "JEFE DE PLANTA": "JEFE DE PLANTA",
    "JEFA DE PLANTA": "JEFE DE PLANTA",
    "JEFE PLANTA": "JEFE DE PLANTA",
    "JEFA PLANTA": "JEFE DE PLANTA",
    "JEFE DE ALMACEN": "JEFE DE ALMACEN",
    "JEFA DE ALMACEN": "JEFE DE ALMACEN",

    # --------------------------------------------------------
    # GERENCIAS
    # --------------------------------------------------------
    "GERENTE": "GERENTE",
    "GERENTE PMA": "GERENTE",
    "GERENTE PLANIFICACION Y RTIC": "GERENTE",

    # --------------------------------------------------------
    # OTROS SOLICITANTES
    # --------------------------------------------------------
    "CONSULTOR": "CONSULTOR",
    "CONSULTORA": "CONSULTOR",
    "PROCESISTA": "PROCESISTA",
    "INSPECTOR": "INSPECTOR",
    "BOMBERO": "BOMBERO",

    # --------------------------------------------------------
    # PASANTES
    # --------------------------------------------------------
    "PASANTE": "PASANTE",
    "PASANTE DE OPERACIONES": "PASANTE",
    "PASANTE DE PROCESOS": "PASANTE",
    "PASANTE DE INSPECCION": "PASANTE",

    # --------------------------------------------------------
    # SEGURIDAD OPERATIVA
    #
    # Solamente estos cargos reciben Módulo 6.
    # --------------------------------------------------------
    "SEGURIDAD OPERATIVA": "SEGURIDAD OPERATIVA",
    "ANALISTA DE SEGURIDAD OPERATIVA": "ANALISTA DE SEGURIDAD OPERATIVA",
    "ANALISTA SEGURIDAD OPERATIVA": "ANALISTA DE SEGURIDAD OPERATIVA",
    "JEFE DE SEGURIDAD OPERATIVA": "JEFE DE SEGURIDAD OPERATIVA",
    "JEFA DE SEGURIDAD OPERATIVA": "JEFE DE SEGURIDAD OPERATIVA",
    "JEFE SEGURIDAD OPERATIVA": "JEFE DE SEGURIDAD OPERATIVA",

    # --------------------------------------------------------
    # SEGURIDAD GENERAL
    #
    # Estos cargos reciben rol Ejecutante.
    # No se deben convertir en Seguridad Operativa.
    # --------------------------------------------------------
    "TECNICO DE SEGURIDAD": "TECNICO DE SEGURIDAD",
    "TECNICO EN SEGURIDAD": "TECNICO DE SEGURIDAD",
    "TECNICA DE SEGURIDAD": "TECNICO DE SEGURIDAD",
    "TECNICA EN SEGURIDAD": "TECNICO DE SEGURIDAD",
    # --------------------------------------------------------
    # REPRESENTANTE TÉCNICO - CONTRATISTAS
    # --------------------------------------------------------
    "RT": "REPRESENTANTE TECNICO",
    "R TECNICO": "REPRESENTANTE TECNICO",
    "RTE TECNICO": "REPRESENTANTE TECNICO",
    "REPRESENTANTE TECNICO": "REPRESENTANTE TECNICO",
    "REPRESENTATE TECNICO": "REPRESENTANTE TECNICO",

    "RESPONSABLE DE SEGURIDAD": "RESPONSABLE DE SEGURIDAD",
    "RESPONSABLE DE HIGIENE Y SEGURIDAD": "RESPONSABLE DE SEGURIDAD",
    "RESPONSABLE HYS": "RESPONSABLE DE SEGURIDAD",
    "COORD HYS": "RESPONSABLE DE SEGURIDAD",
    "COORDINADOR HYS": "RESPONSABLE DE SEGURIDAD",
    "LIC SEGURIDAD E HIGIENE": "RESPONSABLE DE SEGURIDAD",
    "LICENCIADO EN SEGURIDAD E HIGIENE": "RESPONSABLE DE SEGURIDAD",
    "RESPONSABLE DE SEGURIDAD SALUD Y MEDIOAMBIENTE": "RESPONSABLE DE SEGURIDAD",
    "LICENCIADO CALIDAD MEDIO AMBIENTE Y SEGURIDAD E HIGIENE": (
        "RESPONSABLE DE SEGURIDAD"
    ),
}


# ============================================================
# REGLAS POR PALABRAS
# ============================================================

REGLAS_CONTIENE = [
    # --------------------------------------------------------
    # Las reglas más específicas deben ir primero.
    # --------------------------------------------------------

    (
        ["SEGURIDAD", "OPERATIVA"],
        "SEGURIDAD OPERATIVA",
    ),

    (
        ["ANALISTA", "GAS"],
        "ANALISTA DE GASES",
    ),

    (
        ["SUPERVISOR", "MANTENIMIENTO"],
        "SUPERVISOR DE MANTENIMIENTO",
    ),

    (
        ["SUPERVISOR", "MTTO"],
        "SUPERVISOR DE MANTENIMIENTO",
    ),

    (
        ["SUPERVISOR", "MTO"],
        "SUPERVISOR DE MANTENIMIENTO",
    ),

    (
        ["OPERADOR", "SUBESTACION"],
        "OPERADOR DE SUBESTACION",
    ),

    (
        ["DISTRIBUCION", "ELECTRICA"],
        "DISTRIBUCION ELECTRICA",
    ),

    (
        ["OPERADOR", "CONSOLA"],
        "OPERADOR DE CONSOLA",
    ),

    (
        ["OPERADOR", "CLAUS"],
        "OPERADOR DE CONSOLA",
    ),

    (
        ["OPERADOR", "CAMPO"],
        "OPERADOR DE CAMPO",
    ),

    (
        ["AUXILIAR", "CAMPO"],
        "AUXILIAR DE CAMPO",
    ),

    (
        ["INGENIERO", "MANTENIMIENTO"],
        "INGENIERO DE MANTENIMIENTO",
    ),

    (
        ["INGENIERO", "PROYECTO"],
        "INGENIERO DE PROYECTO",
    ),

    (
        ["LIDER", "PROYECTO"],
        "LIDER DE PROYECTO",
    ),

    (
        ["COORDINADOR", "PROYECTO"],
        "COORDINADOR",
    ),

    (
        ["INSPECTOR", "OBRA"],
        "INSPECTOR DE OBRAS",
    ),

    (
        ["INSPECTOR", "MANTENIMIENTO"],
        "INSPECTOR DE MANTENIMIENTO",
    ),

    (
        ["PROGRAMADOR", "PARO"],
        "INSPECTOR DE PAROS",
    ),

    (
        ["ANALISTA", "PARO"],
        "INSPECTOR DE PAROS",
    ),

    (
        ["PLANIFICADOR", "MANTENIMIENTO"],
        "PLANIFICADOR DE MANTENIMIENTO",
    ),

    (
        ["RESPONSABLE", "SEGURIDAD"],
        "RESPONSABLE DE SEGURIDAD",
    ),

    (
        ["RESPONSABLE", "HIGIENE"],
        "RESPONSABLE DE SEGURIDAD",
    ),

    (
        ["TECNICO", "SEGURIDAD"],
        "TECNICO DE SEGURIDAD",
    ),

    (
        ["SUPERVISOR", "PRODUCCION"],
        "SUPERVISOR DE PRODUCCION",
    ),

    (
        ["SUPERVISOR"],
        "SUPERVISOR",
    ),

    (
        ["PASANTE"],
        "PASANTE",
    ),

    (
        ["REPRESENTANTE", "TECNICO"],
        "REPRESENTANTE TECNICO",
    ),
]


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def obtener_cargo_estandar(cargo) -> str:
    """
    Devuelve el nombre estándar de un cargo.

    Orden de búsqueda:

    1. Limpia el texto.
    2. Busca una equivalencia exacta.
    3. Busca una regla por palabras clave.
    4. Si no encuentra coincidencia, devuelve el cargo limpio.

    Devolver el cargo limpio permite que reglas.py lo muestre
    en la hoja de pendientes.
    """
    cargo_limpio = normalizar_texto_cargo(
        cargo
    )

    if not cargo_limpio:
        return ""

    # --------------------------------------------------------
    # EQUIVALENCIA EXACTA
    # --------------------------------------------------------
    if cargo_limpio in EQUIVALENCIAS_EXACTAS:
        return EQUIVALENCIAS_EXACTAS[
            cargo_limpio
        ]

    # --------------------------------------------------------
    # REGLAS POR PALABRAS
    # --------------------------------------------------------
    palabras_cargo = set(
        cargo_limpio.split()
    )

    for (
        palabras_necesarias,
        cargo_estandar,
    ) in REGLAS_CONTIENE:
        if all(
            palabra in palabras_cargo
            for palabra in palabras_necesarias
        ):
            return cargo_estandar

    # --------------------------------------------------------
    # SIN EQUIVALENCIA
    # --------------------------------------------------------
    return cargo_limpio