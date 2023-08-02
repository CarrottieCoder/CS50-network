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
            const post_text = link.parentElement.childNodes[1]
            const text = post_text.innerHTML
            if (!localStorage.getItem(post_text.id)){
                localStorage.setItem(post_text.id, text);
            }
            console.log(post_text)

            //Check if you're canceling or editing
            if (!text.includes("<textarea")){
                // Create textarea
                const edit_Textarea = document.createElement('textarea')
                edit_Textarea.id = 'edit-textarea'
                edit_Textarea.style.width = "100%" 
                edit_Textarea.rows = 8
                edit_Textarea.innerHTML = text

                //Create submit button
                const submit_button =  document.createElement('button')
                submit_button.id = "submit-button"
                submit_button.className = "btn btn-primary"
                submit_button.innerHTML = "Save"

                //Clear div
                post_text.innerHTML = " "
                
                //Add elements to the document
                post_text.append(edit_Textarea)
                post_text.append(submit_button)

                link.textContent = "cancel"
            } else{
                post_text.innerHTML = localStorage.getItem(post_text.id);
                localStorage.removeItem(post_text.id);
                link.textContent = "edit"
            }

        };
    });
    
})

function edit_post(post){
    console.log('Should work')
}