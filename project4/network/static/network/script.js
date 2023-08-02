document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#create-post').onsubmit = () => {
        fetch('/create', {
            method: 'POST',
            body: JSON.stringify({
                body: document.querySelector("#create-body").value
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              console.log(result);
          });
    }
    document.querySelectorAll('.edit-post').forEach((post) => {
        post.onclick = function(event) {
            // Bug: Event propagating
            event.stopPropagation()
            console.log(event.target)
            // Clean the space, create textarea, save text
            text = document.querySelector('#post-text').innerHTML
            document.querySelector('#post-text').innerHTML = " "
            const edit_Textarea  = document.createElement('textarea')

            // Style the textarea
            edit_Textarea.id = 'edit-textarea'
            edit_Textarea.style.width = "100%" 
            edit_Textarea.rows = 8
            edit_Textarea.innerHTML = text

            //Create submit button
            const submit_button =  document.createElement('button')
            submit_button.id = "submit-button"
            submit_button.className = "btn btn-primary"
            submit_button.innerHTML = "Save"
            submit_button.onclick = edit_post(post)

            //Add elements to the document
            document.querySelector('#post-text').append(edit_Textarea)
            document.querySelector('#post-text').append(submit_button)

            post.style.display = 'None'
        };
    });
    
})

function edit_post(post){
    console.log("Clicked")
}