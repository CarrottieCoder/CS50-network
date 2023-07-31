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
})