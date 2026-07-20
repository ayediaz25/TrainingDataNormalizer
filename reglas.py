"""
Reglas de asignación de roles y módulos PETRA.

Proceso general:

1. Se normaliza el cargo mediante equivalencias.py.
2. Se identifica si la persona es contratista o personal propio YPF.
3. Se asigna el rol PETRA.
4. Se asignan los módulos correspondientes.

Reglas principales:

- Contratistas:
    Módulo 1 + Módulo 4 Ejecutante.

- Personal propio YPF:
    El rol depende del cargo.

- Cuando el empleador está vacío:
    Si el cargo es reconocido como un cargo YPF, se infiere
    que corresponde a personal propio YPF.
"""

import re
import unicodedata

from equivalencias import obtener_cargo_estandar


# ============================================================
# MÓDULOS
# ============================================================

MODULO_1 = (
    "Módulo 1| Introducción, matriz, categorización "
    "de tareas, procesos"
)

MODULO_4_EMISOR = (
    "Módulo 4| PeTra-emisor"
)

MODULO_4_VERIFICADOR = (
    "Módulo 4| PeTra- verificador"
)

MODULO_4_AUTORIZANTE = (
    "Módulo 4| PeTra- autorizante"
)

MODULO_4_SOLICITANTE = (
    "Módulo 4| PeTra- solicitante"
)

MODULO_4_EJECUTANTE = (
    "Módulo 4| PeTra- ejecutante"
)

MODULO_4_ANALISTA_GAS = (
    "Módulo 4| PeTra- analista de gases"
)

MODULO_6_FORMADORES = (
    "Módulo 6| Formación de formadores"
)


# ============================================================
# UTILIDADES GENERALES
# ============================================================

def normalizar(valor) -> str:
    """
    Normaliza cualquier texto para realizar comparaciones.

    - Elimina tildes.
    - Convierte a mayúsculas.
    - Reemplaza caracteres especiales por espacios.
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


def es_contratista(empleador) -> bool:
    """
    Detecta si el empleador indica que la persona
    pertenece a una empresa contratista.
    """
    texto = normalizar(
        empleador
    )

    return (
        "CONTRATISTA" in texto
        or "TERCERO" in texto
        or "EXTERNO" in texto
    )


def es_personal_ypf(empleador) -> bool:
    """
    Detecta si el empleador indica que la persona
    pertenece a personal propio YPF.
    """
    texto = normalizar(
        empleador
    )

    return (
        "YPF" in texto
        or "PERSONAL PROPIO" in texto
        or texto == "PROPIO"
        or texto == "INTERNO"
    )


def empleador_esta_vacio(empleador) -> bool:
    """
    Indica si el campo empleador está vacío.
    """
    return normalizar(
        empleador
    ) == ""


def construir_resultado(
    rol: str,
    modulos: list[str],
    regla: str,
) -> dict:
    """
    Devuelve siempre el resultado con la misma estructura.
    """
    return {
        "rol": rol,
        "modulos": modulos,
        "regla": regla,
    }


# ============================================================
# CONFIGURACIÓN DE ROLES
# ============================================================

CONFIGURACION_ROLES = {
    "Emisor": [
        MODULO_1,
        MODULO_4_EMISOR,
    ],

    "Verificador": [
        MODULO_1,
        MODULO_4_VERIFICADOR,
    ],

    "Autorizante": [
        MODULO_1,
        MODULO_4_AUTORIZANTE,
    ],

    "Solicitante": [
        MODULO_1,
        MODULO_4_SOLICITANTE,
    ],

    "Ejecutante": [
        MODULO_1,
        MODULO_4_EJECUTANTE,
    ],

    "Analista de Gas": [
        MODULO_1,
        MODULO_4_ANALISTA_GAS,
    ],

    "Analista de Seguridad": [
    MODULO_1,
    MODULO_4_ANALISTA_GAS,
    ],

    "Formación de formadores": [
        MODULO_1,
        MODULO_6_FORMADORES,
    ],
}


# ============================================================
# MATRIZ EXACTA DE CARGOS YPF
# ============================================================

REGLAS_YPF = {
    # --------------------------------------------------------
    # EMISORES
    # --------------------------------------------------------
    "OPERADOR": "Emisor",
    "OPERADOR DE CAMPO": "Emisor",
    "AUXILIAR DE CAMPO": "Emisor",

    # --------------------------------------------------------
    # VERIFICADORES
    # --------------------------------------------------------
    "OPERADOR DE CONSOLA": "Verificador",

    # --------------------------------------------------------
    # AUTORIZANTES
    # --------------------------------------------------------
    "SUPERVISOR": "Autorizante",
    "SUPERVISOR DE INSTRUMENTOS": "Autorizante",
    "SUPERVISOR DE PRODUCCION": "Autorizante",
    "OPERADOR DE SUBESTACION": "Autorizante",
    "DISTRIBUCION ELECTRICA": "Autorizante",
    "PASANTE": "Autorizante",

    # --------------------------------------------------------
    # SOLICITANTES
    # --------------------------------------------------------
    "SUPERVISOR DE MANTENIMIENTO": "Solicitante",
    "INGENIERO DE PROYECTO": "Solicitante",
    "INGENIERO DE MANTENIMIENTO": "Solicitante",
    "ANALISTA DE OPERACIONES": "Solicitante",
    "INSPECTOR DE PAROS": "Solicitante",
    "INSPECTOR DE OBRAS": "Solicitante",
    "INSPECTOR DE MANTENIMIENTO": "Solicitante",
    "PLANIFICADOR DE MANTENIMIENTO": "Solicitante",
    "JEFE DE PLANTA": "Solicitante",
    "JEFE DE ALMACEN": "Solicitante",
    "COORDINADOR": "Solicitante",
    "LIDER DE PROYECTO": "Solicitante",
    "GERENTE": "Solicitante",
    "CONSULTOR": "Solicitante",
    "INGENIERIA": "Solicitante",
    "PROCESISTA": "Solicitante",
    "INSPECTOR": "Solicitante",
    "BOMBERO": "Solicitante",
    "MECANICA": "Solicitante",
    "SOLICITANTE": "Solicitante",
    "OBRA CIVIL": "Solicitante",
    "ADMINISTRADOR DE OBRA": "Solicitante",

    # --------------------------------------------------------
    # EJECUTANTES YPF
    # --------------------------------------------------------
    "RESPONSABLE DE SEGURIDAD": "Ejecutante",
    "TECNICO DE SEGURIDAD": "Ejecutante",

    # --------------------------------------------------------
    # ANALISTA DE GAS
    # --------------------------------------------------------
    "ANALISTA DE GASES": "Analista de Gas",
    "ANALISTA DE SEGURIDAD": "Analista de Seguridad",

    # --------------------------------------------------------
    # FORMACIÓN DE FORMADORES
    # --------------------------------------------------------
    "SEGURIDAD OPERATIVA": "Formación de formadores",
    "ANALISTA DE SEGURIDAD OPERATIVA": "Formación de formadores",
    "JEFE DE SEGURIDAD OPERATIVA": "Formación de formadores",
}


# ============================================================
# REGLAS GENERALES POR FAMILIA DE CARGO
# ============================================================

def obtener_rol_ypf(
    cargo_estandar: str,
) -> str | None:
    """
    Busca el rol correspondiente a un cargo YPF.

    Primero revisa la matriz exacta.
    Después aplica reglas generales por palabras clave.

    El orden es importante para evitar asignaciones incorrectas.
    """
    cargo_normalizado = normalizar(
        cargo_estandar
    )

    if not cargo_normalizado:
        return None

    # --------------------------------------------------------
    # 1. Coincidencia exacta
    # --------------------------------------------------------
    if cargo_normalizado in REGLAS_YPF:
        return REGLAS_YPF[
            cargo_normalizado
        ]

    # --------------------------------------------------------
    # 2. Formación de formadores
    #
    # Tiene prioridad sobre otras reglas de seguridad.
    # --------------------------------------------------------
    if "SEGURIDAD OPERATIVA" in cargo_normalizado:
        return "Formación de formadores"

    # --------------------------------------------------------
    # 3. Analista de gases
    # --------------------------------------------------------
    if (
        "ANALISTA DE GAS" in cargo_normalizado
        or "ANALISTA DE GASES" in cargo_normalizado
    ):
        return "Analista de Gas"

    # --------------------------------------------------------
    # 4. Supervisor de mantenimiento
    #
    # Es el único supervisor Solicitante.
    # Debe evaluarse antes de la regla general Supervisor.
    # --------------------------------------------------------
    if (
        "SUPERVISOR" in cargo_normalizado
        and (
            "MANTENIMIENTO" in cargo_normalizado
            or "MTTO" in cargo_normalizado
            or "MTO" in cargo_normalizado
        )
    ):
        return "Solicitante"

    # --------------------------------------------------------
    # 5. Operadores de consola
    #
    # Debe evaluarse antes de la regla general Operador.
    # --------------------------------------------------------
    if "CONSOLA" in cargo_normalizado:
        return "Verificador"

    # Algunas denominaciones de CLAUS representan
    # operador de consola.
    if (
        "OPERADOR" in cargo_normalizado
        and "CLAUS" in cargo_normalizado
    ):
        return "Verificador"

    # --------------------------------------------------------
    # 6. Distribución eléctrica y subestaciones
    # --------------------------------------------------------
    if (
        "SUBESTACION" in cargo_normalizado
        or "DISTRIBUCION ELECTRICA" in cargo_normalizado
    ):
        return "Autorizante"

    # --------------------------------------------------------
    # 7. Supervisores
    #
    # Todos los supervisores son Autorizantes,
    # excepto Supervisor de Mantenimiento.
    # --------------------------------------------------------
    if (
        "SUPERVISOR" in cargo_normalizado
        or "SUPERVISION" in cargo_normalizado
    ):
        return "Autorizante"

    # --------------------------------------------------------
    # 8. Pasantes
    # --------------------------------------------------------
    if "PASANTE" in cargo_normalizado:
        return "Autorizante"

    # --------------------------------------------------------
    # 9. Operadores y auxiliares de campo
    # --------------------------------------------------------
    if "AUXILIAR DE CAMPO" in cargo_normalizado:
        return "Emisor"

    if (
        "OPERADOR DE CAMPO" in cargo_normalizado
        or "OP CAMPO" in cargo_normalizado
    ):
        return "Emisor"

    # Cuando el cargo indica únicamente Operador u Operadora,
    # corresponde Emisor.
    if (
        cargo_normalizado == "OPERADOR"
        or cargo_normalizado == "OPERADORA"
    ):
        return "Emisor"

    # Cualquier otro operador no identificado como consola,
    # CLAUS, subestación o distribución eléctrica se toma
    # como Emisor.
    if "OPERADOR" in cargo_normalizado:
        return "Emisor"

    # --------------------------------------------------------
    # 10. Seguridad general
    #
    # Técnico o Responsable de Seguridad YPF:
    # rol Ejecutante.
    # --------------------------------------------------------
    if (
        "TECNICO" in cargo_normalizado
        and "SEGURIDAD" in cargo_normalizado
    ):
        return "Ejecutante"

    if (
        "RESPONSABLE" in cargo_normalizado
        and (
            "SEGURIDAD" in cargo_normalizado
            or "HIGIENE" in cargo_normalizado
            or "HYS" in cargo_normalizado
        )
    ):
        return "Ejecutante"

    # --------------------------------------------------------
    # 11. Solicitantes por familia
    # --------------------------------------------------------
    palabras_solicitante = [
        "INGENIERO",
        "INGENIERIA",
        "LIDER",
        "COORDINADOR",
        "GERENTE",
        "CONSULTOR",
        "PLANIFICADOR",
        "PROGRAMADOR",
        "INSPECTOR",
        "PROCESISTA",
        "JEFE",
        "BOMBERO",
    ]

    if any(
        palabra in cargo_normalizado
        for palabra in palabras_solicitante
    ):
        return "Solicitante"

    # Analista de operaciones.
    if (
        "ANALISTA" in cargo_normalizado
        and "OPERACION" in cargo_normalizado
    ):
        return "Solicitante"

    return None


def cargo_es_reconocido_ypf(
    cargo_estandar: str,
) -> bool:
    """
    Indica si el cargo permite inferir que la persona
    pertenece a personal propio YPF.

    Se utiliza cuando el empleador está vacío.
    """
    return obtener_rol_ypf(
        cargo_estandar
    ) is not None

# ============================================================
# INFERENCIA DEL ROL DESDE LOS MÓDULOS ORIGINALES
# ============================================================

def obtener_primer_rol_desde_modulos(
    modulos_originales,
) -> str | None:
    """
    Obtiene el primer rol encontrado en los módulos originales.

    Si existen dos módulos de rol diferentes, se respeta
    el orden original y se devuelve el primero.

    Ejemplo:
        Módulo 4 Ejecutante;
        Módulo 4 Solicitante;

    Resultado:
        Ejecutante
    """
    if modulos_originales is None:
        return None

    # Si llega una lista, se conserva el orden
    # y se convierte en una única cadena.
    if isinstance(
        modulos_originales,
        (list, tuple, set),
    ):
        texto_modulos = "; ".join(
            str(modulo)
            for modulo in modulos_originales
            if modulo is not None
        )
    else:
        texto_modulos = str(
            modulos_originales
        )

    if not texto_modulos.strip():
        return None

    # Se separan los módulos respetando el orden original.
    partes = re.split(
        r"[;\n]+",
        texto_modulos,
    )

    for parte in partes:
        modulo = normalizar(
            parte
        )

        if not modulo:
            continue

        # Formación de formadores
        if (
            "MODULO 6" in modulo
            and "FORMACION DE FORMADORES" in modulo
        ):
            return "Formación de formadores"

        # Analista de Gas
        if (
            "ANALISTA DE GAS" in modulo
            or "ANALISTA DE GASES" in modulo
        ):
            return "Analista de Gas"

        # Módulo 4 - Emisor
        if (
            "MODULO 4" in modulo
            and "EMISOR" in modulo
        ):
            return "Emisor"

        # Módulo 4 - Verificador
        if (
            "MODULO 4" in modulo
            and "VERIFICADOR" in modulo
        ):
            return "Verificador"

        # Módulo 4 - Autorizante
        if (
            "MODULO 4" in modulo
            and "AUTORIZANTE" in modulo
        ):
            return "Autorizante"

        # Módulo 4 - Solicitante
        if (
            "MODULO 4" in modulo
            and "SOLICITANTE" in modulo
        ):
            return "Solicitante"

        # Módulo 4 - Ejecutante
        if (
            "MODULO 4" in modulo
            and "EJECUTANTE" in modulo
        ):
            return "Ejecutante"

    # Si solamente tiene Módulo 1 u otros módulos
    # que no permiten deducir el rol, no se asigna nada.
    return None

# ============================================================
# REGLA PRINCIPAL
# ============================================================

def obtener_regla(
    cargo,
    empleador,
    modulos_originales=None,
) -> dict:
    """
    Devuelve el rol, los módulos esperados y la regla aplicada.

    Prioridad:

    1. Contratista:
       siempre Ejecutante.

    2. Cargo YPF reconocido:
       se utiliza la matriz de cargos.

    3. Cargo no reconocido:
       se toma el primer rol encontrado en los módulos
       originales.

    4. Sin cargo reconocido ni módulo de rol:
       queda Pendiente.
    """
    cargo_estandar = obtener_cargo_estandar(
            cargo
        )
    
    # REPRESENTANTE TÉCNICO
    # Se considera contratista aunque el empleador esté vacío.
    # --------------------------------------------------------

    if cargo_estandar == "REPRESENTANTE TECNICO":
        return construir_resultado(
            rol="Ejecutante",
            modulos=CONFIGURACION_ROLES[
                "Ejecutante"
            ],
            regla=(
                "Representante Técnico: "
                "se infiere personal contratista "
                "y se asigna Ejecutante"
            ),
        )
        
        


    # --------------------------------------------------------
    # 1. CONTRATISTAS
    # --------------------------------------------------------
    if es_contratista(
        empleador
    ):
        return construir_resultado(
            rol="Ejecutante",
            modulos=CONFIGURACION_ROLES[
                "Ejecutante"
            ],
            regla=(
                "Contratista: asignación automática "
                "de Ejecutante"
            ),
        )

    # --------------------------------------------------------
    # 2. BUSCAR ROL SEGÚN EL CARGO
    # --------------------------------------------------------
    rol_por_cargo = obtener_rol_ypf(
        cargo_estandar
    )

    if rol_por_cargo:
        if es_personal_ypf(
            empleador
        ):
            texto_regla = (
                "Personal propio YPF: "
                + cargo_estandar
            )
        elif empleador_esta_vacio(
            empleador
        ):
            texto_regla = (
                "Empleador vacío: se infiere personal "
                "propio YPF por cargo reconocido: "
                + cargo_estandar
            )
        else:
            texto_regla = (
                "Cargo reconocido: "
                + cargo_estandar
            )

        return construir_resultado(
            rol=rol_por_cargo,
            modulos=CONFIGURACION_ROLES[
                rol_por_cargo
            ],
            regla=texto_regla,
        )

    # --------------------------------------------------------
    # 3. INFERIR DESDE LOS MÓDULOS ORIGINALES
    # --------------------------------------------------------
    rol_por_modulo = obtener_primer_rol_desde_modulos(
        modulos_originales
    )

    if rol_por_modulo:
        return construir_resultado(
            rol=rol_por_modulo,
            modulos=CONFIGURACION_ROLES[
                rol_por_modulo
            ],
            regla=(
                "Cargo sin equivalencia: rol inferido "
                "desde el primer Módulo 4 o Módulo 6 "
                "encontrado: "
                + rol_por_modulo
            ),
        )

    # --------------------------------------------------------
    # 4. SIN INFORMACIÓN SUFICIENTE
    # --------------------------------------------------------
    if es_personal_ypf(
        empleador
    ):
        mensaje = (
            "Cargo YPF sin equivalencia y sin módulo "
            "de rol identificable: "
            + (
                cargo_estandar
                if cargo_estandar
                else "SIN CARGO"
            )
        )
    else:
        mensaje = (
            "Cargo y empleador sin regla confirmada, "
            "y sin módulo de rol identificable"
        )

    return construir_resultado(
        rol="Pendiente",
        modulos=[],
        regla=mensaje,
    )