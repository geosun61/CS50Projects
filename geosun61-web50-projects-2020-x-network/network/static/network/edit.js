import * as func from './func.js';

document.addEventListener('DOMContentLoaded', function() {
  //document // TODO: follow buttons
  let form_id = '#edit-form';
  let editTextArea = '#edit-ta';
  let editbtnid = "#edit-btn"

  let editdiv = document.querySelector("#edit-div");
  let editbtn = document.querySelector(editbtnid);
  let editid = editdiv.dataset.postid;
  let editform = document.querySelector(form_id);

  editform.onsubmit = function() {
    let edittext = document.querySelector(editTextArea).value;
    func.edit(editid, edittext);
    return false;
  }
});
