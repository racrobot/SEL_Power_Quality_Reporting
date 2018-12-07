# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests as reqs
import pprint as pp
import csv
import common_vars as cmvr


def generate_report( ldp_json_arr ):
    
    print("\nGenerate LDP Report...\n")
        
    for page_data in ldp_json_arr:
        
        for d in page_data:
            
            if( "WH3_DEL" in d["channelName"] ):
                
                cmvr.wh3_del.append( [ str(d["deviceName"]), str(d["channelName"]), str(d["channelFunction"]), str(d["value"]), str(d["profileChannelUnits"]), str(d["timestamp"]) ] )
                
            elif( "WH3_REC" in d["channelName"]):
                
                cmvr.wh3_rec.append( [ str(d["deviceName"]), str(d["channelName"]), str(d["channelFunction"]), str(d["value"]), str(d["profileChannelUnits"]), str(d["timestamp"]) ] )
                
            elif( "QH3_DEL" in d["channelName"]):
                
                cmvr.qh3_del.append( [ str(d["deviceName"]), str(d["channelName"]), str(d["channelFunction"]), str(d["value"]), str(d["profileChannelUnits"]), str(d["timestamp"]) ] )
                
            elif( "QH3_REC" in d["channelName"]):
                
                cmvr.qh3_rec.append( [ str(d["deviceName"]), str(d["channelName"]), str(d["channelFunction"]), str(d["value"]), str(d["profileChannelUnits"]), str(d["timestamp"]) ] )
            
    
    with open( cmvr.ldp_report_file, 'w', newline='') as csvfile:
        
        ldp_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        ldp_writer.writerow( ["Device Name", "Channel Name", "Channel Function", "Value", "SI_Unit", "DateTime"] )
        
        for whd, whr, qhd, qhr in zip(cmvr.wh3_del, cmvr.wh3_rec, cmvr.qh3_del, cmvr.qh3_rec):
            
            ldp_writer.writerow( [whd, whr, qhd, qhr]  )
            
    print("\nLDP Report Saved: {}\n".format( cmvr.ldp_report_file ))





                
                
            
        

def get_profileSamples():
    
    print("\nGet Profile Samples:\n")
    
    for idObj in cmvr.ch_ids:
        
#        print( "Device ID: " + str( idObj["deviceId"] ) + "\n" )
#        print( "Device Name: " + str( idObj["deviceName"] ) + "\n" )
#        print( "Device Type: " + str( idObj["deviceType"] ) + "\n" )
#        print( "Channel ID: " + str( idObj["channelId"] ) + "\n" )
#        print( "Channel Number: " + str( idObj["channelNumber"] ) + "\n" )
#        print( "Channel Name: " + str( idObj["channelName"] ) + "\n" )
#        print( "Channel Type: " + str( idObj["channelType"] ) + "\n" )
#        print( "Channel Function: " + str( idObj["channelFunction"] ) + "\n" )
        
        if( "Zocholl_M" in idObj["deviceName"]):
            
            #if( "WH3_DEL" in idObj["channelName"] ):
        
            ch_id = idObj["channelId"]
            dev_id = idObj["deviceId"]
            start_date = "2018-10-29"
            end_date = "2018-10-31"
            
            print("\nGet Load Profile Data: \n")
            
            url = "http://wpul-metertest:5630/api/profilesample/" + str(ch_id) + "?deviceId=" + str(dev_id) + "&StartDate=" + str(start_date) + "&EndDate=" + str(end_date)
            
            print( url + "\n" )
            
            r = reqs.get( url )
    
            js_data = r.json()["data"]
            
            # print( "\n" + str(js_data) + "\n" )
            
            if( len(js_data) > 0 ):
            
                cmvr.ldp_report_data.append( js_data )
        
        
    print("\n\nLDP Data Written to File..\n\n")
    
    print("\nNumber of value objects in LDP data: {}\n".format(len(cmvr.ldp_report_data)))        

    f = open("ldp_data.json","w")
    
    f.write( str(cmvr.ldp_report_data) )
    
    f.close()
    
  
    
    
    
def get_meter_deviceIDs( mtrList, pageData ):
    
    deviceIDs = []
    
    print("Get Device ID's")
    
    for m in mtrList:
        
        for pd in pageData:
            
            for dataObj in pd:
            
                if( m in dataObj["deviceName"] ):
                
                    deviceIDs.append( dataObj["deviceId"] )
                    
                    print("Meter: {} -> ID: {}".format(m,dataObj["deviceId"]))
                    
                    break
                
            break
                    
    return deviceIDs


def get_meter_list( pageData ):
    
    deviceNames = []
    deviceIds = []
        
    for pd in pageData:
        
        for dataObj in pd:
        
            if str( dataObj["deviceName"] ) not in deviceNames:
            
                deviceNames.append( dataObj["deviceName"] )
                deviceIds.append( dataObj["deviceId"] )
                    
    return deviceIds, deviceNames
    
    
    
    
def get_ldp_channelIDs( mtrList, ldList, pageData ):
    
    print("Get Channel ID's")
    
    for m in mtrList:
        
        for cd in pageData:
            
            for d in cd:
            
                if( m in d["deviceName"] ):
                
                    #cmvr.mtr_ch_data.append( d )
                    
                    print("\nMeter: {}".format(m))
                    print("Data: {}".format(d))
                    break
                   
    for pq in ldList:
            
        for mc in pageData:
            
            if( pq in mc["channelName"] ):
        
                cmvr.ch_ids.append( mc )
                
                print("\nPower Quantities: {}".format(pq))
                print("Meter Channel: {}".format(mc))
                break
    
        
        

def get_nextPage( nxtUrl ):

    print("\nNext Page URL Request: \n")

    r = reqs.get( nxtUrl )

    js_data = r.json()["data"]

    pageInfo = r.json()["pageInfo"]
   
    return js_data, pageInfo



def get_profileChannels( sb ):
    
    pageData = []
    
    print("\nProfile Channel Request: \n")

    r = reqs.get("http://wpul-metertest:5630/api/profilechannel")

    js_data = r.json()["data"]

    pageData.append( js_data )

    pageInfo = r.json()["pageInfo"]
    
    try:
        
        nextPageAbsoluteUrl = pageInfo["nextPageAbsoluteUrl"]
        totalPages = int(pageInfo["totalPages"])
        currentPage = int(pageInfo["currentPage"])
        
        sb.update_progress( currentPage, totalPages )
        
        sb.update_status_text( """Next Page Url: {}\nTotal Pages: {}\nCurrent Page: {} \n
                              """.format(nextPageAbsoluteUrl, totalPages, currentPage) )
        
        while( currentPage != totalPages ):
            
            jsData, pageInfo = get_nextPage( nextPageAbsoluteUrl )
            
            pageData.append( jsData )
            
            nextPageAbsoluteUrl = pageInfo["nextPageAbsoluteUrl"]
            totalPages = int(pageInfo["totalPages"])
            currentPage = int(pageInfo["currentPage"])
            
            sb.update_progress( currentPage, totalPages )
            
            sb.update_status_text( """Next Page Url: {}\nTotal Pages: {}\nCurrent Page: {} \n
                              """.format(nextPageAbsoluteUrl, totalPages, currentPage) )
            
    except Exception as e:
        
        print("All data collected from profile channel API...\n")
        print("Error: {}\n".format(e))
        
    return pageData



def get_device_list( sb ):
    
    pageData = []

    r = reqs.get("http://wpul-metertest:5630/api/device")

    js_data = r.json()["data"]

    pageData.append( js_data )

    pageInfo = r.json()["pageInfo"]
    
    try:
        
        nextPageAbsoluteUrl = pageInfo["nextPageAbsoluteUrl"]
        totalPages = int(pageInfo["totalPages"])
        currentPage = int(pageInfo["currentPage"])
        
        sb.update_progress( currentPage, totalPages )
        
        sb.update_status_text( """Next Page Url: {}\nTotal Pages: {}\nCurrent Page: {} \n
                              """.format(nextPageAbsoluteUrl, totalPages, currentPage) )
        
        while( currentPage != totalPages ):
            
            jsData, pageInfo = get_nextPage( nextPageAbsoluteUrl )
            
            pageData.append( jsData )
            
            nextPageAbsoluteUrl = pageInfo["nextPageAbsoluteUrl"]
            totalPages = int(pageInfo["totalPages"])
            currentPage = int(pageInfo["currentPage"])
            
            sb.update_progress( currentPage, totalPages )
            
            sb.update_status_text( """Next Page Url: {}\nTotal Pages: {}\nCurrent Page: {} \n
                              """.format(nextPageAbsoluteUrl, totalPages, currentPage) )
            
    except Exception as e:
        
        print("All data collected from device API...\n")
        print("Error: {}\n".format(e))
        
    return pageData



def sag_event_characterization( durMill, eventDepth ):
    
    eventChar = ""
    
    if( durMill > 20 and durMill <= 150 ):
    
        if( eventDepth > 10 and eventDepth <= 30 ):
            
            eventChar = "Y"
            
        elif( eventDepth > 30 and eventDepth <= 40 ):
            
            eventChar = "X1"
            
        elif( eventDepth > 40 and eventDepth <= 60 ):
            
            eventChar = "X2"
            
        elif( eventDepth > 60 and eventDepth <= 100 ):
            
            eventChar = "T"
            
    elif( durMill > 150 and durMill <= 600 ):
    
        if( eventDepth > 10 and eventDepth <= 20 ):
            
            eventChar = "Y"
            
        elif( eventDepth > 20 and eventDepth <= 60 ):
            
            eventChar = "S"
            
        elif( eventDepth > 60 and eventDepth <= 100 ):
            
            eventChar = "T"
            
    elif( durMill > 600 and durMill <= 3000 ):
    
        if( eventDepth > 10 and eventDepth <= 15 ):
            
            eventChar = "Y"
            
        elif( eventDepth > 15 and eventDepth <= 30 ):
            
            eventChar = "Z1"
            
        elif( eventDepth > 30 and eventDepth <= 100 ):
            
            eventChar = "Z2"
        
    return eventChar



def get_vssi_detail_event( vssiEventURL ):
    
    print("\nVSSI Event Request: \n")
    
    vssiReq = "http://wpul-metertest:5630{}".format( vssiEventURL )

    print("Request URL:\n{}\n".format( str( vssiReq ) ))

    r = reqs.get( vssiReq )

    js_data = r.json()["data"]
    
    return js_data
    



def get_vssi_page_data( dev_id, startDate, endDate ):
    
    vssiData = []
    
    print("\nVSSI Page Data Request: \n")
    
    vssiReq = "http://wpul-metertest:5630/api/vssisummary?DeviceIds={}&StartDate={}&EndDate={}".format(dev_id, startDate, endDate)

    print("Request URL:\n{}\n".format( str( vssiReq ) ))

    r = reqs.get( vssiReq )

    js_data = r.json()["data"]

    vssiData.append( js_data )

    pageInfo = r.json()["pageInfo"]
    
    try:
        
        nextPageAbsoluteUrl = pageInfo["nextPageAbsoluteUrl"]
        totalPages = int(pageInfo["totalPages"])
        currentPage = int(pageInfo["currentPage"])
        
        print("Next Page Url: {}\n".format(nextPageAbsoluteUrl))
        print("Total Pages: {}\n".format(str(totalPages)))
        print("Current Page: {}\n".format(str(currentPage)))
        
        jsonData = None
        
        while( currentPage != totalPages ):
            
            jsonData, pageInfo = get_nextPage( nextPageAbsoluteUrl )
            
            vssiData.append( jsonData )
            
            nextPageAbsoluteUrl = pageInfo["nextPageAbsoluteUrl"]
            totalPages = int(pageInfo["totalPages"])
            currentPage = int(pageInfo["currentPage"])
            
            print("Next Page Url: {}\n".format(nextPageAbsoluteUrl))
            print("Total Pages: {}\n".format(str(totalPages)))
            print("Current Page: {}\n".format(str(currentPage)))
            
    except Exception as e:
        
        print("All data collected from vssi event reports API...\n")
        print("Error: {}\n".format(e))
        
    return vssiData
        


def compile_vssi_report( vssiPageData, startDate, endDate ):
    
    y_cntr = 0
    s_cntr = 0
    x1_cntr = 0
    x2_cntr = 0
    z1_cntr = 0
    z2_cntr = 0
    t_cntr = 0   
    int_cntr = 0
    swell_cntr = 0
    sag_cntr = 0

    for pageArr in vssiPageData:
        
        #vssiEventData = []
        
        for vssiObj in pageArr:
            
            eventType = vssiObj["eventType"]
            iticRegion = vssiObj["iticRegion"]
            timeStamp = vssiObj["timestamp"]
            eventDurationFull = vssiObj["eventDuration"]
            eventDurationMill = vssiObj["durationInMilliseconds"]
            eventDepth = vssiObj["eventDepth"]
            eventChar = sag_event_characterization( int(eventDurationMill), int(eventDepth) )
            phAVbase = vssiObj["phAVbase"]
            vaMin = vssiObj["vaMin"]
            vaMax = vssiObj["vaMax"]
            phBVbase = vssiObj["phBVbase"] 
            vbMin = vssiObj["vbMin"]
            vbMax = vssiObj["vbMax"]
            phCVbase = vssiObj["phCVbase"]
            vcMin = vssiObj["vcMin"]
            vcMax = vssiObj["vcMax"]
            
#            print("\nEvent Type: {}".format( eventType ) )
#            print("Event Region: {}".format( iticRegion ) )
#            print("Event Timestamp: {}".format( timeStamp ) )
#            print("Event Duration Full: {} ms".format( eventDurationFull ) )
#            print("Event Duration Milli-seconds: {} ms".format( eventDurationMill ) )
#            print("Event Depth: {}".format( eventDepth ) )
#            print("Event Characterization: {}".format( eventChar ) )
#            print("Va Base: {}".format( phAVbase ) )
#            print("Va Minimum: {}".format( vaMin ) )
#            print("Va Maximum: {}".format( vaMax ) ) 
#            print("Vb Base: {}".format( phBVbase ) )
#            print("Vb Minimum: {}".format( vbMin ) )
#            print("Vb Maximum: {}".format( vbMax ) ) 
#            print("Vc Base: {}".format( phCVbase ) )
#            print("Vc Minimum: {}".format( vcMin ) )
#            print("Vc Maximum: {}".format( vcMax ) )
            
            if( eventType == "INT" ):
                
                int_cntr += 1
                
            elif( eventType == "SAG" ):
                
                sag_cntr += 1
                
            elif( eventType == "SWEL" ):
                
                swell_cntr += 1
                
                
            if( eventType != "INT" and eventType != "SAG" ):
                
                print("\nEvent Type: -> {}\n".format(eventType))
                
                
            
            if( eventChar == "Y" ):
                
                y_cntr += 1
                
            elif( eventChar == "X1" ):
                
                x1_cntr += 1 
                
            elif( eventChar == "X2" ):
                
                x2_cntr += 1
                
            elif( eventChar == "S" ):
                
                s_cntr += 1
                
            elif( eventChar == "Z1" ):
                
                z1_cntr += 1
                
            elif( eventChar == "Z2" ):
                
                z2_cntr += 1
                
            elif( eventChar == "T" ):
                
                t_cntr += 1
            
            
            #vssiEventArr = get_vssi_event( str( vssiObj["vssiEventUrl"] ) )
            
#            for vssiEventObj in vssiEventArr:
#                
#                print("VSSI Event Data:\n{}\n".format( str( vssiEventObj ) ) )
#                    
#                vssiEventData.append( str( vssiEventObj ) )
            
    print("\nVSSI Number of Occurances Summary:")
    print("Period: {} to {}\n".format(startDate, endDate))
    print("Total Interruptions: {}".format(int_cntr))
    print("Total Swells: {}".format(swell_cntr))
    print("Total Sags: {}".format(sag_cntr))
    print(" Sag Breakdown:")
    print(" -> Y: {}".format(y_cntr))
    print(" -> X1: {}".format(x1_cntr))
    print(" -> X2: {}".format(x2_cntr))
    print(" -> S: {}".format(s_cntr))
    print(" -> Z1: {}".format(z1_cntr))
    print(" -> Z2: {}".format(z2_cntr))
    print(" -> T: {}".format(t_cntr))
    
    vssiReport = {
            
            "Start Date": startDate,
            "End Date": endDate,
            "Total Interruptions": int_cntr,
            "Total Swells": swell_cntr,
            "Total Sags": sag_cntr,
            "Y": y_cntr,
            "X1": x1_cntr,
            "X2": x2_cntr,
            "S": s_cntr,
            "Z1": z1_cntr,
            "Z2": z2_cntr,
            "T": t_cntr    
    }
    
    return vssiReport
    
    


