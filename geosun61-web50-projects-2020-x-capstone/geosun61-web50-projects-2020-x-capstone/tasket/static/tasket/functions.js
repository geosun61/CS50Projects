function get_crsf_token() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

async function get_day_obj(day_id) {
  var dayarr;
  const days = await fetch(`/day/${day_id}`)
    .then(response =>
      response.json()
    ).then(data => dayarr = data)
    .then(() => {
      console.log(dayarr);
    }).catch(error => {
      console.log(error);
    });

  return dayarr;
}

//editing
async function get_task_obj(task_text) {
  var taskarr;
  var task = await fetch(`/task/${task_text}`)
    .then(response =>
      response.json()
    ).then(data => taskarr = data)
    .then(() => {
      console.log(taskarr);
    }).catch(error => {
      console.log(error)
    });

  return taskarr;
}

//export functions for js
//FUNCTIONS FOR ADDTASK HTML AND JS
export function add_task_input(parentid) {
  var parent = document.getElementById(parentid);
  var input = document.createElement("input");
  input.type = 'text';
  input.className = 'form-control tasks';
  input.setAttribute('placeholder', 'Enter the task')
  parent.appendChild(input);
}

export function submit_tasks(task_class, date_id) {
  var valueArr = [];
  var tasks = document.querySelectorAll(task_class);
  var date = document.querySelector(date_id);
  var x;

  valueArr.push(date.value);

  tasks.forEach((el) => {
    x = el.value;

    valueArr.push(x.trim()); //remove whitespace
  });
  console.log(valueArr);
  return valueArr;
}

export async function createTasks(arr) {
  var task = [];

  for (var i = 1; i < arr.length; i++) {
    task.push(arr[i]);
  }
  console.log(task);
  var add = fetch('/add', {
    method: 'POST',
    body: JSON.stringify({
      date: arr[0],
      tasks: task
    }),
    headers: {
      "X-CSRFToken": get_crsf_token(),
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
  });

  return add;
}

async function deleteDay(day_id) {
  fetch(`/delete/${day_id}`, {
    method: 'PUT'
  }).catch(error => {
    console.log(error);
  });

}
//FUNCTIONS FOR INDEX HTML AND JS
//function to combine setTable and orderBy
export async function orderSet(orderby_value) {
  var days = [];
  var res = [];

  res = orderBy(orderby_value);

  console.log(res); //get response and then return
  res.then(result => {
    days = result;
    console.log(days);
  });

  //create orderby and set table
  setTimeout(function() {
    setTable(days);
  }, 100);

  //complete task function
  setTimeout(function() {
    var daysListItems = document.querySelectorAll('.days-tasks-items');

    var taskobj = [];
    var dayobj = [];
    var data1 = [];
    var data2 = [];



    //setting a foreach for the items of the class
    daysListItems.forEach((item) => {
      //setting a onclick event for each list item task
      item.addEventListener('click', event => {
        data1 = get_task_obj(item.dataset.task); //get task object
        data2 = get_day_obj(item.dataset.dayId); //get day object related to task

        console.log("Day Task Clicked/........");
        data1.then(result => {
          taskobj = result;
          console.log(taskobj);
        });

        data2.then(result => {
          dayobj = result;
          console.log(dayobj);
        });

        console.log(item.dataset.task);
        console.log(item.dataset.dayId);
        console.log(dayobj);
        console.log(taskobj);

        if (item.getAttribute('checked') === "true") {
          item.setAttribute('checked', false);
          item.className = 'days-tasks-items';

          setTimeout(function() {
            console.log(dayobj);
            console.log(taskobj);
            completedTask(dayobj.day.id, taskobj.task.id);
          }, 100);

        } else {
          item.setAttribute('checked', true);
          item.className = 'days-tasks-items checkedListItem';

          setTimeout(function() {
            console.log(dayobj);
            console.log(taskobj);
            completedTask(dayobj.day.id, taskobj.task.id);
          }, 100);
        }
      });
    });

  }, 200);

  setTimeout(function() {
    var deleteBtn = document.querySelectorAll('.dltDayBtn');
    deleteBtn.forEach(item => {
      item.addEventListener('click', function() {
        var dayIdval = item.getAttribute("data-day-id");
        var r;
        var dayreq = get_day_obj(dayIdval);
        var dayObj;

        r = confirm(`Are you sure you want to delete day ${dayIdval}?`);
        if (r == true) {
          console.log(`You clicked OK ${dayIdval}!`);
          dayreq.then(response => {
            dayObj = response;
            console.log(dayObj.day.id);
            deleteDay(dayObj.day.id);
          });

          window.location.href = "/";

        } else {
          console.log(`You clicked Cancel ${dayIdval}!`);
        }
      });
    });
  }, 300);
}

//get order of days
async function orderBy(orderbyQuery) {
  var daysarr;

  const days = await fetch(`/orderby/${orderbyQuery}`)
    .then(response =>
      response.json()
    ).then(data => daysarr = data)
    .then(() => {
      console.log(daysarr);
    }).catch(error => console.log(error));

  return daysarr;
}

//organizing table
function setTable(days_obj) {
  var daysTable = document.getElementById('days-table');
  var taskList;

  //clear element
  daysTable.innerHTML = '';

  //creating table body
  var tr = '';
  var n = 0;

  //for loop for each day
  for (var i = 0; i < days_obj.days.length; i++) {
    n = i + 1;
    tr += `<tr><th data-day-id="${days_obj.days[i].id}">` + n + '</th>' //col #1 id set
      +
      `<td data-date="${days_obj.days[i].date}">` + days_obj.days[i].date + "</td>" //col #2 days
      +
      `<td> <ul id="days-tasks-ul-${n}" >`; //col #3 tasks


    tr += `<div id="tasks-uncompleted-${n}">`;//div for uncompleted tasks
    for (var j = 0; j < days_obj.days[i].tasks.length; j++) {
      if (!days_obj.days[i].completed_tasks.includes(days_obj.days[i].tasks[j])) {
        tr += `<li class="days-tasks-items" data-day-id="${days_obj.days[i].id}" data-task="${days_obj.days[i].tasks[j]}" checked="false">` + days_obj.days[i].tasks[j] + "</li>"; //col #3 tasks list
      } else {
        continue;
      }
    }
    tr += '</div>';//end of div for uncompleted tasks

    tr += `<div id="tasks-completed-${n}">`;//div for completed tasks
    if (days_obj.days[i].completed_tasks && days_obj.days[i].completed_tasks.length) {
      tr += '<div class="compTitle"><b>Completed Tasks</b></div>'
      for (var k = 0; k < days_obj.days[i].completed_tasks.length; k++) {
        tr += `<li class="days-tasks-items checkedListItem" data-day-id="${days_obj.days[i].id}" data-task="${days_obj.days[i].completed_tasks[k]}" checked="true">` +
          days_obj.days[i].completed_tasks[k] + "</li>"; //col #3 tasks list
      }
    }
    tr += '</div>';//end of div for uncompleted tasks

    tr += '</ul></td>'; //end of col #3 tasks
    tr += '<td>' + days_obj.days[i].datetime_created + '</td>'; //col #4 date created
    tr += `<td><button type="button" class="btn btn-danger dltDayBtn" data-day-id="${days_obj.days[i].id}">X</button></td></tr>`; //col #5 delete day button
  }
  //add table header and then table body
  daysTable.innerHTML += '<tr><th scope="col">#</th><th scope="col">Day</th><th scope="col">Tasks</th><th scope="col">Date Created</th> <th scope="col">Delete Day?</th></tr>' + tr;
};

async function completedTask(day_id, task_id) {
  var res = await fetch(`/completetask/${day_id}/${task_id}`, {
      method: 'PUT',
      headers: {
        "X-CSRFToken": get_crsf_token(),
        "Accept": "application/json",
        "Content-Type": "application/json"
      }
    })
    .catch(error => {
      console.log(error);
    });

  return res;
}
