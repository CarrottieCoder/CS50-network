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
    document.querySelectorAll('.edit-post').forEach((link) => {
        link.onclick = function() {
            if(!text.includes('<textarea')){
                postParent.innerHTML = " "
                
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

                //Add elements to the document
                postParent.append(edit_Textarea)
                postParent.append(submit_button)

                document.querySelector('#submit-button').onclick = edit_post(post)

                post.innerHTML = "cancel"
            }
            else {
                const edited_text = document.querySelector('#edit-textarea').value
                console.log(edited_text)
                postParent.innerHTML = edited_text
                post.innerHTML = "edit"
            }
        };
    });
    
})

function edit_post(post){
    console.log('Should work')
}