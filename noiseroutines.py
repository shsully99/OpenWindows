import math

#from cv2 import SimpleBlobDetector_Params


# Calculate noise for single element
def calcnoisesingle (selectedelement,
                strIncidentSpectra,
                gsVolume, 
                gsRev):

    #print ("def calcnoisesingle " )
    #print (strIncidentSpectra)
    #print (selectedelement)

    gciMinSpectra = 0
    gciMaxSpectra = 5

    #sSpectra = [float(x) for x in selectedelement["Spectra"].rstrip(';').split("/")]
    sSpectra = [0.0, 0.0, 0.0, 0.0, 0.0]
    #print (selectedelement["Hz125"])

    sSpectra[0] = float(selectedelement["Hz125"])
    sSpectra[1] = float(selectedelement["Hz250"])
    sSpectra[2] = float(selectedelement["Hz500"])
    sSpectra[3] = float(selectedelement["Hz1000"])
    sSpectra[4] = float(selectedelement["Hz2000"])
                
    sIncident = [float(x) for x in strIncidentSpectra.rstrip(';').split("/")]

    strMetric = ""
    if selectedelement["ElementType"] == "Vent":
        strMetric = "Dnew"
    else:
        strMetric = "Rw"

    #print(f"SRI Spectra {sSpectra}")
    #print(f"Incident  Spectra {sIncident}")
    #print(f"rev {gsRev} vol {gsVolume} ")

    # For each frequency from 125 to 2000 Hz
    sInternalElementSpectra = [0.0,0.0,0.0,0.0,0.0]
    sTotal = 0.0
    iLp1 = 0
    while iLp1  < gciMaxSpectra:
        sTemp = 0.0

        if (sIncident[iLp1]) > 0:  
     #       print(type(sIncident[iLp1]))
     #       print(type(selectedelement["FacadeDifference"]))
     #       print(type(selectedelement["Quantity"]))
     #       print(type(sSpectra[iLp1]))     
     #       print(type(gsVolume))                    
     #       print(type(gsRev))                        
            if strMetric == "Rw":
                print (f'Rw + {selectedelement["Quantity"]}   {gsVolume}  {gsRev}' )
                sTemp = sIncident[iLp1]  - selectedelement["FacadeDifference"] - sSpectra[iLp1] + (10 * math.log(selectedelement["Quantity"]/ gsVolume,10)) + (10 * math.log((gsRev),10)) + 11 
                #x = (10 * math.log(selectedelement["Quantity"]/ gsVolume,10)) + 8 + (10 * math.log((gsRev/0.5),10) )
                #print (f'Rw path {sIncident[iLp1]} {selectedelement["FacadeDifference"]} {sSpectra[iLp1]} {x} ')
            else:
                sTemp = sIncident[iLp1] - selectedelement["FacadeDifference"] - sSpectra[iLp1]- (10 * math.log(gsVolume,10)) + (10 * math.log(selectedelement["Quantity"],10)) + (10 * math.log((gsRev),10))+ 21 
                #print ("Dnew path")

        sInternalElementSpectra [iLp1]  = sTemp
        sTotal = sTotal + pow (10 , (sTemp / 10))
        iLp1 = iLp1 + 1

 #   print (f" returning {sTotal}  ")
#    print (10 * math.log(sTotal,10))

#   return 10 * math.log(sTotal,10), sInternalElementSpectra

    sTotal =  10 * math.log(sTotal,10)
    print (f" returning calcnoisesingle {sTotal} {sInternalElementSpectra} ")
    return sTotal, sInternalElementSpectra

            

