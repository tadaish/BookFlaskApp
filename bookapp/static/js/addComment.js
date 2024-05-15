function addComment(bookId) {
    fetch(`/api/books/${bookId}/comments`, {
        method: 'post',
        body: JSON.stringify({
            'content': document.getElementById('content').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
          if (data.status === 200){
              location.reload()
          }
    })
}