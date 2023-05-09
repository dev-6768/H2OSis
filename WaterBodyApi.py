from flask import Flask, render_template, request, Response, send_file, url_for, flash
import geocoder
import geopy
import WaterQualityPrediction
import WaterFinderApi
import WikipediaInformation
import localInformation
import QRCodeGenerator
from sklearn.preprocessing import StandardScaler
import routingLocation
import csvFileTester

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'af91e4a17ca844a5010a'

def quality_checking(a1,a2,a3,a4,a5,a6,a7,a8,a9):
    feature_values = [a1, a2, a3, a4, a5, a6, a7, a8, a9]
    features = ["pH", "Hardness", "Solids", "Chloramines", "Sulphates", "Conductivity", "Organic Carbon", "Trihalomethanes","Turbidity"]
    max_range = [(6.5, 8.5), (60, 120), (100, 1000), (1, 4), (0, 500), (200, 800), (0.1, 1), (0, 100), (0.2, 1)]

    i = 0
    sum = 0
    deficiency = []
    problems = []
    str_neg = "The water is not suitable as the level of"
    for att in feature_values:
        if att > max_range[i][1]:
            problems.append(i)
            str_neg += f", {features[i]}"
        elif att < max_range[i][0]:
            deficiency.append(i)
        else:
            sum += att
        i += 1

    if problems:
        str_neg += " are above normal"
        #print(str_neg)

    if deficiency:
        str_def = "The water is deficient of some basic compositions like"
        for i in deficiency:
            str_def += f", {features[i]}"
        #print(str_def)

        return [str_neg, str_def, problems, deficiency]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/locating", methods = ["GET", "POST"])
def locationApi():
    if(request.method == "POST"):
        locationCity = str(request.form.get("cityname"))
        locationCountry = str(request.form.get("countryname"))
        
        if(locationCity=="" or locationCountry==""):
            
            geocoderObject = geocoder.ip('me')
            first = str(geocoderObject.latlng[0])
            second = str(geocoderObject.latlng[1])
            
            locationObject = geopy.geocoders.Nominatim(user_agent="GetLoc")
            locationCurr = locationObject.reverse(first + ", " + second)
            locationCity = locationCurr.raw['address']['state_district']
            locationCountry = locationCurr.raw['address']['country']
        
        WaterFinderApi.finder(locationCity, locationCountry)
        
        sortedURLList = WaterFinderApi.waterStation(locationCity, locationCountry)
        
        WaterFinderApi.waterStation(locationCity, locationCountry)
        
        WaterFinderApi.drinkingWaterFinder(locationCity, locationCountry)
        
        WaterFinderApi.waterTapFinder(locationCity, locationCountry)

        listOfURL = WaterFinderApi.generalBodyFinder(locationCity, locationCountry)
        url1,url2,url3,url4 = listOfURL[0],listOfURL[1],listOfURL[2],listOfURL[3]
        
        if(url1==0):
            url1=''
        if(url2==0):
            url2=''
        if(url3==0):
            url3=''
        if(url4==0):
            url4=''

        htmlurl1 = '<p>Information about different water bodies in the region : <br><a href="' + url1 + '">Click here to view for water body 1.<br><a href="' + url2 + '">Click here to view for water body 2<br><a href="' + url3 + '">Click here to view for water body 3.<br><a href="' + url4 + '">Click here to view for water body 4.</p>'
        htmlurl2 = csvFileTester.utilityListFunction(sortedURLList)
        route_urls = [url1, url2, url3, url4]

        url_str = routingLocation.routePairFunction(locationCity, locationCountry)
        
        htmlStringlist = WikipediaInformation.wikipediaInfo(locationCity, locationCountry)
        
        #locationString = localInformation.localFinder(locationCity, locationCountry)
        
        cityString = ''#locationString[0]
        countryString = '' #locationString[1]
        
        QRCodeGenerator.qrCodeGenerate(locationCity)
        
        # return '<html><body>Data Submitted. <br><p>More information about the area you searched : <br>' + htmlString + '</p><p>To view more information about the city and country : <br>' + cityString + '<br>' + countryString + '</p><p>To View Map, <a href = "/map">Click here.</a></p><p>To check for water quality : <a href="/prediction">Check water quality.</a></p><p>To check for water stations in the region : <a href="/waterStation">Click here.</a></p><p>To get information about wastewater management stations : <a href="/drinkingWaterFinder">Click here.</a><p>To get information about water taps : <a href="/waterTapFinder">Click here.</a></p></p><p>To get a QR Code about scientific data of the water body, <a href="/index">Click here.</a>'
    
        return render_template('solutions.html',htmlString = htmlStringlist, cityString=cityString, countryString=countryString, url_str=url_str, route_urls=route_urls,  sortedURLList=sortedURLList)

    #return render_template("FrontService.html")
    return render_template("location.html")

@app.route("/map", methods=['GET', 'POST'])
def mapRender():
    return render_template("mapData.html")

@app.route("/waterStation", methods=["GET", "POST"])
def waterStations():
    return render_template("waterStations.html")

@app.route("/drinkingWaterFinder", methods=["GET", "POST"])
def drinkingWaterFinder():
    return render_template("drinkingWaterFinder.html")

@app.route("/waterTapFinder", methods=["GET", "POST"])
def waterTapFinder():
    return render_template("waterTapFinder.html")

@app.route("/generalWaterBodyFile", methods=["GET", "POST"])
def generalWaterBodyFinder():
    return render_template("generalWaterBodyFile.html")

@app.route("/donate-now")
def donate():
    return render_template("donate_now.html")

@app.route("/Soulution_text")
def textual():
    return render_template("Solution_text.html")

@app.route("/specs")
def specs():
    return render_template("specification.html")

@app.route("/filtration")
def filter():
    return render_template("filtration.html")

@app.route("/prediction", methods=['GET', 'POST'])
def predictor():
    if(request.method=="POST"):
        a1 =request.form.get("phvalue")
        a2 =request.form.get("hardness")
        a3 =request.form.get("solids")
        a4 =request.form.get("chloramines")
        a5 =request.form.get("sulphates")
        a6 =request.form.get("conductivity")
        a7 =request.form.get("organiccarbon")
        a8 =request.form.get("trihalomethanes")
        a9 =request.form.get("turbidity")

        if(a1 == '' or a2 == '' or a3 == '' or a4=='' or a5 == '' or a6 == '' or a7 == '' or a8 == '' or a9 == ''):
            return render_template("home.html")

        sc = StandardScaler()

        solutions = ["pH: Install a water filter on your tap to lower pH at the source. A water filter works by removing minerals from your water that can raise the pH, including sodium, fluoride, and potassium.", "HARDNESS: Since hard water contains huge quantity of Calcium, it is effective to use vinegar. Soap up your dishes and glassware to minimize hard water deposits. To remove soap scum, add a combination of one part of apple cider and three parts of purified water.", "SOLIDS: Distillation is simple but requires a setup. The process involves boiling water so that the vapour rises to a cool surface and condenses back to form a liquid. Using an RO Water Purifier can be the best solution to reduce drinking water TDS.", "CHLORAMINES: The reverse osmosis membrane alone technically does not remove chloramines. However, reverse osmosis systems equipped with multiple pre-filters can filter. But it has a very slow rate of production. Chloramines are best removed from water by catalytic carbon filtration.", "SULPHATES: Membrane filtration (like reverse osmosis (RO), nanofiltration (NF), and ultrafiltration (UF)), is one of the most effective technologies for removing sulfates", "CONDUCTIVITY: The conductivity of water can be reduced by removing the number of dissolved solids in the water via flocculation, reverse osmosis (RO), or distillation. Conductivity is also affected by temperature: the warmer the water, the higher the conductivity.", "ORGANIC CARBON: Reducing TOC in water requires the use of a higher UV energy level, which is created at 185nm wavelength.", "TRIHALOMETHANES: The easiest way to reduce or eliminate THMs in drinking water is to use a water pitcher with a carbon filter, install a tap-mounted carbon filter, or to use bottled water.", "TURBIDITY: Coagulation-flocculation, a treatment process where colloids in water are destabilized so they can aggregate and be physically removed, can effectively reduce turbidity when combined with sedimentation and/or filtration. Polyacrylamide (PAM) is a common type of polymeric flocculant that has been successful in reducing sediment erosion and turbidity."]

        a1 = float(a1)
        a2 = float(a2)
        a3 = float(a3)
        a4 = float(a4)
        a5 = float(a5)
        a6 = float(a6)
        a7 = float(a7)
        a8 = float(a8)
        a9 = float(a9)

        msg1 = quality_checking(a1, a2, a3, a4, a5, a6, a7, a8, a9)[0]
        msg2 = quality_checking(a1, a2, a3, a4, a5, a6, a7, a8, a9)[1]
        problems = quality_checking(a1, a2, a3, a4, a5, a6, a7, a8, a9)[2]
        deficiency = quality_checking(a1, a2, a3, a4, a5, a6, a7, a8, a9)[3]

        features = [a1, a2, a3, a4, a5, a6, a7, a8, a9]
        
        # mesg = WaterQualityPrediction.Predictor(a1, a2, a3, a4, a5, a6, a7, a8, a9)
        if problems == []:
            msg = "The water is consumable but it would be better if you perform basic filtration before consuming."
            # msg1 = "The water parameters are on par with quality standards."
        else:
            msg = "The water needs filtration. You can follow few of our filtration methods."
        if deficiency == []:
            msg2 = "The water parameters are on par with quality standards."
        
        
        # mesg =  WaterQualityPrediction.Accurator(pair)
        # return render_template("checking_parm.html", messege=mesg)
        return render_template("params.html", problems=problems, deficiency=deficiency, messege1=msg1, messege2=msg2, messege=msg, solutions=solutions)

    
    return render_template("params.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    return send_file("sourceQRCode.jpg")

if(__name__=="__main__"):
    app.run()
    