    # Basic room details
    #
    #
    #session["gsArea"] 
    #session["gsHeight"] 
    #session["gsVolume"] 
    #session["gsRev"]

    #   List of dictionaries - each dictionary describing the details of a facade 
    #session["facadedetails"] 
    #    Metric="Laeq16", 
    #    Spectra=mystr,
    #    Level=0.0,
    #    Label=session["Laeq16"])

    #   List of dictionaries - each dictionary describing the details of a selected elemenmt of our facade 
    #session["selectedelements"] = []
    #    ElementID=id,Quantity=sQuantity,
    #    ElementType=session["gstrFilterElementType"],
    #    ElementDescription=myElement.Description,
    #    FacadeDifference=                                
    #    session["gsFacadeDifference"],
    #    Hz125=myElement.Hz125,
    #    Hz250=myElement.Hz250,
    #    Hz500=myElement.Hz500,
    #    Hz1000=myElement.Hz1000,
    #    Hz2000=myElement.Hz2000,
    #    elementLevels=elementLevels,
    #    State="Active"

    #   Variables describing the search filters and their default values 
    #
    #   session["gstrFilterElementType"] = "Glazing"
    #   session["gsFilterQuantity"] = session["gsArea"]/2/4
    #   session["gsFacadeDifference"]= 0 
    #   session["elementtypeslist"] = ["Glazing","Wall","Door","OpenArea","Vent"]
    #   session["defaultquantitylist"] = [session["gsArea"]/2/4, (session["gsArea"]/2)*session["gsHeight"], 2,0,5000]

    #   Variable describign current display status, room details, search elemeents or display of selected elements 
    #   session["status"] = "RoomDetails"


#from readline import get_history_length
from urllib.parse import urlencode
#from email.errors import StartBoundaryNotFoundDefect
import os
#from plistlib import InvalidFileException
#from unittest.loader import VALID_MODULE_NAME
import pandas
import math
#import numbers
#import numpy
from pathlib import Path
from flask_login import login_user

#from noiseroutines import calcnoiseall
from noiseroutines import calcnoisesingle
from download import DownloadFile

from ssl import get_server_certificate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for,send_file
from flask_login import LoginManager
from flask import Response


from datetime import datetime
global gpElementData
global strSetinPost
strLevel = "set globally"
app = Flask(__name__)
from forms import LoginForm, RegisterForm
from flask_login import UserMixin
from flask_login import login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
#app.secret_key = 'BAD_SECRET_KEY'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'ElementSRIs.sqlite')

db = SQLAlchemy(app)
login_manager = LoginManager()
 #Added this line fixed the issue.
login_manager.init_app(app)
login_manager.login_view = 'app.login'
login_manager.init_app(app)


    #   Declaration of database class
class ElementSRI(db.Model):

    __tablename__ = 'ElementSRIs'
    UniqueID = db.Column(db.Integer, primary_key=True)
    ElementType= db.Column(db.String(64))
    Description= db.Column(db.String(64))
    Reference= db.Column(db.String(64))
    Metric= db.Column(db.String(64))
    Hz63 = db.Column(db.Integer)
    Hz125 = db.Column(db.Integer)
    Hz250 = db.Column(db.Integer)
    Hz500 = db.Column(db.Integer)
    Hz1000 = db.Column(db.Integer)
    Hz2000 = db.Column(db.Integer)
    Hz4000 = db.Column(db.Integer)
    Hz8000 = db.Column(db.Integer)
    Spectra= Hz125 + "/" + Hz250 + "/" + Hz500 + "/" + Hz1000 + "/" + Hz2000 
    OpenArea = db.Column(db.Integer)

    def __init__(self,     UniqueID ,    ELementType,    Description,    Reference,
                Metric,    Hz63,   Hz125,  Hz250,  Hz500,  Hz1000, Hz2000, Hz4000, Hz8000,  OpenArea):

            UniqueID = self.UniqueID 
            ElementType= self.ElementType
            Description= self.Description
            Reference= self.Reference
            Metric= - self.Metric
            Hz63 = self.Hz63
            Hz125 = self.Hz125
            Hz250 = self.Hz250
            Hz500 = self.Hz500
            Hz1000 = self.Hz1000
            Hz2000 = self.Hz2000
            Hz4000 = self.Hz4000
            Hz8000 = self.Hz8000
            OpenArea = self.OpenArea

    def __repr__(self):
        return '<ElementSRIs %r>' % self.Description


class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    full_name= db.Column(db.String(55),unique=False)

    is_active = db.Column(db.Boolean,default=True)
    email = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return '<User %r>' % self.full_name


# @app.before_first_request
# def create_tables():
#     db.create_all()
def init_db():
    # db.drop_all()
    db.create_all()

    # Create a test user
    # hashed_password = generate_password_hash('12345678v', method='sha256')
    # new_user = User(email='adminss@gmail.com',password=hashed_password)
    # new_user.full_name = 'Nathansssssss'
    # db.session.add(new_user)
    # db.session.commit()
    #
    # new_user.datetime_subscription_valid_until = datetime(2019, 1, 1)
    # db.session.commit()

@app.route('/login/', methods=['GET', 'POST'])
def login():

    error = None

    form = LoginForm(request.form)

    print(form.validate)
    if request.method == 'POST' and form.validate():

        user = User.query.filter_by(email=form.email.data).first()

        print(user,'+++++++++++++++++++',form.email.data)
        if user:

            if check_password_hash(user.password, form.password.data):

                #flash('You have successfully logged in.', "success")

                session['logged_in'] = True

                session['email'] = user.email
                login_user(user)

                return redirect('/')

            else:


                #flash('Username or Password Incorrect', "Danger")

                error = 'Username or Password Incorrect'

                print ("login failed")

                return render_template('logmein.html', form=form, error=error)
                # return redirect(url_for('auth'))


    return render_template('/search.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():

    error = None

    form = RegisterForm(request.form)

    print(form.data,'ggggggggggggggg')

    print(form.data["full_name"])
    print(form.data["email"])

    session["Username"] = form.data["full_name"]
    session["email"] =  form.data["email"]

    if request.method == 'POST':

        print(form.data,'validated')

        if form.data["password"] != form.data["confirm"]:
            error = 'Error. passwords must match'
            return render_template('registration.html', form=form,error=error)

        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(

            full_name=form.full_name.data,

            email=form.email.data,

            password=hashed_password)

        db.session.add(new_user)

        db.session.commit()

        flash('You have successfully registered', 'success')

        return redirect('/')

    else:

        return render_template('register.html', form=form)


#@app.route('/set_option', methods=['post'])
#def set_option():
#    print ("set option")
#    session['val1'] = request.form.get('arg1')
#    session['val2'] = request.form.get('arg2')
#    return Response (status = 200)

@app.route('/logout/')
def logout():
    logout_user()

    session['logged_in'] = False

    return redirect('/')

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

@app.route('/', methods=['POST', 'GET'])
def index():
    print ("def index():")
    #first time in - set up for room details 

    #session["Laeq16"] = "Daytime L<sub>Aeq,16h</sub>"
    #session["Laeq8"] = "Night-time L<sub>Aeq,8h</sub>"
    #session["LamaxV"] = "Ventilation L<sub>AFmax</sub>"
    #session["LamaxO"] = "Overheating L<sub>AFmax</sub>"    

    if request.method == 'POST':
        print("In post method of index")

        session["status"] = "RoomDetails"
        
        return redirect('/search')

    else:        

        print("In get method of index - never executed? ")
        strLevel = "Here is the level"
        strRet = ClearSessionVariables()
       
        return render_template('search.html', facadedetails= session["facadedetails"])


@app.route('/registration/', methods=['GET'])
def Userregistration():
    print ("registration")
    session["Username"] = ""
    session["email"] = ""
    return render_template('registration.html')    

@app.route('/search', methods=['POST', 'GET'])
def search():
    print ("def search():")

    if request.method == 'POST':
        strRet = SetupSessionVariables()
        print(f"*** In post method of search " + strRet + session["status"] + str(session["gsFilterQuantity"]))  

        if (strRet != "Success"):
            print ("setup failed" + strRet)
            return render_template('search.html', BadEntry = strRet,
                                            facadedetails = session["facadedetails"],
                                defaultquantitylist= session["defaultquantitylist"])


        # if (session["status"] == "RoomDetails"):
        #     # Validate RoomDetails - return error or show search display page
        #     strRet = SetupSessionVariables()
        #     if strRet != "Success":
        #         return render_template('search.html',BadEntry = strRet)
        #     else:
        #         session["status"] = "SearchDisplay"
        #         return render_template('search.html')


            # First time Search display, validate entries
    
        querySearch  = GetfromDataBase(1)

        df = SetupSRIs(querySearch)

        session["status"] = "SearchDisplay"

        session.modified = True

        return render_template('search.html',
                                df = df,
                                querySearch = querySearch,
                                facadedetails = session["facadedetails"],
                                defaultquantitylist= session["defaultquantitylist"])

    else:

        print(f"*** In get  method of search - do we ever get here? ")
        session["elementtypeslist"] = ["Glazing", "Wall", "Door", "OpenArea", "Vent"]
        return render_template('search.html')

@app.route('/paginate', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/paginate/<int:page>', methods=['GET', 'POST'])
def paginate(page):
    print ("def paginate(page):")
    page = page
    pages = 5

    querySearch = GetfromDataBase (page)

    df = SetupSRIs (querySearch)    

    print (df)

    return render_template('search.html', querySearch=querySearch, df=df, facadedetails=session["facadedetails"],
                                    defaultquantitylist= session["defaultquantitylist"])

# Toggle elements between selected and deselected 
# Recalculate the noise to take account of the change

@app.route('/change/<int:id>', methods=['GET', 'POST'])
def change(id):
    print(f"def change ({id}): ")    
    #print (session["selectedelements"])
    for k in range(len(session['selectedelements'])):
        print (f" on entry {session['selectedelements'][k]['State']}")    

    for j in range(len(session['selectedelements'])):

        if session['selectedelements'][j]["ElementID"] == id:            
            if session['selectedelements'][j]["State"] == "Inactive":
                session['selectedelements'][j]["State"] = "Active"
            else:
                session['selectedelements'][j]["State"] = "Inactive"

            break

    # Recalc the level per selected element now that we have changed the elements 
    SetupTotals()

    session["FacadeColumn"] = IsFacadeColumnRequired()

    #print (session["selectedelements"])

    for k in range(len(session['selectedelements'])):
        print (f" leaving {session['selectedelements'][k]['State']}")    

    session.modified = True
        
    return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"], 
                                    defaultquantitylist= session["defaultquantitylist"])

#   Add an element 
@app.route('/add/<int:id>', methods=['GET', 'POST'])
def add(id):
    print(f"def add({id}): ")  

    if session["status"] == "ElementDisplay":
        print ("Someone pressed refresh")
        # If we are here in ElementDisplay mode then it means the user has pressed refresh - we do not want to add another element 
        return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"], 
                                    defaultquantitylist= session["defaultquantitylist"])
      
    #if (session['selectedcount'] > 0 ):
    #    print(f"*** Count {len(session['selectedelements'])}")  
            
    myElement = ElementSRI.query.filter(ElementSRI.UniqueID == id).first()

    elementLevels = []
    for i in range (0,len(session["facadedetails"])):
        #if session["facadedetails"][i]["FacadeSpectra"] != "":
        elementLevels.append(dict(Metric=session["facadedetails"][i]["Metric"],
        Level = 0.0,
        Spectra = [0.0,0.0,0.0,0.0,0.0,0.0],
        Percent = 0.0))

    sQuantity = 0.0
    sQuantity = session["gsFilterQuantity"]

    if myElement.Metric == "Dnew":
        if myElement.ElementType == "OpenArea":
            sQuantity = 1
        else: # vent 
            sQuantity = int((session["gsFilterQuantity"] - 1) / (int(myElement.OpenArea))) + 1
    else: 
        if myElement.ElementType == "OpenArea":
            sPercent = 0.0
            strPercent = myElement.Description.split("%")
            sPercent = float(strPercent[0])
            sQuantity = sPercent * session["gsArea"] / 100 

    selectedelement = dict(ElementID=id,Quantity=sQuantity,
                        ElementType=session["gstrFilterElementType"],
                        ElementDescription=myElement.Description,
                        FacadeDifference=                                
                        session["gsFacadeDifference"],
                        Hz125=myElement.Hz125,
                        Hz250=myElement.Hz250,
                        Hz500=myElement.Hz500,
                        Hz1000=myElement.Hz1000,
                        Hz2000=myElement.Hz2000,
                        elementLevels=elementLevels,
                        State="Active")

    session["selectedelements"].append(selectedelement) 

   
    #for i in range (0,len(session["facadedetails"])):
    #    if session["facadedetails"][i]["FacadeSpectra"] != "":
    #        facade = session["facadedetails"][i]
    #        SingleLevel, SpectraLevels = calcnoisesingle (selectedelement, 
    #                            facade["FacadeSpectra"],
    #                            session["gsVolume"],
    #                            session["gsRev"])

    #        selectedelement["elementLevels"][i]["Level"] = SingleLevel
    #        selectedelement["elementLevels"][i]["Spectra"] = SpectraLevels            
       
    #session["selectedelements"].append(selectedelement) 
    #session['selectedcount'] = session['selectedcount'] + 1

    # The percentages have now changed so re-assign them to the array 
    SetupTotals()

    session["FacadeColumn"] = IsFacadeColumnRequired()

    print (f'Just added {len(session["selectedelements"])}')

    # Loop over elememnts and update selected levels
    session["status"] = "ElementDisplay"

    return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"], 
                                    defaultquantitylist= session["defaultquantitylist"])

#   Download currently selected in spreadsheet 
@app.route('/download', methods=['POST', 'GET'])
def download ():

    print ("def download ():")

    strFile = DownloadFile (session["selectedelements"],  session["facadedetails"], session["gsVolume"], session["gsRev"], ElementSRI)

    #return send_file (strFile, attachment_filename='Download.xlsx', as_attachment=True)
    #return send_file (strFile, attachment_filename='Download.xlsx', as_attachment=True)
    return send_file (strFile,  as_attachment=True)

@app.route('/about/', methods=['GET'])
def about ():
    return render_template('about.html')

@app.route('/help/', methods=['GET'])
def help ():
    return render_template('help.html')

@app.route('/contacts/', methods=['GET'])
def contacts ():
    return render_template('contacts.html')

@app.route('/logmein/', methods=['GET'])
def logmein ():
    print ("logmein")
    return render_template('logmein.html')


@app.route('/toggle/', methods=['GET', 'POST'])
def toggle ():
    print ("def toggle ():")
    if session["status"] == "ElementDisplay":
      
        session["status"] = "SearchDisplay"
    else:
        session["status"] = "ElementDisplay"

    return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"]) 

# Someone with s shared link wants to see the elements displayed 
@app.route('/automate', methods=['GET', 'POST'])
def automate():

    print ("def automate():")

    args = request.args
    parsedict= args.to_dict(flat=False)

    session["gsArea"] = float(parsedict['gsArea'][0])
    session["gsHeight"] = float(parsedict['gsHeight'][0])
    session["gsVolume"] = session["gsArea"] * session["gsHeight"] 
    session["gsRev"] = 0.5 

    session["facadedetails"] = []
    metList = parsedict['MetricList'][0].rstrip(']').lstrip('[').split(',')
    spectraList = parsedict['SpectraList'][0].rstrip(']').lstrip('[').split(',')


    session["Laeq16"] = "Daytime L<sub>Aeq,16h</sub>"
    session["Laeq8"] = "Night-time L<sub>Aeq,8h</sub>"
    session["LamaxV"] = "Ventilation L<sub>AFmax</sub>"
    session["LamaxO"] = "Overheating L<sub>AFmax</sub>"  

    for i,j in zip(metList,spectraList):
        Metric = i.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'")
        Spectra = j.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'")
        # Validate the spectra at this point 
        Label = ""

        if Metric == "Laeq16": Label="Daytime L<sub>Aeq,16h</sub>"
        elif Metric == "Laeq8": Label = "Night-time L<sub>Aeq,8h</sub>"
        elif Metric == "LamaxV": Label = "Ventilation L<sub>AFmax</sub>"
        elif Metric == "LamaxO": Label = "Overheating L<sub>AFmax</sub>"  

        # The spectra field should be blank
        strDisplay = ""
        sNoise = 0.0

        if Spectra != "":
            strRet = ValSpectra(Spectra)
            # todo - sort out error here 
            if strRet != "Validated":
                render_template('search.html',BadEntry = strRet)    

            strDisplay, sNoise = SetSpectra(Spectra)
        
        facade = dict(Metric=Metric, FacadeSpectra=Spectra,FacadeLevel=sNoise, FacadeDisplay = strDisplay, InternalSpectra="",InternalLevel=0.0, InternalDisplay="", Label=Label)

        session["facadedetails"].append(facade)
    
    session["selectedelements"] = []
    #session['selectedcount'] = 0

    elIDList = parsedict["ElementIDList"][0].rstrip(']').lstrip('[').split(',')   
    QList = parsedict["QuantityList"][0].rstrip(']').lstrip('[').split(',') 
    FDList = parsedict["FacDifList"][0].rstrip(']').lstrip('[').split(',') 

    for i,j,k in zip(elIDList,QList, FDList):

        ElementID = int(i.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'"))
        Quantity = float(j.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'"))
        FacDif = int(k.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'"))

        myElement = ElementSRI.query.filter(ElementSRI.UniqueID == ElementID).first()
        print(myElement)

        elementLevels = []

        for i in range (0,len(session["facadedetails"])):
            #if session["facadedetails"][i]["FacadeSpectra"] != "":
            elementLevels.append(dict(Metric=session["facadedetails"][i]["Metric"],
            Level = 0.0,
            Spectra = [0.0,0.0,0.0,0.0,0.0,0.0],
            Percent = 0.0))

            selectedelement = dict(ElementID=ElementID,
                                Quantity=Quantity,
                                ElementType=myElement.ElementType,
                                ElementDescription=myElement.Description,
                                FacadeDifference=FacDif,
                                Hz125=myElement.Hz125,
                                Hz250=myElement.Hz250,
                                Hz500=myElement.Hz500,
                                Hz1000=myElement.Hz1000,
                                Hz2000=myElement.Hz2000,
                                elementLevels=elementLevels,
                                State="Active")
    
        for i in range (0,len(session["facadedetails"])):
            if session["facadedetails"][i]["FacadeSpectra"] != "":
                facade = session["facadedetails"][i]
                SingleLevel, InternalSpectra = calcnoisesingle (selectedelement, 
                                    facade["FacadeSpectra"],
                                    session["gsVolume"],
                                    session["gsRev"])

                selectedelement["elementLevels"][i]["Level"] = SingleLevel
                selectedelement["elementLevels"][i]["Spectra"] = InternalSpectra
    
        session["selectedelements"].append(selectedelement) 
        #session['selectedcount'] = session['selectedcount'] + 1

    SetupTotals()

    session["FacadeColumn"] = IsFacadeColumnRequired()

    # Loop over elememnts and update selected levelssession
    session["status"] = "ElementDisplay"

    print ("Returning from automate ")

    return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"],
                                    defaultquantitylist=session["defaultquantitylist"])    
    #return render_template('search.html')    
    
# Share button pressed - build up the url to allow sharing '  
@app.route('/share', methods=['GET', 'POST'])
def share():
    print ("def share():")
    parsedict = {"Version": 1.000, "gsArea": session["gsArea"], "gsHeight" : session["gsHeight"]}
    MetricList = []
    SpectraList = []

    for facade in session["facadedetails"]:
        MetricList.append(facade["Metric"])        
        SpectraList.append(facade["FacadeSpectra"])

    parsedict ["MetricList"] = MetricList
    parsedict["SpectraList"] = SpectraList

    ElementIDList = []
    QuantityList = [] 
    FacDifList = [] 

    for sElement in session["selectedelements"]:
       ElementIDList.append(sElement["ElementID"])
       QuantityList.append(sElement["Quantity"])
       FacDifList.append(sElement["FacadeDifference"])

    parsedict ["ElementIDList"] = ElementIDList
    parsedict["QuantityList"] = QuantityList
    parsedict["FacDifList"] = FacDifList

    shareString = urlencode(parsedict)
    shareString  = "/automate?" + shareString 

    print (shareString )

    session["status"] = "ShareDisplay"
    return render_template('search.html',shareString=shareString, facadedetails=session["facadedetails"],defaultquantitylist= session["defaultquantitylist"])

    #   return ("/automate?" + s)
    

@app.route('/remove/<int:id>', methods=['GET', 'POST'])
def remove(id):
    print(f"*** In remove routine ")    
    #if (session['selectedcount'] > 0 ):
    #    print(f"*** Count {len(session['selectedelements'])}")    
    bFound = False
    for selectedelement in session["selectedelements"]:
        if selectedelement["ElementID"] == id:
            session["selectedelements"].remove(selectedelement)
            bFound = True
    #        session['selectedcount'] = session['selectedcount'] - 1

    if bFound == False: 
        # We have not found a match - most likely someone refreshed the browser after a delete and the URL from a delete was re-actioned 
        print ("No match ")
        return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"],
                                    defaultquantitylist= session["defaultquantitylist"])

    # if we are down to 0 then knock it on the head 
    #if session['selectedcount'] == 0: 
    if len(session['selectedelements']) == 0: 
        for i in range (0,len(session["facadedetails"])):
            session["facadedetails"][i]["InternalLevel"] = 0.0
            session["facadedetails"][i]["InternalDisplay"]= ""            

        # Go back to searching for elements 
        session["status"] = "SearchDisplay"
        #return render_template('search.html')
        return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"],
                                    defaultquantitylist= session["defaultquantitylist"])

    # The percentages have now changed so re-assign them to the array 
    SetupTotals()

    session["FacadeColumn"] = IsFacadeColumnRequired()

    session["status"] = "ElementDisplay"
    return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"],
                                    defaultquantitylist= session["defaultquantitylist"])

# Set up global variables from the user entries
def ClearSessionVariables():

    print ("def clear sessionvaribles")
    #session["gstrRoomType"] = request.form.get('roomtype')

    # Check axh for Room Dimensions and assign variables accordingly
    #print( request.form.get('RoomDimensions'),'ssssssssss')
    #strRD = request.form.get('RoomDimensions').split("x")
    ##print(strRD)
    #if (len(strRD) != 2 ):
    #    return "Error. Enter Room Dimensions in format axh where a = floor area isetupsessionn metres  and h = height in metres"

    #if math.isnan(float(strRD[0])) or math.isnan(float(strRD[1])):
    #    #print("except " + strRD[0] + "/" + strRD[1])
    #    return "Error. Enter Room Dimensions in format axxx h where a = floor area in metres  and h = height in metres"
 
    session["gsArea"] = 7.5
    session["gsHeight"] = 2.4
    session["gsVolume"] = 18.0
    session['RoomDimensions'] = "7.5x2.4"
    #session["RoomDimensions"] = ""
    session["RoomDimensionsLabel"] = "18 m3"

    # Hardcode for now 
    session["gsRev"] = 0.5 

    session["Laeq16"] = "Daytime L<sub>Aeq,16h</sub>"
    session["Laeq8"] = "Night-time L<sub>Aeq,8h</sub>"
    session["LamaxV"] = "Ventilation L<sub>AFmax</sub>"
    session["LamaxO"] = "Overheating L<sub>AFmax</sub>"    

    session["facadedetails"] = []
    facade = dict(Metric="Laeq16", FacadeSpectra="46.0-46.0-52.0-50.0-45.0",FacadeLevel=56.0, FacadeDisplay = "46.0-46.0-52.0-50.0-45.0 (56.0)", InternalSpectra="",InternalLevel=0.0, InternalDisplay="",
    Label=session["Laeq16"])
    session["facadedetails"].append(facade)

    facade = dict(Metric="Laeq8", FacadeSpectra="",FacadeLevel=0.0, FacadeDisplay = "", InternalSpectraA="",InternalLevel=0.0, InternalDisplay="",
    Label=session["Laeq8"])
    session["facadedetails"].append(facade)

    facade = dict(Metric="LamaxV", FacadeSpectra="",FacadeLevel=0.0, FacadeDisplay = "", InternalSpectra="",InternalLevel=0.0, InternalDisplay="",
    Label=session["LamaxV"])
    session["facadedetails"].append(facade)

    facade = dict(Metric="LamaxO", FacadeSpectra="",FacadeLevel=0.0, FacadeDisplay = "", InternalSpectra="",InternalLevel=0.0, InternalDisplay="",
    Label=session["LamaxO"])
    session["facadedetails"].append(facade)
    
    session["selectedelements"] = []

    session["gstrFilterElementType"] = "Glazing"
    session["gsFilterQuantity"] = 2

    session["elementtypeslist"] = ["Glazing","Wall","Door","OpenArea","Vent"]
    session["defaultquantitylist"] = [2, 10 , 2,0,2500]

    print (session["defaultquantitylist"])

    session["gsFacadeDifference"]= 0 
    session["gstrFilterField"] = ""

    session['Laeq16Spectra'] = ""
    session['Laeq8Spectra']  = ""
    session['LamaxvSpectra']  = ""
    session['LamaxoSpectra']  = ""

    session['Laeq16SpectraLabel']  = ""
    session['Laeq8SpectraLabel']  = ""
    session['LamaxvSpectraLabel']  = ""
    session['LamaxoSpectraLabel']  = ""
    session["status"] = "RoomDetails"
    session["elementtypeslist"] = ["Glazing", "Wall", "Door", "OpenArea", "Vent"]

    return "Success"

def SetupSessionVariables():

    print ("def setupsessionvaribles")

    #session["gstrRoomType"] = request.form.get('roomtype')
    iCount = 0

    strText = request.form.get('Laeq16Spectra')
    if strText != "":
        strInput = strText.split()
        iCount = iCount + 1
        session["facadedetails"][0]["FacadeSpectra"] = strInput[0]
        session["facadedetails"][0]["FacadeLevel"] = strInput[1]
        session["facadedetails"][0]["FacadeDisplay"] = strInput[0] + " " + strInput[1]
        strError = ValSpectra(strInput[0])
        if strError != "Validated":
            return strError
    else:
        session["facadedetails"][0]["FacadeSpectra"] = ""
        session["facadedetails"][0]["FacadeLevel"] = ""
        session["facadedetails"][0]["FacadeDisplay"] = ""
        session["facadedetails"][0]["InternalSpectra"] = ""
        session["facadedetails"][0]["InternalLevel"] = 0.0
        session["facadedetails"][0]["InternalDisplay"] = ""

    strText = request.form.get('Laeq8Spectra')
    if strText != "":
        strInput = strText.split()
        iCount = iCount + 1
        session["facadedetails"][1]["FacadeSpectra"] = strInput[0]
        session["facadedetails"][1]["FacadeLevel"] = strInput[1]
        session["facadedetails"][1]["FacadeDisplay"] = strInput[0] + " " + strInput[1]
        strError = ValSpectra(strInput[0])
        if strError != "Validated":
            return strError
    else:
        session["facadedetails"][1]["FacadeSpectra"] = ""
        session["facadedetails"][1]["FacadeLevel"] = ""
        session["facadedetails"][1]["FacadeDisplay"] = ""
        session["facadedetails"][1]["InternalSpectra"] = ""
        session["facadedetails"][1]["InternalLevel"] = 0.0
        session["facadedetails"][1]["InternalDisplay"] = ""


    strText =  request.form.get('LamaxvSpectra')
    if strText != "":
        strInput = strText.split()
        iCount = iCount + 1
        session["facadedetails"][2]["FacadeSpectra"] = strInput[0]
        session["facadedetails"][2]["FacadeLevel"] = strInput[1]
        session["facadedetails"][2]["FacadeDisplay"] = strInput[0] + " " + strInput[1]
        strError = ValSpectra(strInput[0])
        if strError != "Validated":
            return strError
    else:
        session["facadedetails"][2]["FacadeSpectra"] = ""
        session["facadedetails"][2]["FacadeLevel"] = ""
        session["facadedetails"][2]["FacadeDisplay"] = ""
        session["facadedetails"][2]["InternalSpectra"] = ""
        session["facadedetails"][2]["InternalLevel"] = 0.0
        session["facadedetails"][2]["InternalDisplay"] = ""


    strText =  request.form.get('LamaxoSpectra')
    if strText != "":
        strInput = strText.split()
        iCount = iCount + 1
        session["facadedetails"][3]["FacadeSpectra"] = strInput[0]
        session["facadedetails"][3]["FacadeLevel"] = strInput[1]
        session["facadedetails"][3]["FacadeDisplay"] = strInput[0] + " " + strInput[1]
        strError = ValSpectra(strInput[0])
        if strError != "Validated":
            return strError
    else:
        session["facadedetails"][3]["FacadeSpectra"] = ""
        session["facadedetails"][3]["FacadeLevel"] = ""
        session["facadedetails"][3]["FacadeDisplay"] = ""
        session["facadedetails"][3]["InternalSpectra"] = ""
        session["facadedetails"][3]["InternalLevel"] = 0.0
        session["facadedetails"][3]["InternalDisplay"] = ""

    if iCount == 0:
        return "Error. there must be at last one entry for spectra."
        print ("No Spectra")


    # Check axh for Room Dimensions and assign variables accordingly
    print( request.form.get('RoomDimensions'),'ssssssssss')
    strRD = request.form.get('RoomDimensions').split("x")
    #print(strRD)
    if (len(strRD) != 2 ):
        return "Error. Enter Room Dimensions in format axh where a = floor area in metres  and h = height in metres"

    if math.isnan(float(strRD[0])) or math.isnan(float(strRD[1])):
        #print("except " + strRD[0] + "/" + strRD[1])
        return "Error. Enter Room Dimensions in format axxx h where a = floor area in metres  and h = height in metres"

    varRD = [0.0, 0.0]
    varRD[0] = float(strRD[0])
    varRD[1] = float(strRD[1])

    session["gsArea"] = varRD[0]
    session["gsHeight"] = varRD[1]
    session["gsVolume"] = varRD[0] * varRD[1]

    # Hardcode for now 
    session["gsRev"] = 0.5 
   
    #session["facadedetails"] = []
    
    # set up facade details arrau 
    #mystr = request.form.get('Laeq16Spectra')
    #if mystr != "":
    #    facade = dict(Metric="Laeq16", Spectra=mystr,Level=0.0,Label=session["Laeq16"])
    #    session["facadedetails"].append(facade)

    #mystr = request.form.get('Laeq8Spectra')
    #if mystr != "":
    #    facade = dict(Metric="Laeq8", Spectra=mystr, FacadeSpectra=mystr,Level=0.0,Label=session["Laeq8"])
    #    session["facadedetails"].append(facade)

    #mystr = request.form.get('LamaxvSpectra')
    #if mystr != "":
    #    facade = dict(Metric="LamaxV",  Spectra=mystr,Level=0.0,Label=session["LamaxV"])
    #    session["facadedetails"].append(facade)

    #mystr = request.form.get('LamaxoSpectra')
    #if mystr != "":
    #    facade = dict(Metric="LamaxO", Spectra=mystr,Level=0.0,Label=session["LamaxO"])
    #    session["facadedetails"].append(facade)
    
    # check format is 99.9-99.9-99.9-99.9-99.9-99.9


    session['RoomDimensions'] = request.form.get('RoomDimensions')
    session['RoomDimensionsLabel'] = request.form.get('RoomDimensionsLabel')

    # First time Search display, validate entries
    session["gstrFilterElementType"] = request.form.get('elementtype')
    if session["gstrFilterElementType"] != "OpenArea":
        try:
            session["gsFilterQuantity"] = float(request.form.get('Quantity'))
        except:
            return ("Error. Enter quantity")

        if (session["gsFilterQuantity"] == 0):
            return ("Error. Quantity must be greater than 0")

    session["gsFacadeDifference"] = int(request.form.get('quietfacade'))

    session["gstrFilterField"] = request.form.get('FilterField')

    # New defaults for search

    session["defaultquantitylist"] = [session["gsArea"]/2/4, (session["gsArea"]/2)*session["gsHeight"], 2,0,5000]
    if session["gstrFilterElementType"] == "Glazing":session["defaultquantitylist"][0] = session["gsFilterQuantity"]
    elif session["gstrFilterElementType"] == "Wall":session["defaultquantitylist"][1] = session["gsFilterQuantity"]
    elif session["gstrFilterElementType"] == "Door":session["defaultquantitylist"][2] = session["gsFilterQuantity"]
    elif session["gstrFilterElementType"] == "OpenArea":session["defaultquantitylist"][3] = session["gsFilterQuantity"]
    elif session["gstrFilterElementType"] == "Vent":session["defaultquantitylist"][4] = session["gsFilterQuantity"]

    print("After setup")
    print(session["facadedetails"])

    #session['selectedcount'] = 0
    #if (session['selectedcount'] > 0 ):
    #    print(f"*** Count {len(session['selectedelements'])}")    
    
    #session["SelectedCount"] = 0;

    session.modified = True

    return "Success"


def ValSpectra(strSpectra):
    print ("def ValSpectra")
    print (strSpectra)
    for str in strSpectra.split('-'):
        if(math.isnan(float(str))):
            return "Error. Invalid spectra entry. Enter format 99.9-99.9-99.9-99.9-99.9-99.9"
    
    return "Validated"

def SetSpectra (strSpectra):

    print ("def SetSpectra")    

    # Receives a spectra string e.g. "46.0-46.0-52.0-50.0-45.0 (56.0)" which has been validated and returns 
    # a display string "46.0-46.0-52.0-50.0-45.0 (56.0) and a total e.g. 56"

    sAntiLogTot = 0.0

    for mystr in strSpectra.split('-'):
        if(math.isnan(float(mystr))):
            return "Error. Invalid spectra entry. Enter format 99.9-99.9-99.9-99.9-99.9-99.9"
        print (mystr)
        sAntiLogTot = sAntiLogTot + pow (10 , (float(mystr) / 10))  

    sTot = round(10 * math.log(sAntiLogTot,10) ,1)
    strDisplayString  = strSpectra + " (" + str(sTot) + ")"

    return strDisplayString, sTot

def GetfromDataBase(page):
    # Read from thee database for a page 
    print ("def GetfromDataBase (page):")

    pages = 5
            
    tag = "%{}%".format(session["gstrFilterField"])

    PageofElements = ElementSRI.query.filter(ElementSRI.ElementType == session["gstrFilterElementType"], ElementSRI.Description.like(tag)).paginate(page=page,per_page=5,error_out=False)

    return PageofElements 

def SetupSRIs (PageofElements):
    print ("def SetupSRIs (PageofElements):")

    # Set up a pandas dataframe of SRIs which will be displayed by jinja alongside a page of element data 
    df = pandas.DataFrame()

    for facade in session["facadedetails"]:
        if facade["FacadeSpectra"] != "":
            tstr = facade["Metric"]
            df[tstr] =  0.0
    df['UniqueID'] = 0.0
    
    i=0
    # For each row in a page of elements, set up the SRIs for each metric
    for Row in PageofElements.items:

        sQuantity = 0.0
        sQuantity = session["gsFilterQuantity"]
        if Row.Metric == "Dnew":
            if Row.ElementType == "OpenArea":
                sQuantity = 1
            else: # vent 
                sQuantity = int((session["gsFilterQuantity"] - 1) / (int(Row.OpenArea))) + 1
        else: 
            if Row.ElementType == "OpenArea":
                sPercent = 0.0
                strPercent = Row.Description.split("%")
                sPercent = float(strPercent[0])
                sQuantity = sPercent * session["gsArea"] /100

        # Put our element into a dictionay that calc noise can understnd 
        selectedelement = dict(ElementID=Row.UniqueID,
                            Quantity=sQuantity,
                            ElementType=session["gstrFilterElementType"],
                            ElementDescription=Row.Description,
                            FacadeDifference=session["gsFacadeDifference"],
                            Hz125=Row.Hz125, 
                            Hz250=Row.Hz250, 
                            Hz500=Row.Hz500, 
                            Hz1000=Row.Hz1000,
                            Hz2000=Row.Hz2000,
                            State="Active")

        for facade in session["facadedetails"]:
            if facade["FacadeSpectra"] != "":
                sNoise, sSpectra = calcnoisesingle (selectedelement, 
                                    facade["FacadeSpectra"],
                                    session["gsVolume"],
                                    session["gsRev"])
                
                #Row[facadedetails["Metric"]] = sNoise
                # todo tidy up 
                tstr = facade["Metric"]

                # Show the level with the "new" nosie added
                lTotalAntiLog =  pow (10 , (facade["InternalLevel"] / 10)) + pow (10 , (sNoise / 10))                
                print (f' snoise {sNoise} facadedetailsLevel {facade["InternalLevel"] } ' )
                df.loc[i,[tstr]] = 10 * math.log(lTotalAntiLog,10)
            
        df.loc[i,['UniqueID']] = Row.UniqueID        

        i=i+1

    return df 

def IsFacadeColumnRequired():
    # Called after the elements array is chenged to determine if we need to show a facade column 
    for j in range (0,len(session["selectedelements"])):
        if session["selectedelements"][j]["FacadeDifference"] > 0:
            return True
    return False 
    
def SetupTotals():
    
    print ("def SetupTotals():")

    # for each facade detail recalculate the sound level for all of the elements
    for i in range (0,len(session["facadedetails"])):

        if session["facadedetails"][i]["FacadeSpectra"] != "":

            #lTotalAntiLog  = 0.0 
            #sTemp = 0.0

            #sAllSpectra  = [0.0, 0.0, 0.0, 0.0, 0.0]
            # Iterate over the selected elements
            j = 0
            for j in range (0,len(session["selectedelements"])):

                if session["selectedelements"][j]["State"] == "Active":

                    sTotalElement, sInternalSpectraElement = calcnoisesingle(session["selectedelements"][j],
                                    session["facadedetails"][i]["FacadeSpectra"],
                                    session["gsVolume"], 
                                    session["gsRev"])
                
                    #j=0
                    #for j in range(0,len(sAllSpectra)):
                    #    sAllSpectra[j] = sAllSpectra[j] + pow (10 , (sInternalSpectraElement[j] / 10))
                    
                    session["selectedelements"][j]["elementLevels"][i]["Level"] = sTotalElement
                    session["selectedelements"][j]["elementLevels"][i]["Spectra"] = sInternalSpectraElement

    gciMaxSpectra =5

    # We have have added, modded, removed or turned off an element so recalculate the totals based on the values of the elements array
    for i in range (0,len(session["facadedetails"])):
        if session["facadedetails"][i]["FacadeSpectra"] != "":
            sAntiLogOverall = 0.0
            sAntiLogSpectra = [0.0,0.0,0.0,0.0,0.0]
            for j in range (0,len(session["selectedelements"])):
                if session["selectedelements"][j]["State"] == "Active":            
                    sElementLevel = session["selectedelements"][j]["elementLevels"][i]["Level"] 
                    sElementSpectra = session["selectedelements"][j]["elementLevels"][i]["Spectra"]                     
                    print (f" Looping {sElementLevel} {sElementSpectra}")
                    iLp1 = 0
                    while iLp1  < gciMaxSpectra:
                        sAntiLogSpectra[iLp1] = sAntiLogSpectra[iLp1]+ pow (10, sElementSpectra[iLp1]/10)
                        iLp1+=1

                    sAntiLogOverall = sAntiLogOverall + pow (10, sElementLevel/10)

            session["facadedetails"][i]["InternalLevel"] = 10 * math.log(sAntiLogOverall,10)
            session["facadedetails"][i]["InternalSpectra"], session["facadedetails"][i]["InternalDisplay"] = AntiLogSpectraToString(sAntiLogSpectra)
            
            session["facadedetails"][i]["facadeBackColourClass"] = SetBackColourClass(session["facadedetails"][i]["InternalLevel"],
                                                                                      session["facadedetails"][i]["Metric"])
            session["facadedetails"][i]["InternalLevel"]


            print ( session["facadedetails"][i]["InternalSpectra"])
            print (session["facadedetails"][i]["InternalDisplay"])

    # Called after the selected elements array has changed to update the percentages on each element.     
    # Also a good time to 0 out unuued spectra
    print ("-------------------------------")
    for i in range (0,len(session["facadedetails"])):
        if session["facadedetails"][i]["FacadeSpectra"] != "":
            sTotal = session["facadedetails"][i]["InternalLevel"]
            for j in range (0,len(session["selectedelements"])):
                if session["selectedelements"][j]["State"] == "Active":
                    sElementLevel = session["selectedelements"][j]["elementLevels"][i]["Level"]
                    session["selectedelements"][j]["elementLevels"][i]["Percent"] = round((pow (10 , (sElementLevel / 10)) / pow (10 , (sTotal / 10)))* 100,1)
                else:
                    session["selectedelements"][j]["elementLevels"][i]["Percent"] = 0

    print ("return SetupTotals():")

    return 

def AntiLogSpectraToString(sAntiLogSpectra):
    # Receives an array of 5 antilogs and returns an array of 5 logs  and disply string
    gciMaxSpectra = 5

    sInternalSpectra = [0.0,0.0,0.0,0.0,0.0]
    strInternalDisplay = ""
    sAntiLogTot = 0.0

    iLp1 = 0
    while iLp1  < gciMaxSpectra:
        sInternalSpectra[iLp1] = 10 * math.log(sAntiLogSpectra[iLp1],10)
        if iLp1 > 0: 
            strInternalDisplay = strInternalDisplay + "-"
        strInternalDisplay = strInternalDisplay + str(round(sInternalSpectra[iLp1],1))
        sAntiLogTot += sAntiLogSpectra[iLp1]
        iLp1 = iLp1 + 1 
    
    strInternalDisplay = strInternalDisplay + " (" + str(round(10 * math.log(sAntiLogTot,10),1)) + ")"

    return sInternalSpectra, strInternalDisplay

def SetBackColourClass(sLevel, strMetric):
    # Depending on the metric and the level - set the background colour to alert the user 
    if (strMetric) == "Laeq16":
        if sLevel > 35:
            strBackColor = "BackRed"
        else:
            strBackColor = "BackGreen"
    elif (strMetric) == "Laeq8":
        if sLevel > 30:
            strBackColor = "BackRed"
        else:
            strBackColor = "BackGreen"            
    elif (strMetric) == "LamaxV":
        if sLevel > 45:
            strBackColor = "BackRed"
        else:
            strBackColor = "BackGreen"
    elif (strMetric) == "LamaxO":
        if sLevel > 60:
            strBackColor = "BackRed"
        else:
            strBackColor = "BackGreen"            
    return strBackColor

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    # with app.app_context():
    #     init_db()

    app.run(debug=True)