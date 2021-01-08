document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = function() {
    let recp = document.querySelector('#compose-recipients').value;
    let subj = document.querySelector('#compose-subject').value;
    let bd = document.querySelector('#compose-body').value;

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
          recipients: recp,
          subject: subj,
          body: bd,
          read: false
        })
      })
      .then(response => {
        if (response.status === 201) { //email sent successfully load sent email box
          load_mailbox('sent');
        }
      })
      .then(result => {
        console.log(result);
      });
    return false; // to stop reloading of inbox DOMContentLoaded after form submission
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(mailbox);
      console.log(emails);
      // hide archive button if sent email else show button
      if (mailbox === 'sent') {
        document.getElementById('archivebtn').style.display = 'none';
      } else {
        document.getElementById('archivebtn').style.display = '';
      }
      Array.from(emails).forEach(emailsDiv)
    });
}

function emailsDiv(element) {
  let divEmails = document.createElement("div");
  divEmails.className = 'email'; //set class name for html
  divEmails.id = `email${element.id}`; //set email id
  divEmails.innerHTML = ''; //clear innerHTML
  divEmails.innerHTML += `<table><b>${element.sender}</b> ${element.subject} <div style="float:right">${element.timestamp}</div></table>`; //set innerHTML

  //on click event
  divEmails.addEventListener('click', function() {
    // Show the email view and hide other views
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';

    //clear innerHTML
    document.querySelector('#mail-sender').innerHTML = element.sender;
    document.querySelector('#mail-recp').innerHTML = element.recipients;
    document.querySelector('#mail-subj').innerHTML = element.subject;
    document.querySelector('#mail-time').innerHTML = element.timestamp;
    document.querySelector('#mail-body').innerHTML = element.body;

    fetch(`/emails/${element.id}`)
      .then(response => response.json())
      //load email-view
      .then(email => {
        // Print email
        console.log(email);

        //add on click event for reply
        document.getElementById('replybtn').onclick = () => {
          reply(element.id)
        };

        //add on click event for archive

        if (email.archived === false) {
          document.querySelector('#archivebtn').innerHTML = "Archive";
          document.getElementById('archivebtn').onclick = () => {
            archive(email.id)
          };

        } else {
          document.querySelector('#archivebtn').innerHTML = "Unarchive";
          document.getElementById('archivebtn').onclick = () => {
            unarchive(email.id)
          };

        }
      });

    //update read value when clicked on email
    fetch(`/emails/${element.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });

  });

  //append the emails div to emails-view div
  document.querySelector('#emails-view').appendChild(divEmails);

  //add gray background if email is read
  if (element.read === true) {
    document.querySelector(`#email${element.id}`).style.backgroundColor = "gray";
  }

}

function reply(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email);

      // Show compose view and hide other views
      document.querySelector('#email-view').style.display = 'none';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';

      // Clear out composition fields
      document.querySelector('#compose-recipients').value = '';
      document.querySelector('#compose-subject').value = '';
      document.querySelector('#compose-body').value = '';

      // input reply values to composition fields
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      document.querySelector('textarea').value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n ${email.body}`;

      //check whether subject includes Re:
      if (email.subject.includes("Re:") === false) {
        document.querySelector('#compose-subject').value = `Re:  ${email.subject}`;
      } else {
        document.querySelector('#compose-subject').value = `${email.subject}`;
      }

      document.querySelector('#compose-form').onsubmit = function() {

        let recp = document.querySelector('#compose-recipients').value;
        let subj = document.querySelector('#compose-subject').value;
        let bd = document.querySelector('#compose-body').value;

        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
              recipients: recp,
              subject: subj,
              body: bd,
              read: false
            })
          })
          .then(response => {
            if (response.status === 201) { //email sent successfully load sent email box
              load_mailbox('sent');
            }
          })
          .then(result => {
            console.log(result);
          });
        return false; // to stop reloading of inbox DOMContentLoaded after form submission
      }
    });
}

function archive(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  }).then(() => load_mailbox('inbox'));
  return false;
}

function unarchive(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  }).then(() => load_mailbox('inbox'));
  return false;
}
