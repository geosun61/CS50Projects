import * as func from './func.js';

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#newpost-body').value = '';

  let form_id = '#newpost-form';
  let post_body = '#newpost-body';
  let logged_in = document.querySelector('#logged_in');
  let logged_in_username = logged_in.dataset.login;

  func.post(form_id, post_body); //function to post

  //setup for edit button
  let usernameHeaders = document.querySelectorAll(".usernames");
  let postEdit = document.querySelectorAll(".edit_link");
  let postheader = document.querySelectorAll(".post-header");

  let post_user = [];

  for (let i = 0; i < usernameHeaders.length; i++) {
    post_user.push(usernameHeaders[i].innerHTML);
    if (usernameHeaders[i].innerHTML === logged_in_username) {
      let post_id = postEdit[i].dataset.postid;
      postEdit[i].style = "display:block";
    }
  }
  console.log(post_user);

  //setup for like button
  let likeBtns = document.querySelectorAll(".like_btn");
  let spanlikes = document.querySelectorAll(".likes");
  let spanNoOfLikes = document.querySelectorAll('.likeNo');
  let post_ids = [];
  var x = 0;

  for (let i = 0; i < spanlikes.length; i++) {
    let postid = spanlikes[i].dataset.id;
    post_ids.push(postid);

    spanlikes[i].onclick = function() {
      func.like_post(postid)
        .then(result => {
          x = parseInt(result.likes);
          if (result.liked === true) {
            likeBtns[i].setAttribute("class", 'fas fa-heart like_btn');
            x++;
          }
          else{
            likeBtns[i].setAttribute("class", 'far fa-heart like_btn');
            x--;
          }
          spanNoOfLikes[i].innerHTML = x;
        });

    }
  }

  console.log(post_ids);
});
