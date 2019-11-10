var express = require('express');
var app = express();
app.use(express.static('public'));

app.get('/',function (req, res) {
  res.render("index");
  console.log("Get request has been made!");
});

app.listen(process.env.PORT,process.env.IP, function() { 
  console.log('Server listening'); 
});


