# normalizador.py

from pathlib import Path
import re
import unicodedata

import pandas as pd

from reglas import obtener_regla


# ============================================================
# UTILIDADES DE LIMPIEZA
# ============================================================

def normalizar_texto(valor) -> str:
    """
    Convierte cualquier valor en texto limpio:
    - reemplaza valores vacíos por "";
    - elimina espacios al inicio y al final;
    - reemplaza múltiples espacios por uno solo.
    """
    if pd.isna(valor):
        return ""

    return re.sub(r"\s+", " ", str(valor).strip())


def normalizar_para_comparar(valor) -> str:
    """
    Normaliza un texto para comparaciones:
    - elimina tildes;
    - convierte a mayúsculas;
    - limpia espacios.
    """
    texto = normalizar_texto(valor)

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    return texto.upper()


def normalizar_dni(valor) -> str:
    """
    Conserva únicamente los números del DNI.

    Ejemplo:
        26.236.846 -> 26236846
    """
    if pd.isna(valor):
        return ""

    return re.sub(r"\D", "", str(valor))


def detectar_columna(
    columnas: list[str],
    nombres_posibles: list[str],
) -> str:
    """
    Busca una columna comparando nombres completos.
    """
    columnas_normalizadas = {
        normalizar_para_comparar(columna): columna
        for columna in columnas
    }

    for nombre in nombres_posibles:
        clave = normalizar_para_comparar(nombre)

        if clave in columnas_normalizadas:
            return columnas_normalizadas[clave]

    raise ValueError(
        "No se encontró ninguna de estas columnas: "
        + ", ".join(nombres_posibles)
    )


def detectar_columna_por_contenido(
    columnas: list[str],
    palabras_clave: list[str],
) -> str:
    """
    Busca una columna cuyo encabezado contenga alguna palabra clave.
    """
    for columna in columnas:
        columna_normalizada = normalizar_para_comparar(columna)

        for palabra in palabras_clave:
            palabra_normalizada = normalizar_para_comparar(palabra)

            if palabra_normalizada in columna_normalizada:
                return columna

    raise ValueError(
        "No se encontró una columna que contenga: "
        + ", ".join(palabras_clave)
    )


# ============================================================
# LECTURA DEL ARCHIVO
# ============================================================

def leer_archivo(ruta_archivo: str | Path) -> pd.DataFrame:
    """
    Lee archivos Excel, CSV o TXT.
    """
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta}"
        )

    extension = ruta.suffix.lower()

    if extension in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(
            ruta,
            dtype=str,
        )

    if extension == ".csv":
        return pd.read_csv(
            ruta,
            dtype=str,
        )

    if extension == ".txt":
        return pd.read_csv(
            ruta,
            sep="\t",
            dtype=str,
            header=None,
        )

    raise ValueError(
        f"Formato no permitido: {extension}"
    )


# ============================================================
# MAPEO DE COLUMNAS DEL FORMS
# ============================================================

def preparar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el archivo original del Forms en una estructura estándar.

    Formato conocido del Forms:
    - ID
    - Hora de inicio
    - Hora de finalización
    - Apellido
    - Nombre2
    - DNI
    - Fecha capacitación
    - Complejo
    - Puesto
    - Módulo y rol en el que te capacitaste
    - Empleador
    """

    # TXT sin encabezados.
    if all(isinstance(columna, int) for columna in df.columns):
        if len(df.columns) < 13:
            raise ValueError(
                "El TXT no tiene la cantidad esperada de columnas."
            )

        columnas = {
            "ID": df.columns[0],
            "Inicio": df.columns[1],
            "Fin": df.columns[2],
            "Apellido": df.columns[6],
            "Nombre": df.columns[7],
            "DNI": df.columns[8],
            "Fecha capacitación": df.columns[9],
            "Complejo": df.columns[10],
            "Cargo": df.columns[11],
            "Módulos": df.columns[12],
            "Tipo personal": (
                df.columns[13]
                if len(df.columns) > 13
                else None
            ),
        }

    else:
        columnas_originales = list(df.columns)

        columnas = {
            "ID": detectar_columna(
                columnas_originales,
                ["ID", "Id"],
            ),
            "Inicio": detectar_columna(
                columnas_originales,
                [
                    "Hora de inicio",
                    "Inicio",
                    "Start time",
                ],
            ),
            "Fin": detectar_columna(
                columnas_originales,
                [
                    "Hora de finalización",
                    "Fin",
                    "Completion time",
                ],
            ),
            "Apellido": detectar_columna(
                columnas_originales,
                [
                    "Apellido",
                    "Apellidos",
                ],
            ),
            "Nombre": detectar_columna(
                columnas_originales,
                [
                    "Nombre2",
                    "Nombre 2",
                    "Nombres",
                    "Nombre",
                ],
            ),
            "DNI": detectar_columna(
                columnas_originales,
                [
                    "DNI",
                    "Documento",
                ],
            ),
            "Fecha capacitación": detectar_columna(
                columnas_originales,
                [
                    "Fecha capacitación",
                    "Fecha de capacitación",
                ],
            ),
            "Complejo": detectar_columna(
                columnas_originales,
                ["Complejo"],
            ),
            "Cargo": detectar_columna(
                columnas_originales,
                [
                    "Puesto",
                    "Cargo",
                    "Función",
                ],
            ),
            "Módulos": detectar_columna_por_contenido(
                columnas_originales,
                [
                    "Módulo y rol",
                    "Modulo y rol",
                    "te capacitaste",
                ],
            ),
        }

        try:
            columnas["Tipo personal"] = detectar_columna(
                columnas_originales,
                [
                    "Empleador",
                    "Tipo de personal",
                    "Tipo personal",
                ],
            )
        except ValueError:
            columnas["Tipo personal"] = None

    resultado = pd.DataFrame()

    for nombre_estandar, columna_origen in columnas.items():
        if columna_origen is None:
            resultado[nombre_estandar] = ""
        else:
            resultado[nombre_estandar] = df[columna_origen]

    return resultado


# ============================================================
# LIMPIEZA
# ============================================================

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia textos, DNI y fechas.
    """
    df = df.copy()

    columnas_texto = [
        "ID",
        "Apellido",
        "Nombre",
        "Complejo",
        "Cargo",
        "Módulos",
        "Tipo personal",
    ]

    for columna in columnas_texto:
        df[columna] = df[columna].apply(
            normalizar_texto
        )

    df["DNI"] = df["DNI"].apply(
        normalizar_dni
    )

    # dayfirst=False porque Forms exporta normalmente MM/DD/YYYY.
    df["Inicio"] = pd.to_datetime(
        df["Inicio"],
        errors="coerce",
    )

    df["Fin"] = pd.to_datetime(
        df["Fin"],
        errors="coerce",
    )

    df["Fecha capacitación"] = pd.to_datetime(
        df["Fecha capacitación"],
        errors="coerce",
    )

    return df


def unir_modulos(serie: pd.Series) -> str:
    """
    Une los módulos originales de registros duplicados sin repetirlos.
    """
    modulos_encontrados: list[str] = []
    claves_vistas: set[str] = set()

    for valor in serie.dropna():
        for parte in str(valor).split(";"):
            modulo = normalizar_texto(parte)

            if not modulo:
                continue

            clave = normalizar_para_comparar(modulo)

            if clave not in claves_vistas:
                claves_vistas.add(clave)
                modulos_encontrados.append(modulo)

    if not modulos_encontrados:
        return ""

    return "; ".join(modulos_encontrados) + ";"


def elegir_valor_mas_completo(
    serie: pd.Series,
) -> str:
    """
    Conserva el valor más frecuente.
    Si hay empate, conserva el más largo.
    """
    valores = [
        normalizar_texto(valor)
        for valor in serie
        if normalizar_texto(valor)
    ]

    if not valores:
        return ""

    frecuencias: dict[str, int] = {}

    for valor in valores:
        clave = normalizar_para_comparar(valor)
        frecuencias[clave] = frecuencias.get(clave, 0) + 1

    mayor_frecuencia = max(frecuencias.values())

    claves_principales = {
        clave
        for clave, cantidad in frecuencias.items()
        if cantidad == mayor_frecuencia
    }

    candidatos = [
        valor
        for valor in valores
        if normalizar_para_comparar(valor)
        in claves_principales
    ]

    return max(candidatos, key=len)


# ============================================================
# CONSOLIDACIÓN POR DNI
# ============================================================

def consolidar_por_dni(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Deja una sola fila por usuario.

    Identificador principal:
    - DNI;
    - si falta DNI, Apellido + Nombre.
    """
    df = df.copy()

    df["Clave usuario"] = df.apply(
        lambda fila: (
            fila["DNI"]
            if fila["DNI"]
            else (
                normalizar_para_comparar(
                    fila["Apellido"]
                )
                + "|"
                + normalizar_para_comparar(
                    fila["Nombre"]
                )
            )
        ),
        axis=1,
    )

    filas_consolidadas: list[dict] = []

    for _, grupo in df.groupby(
        "Clave usuario",
        dropna=False,
        sort=False,
    ):
        grupo = grupo.sort_values(
            by="Inicio",
            na_position="first",
        )

        ultima_fila = grupo.iloc[-1]

        fechas_capacitacion = (
            grupo["Fecha capacitación"]
            .dropna()
            .sort_values()
        )

        if not fechas_capacitacion.empty:
            fecha_capacitacion = (
                fechas_capacitacion.iloc[-1]
            )
        else:
            fecha_capacitacion = pd.NaT

        inicio_original = ultima_fila["Inicio"]
        fin_original = ultima_fila["Fin"]

        inicio_corregido = inicio_original
        fin_corregido = fin_original

        fecha_corregida = False

        if pd.notna(fecha_capacitacion):
            if pd.notna(inicio_original):
                if (
                    inicio_original.date()
                    != fecha_capacitacion.date()
                ):
                    fecha_corregida = True

                inicio_corregido = (
                    inicio_original.replace(
                        year=fecha_capacitacion.year,
                        month=fecha_capacitacion.month,
                        day=fecha_capacitacion.day,
                    )
                )

            if pd.notna(fin_original):
                fin_corregido = (
                    fin_original.replace(
                        year=fecha_capacitacion.year,
                        month=fecha_capacitacion.month,
                        day=fecha_capacitacion.day,
                    )
                )

        filas_consolidadas.append(
            {
                "ID": ultima_fila["ID"],
                "Inicio original": inicio_original,
                "Inicio": inicio_corregido,
                "Fin": fin_corregido,
                "Apellido": elegir_valor_mas_completo(
                    grupo["Apellido"]
                ),
                "Nombre": elegir_valor_mas_completo(
                    grupo["Nombre"]
                ),
                "DNI": ultima_fila["DNI"],
                "Fecha capacitación": (
                    fecha_capacitacion
                ),
                "Complejo": elegir_valor_mas_completo(
                    grupo["Complejo"]
                ),
                "Cargo": elegir_valor_mas_completo(
                    grupo["Cargo"]
                ),
                "Tipo personal": (
                    elegir_valor_mas_completo(
                        grupo["Tipo personal"]
                    )
                ),
                "Módulos originales": unir_modulos(
                    grupo["Módulos"]
                ),
                "Cantidad de registros": len(grupo),
                "Fecha corregida": (
                    "Sí"
                    if fecha_corregida
                    else "No"
                ),
            }
        )

    resultado = pd.DataFrame(
        filas_consolidadas
    )

    return resultado


# ============================================================
# REGLAS Y CORRECCIONES
# ============================================================

def aplicar_reglas(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aplica las reglas para determinar el rol y los módulos.

    Prioridad utilizada por reglas.py:

    1. Si es contratista:
       - siempre Ejecutante.

    2. Si el cargo tiene una regla conocida:
       - asigna el rol correspondiente al cargo.

    3. Si el cargo no tiene una regla conocida:
       - revisa los módulos originales;
       - toma el PRIMER rol encontrado.

       Ejemplo:
           Módulo 1;
           Módulo 4 Ejecutante;
           Módulo 4 Solicitante;

       Resultado:
           Ejecutante

    4. Si no existe ninguna regla ni módulo
       que permita identificar el rol:
       - queda Pendiente / REVISAR.
    """
    df = df.copy()

    # --------------------------------------------------------
    # OBTENER REGLA PARA CADA USUARIO
    # --------------------------------------------------------
    #
    # Ahora también enviamos "Módulos originales".
    #
    # Esto permite que reglas.py pueda utilizar los módulos
    # como segunda fuente para determinar el rol cuando
    # el cargo no se encuentra en la matriz.
    # --------------------------------------------------------

    resultados = df.apply(
        lambda fila: obtener_regla(
            cargo=fila["Cargo"],
            empleador=fila["Tipo personal"],
            modulos_originales=fila[
                "Módulos originales"
            ],
        ),
        axis=1,
    )

    # --------------------------------------------------------
    # ROL ASIGNADO
    # --------------------------------------------------------

    df["Rol asignado"] = resultados.apply(
        lambda resultado: resultado["rol"]
    )

    # --------------------------------------------------------
    # MÓDULOS ESPERADOS
    # --------------------------------------------------------
    #
    # Los módulos se generan según el rol finalmente asignado.
    # --------------------------------------------------------

    df["Módulos esperados"] = resultados.apply(
        lambda resultado: (
            "; ".join(
                resultado["modulos"]
            ) + ";"
            if resultado["modulos"]
            else ""
        )
    )

    # --------------------------------------------------------
    # REGLA APLICADA
    # --------------------------------------------------------

    df["Regla aplicada"] = resultados.apply(
        lambda resultado: resultado[
            "regla"
        ]
    )

    # --------------------------------------------------------
    # TIPO DE PERSONAL CORREGIDO
    # --------------------------------------------------------
    #
    # Se normaliza cada usuario como:
    # - Contratista
    # - Personal propio YPF
    #
    # Se conserva la columna original "Tipo personal"
    # para poder auditar el dato recibido desde Forms.
    # --------------------------------------------------------

    def obtener_tipo_personal_corregido(
        fila: pd.Series,
    ) -> str:
        """
        Determina si el usuario es Contratista
        o Personal propio YPF.

        Prioridad:

        1. Si el dato original indica contratista,
        tercero o externo -> Contratista.

        2. Si el dato original indica YPF o personal propio
        -> Personal propio YPF.

        3. Representante Técnico -> Contratista.

        4. Si el rol es Ejecutante y el tipo está vacío
        -> Contratista.

        5. Si el cargo fue reconocido como cargo YPF
        y no es Ejecutante -> Personal propio YPF.

        6. Como último respaldo:
        cualquier rol interno distinto de Ejecutante
        -> Personal propio YPF.
        """

        tipo_original = normalizar_para_comparar(
            fila["Tipo personal"]
        )

        cargo = normalizar_para_comparar(
            fila["Cargo"]
        )

        rol = normalizar_para_comparar(
            fila["Rol asignado"]
        )

        regla = normalizar_para_comparar(
            fila["Regla aplicada"]
        )

        # ----------------------------------------------------
        # 1. CONTRATISTA EXPLÍCITO
        # ----------------------------------------------------

        if (
            "CONTRATISTA" in tipo_original
            or "TERCERO" in tipo_original
            or "EXTERNO" in tipo_original
        ):
            return "Contratista"

        # ----------------------------------------------------
        # 2. PERSONAL PROPIO YPF EXPLÍCITO
        # ----------------------------------------------------

        if (
            "YPF" in tipo_original
            or "PERSONAL PROPIO" in tipo_original
            or tipo_original == "PROPIO"
        ):
            return "Personal propio YPF"

        # ----------------------------------------------------
        # 3. REPRESENTANTE TÉCNICO
        # ----------------------------------------------------

        variantes_representante_tecnico = [
            "REPRESENTANTE TECNICO",
            "REPRESENTATE TECNICO",
            "RTE TECNICO",
            "R TECNICO",
            "RT",
        ]

        if cargo in variantes_representante_tecnico:
            return "Contratista"

        # ----------------------------------------------------
        # 4. EJECUTANTE SIN TIPO DE PERSONAL
        # ----------------------------------------------------
        #
        # Según la regla definida para este proceso,
        # si no tenemos empleador y el rol resultante
        # es Ejecutante, se clasifica como Contratista.
        # ----------------------------------------------------

        if rol == "EJECUTANTE":
            return "Contratista"

        # ----------------------------------------------------
        # 5. REGLA QUE IDENTIFICA PERSONAL YPF
        # ----------------------------------------------------

        if (
            "PERSONAL PROPIO YPF" in regla
            or "SE INFIERE PERSONAL PROPIO YPF" in regla
        ):
            return "Personal propio YPF"

        # ----------------------------------------------------
        # 6. ROLES INTERNOS
        # ----------------------------------------------------

        roles_ypf = {
            "EMISOR",
            "VERIFICADOR",
            "AUTORIZANTE",
            "SOLICITANTE",
            "ANALISTA DE GAS",
            "ANALISTA DE SEGURIDAD",
            "FORMACION DE FORMADORES",
        }

        if rol in roles_ypf:
            return "Personal propio YPF"

        # ----------------------------------------------------
        # RESPALDO
        # ----------------------------------------------------

        return "Sin definir"


    df["Tipo personal corregido"] = df.apply(
        obtener_tipo_personal_corregido,
        axis=1,
    )
    # --------------------------------------------------------
    # MÓDULOS CORREGIDOS
    # --------------------------------------------------------
    #
    # Si logramos asignar un rol:
    # usamos los módulos esperados.
    #
    # Si sigue Pendiente:
    # conservamos los módulos originales.
    # --------------------------------------------------------

    df["Módulos corregidos"] = df.apply(
        lambda fila: (
            fila["Módulos esperados"]
            if fila["Rol asignado"]
            != "Pendiente"
            else fila["Módulos originales"]
        ),
        axis=1,
    )

    # --------------------------------------------------------
    # DESCRIBIR LAS CORRECCIONES REALIZADAS
    # --------------------------------------------------------

    def describir_correccion(
        fila: pd.Series,
    ) -> str:
        """
        Genera un texto indicando qué modificaciones
        se realizaron sobre cada usuario.
        """
        cambios: list[str] = []

        # ----------------------------------------------------
        # REGISTROS DUPLICADOS CONSOLIDADOS
        # ----------------------------------------------------

        if fila["Cantidad de registros"] > 1:
            cambios.append(
                "Se consolidaron "
                f"{fila['Cantidad de registros']} "
                "registros"
            )

        # ----------------------------------------------------
        # FECHA CORREGIDA
        # ----------------------------------------------------

        if fila["Fecha corregida"] == "Sí":
            cambios.append(
                "La fecha de inicio se ajustó a "
                "la fecha de capacitación"
            )

        # ----------------------------------------------------
        # COMPARAR MÓDULOS
        # ----------------------------------------------------

        originales = normalizar_para_comparar(
            fila["Módulos originales"]
        )

        corregidos = normalizar_para_comparar(
            fila["Módulos corregidos"]
        )

        if originales != corregidos:
            cambios.append(
                "Se completaron o reemplazaron "
                "los módulos según el rol asignado"
            )

        # ----------------------------------------------------
        # INDICAR SI EL ROL FUE INFERIDO DESDE LOS MÓDULOS
        # ----------------------------------------------------

        regla_aplicada = normalizar_para_comparar(
            fila["Regla aplicada"]
        )

        if (
            "INFERIDO" in regla_aplicada
            and "MODULO" in regla_aplicada
        ):
            cambios.append(
                "El rol se obtuvo desde los "
                "módulos originales"
            )

        # ----------------------------------------------------
        # PENDIENTES
        # ----------------------------------------------------

        if fila["Rol asignado"] == "Pendiente":
            cambios.append(
                "Cargo, empleador y módulos "
                "sin regla confirmada"
            )

        # ----------------------------------------------------
        # SIN CAMBIOS
        # ----------------------------------------------------

        if not cambios:
            return "Sin cambios"

        return " | ".join(
            cambios
        )

    # --------------------------------------------------------
    # CREAR COLUMNA DE CORRECCIÓN
    # --------------------------------------------------------

    df["Corrección realizada"] = df.apply(
        describir_correccion,
        axis=1,
    )

    # --------------------------------------------------------
    # ESTADO FINAL
    # --------------------------------------------------------
    #
    # Solo quedan para revisar aquellos casos donde
    # realmente no pudimos determinar ningún rol.
    # --------------------------------------------------------

    df["Estado"] = df[
        "Rol asignado"
    ].apply(
        lambda rol: (
            "REVISAR"
            if rol == "Pendiente"
            else "OK"
        )
    )

    return df

# ============================================================
# PROCESO COMPLETO
# ============================================================

def normalizar_archivo(
    ruta_archivo: str | Path,
) -> pd.DataFrame:
    """
    Ejecuta el proceso completo.

    Regla adicional:
    - conserva únicamente registros del complejo CILC.
    """
    df_original = leer_archivo(
        ruta_archivo
    )

    df_preparado = preparar_columnas(
        df_original
    )

    df_limpio = limpiar_datos(
        df_preparado
    )

    # Solo CILC.
    df_limpio = df_limpio[
        df_limpio["Complejo"].apply(
            normalizar_para_comparar
        ) == "CILC"
    ].copy()

    if df_limpio.empty:
        raise ValueError(
            "El archivo no contiene registros "
            "del complejo CILC."
        )

    df_consolidado = consolidar_por_dni(
        df_limpio
    )

    df_resultado = aplicar_reglas(
        df_consolidado
    )

    df_resultado = df_resultado.sort_values(
        by=["Apellido", "Nombre"],
        kind="stable",
    ).reset_index(drop=True)

    return df_resultado