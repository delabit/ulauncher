#!/usr/bin/env python
#-*- encoding: utf-8 *-*

#System
import os
import sys
from gi.repository import Gtk,Gdk

class Launcher:
    
    def __init__(self):
        self.unity_launcher_path='/usr/share/applications/'
        self.launch_extension='.desktop'        

    def create_content(self,app_name,app_description,app_category,app_exec_path,app_icon_path,app_terminal):
        content="[Desktop Entry]\n"
        content=content + "Name=" + app_name + "\n"
        content=content + "Comment=" + app_description + "\n"
        if app_category!="":
            content=content + "Categories=" + app_category + "\n"
        content=content + "Exec=" + app_exec_path + "\n"
        content=content + "Icon=" + app_icon_path + "\n"
        content=content + "Terminal=" + app_terminal + "\n"
        content=content + "Type=Application"
        return content

    def create_file(self,app_name,content):
        filename=self.unity_launcher_path + app_name.replace(' ','-').lower() + self.launch_extension
        launch_file=open(filename,"w")
        launch_file.write(content)
        launch_file.close()     


class Gui:

    def __init__(self):
        #Application directory
        self.initial_directory=os.path.dirname(os.path.realpath(__file__))

        #Clipboard data        
        self.clipboard=Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.entry=Gtk.Entry()
        
        #init variables
        self.app_name=""
        self.app_description=""
        self.app_exec_path=""
        self.app_icon_path=self.initial_directory + "/default-icon.png"
                
        #Window design import from glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main_window.glade")

        #Signals
        signals={
            "on_delete_window": self.on_delete_window,
            "on_accept_click": self.on_accept_click,
            "on_cancel_click": self.on_cancel_click,
            "on_nav_app_exec_path_set": self.on_nav_app_exec_path_set,
            "on_nav_app_icon_path_set": self.on_nav_app_icon_path_set,
            "on_menu_about_click": self.on_menu_about_click,
            "on_menu_exit_click": self.on_menu_exit_click,
            "on_menu_copy_click": self.on_menu_copy_click,
            "on_menu_paste_click": self.on_menu_paste_click,
            "on_menu_cut_click": self.on_menu_cut_click,
        }
        self.builder.connect_signals(signals)
        
        #Fill category list
        self.populateCategoryList()
        
        #Window show
        window = self.builder.get_object("main_window")
        window.show_all()        

    # Widgets signals functions
    def on_delete_window(self,widget):
        Gtk.main_quit()
        sys.exit(0)

    def on_accept_click(self,widget):       
        #Input texts
        self.app_name=self.builder.get_object("txt_app_name").get_text()
        self.app_description=self.builder.get_object("txt_app_description").get_text()
        self.app_terminal=str(self.builder.get_object("chk_terminal").get_active())
        #Selected category
        index=self.lstCategories.get_active()
        self.app_category=self.lstCategories.get_model()[index][0]

        if self.checkVariables():
            #After check variables, create launch file and content
            launcher=Launcher()
            content=launcher.create_content(self.app_name, self.app_description, self.app_category, self.app_exec_path, self.app_icon_path, self.app_terminal)
            launcher.create_file(self.app_name, content)
            #Success dialog
            dlgSuccess=self.builder.get_object("dlgSuccess")
            dlgSuccess.run()            
            sys.exit(0)
        else:
            #Error Dialog
            dlgError=self.builder.get_object("dlgError")
            dlgError.run()                        
            dlgError.hide()
    
    def on_nav_app_exec_path_set(self,widget):
        fileChoser=self.builder.get_object("nav_app_exec_path")
        self.app_exec_path=fileChoser.get_filename()        

    def on_nav_app_icon_path_set(self,widget):
        fileChoser=self.builder.get_object("nav_app_icon_path")
        self.app_icon_path=fileChoser.get_filename()
        self.builder.get_object("img_icon").set_from_file(self.app_icon_path)

    def on_cancel_click(self,widget):
        Gtk.main_quit()
        sys.exit(0)

    def on_menu_exit_click(self,widget):
        sys.exit(0)

    def on_menu_copy_click(self,widget):
        self.clipboard.set_text(self.entry.get_text(),-1)

    def on_menu_paste_click(self,widget):
        text=self.clipboard.wait_for_text()
        if text!=None:
            self.entry.set_text(text)

    def on_menu_cut_click(self,widget):
        self.clipboard.set_text(self.entry.get_text(),-1)
        self.entry.set_text("")

    def on_menu_about_click(self,widget):
        dlgAbout=self.builder.get_object("about_window")
        resp=dlgAbout.run()        
        dlgAbout.hide()        

    #Functions
    def checkVariables(self):         
        if len(self.app_name)>0:
            name=True
        else:
            name=False          
        if len(self.app_exec_path)>0:
            exe=True            
        else:
            exe=False
        if len(self.app_icon_path)==0:
            self.app_icon_path= self.initial_directory + "/default-icon.png"
        if name and exe:
            return True
        else:
            return False

    def populateCategoryList(self):        
        self.lstCategories=self.builder.get_object("lstCategories")
        listStore= Gtk.ListStore(str)        
        elements=("","AudioVideo","Audio","Video","Development","Education","Game","Graphics","Network","Office","Settings","System","Utility")
        for element in elements:                        
            listStore.append([element])        
        self.lstCategories.set_model(listStore)                
        cell=Gtk.CellRendererText()        
        self.lstCategories.pack_start(cell,True)
        self.lstCategories.add_attribute(cell, 'text', 0)

#Launch Gui
gui=Gui()
Gtk.main()
