// Login pop-up functions
function openForm() {
    document.getElementById("myFormDiv").style.display = "block";
    document.getElementById("myForm").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("myFormDiv").style.display = "none";
    document.getElementById("myForm").style.display = "none";
  }

// Login pop-up event listener
// Add event listener to the page
document.addEventListener('click', event => {

    // Find what was clicked on
    const clickedElement = event.target;

    // Check if the user clicked on a hide button
    if (clickedElement.className === 'form-control ui-autocomplete-input') {
        
        console.log("working");
        openForm();
    }
})

// Register page form validation
function formValidation() {
    var uemail = document.registration.email;
    var upassword = document.registration.password;
    if (emailValidation(uemail)) {
        if (passwordValidation(upassword)) {
            return true;
        }
    return false;
    }
}

function emailValidation(uemail) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (uemail.value.match(mailformat)) {
        return true;
    }
    else {
        alert("You have entered an invalid email address!");
        uemail.focus();
        return false;
    }
}

function passwordValidation(upassword) {
    var password = upassword.value;
    if (password.length == 0) {
        alert("Password field cannot be empty")
        upassword.focus();
        return false;
    }
    console.log("password not empty");
    if (password.length < 8) {
        alert("Password should contain at least 8 characters")
        upassword.focus();
        return false;
    }
    else if(password.length > 30) {
        alert("Password should be less than 30 characters")
        upassword.focus();
        return false;
    }
    else if (password.search(/\d/) == -1) {
        alert("Password should contain at least 1 number")
        upassword.focus();
        return false;
    }
    else if (password.search(/[a-zA-Z]/) == -1) {
        alert("Password should contain at least 1 letter")
        upassword.focus();
        return false;
    }
    return true;
}

// Autofill dates
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Find required dates
    const today = new Date()
    const tomorrow = new Date(today)
    const weekTomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    weekTomorrow.setDate(weekTomorrow.getDate() + 8)
    let tomorrowsFormattedDate = tomorrow.getFullYear() + "-" + (tomorrow.getMonth() + 1) + "-" + tomorrow.getDate()
    let weekTomorrowsFormattedDate = weekTomorrow.getFullYear() + "-" + (weekTomorrow.getMonth() + 1) + "-" + weekTomorrow.getDate()


    // Populate the form's date fields with these variables
    document.querySelector("#idDeparturedate").value = tomorrowsFormattedDate;
    document.querySelector("#idReturndate").value = weekTomorrowsFormattedDate;
})

// Radio button toggle
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    // Select both radio buttons
    if (document.querySelector('input[name="optradio"]')) {
        // Iterate through each of the buttons
        document.querySelectorAll('input[name="optradio"]').forEach((elem) => {
            // Add an event listener for when the button's value is changed (true/false)
            elem.addEventListener("change", function(event) {
            var item = event.target.value;
            if (item == "true") {
                document.querySelector("#idReturndate").value = '';
                document.querySelector("#idReturndate").disabled = true;
                console.log("Disabled");
            }
            else {
                document.querySelector("#idReturndate").disabled = false;
                console.log("Enabled")
            }
            console.log(item);
        });
        });
    }
})

// Disabled return date - toggle radio
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Add an event listener for a click on the return date element
    document.querySelector("#returnDateDiv").addEventListener("click", function(event) {
        console.log("Clicked")
        // Check if return date element is disabled
        if (document.querySelector("#idReturndate").disabled == true) {
            document.querySelector("#idReturndate").disabled = false;
            document.querySelector("#returnOption").checked = true;
        }
        else {
            console.log("It's false")
        }
    })
})

// Radio toggle - disable return date
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    // Select both radio buttons
    if (document.querySelector('input[name="optradio"]')) {
        // Iterate through each of the buttons
        document.querySelectorAll('input[name="optradio"]').forEach((elem) => {
            // Add an event listener for when the button's value is changed (true/false)
            elem.addEventListener("change", function(event) {
            var item = event.target.value;
            if (item == "true") {
                document.querySelector("#idReturndate").value = '';
                document.querySelector("#idReturndate").disabled = true;
                console.log("Disabled");
            }
            else {
                document.querySelector("#idReturndate").disabled = false;
                console.log("Enabled")
            }
            console.log(item);
        });
        });
    }
})