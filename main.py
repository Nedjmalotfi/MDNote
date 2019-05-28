#!/usr/bin/python

import json
from time import ctime

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

#KMDS
from kivymd.theming import ThemeManager
from kivymd.list import TwoLineListItem

class EditScreen(Screen):
    pass
class MainScreen(Screen):
    pass
class tlli(TwoLineListItem):
    def __init__(self,dtext,nid,**kwargs):
        super().__init__(**kwargs)
        self.dtext = dtext
        self.nid = nid
class MDNoteApp(App):
    def build(self):
        self.itme = None
        self.data = {}
        self.count = 0
        self.transition = SlideTransition()
        root = ScreenManager(transition=self.transition)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'Indigo' #'Purple'
        self.theme_cls.accent_palette = 'Gray'
        self.theme_cls.theme_style = 'Dark'
        self.ms = MainScreen(name='main')
        self.es = EditScreen(name='edit')
        root.add_widget(self.ms)
        root.add_widget(self.es)
        self.laoddata()
        return root
    def laoddata(self):
        i = 0
        with open('data/data.json') as json_file:
            data = json.load(json_file)
            self.data.update(data)
            for i in data:
                tli = tlli(text=data[str(i)]['title'],dtext=data[str(i)]['text'],secondary_text=data[str(i)]['time'],nid=data[str(i)]['nid'])
                self.ms.ids.ml.add_widget(tli)
            self.count = int(i)
    def gotoedit(self):
        if self.itme: 
            self.transition.direction = 'left'
            self.root.current = 'edit'
        else:
            self.es.ids.title.text = ''
            self.es.ids.text.text = ''
            self.itme = None
            self.transition.direction = 'left'
            self.root.current = 'edit'
    def gotomain(self):
        if self.itme :
            ti = ctime()
            title = self.es.ids.title.text
            txt = self.es.ids.text.text
            self.itme.dtext = txt
            self.itme.text = title
            self.itme.secondary_text = ti
            #
            nid = str(self.itme.nid)
            self.data[nid]['title'] = title
            self.data[nid]['text'] = txt
            self.data[nid]['time'] = ti
            self.transition.direction = 'right'
            self.root.current = 'main' 
        else:
            self.transition.direction = 'right'
            self.root.current = 'main'
    def add(self):
        self.count = self.count + 1
        ti = ctime()
        title = self.es.ids.title.text
        dtext = self.es.ids.text.text
        nid = self.count
        tli = tlli(text=title,dtext=dtext,secondary_text=ti,nid=nid)
        data = {
              str(self.count):{
              "title":title,
	          "text":dtext,
	          "time":ti,
	          "nid":nid
              }
         }
        self.data.update(data)
        self.ms.ids.ml.add_widget(tli)
        self.itme = None
        self.gotomain()
    def edit(self,title,text,itme):
        self.es.ids.title.text = title
        self.es.ids.text.text = text
        self.itme = itme
        self.gotoedit()
    def on_stop(self):
        with open('data/data.json','w') as jout:
            json.dump(self.data,jout)
    def can(self):
        if self.itme:
           self.ms.ids.ml.remove_widget(self.itme)
           self.data.pop(str(self.itme.nid))
           self.itme = None
           self.gotomain()
        else:
           self.gotomain()
if __name__ == '__main__':
    MDNoteApp().run()
