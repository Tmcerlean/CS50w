// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // If hide button is clicked, delete the post
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

            // Append the form to the body
            document.getElementsByTagName("body")[0] 
            .appendChild(newDiv); 

            // On form submission run a function 
            newForm.onsubmit = (event) => {

                // Prevent the form from submitting
                newForm.preventDefault();

                // Save the post ID in a variable (after submission)
                postId = clickedParent.dataset.postid;

                // Save the new text in a variable (after submission)
                postContent = newTextarea.value;

                // Save the post ID and text in a JSON object (after submission)
                newData = {postID, postContent}

                // Define XML HTTP request
                var xhr = new XMLHttpRequest();

                // 
                xhr.open("POST", '/editpost', true);

                
                xhr.setRequestHeader('Content-Type', 'application/json');

                // Send POST request of JSON object (converted to string) new view (to save the post)
                xhr.send(JSON.stringify({
                    value: value
                }));
                // Replace the original text with the newly submitted text

        }
        
    })
})