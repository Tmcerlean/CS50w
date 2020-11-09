// Edit post 
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Add event listener to the page
    document.addEventListener('click', event => {

        // Find what was clicked on
        const clickedElement = event.target;

        // Set variable for parent element (div) clicked on
        const clickedParent = event.target.parentElement;

        // Check if the user clicked on a hide button
        if (clickedElement.className === 'btn btn-primary edit-button') {
            
            // Hide the existing parent element
            clickedParent.style.display = "none";

            // Create a new div
            var newDiv = document.createElement('div');
            newDiv.className = "container media mt-3 border postbody";

            // Render a new form and append to div
            const newForm = newDiv.appendChild(document.createElement("form"));
        
            // Create a new textarea element
            var newTextarea = document.createElement("textarea");

            // Populate textarea with original text
            originalText = clickedParent.querySelector(".posttext").innerText;
            newTextarea.value = originalText;

            // Create a new submit button element
            var submitButton = document.createElement("input");
            submitButton.setAttribute("type", "submit");
            submitButton.setAttribute("value", "Submit");

            // Append the textarea to the form
            newForm.appendChild(newTextarea);

            // Append the submit button to the form
            newForm.appendChild(submitButton);

            // Append the div to the body
            document.getElementsByTagName("body")[0] 
            .appendChild(newDiv); 

            // On form submission run a function 
            newForm.onsubmit = (event) => {

                // Prevent the form from submitting
                event.preventDefault();

                // Save the post ID in a variable (after submission)
                postId = clickedParent.dataset.postid;

                // Save the new text in a variable (after submission)
                postContent = newTextarea.value;

                // Save the post ID and text in a JSON object (after submission)
                const data = {postId, postContent};
            
                // Use fetch() to POST JSON-encoded data (converted to string) to new view (save post)
                fetch('/editpost', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                mode: 'same-origin',
                body: JSON.stringify(data),
                })

                // Unhide the original parent element
                clickedParent.style.display = "";

                // Populate the original 
                clickedParent.querySelector(".posttext").innerText = newTextarea.value;

                // Remove the newly created div
                newDiv.remove();
        }
        
    }
})})


// Acquire the CSRF token cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// Like/unlike post 
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Add event listener to the page
    document.addEventListener('click', event => {

        // Find what was clicked on
        const clickedElement = event.target;

        // Find who clicked on the link

        // Find which post they liked

        // POST request to add to server

        // Response returns count of likes - display this updated value in HTML