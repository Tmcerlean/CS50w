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
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // GET request
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Print emails to console
    console.log(emails);

    // Iterate through each email
    for(var i = 0; i < emails.length; i++) {
      let email = emails[i];
        
      // Create div and append email content to HTML
      var emaildiv = document.createElement('div');
      emaildiv.style.borderStyle = 'solid';
      emaildiv.style.borderColor = 'black';
      emaildiv.style.borderWidth = '0.1rem';
      emaildiv.style.borderRadius = '0';
      emaildiv.style.marginBottom = '0.2rem';
      emaildiv.style.padding = '0.3rem';
      emaildiv.innerHTML = `<b>${email.sender}</b> --- ${email.subject}<br>${email.timestamp}`;
      
      // If individual email selected then view email
      emaildiv.addEventListener('click', () => view_email(email));

      // Populate div HTML with emails
      document.querySelector('#emails-view').append(emaildiv); 
      console.log(email.read);

      // Colour backgrounds based on whether emails have been read
      if (email.read == true) {
        emaildiv.style.backgroundColor = 'lightgrey';
      }

      console.log(email);
  }   
});}


// View email
function view_email(email) {
  console.log(email.id);

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'block';

  // GET request
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {
    
    // Create div, set class, and append email content to HTML
    var reademail = document.createElement('div');
    reademail.style.borderStyle = 'solid';
    reademail.style.borderColor = 'black';
    reademail.style.borderWidth = '0.1rem';
    reademail.style.borderRadius = '0';
    reademail.style.marginBottom = '0.2rem';
    reademail.style.padding = '0.3rem';
    reademail.innerHTML = `
    <b>From:</b> ${email.sender}<br>
    <b>To:</b> ${email.recipients}<br>
    <b>Subject:</b> ${email.subject}<br>
    <b>Timestamp:</b> ${email.timestamp}<br>
    <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button> <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
    <hr>
    ${email.body}`;

    // Populate div HTML with emails
    document.querySelector('#single-view').append(reademail); 
    
    // Mark unread emails as read
    if (email.read === false) {
      read(email);
    }      

    // Listen for Reply button press
    document.querySelector('#reply').addEventListener('click', () => reply(email));

    // Listen for Archive button press
    document.querySelector('#archive').addEventListener('click', () => archive(email));
});
}


// Read
function read(email) {
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}


// Reply
function reply(email) {

    // Do something
    compose_email();
    document.querySelector("#compose-recipients").value = email.sender;
    document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
    document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"`;
}


// Archive
function archive(email) {

    // Check if in archive
    if (email.archived == false) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
    }
    else {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
    }
}


// Send email
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#sendmail').addEventListener('click', function() {
    // Send a POST request with the email content
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
  })});
