//all export functions for network
function get_crsf_token() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
//post form
export function post(form_id, post_body) {
  window.onload = function() {
    document.querySelector(form_id).onsubmit = function() {
      let bd = document.querySelector(post_body).value;

      fetch('/post', {
        method: 'POST',
        body: JSON.stringify({
          body: bd,
          likes: 0
        })
      }).then(response => {
        console.log(response.json());
      });
    }
  }
}

//follow user
export async function follow(username) {
 const follow = await fetch(`/follow/${username}`, {
    method: 'PUT'
  }).then(response => {
    setTimeout(100);
    if (response.status === 201) {
      return response.json();
    }
    console.log(response.json());

  }).catch(error => {
    console.error(error);
  });

  return follow;
}

//edit form
export function edit(post_id, post_body) {
  fetch(`/post/edit/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      id: post_id,
      body: post_body
    }),
    headers: {
      "X-CSRFToken": get_crsf_token(),
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
  }).then(response => {
      console.log(response.json());
      window.location.href="/";
  });
}

export async function like_post(post_id){
  const like= await fetch(`/post/like/${post_id}`, {
    method: 'PUT'
  }).then(response => {
    setTimeout(100);
    if (response.status === 201) {
      return response.json();
    }
  }).catch(error => {
    console.error(error);
  });

  return like;
}

export function get_user_data(username) {
  const user_data = [];
  fetch(`/user/${username}`)
    .then(response => {
      setTimeout(100);
      console.log(response.json());
      user_data = response.json();
      console.log(user_data);
    }).catch(error => {
      console.error(error);
    });
  return user_data;
}
