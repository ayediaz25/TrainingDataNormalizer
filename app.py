# app.py

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from excel_salida import generar_excel
from normalizador import normalizar_archivo


class AplicacionNormalizador:
    def __init__(
        self,
        root: tk.Tk,
    ) -> None:

        self.root = root

        self.root.title(
            "Normalizador de Capacitaciones"
        )
        self.root.geometry("900x640")
        self.root.minsize(900, 640)

        self.ruta_archivo = tk.StringVar()

        self.ruta_salida = tk.StringVar()

        self.estado = tk.StringVar(
            value=(
                "Seleccioná el archivo original "
                "descargado del Forms."
            )
        )

        self.ultima_ruta_salida: Path | None = None

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self) -> None:
        """Configura los estilos de la aplicación."""

        estilo = ttk.Style()

        estilo.configure(
            "BotonPrincipal.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(30, 14),
        )

        estilo.configure(
            "BotonExaminar.TButton",
            font=("Segoe UI", 10),
            padding=(14, 7),
        )

        estilo.configure(
            "Estado.TLabel",
            font=("Segoe UI", 10, "bold"),
        )

    def crear_interfaz(self) -> None:
        """Crea los controles de la ventana."""

        contenedor = ttk.Frame(
            self.root,
            padding=25,
        )

        contenedor.pack(
            fill="both",
            expand=True,
        )

        titulo = ttk.Label(
            contenedor,
            text=(
                "NORMALIZADOR DE "
                "CAPACITACIONES"
            ),
            font=("Segoe UI", 18, "bold"),
        )

        titulo.pack(
            pady=(0, 8),
        )

        subtitulo = ttk.Label(
            contenedor,
            text=(
                "Seleccioná la copia diaria sin corregir. "
                "El programa generará un nuevo Excel normalizado."
            ),
            font=("Segoe UI", 10),
        )

        subtitulo.pack(
            pady=(0, 25),
        )

        marco_archivo = ttk.LabelFrame(
            contenedor,
            text="Archivo de entrada",
            padding=15,
        )

        marco_archivo.pack(
            fill="x",
            pady=(0, 20),
        )

        entrada_ruta = ttk.Entry(
            marco_archivo,
            textvariable=self.ruta_archivo,
            width=75,
        )

        entrada_ruta.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew",
        )

        boton_examinar = ttk.Button(
            marco_archivo,
            text="Examinar",
            command=self.seleccionar_archivo,
            style="BotonExaminar.TButton",
        )

        boton_examinar.grid(
            row=0,
            column=1,
        )

        marco_archivo.columnconfigure(
            0,
            weight=1,
        )
        # ============================================================
        # CARPETA DE SALIDA
        # ============================================================

        marco_salida = ttk.LabelFrame(
            contenedor,
            text="Carpeta de salida",
            padding=15,
        )

        marco_salida.pack(
            fill="x",
            pady=(0, 20),
        )

        entrada_salida = ttk.Entry(
            marco_salida,
            textvariable=self.ruta_salida,
            width=75,
        )

        entrada_salida.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew",
        )

        boton_salida = ttk.Button(
            marco_salida,
            text="Examinar",
            command=self.seleccionar_carpeta_salida,
            style="BotonExaminar.TButton",
        )

        boton_salida.grid(
            row=0,
            column=1,
        )

        marco_salida.columnconfigure(
            0,
            weight=1,
        )
        marco_proceso = ttk.LabelFrame(
            contenedor,
            text="Proceso automático",
            padding=15,
        )

        marco_proceso.pack(
            fill="x",
            pady=(0, 20),
        )

        tareas = [
            "Consolidar duplicados por DNI",
            "Dejar una fila por usuario",
            "Corregir fecha de inicio y capacitación",
            "Asignar rol según cargo y empleador",
            "Generar hojas de resumen y pendientes",
            "Crear gráficos dentro del Excel",
        ]

        for numero, tarea in enumerate(tareas):
            ttk.Label(
                marco_proceso,
                text=f"✓ {tarea}",
            ).grid(
                row=numero,
                column=0,
                sticky="w",
                pady=3,
            )

        self.boton_procesar = ttk.Button(
            contenedor,
            text="PROCESAR Y GENERAR EXCEL",
            command=self.procesar_archivo,
            style="BotonPrincipal.TButton",
        )

        self.boton_procesar.pack(
            pady=(5, 15),
        )

        self.boton_abrir = ttk.Button(
            contenedor,
            text="ABRIR EXCEL GENERADO",
            command=self.abrir_excel,
            state="disabled",
        )

        self.boton_abrir.pack(
            pady=(0, 15),
        )

        self.barra_progreso = ttk.Progressbar(
            contenedor,
            mode="indeterminate",
            length=500,
        )

        self.barra_progreso.pack(
            fill="x",
            padx=120,
            pady=(0, 15),
        )

        etiqueta_estado = ttk.Label(
            contenedor,
            textvariable=self.estado,
            style="Estado.TLabel",
            anchor="center",
        )

        etiqueta_estado.pack(
            fill="x",
        )

    def seleccionar_archivo(self) -> None:
        """Abre el explorador para seleccionar el Excel."""

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo del Forms",
            filetypes=[
                (
                    "Archivos permitidos",
                    "*.xlsx *.xlsm *.xls *.csv *.txt",
                ),
                (
                    "Archivos Excel",
                    "*.xlsx *.xlsm *.xls",
                ),
                (
                    "Archivos CSV",
                    "*.csv",
                ),
                (
                    "Archivos TXT",
                    "*.txt",
                ),
            ],
        )

        if ruta:
            self.ruta_archivo.set(ruta)
            self.estado.set(
                f"Archivo seleccionado: "
                f"{Path(ruta).name}"
            )

            self.boton_abrir.config(
                state="disabled"
            )
    def seleccionar_carpeta_salida(self) -> None:
        """
        Permite seleccionar la carpeta donde se guardará
        el Excel corregido.
        """

        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta de salida"
        )

        if carpeta:
            self.ruta_salida.set(carpeta)

            self.estado.set(
                "Carpeta de salida seleccionada: "
                f"{carpeta}"
            )
    def procesar_archivo(self) -> None:
        """Normaliza el archivo y genera el Excel final."""

        ruta_texto = (
            self.ruta_archivo
            .get()
            .strip()
        )

        if not ruta_texto:
            messagebox.showwarning(
            "Archivo faltante",
            "Primero seleccioná el archivo del Forms.",
            )
            return

        ruta_entrada = Path(ruta_texto)

        if not ruta_entrada.exists():
            messagebox.showerror(
            "Archivo no encontrado",
            "La ruta seleccionada no existe.",
            )
            return

        try:
            self.boton_procesar.config(
                state="disabled"
            )

            self.boton_abrir.config(
                state="disabled"
            )

            self.barra_progreso.start(12)

            self.estado.set(
                "Leyendo y normalizando el archivo..."
            )

            self.root.update_idletasks()

            # Normalizar archivo
            resultado = normalizar_archivo(
                ruta_entrada
            )

            self.estado.set(
                "Generando Excel corregido..."
            )

            self.root.update_idletasks()

            # Crear nombre del archivo de salida
            nombre_salida = (
                f"{ruta_entrada.stem}"
                "_CORREGIDO.xlsx"
            )

            # Obtener carpeta de salida seleccionada
            carpeta_salida_texto = (
                self.ruta_salida
                .get()
                .strip()
            )

            # Si se seleccionó una carpeta de salida,
            # usamos esa carpeta.
            if carpeta_salida_texto:
                carpeta_salida = Path(
                    carpeta_salida_texto
                )

            # Si no se seleccionó una carpeta,
            # guardamos junto al archivo original.
            else:
                carpeta_salida = (
                    ruta_entrada.parent
                )

            # Construir ruta final
            ruta_salida = (
                carpeta_salida
                / nombre_salida
            )

            # Generar Excel
            generar_excel(
                resultado,
                ruta_salida,
            )

            # Calcular estadísticas
            cantidad_usuarios = len(
                resultado
            )

            cantidad_pendientes = int(
                (
                    resultado["Estado"]
                    == "REVISAR"
                ).sum()
            )

            cantidad_duplicados = int(
                (
                    resultado[
                        "Cantidad de registros"
                    ] > 1
                ).sum()
            )

            # Guardar última ruta generada
            self.ultima_ruta_salida = (
                ruta_salida
            )

            self.estado.set(
                "Excel generado correctamente."
            )

            self.boton_abrir.config(
                state="normal"
            )

            # Mensaje final
            mensaje = (
                "Proceso terminado correctamente.\n\n"
                f"Usuarios únicos: "
                f"{cantidad_usuarios}\n"
                f"Duplicados consolidados: "
                f"{cantidad_duplicados}\n"
                f"Pendientes de revisión: "
                f"{cantidad_pendientes}\n\n"
                "Archivo generado en:\n"
                f"{ruta_salida}"
            )

            messagebox.showinfo(
                "Proceso terminado",
                mensaje,
            )

        except PermissionError:
            self.estado.set(
                "No se pudo guardar el archivo."
            )

            messagebox.showerror(
                "Archivo abierto",
                (
                    "No se pudo generar el Excel.\n\n"
                    "Verificá que el archivo corregido "
                    "no esté abierto en Excel."
                ),
            )

        except Exception as error:
            self.estado.set(
                "Ocurrió un error."
            )

            messagebox.showerror(
                "Error al procesar",
                str(error),
            )

        finally:
            self.barra_progreso.stop()

            self.boton_procesar.config(
                state="normal"
            )

    def abrir_excel(self) -> None:
        """Abre el último Excel generado."""

        if (
            self.ultima_ruta_salida is None
            or not self.ultima_ruta_salida.exists()
        ):
            messagebox.showwarning(
                "Archivo no disponible",
                "Primero generá el Excel corregido.",
            )
            return

        os.startfile(
            self.ultima_ruta_salida
        )


def main() -> None:
    root = tk.Tk()
    AplicacionNormalizador(root)
    root.mainloop()


if __name__ == "__main__":
    main()