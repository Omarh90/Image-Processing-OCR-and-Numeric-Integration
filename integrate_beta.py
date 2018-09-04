
about = \
"""
Integrate - Alpha

Instructions:
1) Set parameters on right:

    o Select radiobutton to indicate whether peak is from Carbon, Nitrogen, or Sulfur
    o Input sample weight(default is 2500 mg)
    o Input correction factor, derived from ratio of expected versus
       values of calibration verification sample (default value is 1.00)
        
2) Right click and drag under are a of curve to integrate peak.
3) Note integration value on right.
4) Files autogenerated for traceability purposes under "filename_calc" in same directory as screen capture.
6) Save to generate report with user initials and sample ID.

Settings:

   o Subtract: counts negative area in case where integration value is above
   o Custom: integrate any screen cap. (Coming soon)

Colors:

   o Pick colors used in chart.(Coming soon)

Written by Omar Ali, 2018.

"""

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import *
#from ttk import *
import pyperclip
from shutil import copyfile
import pdb
import os
from PIL import Image, ImageTk
import manually

#TODO:
#   * fix error->quant->error bug
#   * colors

class Cnv(Canvas):
    
    subtr = 0
    custm = 0
    int_coord = []
    trace_coord = [0,0]
    line_id1 = 0
    line_id2 = 0
    int_counter = 1
    trace_counter = 1
    txt_f = 0
    txt_wt = 0
    txt_el = ""
    el = ""
    resetbtn = False

    def __init__(self, root, im):
        
        Canvas.__init__(self, width=500, height=500)
        self.filename = 'test1.png'
        self.filenameint = 'test1.png'
        self.event_add('<<B3-drag-Release>>','<Button-3>', '<ButtonRelease-3>')
        self.bind('<<B3-drag-Release>>', self.clicktrack_int)
        self.event_add('<<B3-drag>>','<Button-3>', '<Motion>')
        self.bind('<<B3-drag>>', self.clicktrack_int)
        self.realtimeint = [0]
        self.int_coord = []
        self.im = im
        self.w1, self.h1 = self.im.size 
        self.imint = im
        self.w2, self.h2 = self.imint.size
        self.integrate = False
        self.graph = ImageTk.PhotoImage(self.im)
        self.create_image((0,0),anchor=NW, image=self.graph)
        self.graphint = ImageTk.PhotoImage(self.imint)
        self.create_image((0,0), anchor=NW, image=self.graphint)
        self.el = StringVar()
        self.grid(row=1, column=1, columnspan=10, rowspan=10, padx=7 ,pady=5)
        
    def set_parameters(self):
        
        try:
            Cnv.corr = txt_f.get()
            Cnv.wt = txt_wt.get()
            Cnv.el = rd_el.el.get()
            float(txt_f.get())
            float(txt_wt.get())
            if Cnv.resetbtn or len(Cnv.el) != 1 or len(str(Cnv.wt)) > 10 or len(str(Cnv.corr)) > 10:
                raise ValueError
        except ValueError:
            self.realtimeint = [['','','',0,'Invalid Parameter Error!'],'','','']
            rs.changeconc(self.realtimeint[0])
            Cnv.trace_coord[0] = 0
            self.get_file(self.realtimeint[1], integrate = Cnv.integrate)
             
    def quantify(self):

        x1, y1, x2, y2  = self.coord[0][0], self.coord[0][1], self.coord[1][0], self.coord[1][1]
        self.set_parameters()
        self.realtimeint =  manually.integrate(gui=True, subtract=Cnv.subtr.get(), custom=Cnv.custm.get(), save=False, colorint=False,
            gui_info=[[(x1,y1), (x2,y2)], self.filename, [float(txt_f.get()),float(txt_wt.get()), Cnv.el, ''], ['colors']])
        rs.changeconc(self.realtimeint[0])
        self.imint = Image.open(self.filenameint)
        self.w2, self.h2 = self.imint.size            
        self.graphint = ImageTk.PhotoImage(self.imint)
        self.create_image((self.w2/2,self.h2/2), anchor=CENTER, image=self.graphint)
        Cnv.line_id2 = self.create_line(x1, y1, x2, y2, fill="red", width=2)
            
    def clicktrack_int(self, event):
        
        x1,y1 = (event.x, event.y)
        if (str(event.type)=='ButtonRelease' or str(event.type)=='ButtonPress'):
            if len(Cnv.int_coord) >= 2:
                Cnv.int_coord = []
            Cnv.int_coord.append((event.x, event.y))
            if len(Cnv.int_coord) == 2:
                Cnv.resetbtn = False
                Cnv.draw_intmarker(self, Cnv.int_coord, event)

        if str(event.type)=='ButtonPress':
            if Cnv.line_id2:
                self.delete(Cnv.line_id2)
            Cnv.trace_coord[0] = (event.x, event.y)
            
        if str(event.type)=='Motion':
            Cnv.trace_coord[1] = (event.x,event.y)
            if Cnv.trace_coord[0] != 0 and Cnv.trace_coord[1] != 0:
                Cnv.draw_intmarker(self, Cnv.trace_coord, event)
        if str(event.type)=='ButtonRelease':
            Cnv.trace_coord[0] = 0

    def draw_intmarker(self, coord, event):

        self.coord=coord
        x1, y1, x2, y2 =(coord[0][0], coord[0][1], coord[1][0], coord[1][1])

        if str(event.type) == 'Motion':
            if Cnv.line_id2:
                self.delete(Cnv.line_id2)
            Cnv.line_id2 = self.create_line(x1,y1,x2,y2,fill="red", width=2)
            
        else:
            if Cnv.line_id1:
                self.delete(Cnv.line_id1)
            if Cnv.line_id2:
                self.delete(Cnv.line_id2)
            Cnv.line_id1 = self.create_line(x1,y1,x2,y2,fill="blue")
            try:
                self.quantify()
                Cnv.integrate = True
                self.get_file(self.realtimeint[1], integrate = Cnv.integrate)
                Cnv.line_id1 = self.create_line(x1,y1,x2,y2,fill="red", width=2)
            except IndexError:
                Cnv.integrate = True
                self.realtimeint = [['','','',0,'Integration Error!'],'','','']
                Cnv.trace_coord[0] = 0
                self.delete(Cnv.line_id2)
                rs.changeconc(self.realtimeint[0])
                self.get_file(self.realtimeint[1], integrate = Cnv.integrate)

    def get_file(self, filenameint=0, integrate = False):

        if integrate == True:
            self.filenameint = filenameint
            self.imint = Image.open(self.filenameint)
            self.w2, self.h2 = self.imint.size
            self.graphint = ImageTk.PhotoImage(self.imint)
            self.create_image((self.w2/2,self.h2/2), anchor=CENTER, image = self.graphint)
            
        if filenameint==0:
            self.filename_t = askopenfilename(defaultextension='.',
                filetypes=[('All picture files',('*.bmp', '*.gif', '*.png', '*.jpg')),
                    ('Bitmap, (*.bmp)','*.bmp'), ('GIF (*.gif)','*.gif'),
                    ('PNG (*.png)', '*.png'), ('JPEG (*.jpg)','*.jpg')])
            if self.filename_t:
                self.filename = self.filename_t
                self.filenameint = self.filename
                self.im = Image.open(self.filename)
                self.imint = Image.open(self.filenameint)
                self.w1, self.h1 = self.im.size
                self.w2, self.h2 = self.imint.size            
                self.graph = ImageTk.PhotoImage(self.im)
                self.create_image((self.w1/2,self.h1/2), anchor=CENTER, image=self.graph)
                self.graphint = ImageTk.PhotoImage(self.imint)
                self.create_image((self.w2/2,self.h2/2), anchor=CENTER, image=self.graphint)

    def get_clipboard(self):

        pass

    def reset(self):

        self.create_image((self.w1/2,self.h1/2), anchor=CENTER, image = self.graph)
        self.delete(Cnv.line_id1)
        self.delete(Cnv.line_id2)
        Cnv.resetbtn = True

class ResultsSummary(Text):

    def __init__(self, root, results):

        Text.__init__(self, root, width=35, height=35, relief = FLAT, bg = cnv['bg'], padx=4, font='System')
        self.insert(index = END, chars = 'Rightclick and drag underneath curve to \
        integrate results. \n\n \
        Change element, factor or sample \n amount and click "Quant" to update. \n \
        Save to autogenerate report.')
        self.conc = results[0]

    def changeconc(self,results):

        try:
            self.el = results[2]
        except IndexError:
            self.el = ''
        if self.el =='C':
            self.element = 'Carbon'
        elif self.el =='N':
            self.element = 'Nitrogen'
        elif self.el =='S':
            self.element = 'Sulfur'
        else:
            self.element = ''
        self.header = "Total " + self.element + " Results:\n" + \
            "_______________________________\n\n"
        self.conc = results[0]
        self.area = '\n' + results[1]
        self.ret_time = '\n' "Retention time = "+ str(round(results[3],2)) + ' sec'
        self.error = '\n' + results[4]
        self.config(state=NORMAL)
        self.configure()
        self.delete(index1="1.0", index2=END)
        self.insert(index = END, chars = self.header)
        self.insert(index = END, chars=self.conc)
        self.insert(index = END, chars=self.area)
        self.insert(index = END, chars=self.ret_time)
        self.insert(index = END, chars=self.error)
        self.config(state=DISABLED)
        
    def reset(self):

        self.config(state=NORMAL)
        self.configure()
        self.delete(index1="1.0", index2=END)
        self.config(state=DISABLED)

class ResultsReport(Text):
    
    def __init__(self):

        self.null = 0

class Radiobtn(Radiobutton):

    def __init__(self, root, options):

        self.radio_row = 4
        self.rd_align=[3,3,0]
        self.el = StringVar()
        for i in range(0,len(options)):
           self.radio_row+=1
           Radiobutton.__init__(self, root, text = options[i], variable = self.el, value = options[i], command = None)
           self.grid(row=self.radio_row, column=13, rowspan = 1, padx=self.rd_align[i])
           
class Options(Toplevel):

    def __init__(self,root):

        Toplevel.__init__(self, root)
        self.iconbitmap('iconbitmap.ico')
        self.title=self.title('Settings')
        self.geometry('200x100')
        self.withdraw()
        self.lbl_subt = Label(self, text='Quantification:')
        self.lbl_subt.grid(column=1, row=1)
        self.lbl_subt.grid(column=1, row=2)
        Cnv.subtr = IntVar(0)
        Cnv.custm = IntVar(0)
        self.subchk = Checkbutton(self, text='Subtract', variable=Cnv.subtr)
        self.subchk.grid(column=1, row=3)
        self.cstchk = Checkbutton(self, text='Custom', variable=Cnv.custm)
        self.cstchk.config(state=DISABLED)
        self.cstchk.grid(column=1, row=4)
        self.bt_ok = Button(self, text='OK', command=self.settings_getattr)
        self.bt_ok.grid(column=1, row=5)
        self.bt_ex = Button(self, text='Cancel', command=self.withdraw)
        self.bt_ex.grid(column=2, row=5)
        self.protocol('WM_DELETE_WINDOW', self.withdraw)
        self.bind('<Escape>', lambda x: self.withdraw())

    def options_menu(self):

        self.deiconify()

    def settings_getattr(self):

        Cnv.subtr.get()
        Cnv.custm.get()
        self.withdraw()
        
class Save(Toplevel):

    def __init__(self,root):

        Toplevel.__init__(self, root)
        self.iconbitmap('iconbitmap.ico')
        self.title=self.title('Save')
        self.geometry('250x75')
        self.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.clear)
        self.bind('<Escape>', lambda x: self.clear())
        self.bind('<Return>', lambda x: self.save())
        self.lbl_flnm = Label(self, text='Sample ID:')
        self.lbl_flnm.grid(column=1, row=1)
        self.ent_flnm = Entry(self, width=20)
        self.ent_flnm.grid(column=2, row=1)
        self.lbl_user = Label(self, text='User Initials:')
        self.lbl_user.grid(column=1, row=2)
        self.ent_user = Entry(self, width=10)
        self.ent_user.grid(column=2, row=2, sticky=W)
        self.bt_ok = Button(self, text='Save...', command=self.save, padx=10)
        self.bt_ok.grid(column=0, row=4, columnspan=2)
        self.bt_ex = Button(self, text='Cancel', command=self.clear, padx=3)
        self.bt_ex.grid(column=4, row=4, columnspan=2)
        self.saveint=[]
        
    def save_dialog(self):

        self.deiconify()

    def save(self):

        self.withdraw()
        self.sample_ID =self.ent_flnm.get()
        self.filename_t = str(self.sample_ID) + ' ' + str(Cnv.el) + '_m'
        self.user_ID = self.ent_user.get()
        self.filename_s = asksaveasfilename(
            initialdir='',
            title='Save',
            initialfile=self.filename_t,
            defaultextension='.png',                                            
            filetypes=[('PNG (*.png)', '*.png'), ('Bitmap, (*.bmp)','*.bmp'),
                       ('GIF (*.gif)','*.gif'), ('JPEG (*.jpg)','*.jpg')])
        if self.filename_s:
            x1, y1, x2, y2  = cnv.coord[0][0], cnv.coord[0][1], cnv.coord[1][0], cnv.coord[1][1]
            self.saveint = manually.integrate(gui=True, subtract=Cnv.subtr.get(), custom=Cnv.custm.get(), save=True, colorint=True,
                gui_info=[[(x1,y1), (x2,y2)], cnv.filename, [float(txt_f.get()), float(txt_wt.get()), Cnv.el, self.user_ID, self.sample_ID], ['colors']])
            self.filename_int=self.saveint[1]
            im_save = Image.open(self.filename_int)
            im_save.save(self.filename_s)
            self.oldfilename_report = os.path.join('.'.join(str(cnv.filename).split('.')[:-1]) + '_calc',
                '.'.join(str(os.path.split(cnv.filename)[-1]).split('.')[:-1]) +'_report.txt')
            self.newfilename_report = self.filename_s[:-4] +'_report.txt'            
            copyfile(self.oldfilename_report, self.newfilename_report)
            self.oldfilename_orig = cnv.filename
            if self.filename_s[-6:-4] == '_m':
                self.newfilename_orig = self.filename_s[:-6] +'_orig.png'                
            else:
                self.newfilename_orig = self.filename_s[:-4] +'_orig.png'
            
            copyfile(self.oldfilename_orig, self.newfilename_orig)
            self.clear()
        else:
            self.clear()
            
    def clear(self):

        self.withdraw()
        self.ent_flnm.delete(0, END)
        self.ent_user.delete(0, END)
        
class Aboutme(Toplevel):

    def __init__(self,root):

        Toplevel.__init__(self, root)
        self.iconbitmap('iconbitmap.ico')
        self.title=self.title('About Integrate')
        self.geometry('600x400')
        self.withdraw()
        self.protocol('WM_DELETE_WINDOW', self.withdraw)
        self.bind('<Escape>', lambda x: self.withdraw())
        self.bind('<Return>', lambda x: self.withdraw())
        self.txt_abt=Text(self, width=200, height=35, relief = FLAT, bg = cnv['bg'], padx=10, font=lbl_spc1['font'])
        self.txt_abt.insert(index = END, chars = about)
        self.txt_abt.grid(column=1, row=1, columnspan=3)
        self.bt_ok = Button(self, text='OK', command=self.withdraw)
        self.bt_ok.grid(column=1, row=5, columnspan=2)

    def show(self):

        self.deiconify()

root = Tk()
root.iconbitmap('iconbitmap.ico')
root.title('Integrate')
root.geometry('800x550')

im = Image.open('test1.png')
cnv = Cnv(root, im)
cnv.get_file(filenameint='test1.png')

lbl_spc1 = Label(root, text='                ')
lbl_spc1.grid(row=4, column = 11)

lbl_spc2 = Label(root, text='                ')
lbl_spc2.grid(row=9, column = 11)


optw = Options(root)
svtw = Save(root)
abt = Aboutme(root)

btn_calc = Button(root, text='Quant', command=cnv.quantify ,pady=7)
btn_calc.grid(row=2, column=12)

btn_reset = Button(root, text='Reset', command=lambda: [cnv.reset(), rs.reset()], pady=7)
btn_reset.grid(row=2, column=13)

lbl_r = Label(root, text='Parameters:            ')
lbl_r.grid(row=5, column=11)

lbl_f = Label(root, text='   Correction Factor:')
lbl_f.grid(row=6, column=11)

txt_f = Entry(root, width=5)
txt_f.grid(row=6, column=12)
txt_f.insert(END, float(1.000))

lbl_wt = Label(root, text='     Sample mass (mg):')
lbl_wt.grid(row=7, column=11)

txt_wt = Entry(root, width=5)
txt_wt.grid(row=7, column=12)
txt_wt.insert(END, 2500)

rd_el = Radiobtn(root, ['C', 'N', 'S'])
rd_el.el.set('C')

rs = ResultsSummary(root,'0')
rs.grid(row=10, column=11, rowspan=10, columnspan=5, padx=10)
            
menu = Menu(root)
root.config(menu=menu)

dropdown1 = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=dropdown1)
dropdown1.add_command(label='Open...', command = cnv.get_file)
dropdown1.add_command(label='Save...', command = svtw.save_dialog)
dropdown1.add_command(label='Exit', command = root.destroy)

dropdown2 = Menu(menu, tearoff=0)
menu.add_cascade(label='Edit', menu=dropdown2)
dropdown2.add_command(label='Paste Clipboard...', command = cnv.get_clipboard, state=DISABLED)
dropdown2.add_command(label='Settings...', command = optw.options_menu)
dropdown2.add_command(label='Colors...', command = None, state=DISABLED)

dropdown3 = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=dropdown3)
dropdown3.add_command(label='About Integrate Application...', command= abt.show)
    
root.mainloop()
