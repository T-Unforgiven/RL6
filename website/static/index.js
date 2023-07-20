function deleteNote(noteId){
    fetch('/delete-note', { method: 'POST', body: JSON.stringify({noteId: noteId}), }).then((_res) => {window.location.href = "/";});
}

function download(url) {
    const a = document.createElement('a')
    a.href = url
    a.download = url.split('/').pop()
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }