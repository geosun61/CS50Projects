import * as func from './functions.js';

document.addEventListener('DOMContentLoaded', function() {
  var olddatebtn = document.getElementById('old-datebtn');
  var latestdatebtn = document.getElementById('latest-datebtn');
  var datecreatedbtn = document.getElementById('date-createdbtn');
  var daysTable = document.getElementById('days-table');


  var orderby_value = "date";
  var days = [];
  var res = [];
  func.orderSet(orderby_value);

  olddatebtn.onclick = function() {
    orderby_value = olddatebtn.value;
    func.orderSet(orderby_value);
  };

  latestdatebtn.onclick = function() {
    orderby_value = latestdatebtn.value;
    func.orderSet(orderby_value);
  };

  datecreatedbtn.onclick = function() {
    orderby_value = datecreatedbtn.value;
    func.orderSet(orderby_value);
  };

  
});
