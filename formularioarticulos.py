import tkinter as tk
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st

import pyodbc
from tkinter import messagebox


class FormularioArticulos:
    def __init__(self, root):
        self.root = root

        self.root.geometry("575x325")
        self.root.resizable(False, False)
        self.root.title("SYST_CONTROL(COM_DELFINA®)-->(INVENTARIO Y STOCK)")
        self.root.iconbitmap("recursos\\COM_DELFINA.ico")

        imagenes = {
            'save': PhotoImage(file='recursos\\icon_upd.png'),
            'fondo': PhotoImage(file='recursos\\FONDO.png')
        }

        # =============================================================
        # FONDO PANTALLA PRINCIPAL
        # =============================================================
        self.fondo = Label(self.root, image=imagenes['fondo'], bg="#003366", fg='White',
                           font=("Cooper Black", 12), compound="left")
        self.fondo.image = imagenes['fondo']
        self.fondo.place(x=0, y=35)

        self.txt = "CONTROL DE INVENTARIO Y STOCK"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("Cooper Black", 18), bg="#000000",
                             fg='black', bd=5, relief=FLAT)
        self.heading.place(x=0, y=0, width=650)
        self.slider()
        self.heading_color()

        # ========================================================================
        # ===========================COD. BARRA===================================
        # ========================================================================

        self.label1=Label(self.root, text="CÓD. BARRA      :", bg="#be1d2c", fg="WHITE", font=("Cooper Black", 11))
        self.label1.place(x=20, y=160)
        self.codigomod=StringVar()
        self.entrycodigo=Entry(self.root, textvariable=self.codigomod)
        self.entrycodigo.focus()
        self.entrycodigo.bind('<Return>',self.consultar_mod)
        self.entrycodigo.place(x=150, y=160, width=250)

        # ========================================================================
        # ======================NOMBRE DEL PRODUCTO===============================
        # ========================================================================

        self.label2=Label(self.root, text="PRODUCTO       :", bg="#be1d2c", fg="WHITE", font=("Cooper Black", 11))        
        self.label2.place(x=20, y=190)
        self.descripcionmod=StringVar()
        self.entrydescripcion=Entry(self.root, textvariable=self.descripcionmod, state='readonly', width=50)
        self.entrydescripcion.place(x=150, y=190, width=310)

        # ========================================================================
        # ==============================STOCK=====================================
        # ========================================================================

        self.label3=Label(self.root, text="STOCK               :", bg="#be1d2c", fg="WHITE", font=("Cooper Black", 11))        
        self.label3.place(x=20, y=220)
        self.stock_a=StringVar()
        self.stock_ant_mod=Entry(self.root, textvariable=self.stock_a, state='readonly')
        self.stock_ant_mod.place(x=150, y=220, width=65)

        # ========================================================================
        # ===========================CANTIDAD=====================================
        # ========================================================================

        self.label4=Label(self.root, text="CANTIDAD          :", bg="#be1d2c", fg="WHITE", font=("Cooper Black", 11))        
        self.label4.place(x=20, y=250)
        self.cant=StringVar()
        self.entrycant=Entry(self.root, textvariable=self.cant)
        self.entrycant.place(x=150, y=250, width=50)

        # ========================================================================
        # ==========================Botón de Guardar==============================
        # ========================================================================

        self.sinc_button = Button(self.root, image=imagenes['save'], text=' SINCRONIZAR STOCK ', bg="#145A32",
                                  fg='White', font=("Cooper Black", 12), command=self.validation, compound="left")
        self.sinc_button.image = imagenes['save']
        self.sinc_button.place(x=200, y=280)
    
    def slider(self):
        """creates slides for heading by taking the text,
        and that text are called after every 100 ms"""
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text + self.txt[self.count]
            self.heading.config(text=self.text)
        self.count += 1

        self.heading.after(100, self.slider)

    def heading_color(self):
        """
        configures heading label
        :return: every 50 ms returned new random color.
        """
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def consultar_mod(self, e):
        if self.entrycodigo.get() == '':
            messagebox.showwarning("SYST_CONTROL(COM_DELFINA®)-->(ADVERTENCIA)",
                                   "INGRESE EL CAMPO: CÓDIGO DE BARRA")
            self.borrar_d()           
            self.entrycodigo.focus()

        else:
            try:
                self.connection = pyodbc.connect(driver='{SQL Server Native Client 11.0};', server='192.168.1.100',
                                            database='COMDELFINA', trusted_connection='yes')
                self.cursor = self.connection.cursor()

                query0 = 'select Nombre from INV_PRODUCTOS where CódigoBarra1=?'
                datos0 = (self.entrycodigo.get())
                data0 = self.cursor.execute(query0, datos0)

                datos_p = self.cursor.fetchall()

                if datos_p:
                    for productos in datos_p:
                        self.descripcionmod.set(productos[0])

                        query1 = 'SELECT Stock FROM INV_PD_BODEGA_STOCK JOIN INV_PRODUCTOS ON INV_PD_BODEGA_STOCK.ProductoID=INV_PRODUCTOS.ID WHERE CódigoBarra1=?'
                        datos1 = (self.entrycodigo.get())
                        data1 = self.cursor.execute(query1, datos1)
                        for productos1 in data1:
                            self.stock_a.set(productos1[0])
                            self.entrycant.focus()

                else:
                    messagebox.showerror("SYST_CONTROL(COM_DELFINA®)-->(ERROR)", f"PRODUCTO NUEVO!!!\nDEBE REGISTAR PRIMERO.")
                    self.borrar_d()

            except BaseException as msg:
                messagebox.showerror("SYST_CONTROL(COM_DELFINA®)-->(ERROR)", f"NO FUÉ POSIBLE CONECTARSE CON EL SERVIDOR,\n"
                                                                    f"REVISE LA CONEXIÓN: {msg}")
                self.borrar_d()
    
    def validation(self):
        if self.entrycodigo.get() == '':
            messagebox.showwarning("SYST_CONTROL(COM_DELFINA®)-->-(ADVERTENCIA)",
                                   "INGRESE EL CAMPO: CÓDIGO DE BARRA")
            self.borrar_d()           
            self.entrycodigo.focus()

        elif self.cant.get() == '':
            messagebox.showwarning("SYST_CONTROL(COM_DELFINA®)-->-(ADVERTENCIA)", "INGRESE EL CAMPO: CANTIDAD")
            self.borrar_d()
            self.entrycant.focus()

        else:
            self.modifica()

    def modifica(self):
        try:
            self.connection = pyodbc.connect(driver='{SQL Server Native Client 11.0};', server='192.168.1.100',
                                         database='COMDELFINA', trusted_connection='yes')
            self.cursor = self.connection.cursor()

            query = 'UPDATE INV_PD_BODEGA_STOCK SET Stock =Stock+? FROM INV_PD_BODEGA_STOCK JOIN INV_PRODUCTOS ON INV_PD_BODEGA_STOCK.ProductoID=INV_PRODUCTOS.ID WHERE CódigoBarra1=?'
            values = (self.cant.get(), self.entrycodigo.get())
            self.cursor.execute(query, values)
            self.connection.commit()

            self.stock_actual = StringVar()
            self.stock_ac()
            
            messagebox.showinfo("SYST_CONTROL(COM_DELFINA®)-->-->(ÉXITO)",
                                f"STOCK ACTUAL DEL PRODUCTO: {self.descripcionmod.get()}\n"
                                f"ES: {self.stock_actual.get()}")
            self.borrar_d()

        except BaseException as msg:
            messagebox.showerror("SYST_CONTROL(COM_DELFINA®)-->", f"NO FUÉ POSIBLE CONECTARSE CON EL SERVIDOR,\n"
                                                                  f"REVISE LA CONEXIÓN: {msg}")
            self.borrar_d()

    def borrar_d(self):
        self.codigomod.set("")
        self.descripcionmod.set("")
        self.stock_a.set("")
        self.cant.set("")
        self.entrycodigo.focus()
    
    def stock_ac(self):
        try:
            self.connection = pyodbc.connect(driver='{SQL Server Native Client 11.0};', server='192.168.1.100',
                                         database='COMDELFINA', trusted_connection='yes')
            self.cursor = self.connection.cursor()

            
            query1 = 'SELECT Stock FROM INV_PD_BODEGA_STOCK JOIN INV_PRODUCTOS ON INV_PD_BODEGA_STOCK.ProductoID=INV_PRODUCTOS.ID WHERE CódigoBarra1=?'
            datos1 = (self.entrycodigo.get())
            data1 = self.cursor.execute(query1, datos1)
            for productos1 in data1:
                self.stock_actual.set(productos1[0])

        except BaseException as msg:
            messagebox.showerror("SYST_CONTROL(IFAP®)-->(ERROR)", f"NO FUÉ POSIBLE CONECTARSE CON EL SERVIDOR,\n"
                                                                  f"REVISE LA CONEXIÓN: {msg}")

def win():
    root = Tk()
    FormularioArticulos(root)
    root.mainloop()


if __name__ == '__main__':
    win()
