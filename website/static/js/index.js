function deleteNote(noteId) {
  console.log(`function called with ${noteId}`);
  // send a request object to the server at route > '/delete-note'
  // this request has body hold the noteId to be deleted
  // stringify >> convert the js data into json string (json inside '')
  request_obj = {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  };
  fetch("/delete-note", request_obj)
    .then((response) => {
      return response.json();
    })
    .then((body) => {
      // send get request to this url
      // redirect the page to that route '/' and if there a waiting flash message, it will
      // be displayed successfully
      console.log('deletion status is ',body['status']); 
      // alert(`deletion status is  ${body.status}`);
      window.location.href = "/";
    });
}
