
function ValRoomDimensions(val)
{
  var rD  = [ ];
  var sHeight = 0.0;
  var sArea  = 0.0;
  var sVol = 0.0; 

  rD = val.split("x");
  if (rD.length == 1) 
  // One element in var - assume 
  {
    sHeight = 2.3;
    sArea = val/2.3
    sVol = val;
  }
  else if (rD.length == 2) {
    sArea = rD[0];
    sHeight = rD[1];
    sVol = sArea * sHeight
  }
  else if (rD.length == 3) {
    sArea = rD[0]*rD[1]
    sHeight = rD[2]
    sVol = sArea * sHeight
  }
  else
  {
      alert ("Incorrect input" + rD.length)
      return
  }
  //test for NAN 
  if (parseFloat(sArea) != parseFloat(sArea)){
      alert ("Incorrect input area")
      return
  }
  //test for NAN 
  if (parseFloat(sHeight) != parseFloat(sHeight)){
      alert ("Incorrect input height")
      return
  }

  sArea = (parseFloat(sArea)).toFixed(1)
  sHeight = (parseFloat(sHeight)).toFixed(1)
  sVol = (parseFloat(sVol)).toFixed(1)
  document.getElementsByName('RoomDimensions')[0].value = sArea + "x"  + sHeight
  $("#RoomDimensionsLabel").text(sVol + " m3");
  $(document).ready()
  {
    var val1 = 1
    var val2 = 2
    $.ajax({
      url: "./set_option",
      type: "POST",
      data: {arg1:val1, arg2:val2}
    });
  };
  /*document.getElementById('RoomDimensionsLabel').value = "   " + sVol + " m3"*/
}

function ValSpectra(val, call)
{
  //console.log (" ValSpectra " + val + " - " + call)
  // Try splitting by tab,comma,dash and slash.
  var spectra = [ ];
  var strSpectra = ""
  var iCount=-1;
  // Assume specta had been entered 99.99/99.99/99.99/99.99/99.99 = Find out 
  if (val.indexOf("/") > -1) {
    spectra = val.split("/");
  }        
  else if (val.indexOf("-") > -1) {
    spectra = val.split("-");  
  }
  else if (val.indexOf(",") > -1) {
    spectra = val.split(","); 
  }
  else if (val.indexOf("\t") > -1) {
    spectra = val.split("\t");    
  }
  // If 5 elements in array assume that a spectra has been entered
  //alert("Spectra" + spectra  +  " - " + "Length " + spectra.length)

  var Overall = ""
  if (spectra.length == 5){
    //alert("Before calc")
    Overall = CalcSpectra(spectra);
    //alert("after  calc" + Overall)
    strSpectra = parseFloat(spectra[0]).toFixed(1) + "-" +parseFloat(spectra[1]).toFixed(1)  + "-" +parseFloat(spectra[2]).toFixed(1)  + "-" + parseFloat(spectra[3]).toFixed(1)  + "-" +parseFloat(spectra[4]).toFixed(1) 
    //alert("strSpectra   " + Overall)
  }
  // else assume user has entered value - set up defailt spectra 
  else  if (typeof(val) == Number || !isNaN(parseFloat(val))) {
    spectra[0] = val - 10
    spectra[1] = val - 10
    spectra[2] = val - 4
    spectra[3] = val - 6
    spectra[4] = val - 11
    Overall = parseFloat(val).toFixed(1);
    strSpectra = spectra[0].toFixed(1) + "-" +spectra[1].toFixed(1)  + "-" +spectra[2].toFixed(1)  + "-" + spectra[3].toFixed(1)  + "-" +spectra[4].toFixed(1) 
  }
  if (Overall >0)
  {
    if (call==1){
      document.getElementsByName('Laeq16Spectra')[0].value =  strSpectra   + " (" + Overall + ")"
      /*document.getElementByID('Laeq16SpectraLabel').innerText = Overall + " dB(A)"
      $("#Laeq16SpectraLabel").text(Overall);*/
    }
    else if (call == 2){
      document.getElementsByName('Laeq8Spectra')[0].value = strSpectra + " (" + Overall + ")"
    /* document.getElementByID('Laeq8SpectraLabel').value = Overall + " dB(A)"
      $("#Laeq8SpectraLabel").text(Overall );*/
    }
    else if (call == 3){
      document.getElementsByName('LamaxvSpectra')[0].value = strSpectra + " (" + Overall + ")"
      /*document.getElementById('LamaxvSpectraLabel').value = Overall + " dB(A)"
      $("#LamaxvSpectraLabel").text(Overall);*/
    }      
    else if (call == 4){
      document.getElementsByName('LamaxoSpectra')[0].value = strSpectra + " (" + Overall + ")"
      /*document.getElementById('LamaxoSpectraLabel').value = Overall + " dB(A)"
      $("#LamaxoSpectraLabel").text(Overall );*/
    }
  }
  else
  {
    alert ("got here")
    if (call==1){
      document.getElementsByName('Laeq16Spectra')[0].value = ""
    }
    else if (call == 2){
      document.getElementsByName('Laeq8Spectra')[0].value = ""
    }
    else if (call == 3){
      document.getElementsByName('LamaxvSpectra')[0].value = ""
    }      
    else if (call == 4){
      document.getElementsByName('LamaxoSpectra')[0].value = "" 
    }
   }
}
function Copy_Text()
{
  var copyText = document.getElementById("ShareString");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard
    .writeText(copyText.value)
    .then(() => {
      alert("successfully copied");
    })
    .catch(() => {
      alert("something went wrong");
    });;
}
function CalcSpectra(spectra)
{
  //alert("CalcSpectra")

  var sTot=0.0;
  var sTot1=0.0;
  var fVal = 0.0; 
  var iLoop;
  for (iLoop=0; iLoop<=4; iLoop++)
  {
    //sTot=sTot+ (10 * Math.log10(parseFloat(spectra[i])));
    fVal = parseFloat(spectra[iLoop])
    sTot=sTot+ Math.pow(10,  (fVal/10));
  }
  sTot1 = 10* Math.log10(sTot);
  //alert ("sTot1 "+ sTot1)
  return sTot1.toFixed(1);
}

function FilterConfig(val)
{
   
    switch(val)
    {
        case "Glazing":
          document.getElementById('QuantityLabel').innerHTML = " Quantity"
          document.getElementById('QuantityMetric').innerHTML = "   "          
          document.getElementById('Quantity').disabled = false 
          document.getElementsByName('Quantity')[0].value = document.getElementById("dql").dataset.def0
          document.getElementById('qRow').style.visibility = "visible"          
          break;          

        case "Wall":
          document.getElementById('QuantityLabel').innerHTML  = " Quantity"   
          document.getElementById('QuantityMetric').innerHTML = "   "          
          document.getElementById('Quantity').disabled = false 
          document.getElementsByName('Quantity')[0].value = document.getElementById("dql").dataset.def1
          document.getElementById('qRow').style.visibility = "visible"          
          break;          

        case "Door":
          document.getElementById('QuantityLabel').innerHTML = " Area"
          document.getElementById('QuantityMetric').innerHTML = " m2"
          document.getElementById('Quantity').disabled = false 
          document.getElementsByName('Quantity')[0].value = document.getElementById("dql").dataset.def2
          document.getElementById('qRow').style.visibility = "visible"          
          break;

        case "OpenArea":
            document.getElementById('QuantityLabel').innerHTML = "                "
            document.getElementById('QuantityMetric').innerHTML = "   "            
            document.getElementById('Quantity').disabled = true
            document.getElementsByName('Quantity')[0].value = document.getElementById("dql").dataset.def3
            document.getElementById('qRow').style.visibility = "hidden"
            break;

        case "Vent":
            document.getElementById('QuantityLabel').innerHTML = " Minimum Equivalent Area"
            document.getElementById('QuantityMetric').innerHTML = "  mm2 "            
            document.getElementById('Quantity').disabled = false
            document.getElementsByName('Quantity')[0].value = document.getElementById("dql").dataset.def4
            document.getElementById('qRow').style.visibility = "visible"          
            break;
    }
}

