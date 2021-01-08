import * as func from './functions.js';
var msg1 = false;
var msg2 = false;

document.addEventListener('DOMContentLoaded', function() {
  var addTaskBtn = document.getElementById('addtask_btn');
  var tasks_submit = document.getElementById('submit_tasks_btn');
  var msgDiv1 = document.getElementById('message1');
  var msgDiv2 = document.getElementById('msgExists');

  msgDiv1.style.display = 'none';
  msgDiv2.style.display = 'none';

  addTaskBtn.addEventListener('click', () => {
    func.add_task_input('newtasksdiv');
  });
  var arr = [];
  tasks_submit.addEventListener('click', () => {
    arr = func.submit_tasks('.tasks', '#date_field');
    console.log(arr);

    //error checks for date and at least one task has to be entered to be submitted
    if (arr[0] === '' || arr[1] === '') {
      for (var i = 0; i < arr.length; i++) {
        console.log(i);
        if (arr[i] === "") {
          var divCon = document.querySelector('.container');
          var errElement = document.createElement("div");
          if (i === 0) {//show error for user to enter date
            errElement.id = 'alertEnterDate1';
            errElement.className = 'alert alert-primary alert-dismissable fade show';
            errElement.innerHTML = '<button class="close" type="button" data-dismiss="alert"><span aria-hidden="true">&times;</span></button><p>Enter Date alert</p>';
            errElement.setAttribute('role', 'alert');

            divCon.appendChild(errElement);
          } else {//show error for user to enter at least one task
            errElement.id = `alertEnterTask${i}`;
            errElement.className = 'alert alert-secondary alert-dismissable fade show';
            errElement.innerHTML = `<button class="close" type="button" data-dismiss="alert"><span aria-hidden="true">&times;</span></button><p>Enter at least one task</p>`;
            errElement.setAttribute('role', 'alert');

            divCon.appendChild(errElement);
          }
        }
      }

    } else {
      var create = func.createTasks(arr);
      var res;
      create.then(result =>{
        res = result;
        console.log(res);
        if (res.status == 400) {
          var dateF = document.getElementById('date_field');
          msgDiv2.innerHTML = "There is already an entry for  "+ dateF.value + ". You will have to delete the original entry first then submit again.";
          msgDiv2.style.display = "block";
        }else {
            msg2 = true;
            if (msg2 == true) {
              var msgDiv = document.getElementById('message1');
              msgDiv.style.display = 'block';

              setTimeout(function() {
                window.location.href = '/';
              }, 5000);
            }
            msg2 = false;
        }
      });
    }
  });
});
