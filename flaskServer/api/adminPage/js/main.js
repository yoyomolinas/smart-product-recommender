
document.getElementsByClassName("login100-form-btn")[0].addEventListener("click",clickButton);
function clickButton(){
  if(document.getElementsByName("username")[0].value=='emre' && document.getElementsByName("pass")[0].value=='emre'){
    document.write('<html><body style="margin:0px;padding:0px;overflow:hidden" ><embed src="Deep_Fashion_Results.pdf" width="100%" height="100%" /></body></html>');
    console.log("You pushed the right button")
  }else{
    alert("Unsuccessful Login");
  }

};

//<iframe src="'+link+'"  frameborder="0" style="overflow:hidden;height:100%;width:100%" height="100%" width="100%"></iframe>
