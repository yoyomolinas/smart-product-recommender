
document.getElementsByClassName("login100-form-btn")[0].addEventListener("click",clickButton);
function clickButton(){
    if(document.getElementsByName("username")[0].value=='mtsezgin@ku.edu.tr' && document.getElementsByName("pass")[0].value=='mts'){
    document.write('<iframe width="100%" height="100%" src="https://datastudio.google.com/embed/reporting/cc23726b-2793-4822-886f-98bb4ef5ecd5/page/C3R9" frameborder="0" style="border:0" allowfullscreen></iframe>');
    console.log("You pushed the right button")
  }else{
    alert("Unsuccessful Login");
  }
};
