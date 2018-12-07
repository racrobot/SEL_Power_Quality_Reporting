# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 08:29:49 2018

@author: arnocomb

Convert Ui -> Py file:
pyuic5 --from-imports main.ui -o main.py
pyuic5 --from-imports statusbar.ui -o statusbar.py
"""

import sys
from pystray import MenuItem as item
import pystray
from PIL import Image
from time import sleep
from threading import Thread
import json
import os
from sel_pq_report_gen import *
from common_vars import *
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from main import Ui_Dialog
from statusbar import Ui_statusBarDialog


def func_thread_inst( func ):
    
    t_inst = Thread( target = func )
    
    t_inst.start()



class StatusBar(QDialog):
    def __init__(self):
        super().__init__()
        self.statusbar = Ui_statusBarDialog()
        self.statusbar.setupUi(self)
        self.statusbar.progressBar.setMaximum(100)
        self.hide()
        
    def run(self):
        
        self.show()
        
    def finish(self):
        
        sleep(2)
        self.hide()
        
    def update_progress(self, current, total):
        
        val = int( (current/total) * 100 )
        
        self.statusbar.progressBar.setValue( val )
        QApplication.processEvents() 
        
    def update_status_text(self, text):
        
        self.statusbar.statusUpdateValueLabel.setText( text )
        QApplication.processEvents() 
        



class MainApp(QDialog):
    def __init__(self):
        super().__init__()
        self.main = Ui_Dialog()
        self.main.setupUi(self)
        self.showNormal()
        self.setFocus()
        
    def init_signals_slots( self ):
        
        self.main.updateListPushButton.clicked.connect( self.update_via_api_meter_list_table )
        
        self.main.testConnectionpushButton.clicked.connect( self.check_team_connection_status_thread )
        
        self.main.saveCommandLinkButton.clicked.connect( self.hide )
        
        self.main.hostNameLineEdit.textChanged.connect( self.update_config_hostname )
        
        self.main.portNumberLineEdit.textChanged.connect( self.update_config_portnumber )
        
        #self.main.meterTableWidget.itemClicked.connect( self.get_selected_items )
        
        self.main.saveSelectedMeterListPushButton.clicked.connect( self.update_config_selected_meterslist )
        
        self.main.fileDialogPushButton.clicked.connect( self.update_config_reportsfolder )
        
        
    def load_user_config( self ):
        
        #print("Load User Config")
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            #print("Current Config: {}".format( str( config ) ))
            
        host = config['hostname']
        port = config['portnumber']
        reportsFolder = config['reportsFolder']
        
        self.main.hostNameLineEdit.setText( str(host) )
        self.main.portNumberLineEdit.setText( str(port) )
        self.main.reportsFolderLineEdit.setText( str( reportsFolder ) )
        
        QApplication.processEvents()
        
    
    def get_config_meterlist( self ):
        
        config = ""
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            
        return json.loads( config['meterList'].replace("\'", "\"" ) )
            
        
    def update_user_config( self, setting, newVal ):
        
        #print("Update User Config")
        config = ""
        
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        with open('config.json', 'w') as f:
            config[ str(setting) ] = str( newVal )
            json.dump(config, f)
            
            
    def update_config_hostname( self ):
        
        hostname = self.main.hostNameLineEdit.text()
        
        self.update_user_config( 'hostname', hostname )
        
    def update_config_portnumber( self ):
        
        portnumber = self.main.portNumberLineEdit.text()
        
        self.update_user_config( 'portnumber', portnumber )
        
    
    def update_config_reportsfolder( self ):
        
        reportDirectory = ""
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self,"PQ Reports Folder", "","All Files (*);;Excel Files (*.csv)", options=options)
        
        reportDirectory = QFileDialog.getExistingDirectory(self,"PQ Reports Folder")
        
        print("{}".format( reportDirectory ))
        
        if reportDirectory:
            
            self.main.reportsFolderLineEdit.setText( reportDirectory )
            self.update_user_config( 'reportsFolder', reportDirectory )
        
        
        
    def update_config_meterlist( self, meterListJSON ):
        
        self.update_user_config( 'meterList', meterListJSON )
        
        
    def check_team_connection_status( self ):
        
        hostname = self.main.hostNameLineEdit.text()
        
        portnumber = self.main.portNumberLineEdit.text()
        
        if( hostname != "" and portnumber != "" ):
        
            base_api = "http://{}:{}".format(hostname, portnumber)
            
        else:
            
            base_api = "http://localhost:5630"
            
        
        try:
        
            r = reqs.get("{}/api/team/version".format(base_api))
    
            js_data = r.json()["data"]
            
            masterDbVersion = js_data["masterDbVersion"]
            
            self.main.connectionStatusLabel.setText( "Client Connected" )
        
        except Exception as e:
            
            self.main.connectionStatusLabel.setText( "Client Connection Failed !" )
            
    def check_team_connection_status_thread( self ):
        
        func_thread_inst( func = self.check_team_connection_status )
        
        
    def init_meter_list_table( self ):
        
        meterList = self.get_config_meterlist()
        
        row_len = len( meterList )
        
        self.main.meterTableWidget.setRowCount( row_len )
        self.main.meterTableWidget.setColumnCount( 3 )
        self.main.meterTableWidget.setHorizontalHeaderLabels(["ID", "Meter Name", "Included"])
        
        row = 0
        col = 0
        
        for meterObj in meterList:
            
            self.main.meterTableWidget.setItem( row, col, QTableWidgetItem( str( meterObj['deviceId'] ) ) )
            self.main.meterTableWidget.setItem( row, col + 1 , QTableWidgetItem( str( meterObj['deviceName'] ) ) )
            self.main.meterTableWidget.setItem( row, col + 2 , QTableWidgetItem( str( meterObj['selected'] ) ) )
            
            row += 1
        
        
    def update_via_api_meter_list_table( self ):
        
        global sb, m
        
        #QMessageBox.about(self, "Click Event", "Update meter list table")
        
        deviceNames = []
        deviceIds = []
        pageData = []
        
        try:
            
            sb.run()
            
            sb.update_progress( 0, 1 )
            
            pageData = get_device_list( sb )
            
            sb.finish()
            
            deviceIds, deviceNames = get_meter_list( pageData )
        
        except Exception as e:
            
            QMessageBox.warning(self, "Error Event", str( e ))
            #meterList = [{"deviceId": 1, "deiceName":"LEW_735"}, {"deviceId": 2, "deviceName":"Zocholl_M_735"}]
            
    
        row_len = len( deviceIds )
        
        self.main.meterTableWidget.setRowCount( row_len )
        self.main.meterTableWidget.setColumnCount( 3 )
        self.main.meterTableWidget.setHorizontalHeaderLabels(["ID", "Meter Name", "Included"])
        
        row = 0
        col = 0
        
        meterListJSON = []
        
        for id, dn in zip(deviceIds, deviceNames):
            
            self.main.meterTableWidget.setItem( row, col, QTableWidgetItem( str( id ) ) )
            self.main.meterTableWidget.setItem( row, col + 1 , QTableWidgetItem( str(dn) ) )
            self.main.meterTableWidget.setItem( row, col + 2 , QTableWidgetItem( "false" ) )
            meterListJSON.append( { "deviceId": id, "deviceName": dn, "selected": "false" } ) 
            
            row += 1
            
        self.update_config_meterlist( meterListJSON )
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please reselect meters to be included in the PQ report.")
        msg.setWindowTitle("Meter List Updated")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        
        
    def update_config_selected_meterslist( self ):
        
        meterListFull = self.get_config_meterlist()
        
        full_list_len = len( meterListFull )
        
        selectedItems = self.main.meterTableWidget.selectedItems()
        
        selected_list_len = len( selectedItems ) - 1
        
        device_id = ""
        
        for k in range( full_list_len ):
            
            device_id = meterListFull[k]['deviceId']
            
            meterListFull[k]['selected'] = "false"
            
            for i in range( selected_list_len ):
                
                #print("Selected Item: {}".format( str(selectedItems[i].text()) ))
            
                deviceId = selectedItems[i].text()
                
                if str( deviceId ) in str( device_id ):
                    
                    meterListFull[k]['selected'] = "true"
                    
                    break
                    
        self.update_config_meterlist( meterListFull )
        
        self.init_meter_list_table()
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("PQ report meter list updated !")
        msg.setWindowTitle("Meter Selection")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        
  

def statusBar_Thread():
    global sb
    
    sb = StatusBar()
    
    
    
        
def main():
    global sb, m, curDir
    
    curDir = os.path.dirname(os.path.abspath(__file__))

    app = QApplication(sys.argv)
    
    
    m = MainApp()
    
    m.init_signals_slots()
    
    m.load_user_config()
    
    m.init_meter_list_table()
    
    
    sb = StatusBar()
    
    func_thread_inst( func = sb.finish )
    
    func_thread_inst( func = m.check_team_connection_status )

    
    sys.exit(app.exec_())
    
    
    
def show_main():
    global m, icon
    
    m.showNormal()
    m.repaint()
    m.setFocus()
    QApplication.processEvents()
    
def hide_main():
    global m, icon
    
    m.hide()
    QApplication.processEvents()
    
def close_main():
    global m, icon
    
    icon.stop()
    m.close()
    QApplication.processEvents()
    
#    pageData = get_profileChannels()
#    
#    meterList = []
#    
#    print("\nMeter List:\n")
#    
#    for pd in pageData:
#        
#        if( pd["deviceName"] not in meterList ):
#        
#            meterList.append( pd["deviceName"] )
#            
#            print("{}".format( str( pd["deviceName"] ) ))
    
#    if( len( pageData ) > 0 ):
#        
#        #get_ldp_channelIDs( cmvr.mtr_list, cmvr.ldlist1, pageData )
#        
#        deviceIDs = get_meter_deviceIDs( cmvr.mtr_list, pageData )
#        
#        for id in deviceIDs:
#            
#            vssiData = get_vssi_page_data( id, cmvr.startDate, cmvr.endDate )
#            
#            compile_vssi_report( vssiData, cmvr.startDate, cmvr.endDate ) 

        #get_ldp_channelIDs( ldlist = cmvr.ldlist2 )
    
        #get_profileSamples()
        #generate_report( ldp_json_arr = cmvr.ldp_report_data )
 
    
    
    
global sb, m, icon

mainT = Thread( target = main )
    
image = Image.open("C:\Python_Projects\SEL Power Quality Reporting\Icons\sel.jpg")

menu = ( item('Open', lambda :  show_main() ), item('Quit', lambda :  close_main() )  )

#menu = (item('Start', lambda :  mainT.start() ) , item('Quit', lambda :  close_main() ) )

icon = pystray.Icon("SEL", image, "PQ Report Tool", menu)

icon.run( mainT.start() )    



















    
