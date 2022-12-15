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

from noiseroutines import calcnoiseall
from noiseroutines import calcnoisesingle
from download import DownloadFile

from ssl import get_server_certificate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask import Flask, render_template, flash, redirect, request, session, logging, url_for,send_file
from flask_login import LoginManager

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

    form = LoginForm(request.form)

    print(form.validate)
    if request.method == 'POST' and form.validate():

        user = User.query.filter_by(email=form.email.data).first()

        print(user,'+++++++++++++++++++',form.email.data)
        if user:

            if check_password_hash(user.password, form.password.data):

                flash('You have successfully logged in.', "success")

                session['logged_in'] = True

                session['email'] = user.email
                login_user(user)

                return redirect('/')

            else:

                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('auth'))


    return render_template('/search.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)

    print(form.data,'ggggggggggggggg')

    if request.method == 'POST' and form.validate():

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

    session["Laeq16"] = "Daytime L<sub>Aeq,16h</sub>"
    session["Laeq8"] = "Night-time L<sub>Aeq,8h</sub>"
    session["LamaxV"] = "Ventilation L<sub>AFmax</sub>"
    session["LamaxO"] = "Overheating L<sub>AFmax</sub>"    

    if request.method == 'POST':
        print("In post method of index")

        session["status"] = "RoomDetails"
        
        return redirect('/search')

    else:        

        print("In get method of index - never executed? ")
        strLevel = "Here is the level"
        # strRet = SetupSessionVariables()
        session["status"] = "RoomDetails"
        session["elementtypeslist"] = ["Glazing", "Wall", "Door", "OpenArea", "Vent"]
        return render_template('search.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    print ("def search():")

    if request.method == 'POST':
        strRet = SetupSessionVariables()
        print(f"*** In post method of search " + session["status"] )  
        # if (session["status"] == "RoomDetails"):
        #     # Validate RoomDetails - return error or show search display page
        #     strRet = SetupSessionVariables()
        #     if strRet != "Success":
        #         return render_template('search.html',BadEntry = strRet)
        #     else:
        #         session["status"] = "SearchDisplay"
        #         return render_template('search.html')


            # First time Search display, validate entries
        session["gstrFilterElementType"] = request.form.get('elementtype')
        if session["gstrFilterElementType"] != "OpenArea":
            try:
                session["gsFilterQuantity"] = float(request.form.get('Quantity'))
            except:
                strRet = "Enter quantity"
                return render_template('search.html',BadEntry = strRet)

            if (session["gsFilterQuantity"] == 0):
                strRet = "Must be greater than 0 "
                return render_template('search.html',BadEntry = strRet)

        session["gsFacadeDifference"] = int(request.form.get('quietfacade'))

        session["gstrFilterField"] = request.form.get('FilterField')

        querySearch  = GetfromDataBase(1)

        df = SetupSRIs(querySearch)

        session["status"] = "SearchDisplay"
        # New defaults for search

        session["defaultquantitylist"] = [session["gsArea"]/2/4, (session["gsArea"]/2)*session["gsHeight"], 2,0,5000]
        if session["gstrFilterElementType"] == "Glazing":session["defaultquantitylist"][0] = session["gsFilterQuantity"]
        elif session["gstrFilterElementType"] == "Wall":session["defaultquantitylist"][1] = session["gsFilterQuantity"]
        elif session["gstrFilterElementType"] == "Door":session["defaultquantitylist"][2] = session["gsFilterQuantity"]
        elif session["gstrFilterElementType"] == "OpenArea":session["defaultquantitylist"][3] = session["gsFilterQuantity"]
        elif session["gstrFilterElementType"] == "Vent":session["defaultquantitylist"][4] = session["gsFilterQuantity"]

        session.modified = True

        print('mtkkkkkkkkkkkkkkav',querySearch)

        session['RoomDimensions'] =request.form.get('RoomDimensions')
        session['Laeq16Spectra'] = request.form.get('Laeq16Spectra')
        session['Laeq8Spectra'] = request.form.get('Laeq8Spectra')
        session['LamaxvSpectra'] = request.form.get('LamaxvSpectra')
        session['LamaxoSpectra'] = request.form.get('LamaxoSpectra')

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
    #if (session['selectedcount'] > 0 ):
    #    print(f"*** Count {len(session['selectedelements'])}")  
            
    myElement = ElementSRI.query.filter(ElementSRI.UniqueID == id).first()
    print (myElement)

    elementLevels = []
    for i in range (0,len(session["facadedetails"])):
        elementLevels.append(dict(Metric=session["facadedetails"][i]["Metric"],
        Level = 0.0,
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
    
    for i in range (0,len(session["facadedetails"])):
        facade = session["facadedetails"][i]
        SingleLevel = calcnoisesingle (selectedelement, 
                            facade["Spectra"],
                            session["gsVolume"],
                            session["gsRev"])

        selectedelement["elementLevels"][i]["Level"] = SingleLevel
       

    session["selectedelements"].append(selectedelement) 
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

    return send_file (strFile, attachment_filename='Download.xlsx', as_attachment=True)
@app.route('/about/', methods=['GET'])
def about ():
    return render_template('about.html')


@app.route('/contacts/', methods=['GET'])
def contacts ():
    return render_template('contacts.html')

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
    session["facadedetails"] = []

    session["Laeq16"] = "Daytime L<sub>Aeq,16h</sub>"
    session["Laeq8"] = "Night-time L<sub>Aeq,8h</sub>"
    session["LamaxV"] = "Ventilation L<sub>AFmax</sub>"
    session["LamaxO"] = "Overheating L<sub>AFmax</sub>"  


    for i,j in zip(metList,spectraList):
        Metric = i.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'")
        Spectra = j.rstrip(" ").lstrip(" ").rstrip("'").lstrip("'")
        Label = ""

        if Metric == "Laeq16": Label="Daytime L<sub>Aeq,16h</sub>"
        elif Metric == "Laeq8": Label = "Night-time L<sub>Aeq,8h</sub>"
        elif Metric == "LamaxV": Label = "Ventilation L<sub>AFmax</sub>"
        elif Metric == "LamaxO": Label = "Overheating L<sub>AFmax</sub>"  

        facade = dict(Metric=Metric, Spectra=Spectra,Level=0.0,Label=Label)
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
            elementLevels.append(dict(Metric=session["facadedetails"][i]["Metric"],
            Level = 0.0,
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
            facade = session["facadedetails"][i]
            SingleLevel = calcnoisesingle (selectedelement, 
                                facade["Spectra"],
                                session["gsVolume"],
                                session["gsRev"])

            selectedelement["elementLevels"][i]["Level"] = SingleLevel
    
        session["selectedelements"].append(selectedelement) 
        #session['selectedcount'] = session['selectedcount'] + 1

    SetupTotals()

    session["FacadeColumn"] = IsFacadeColumnRequired()

    # Loop over elememnts and update selected levelssession
    session["status"] = "ElementDisplay"

    print ("Returning from autoimate ")

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

    for sMetric in session["facadedetails"]:
        MetricList.append(sMetric["Metric"])        
        SpectraList.append(sMetric["Spectra"])

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


    s = urlencode(parsedict)
    print (s)

    return ("/automate?" + s)
    

@app.route('/remove/<int:id>', methods=['GET', 'POST'])
def remove(id):
    print(f"*** In remove routine ")    
    #if (session['selectedcount'] > 0 ):
    #    print(f"*** Count {len(session['selectedelements'])}")    

    for selectedelement in session["selectedelements"]:
        if selectedelement["ElementID"] == id:
            session["selectedelements"].remove(selectedelement)
    #        session['selectedcount'] = session['selectedcount'] - 1

    # if we are down to 0 then knock it on the head 
    #if session['selectedcount'] == 0: 
    if len(session['selectedelements']) == 0: 
        for i in range (0,len(session["facadedetails"])):
            session["facadedetails"][i].update({"Level":0.0})
            
        # Go back to searching for elements 
        session["status"] = "SearchDisplay"
        return render_template('search.html')

    # for each metric recalc the sound level 
    for i in range (0,len(session["facadedetails"])):
        facade = session["facadedetails"][i]
        sNoise = calcnoiseall (session["selectedelements"], 
                            facade["Spectra"],
                            session["gsVolume"],
                            session["gsRev"])
        
        session["facadedetails"][i].update({"Level":sNoise})

        print (f'Total Noise level for {i} is {sNoise})')

    # The percentages have now changed so re-assign them to the array 
    SetupTotals()

    session["FacadeColumn"] = IsFacadeColumnRequired()

    session["status"] = "ElementDisplay"
    return render_template('search.html',selected=session["selectedelements"],facadedetails=session["facadedetails"],
                                    defaultquantitylist= session["defaultquantitylist"])

# Set up global variables from the user entries
def SetupSessionVariables():

    print ("def setupsessionvaribles")
    #session["gstrRoomType"] = request.form.get('roomtype')

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

    session["facadedetails"] = []
    
    mystr = request.form.get('Laeq16Spectra')
    if mystr != "":
        facade = dict(Metric="Laeq16", Spectra=mystr,Level=0.0,Label=session["Laeq16"])
        session["facadedetails"].append(facade)

    mystr = request.form.get('Laeq8Spectra')
    if mystr != "":
        facade = dict(Metric="Laeq8", Spectra=mystr,Level=0.0,Label=session["Laeq8"])
        session["facadedetails"].append(facade)

    mystr = request.form.get('LamaxvSpectra')
    if mystr != "":
        facade = dict(Metric="LamaxV", Spectra=mystr,Level=0.0,Label=session["LamaxV"])
        session["facadedetails"].append(facade)

    mystr = request.form.get('LamaxoSpectra')
    if mystr != "":
        facade = dict(Metric="LamaxO", Spectra=mystr,Level=0.0,Label=session["LamaxO"])
        session["facadedetails"].append(facade)
    
    # check format is 99.9-99.9-99.9-99.9-99.9-99.9
    for facade in session["facadedetails"]:
        for str in facade["Spectra"].split('-'):
            if(math.isnan(float(str))):
                return "Error. Invalid spectra entry. Enter format 99.9-99.9-99.9-99.9-99.9-99.9"

    if len(session["facadedetails"]) == 0:
        return "Error. there must be at last one entry for spectra."

    print("After setup")
    print(session["facadedetails"])

    #session['selectedcount'] = 0
    #if (session['selectedcount'] > 0 ):
    #    print(f"*** Count {len(session['selectedelements'])}")    
    
    #session["SelectedCount"] = 0;
    session["selectedelements"] = []

    session["gstrFilterElementType"] = "Glazing"
    # 1/4 of wall area
    session["gsFilterQuantity"] = session["gsArea"]/2/4

    session["elementtypeslist"] = ["Glazing","Wall","Door","OpenArea","Vent"]
    session["defaultquantitylist"] = [session["gsArea"]/2/4, (session["gsArea"]/2)*session["gsHeight"], 2,0,5000]

    print (session["defaultquantitylist"])

    session["gsFacadeDifference"]= 0 
    session["gstrFilterField"] = ""
    session.modified = True

    return "Success"

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

        for facadedetails in session["facadedetails"]:

            sNoise = calcnoisesingle (selectedelement, 
                                facadedetails["Spectra"],
                                session["gsVolume"],
                                session["gsRev"])
            
            #Row[facadedetails["Metric"]] = sNoise
            # todo tidy up 
            tstr = facadedetails["Metric"]

            # Show the level with the "new" nosie added
            lTotalAntiLog =  pow (10 , (facadedetails["Level"] / 10)) + pow (10 , (sNoise / 10))                
            print (f' snoise {sNoise} facadedetailsLevel {facadedetails["Level"] } ' )
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

    # We have have added, modded or turned off an element so recalculate the totals
    for i in range (0,len(session["facadedetails"])):
        sAntiLog = 0.0
        for j in range (0,len(session["selectedelements"])):
            if session["selectedelements"][j]["State"] == "Active":            
                sElementLevel = session["selectedelements"][j]["elementLevels"][i]["Level"] 
                sAntiLog = sAntiLog + pow (10, sElementLevel/10)
        session["facadedetails"][i]["Level"] = 10 * math.log(sAntiLog,10)
 
    # Called after the selected elements array has changed to update the percentages on each element.     
    # Also a good time to determine whether we have a 

    for i in range (0,len(session["facadedetails"])):
        sTotal = session["facadedetails"][i]["Level"]
        for j in range (0,len(session["selectedelements"])):
            if session["selectedelements"][j]["State"] == "Active":
                sElementLevel = session["selectedelements"][j]["elementLevels"][i]["Level"]
                session["selectedelements"][j]["elementLevels"][i]["Percent"] = round((pow (10 , (sElementLevel / 10)) / pow (10 , (sTotal / 10)))* 100,1)
            else:
                session["selectedelements"][j]["elementLevels"][i]["Percent"] = 0


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    # with app.app_context():
    #     init_db()


    app.run(debug=True)


