import tkinter as tk
from tkinter import ttk, messagebox

from iu.base.ventana_base import VentanaBase
from services.periodo_service import PeriodoService


class ListarPeriodosView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Períodos Académicos",
            ancho=760,
            alto=460
        )

        self.service = PeriodoService()
        self._configurar_estilos()
        self._crear_widgets()
        self._cargar_periodos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#2C3E50"
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=26
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#34495E",
            foreground="white"
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#2C3E50")]
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )

        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=25, pady=20)

        ttk.Label(
            contenedor,
            text="Listado de Períodos Académicos",
            style="Titulo.TLabel"
        ).pack(pady=(0, 15))

        columnas = ("nombre", "inicio", "fin", "estado")
        self.tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=11
        )

        self.tabla.heading("nombre", text="Período")
        self.tabla.heading("inicio", text="Fecha Inicio")
        self.tabla.heading("fin", text="Fecha Fin")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("nombre", width=200)
        self.tabla.column("inicio", width=120, anchor="center")
        self.tabla.column("fin", width=120, anchor="center")
        self.tabla.column("estado", width=120, anchor="center")

        self.tabla.tag_configure("par", background="#F8F9F9")
        self.tabla.tag_configure("impar", background="#ECF0F1")

        self.tabla.pack(expand=True, fill="both", pady=10)

        frame_botones = ttk.Frame(contenedor)
        frame_botones.pack(pady=15)

        self.btn_finalizar = ttk.Button(
            frame_botones,
            text="Finalizar período activo",
            style="Primary.TButton",
            command=self._finalizar_periodo
        )
        self.btn_finalizar.pack(side="left", padx=8)

        self.btn_eliminar = ttk.Button(
            frame_botones,
            text="Eliminar período",
            style="Danger.TButton",
            command=self._eliminar_periodo
        )
        self.btn_eliminar.pack(side="left", padx=8)

        ttk.Button(
            frame_botones,
            text="Cerrar",
            command=self.destroy
        ).pack(side="left", padx=8)

    def _cargar_periodos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        periodos = self.service.listar_periodos()
        hay_activo = False

        for i, p in enumerate(periodos):
            estado = "ACTIVO" if p.activo else "FINALIZADO"
            tag = "par" if i % 2 == 0 else "impar"

            if p.activo:
                hay_activo = True

            self.tabla.insert(
                "",
                "end",
                values=(
                    p.nombre,
                    p.fecha_inicio,
                    p.fecha_fin,
                    estado
                ),
                tags=(tag,)
            )

        self.btn_finalizar["state"] = "normal" if hay_activo else "disabled"

    def _finalizar_periodo(self):
        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea finalizar el período activo?"
        )

        if not confirmar:
            return

        try:
            periodo = self.service.finalizar_periodo_activo()
            messagebox.showinfo(
                "Éxito",
                f"Período {periodo.nombre} finalizado correctamente"
            )
            self._cargar_periodos()

        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))

    def _eliminar_periodo(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar un período para eliminar"
            )
            return

        valores = self.tabla.item(seleccionado, "values")
        nombre_periodo = valores[0]
        estado = valores[3]

        mensaje = f"¿Está seguro de eliminar el período {nombre_periodo}?"

        if estado == "ACTIVO":
            mensaje += "\n\n⚠ Este período está ACTIVO."

        confirmar = messagebox.askyesno("Confirmar eliminación", mensaje)

        if not confirmar:
            return

        try:
            self.service.eliminar_periodo(nombre_periodo)

            messagebox.showinfo(
                "Éxito",
                f"Período {nombre_periodo} eliminado correctamente"
            )

            self._cargar_periodos()

        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
