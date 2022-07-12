console.log('Hey Dad! 👋');


function deleteAllUsers(){
    fetch('/deleteAllUsers')
        .then(location.reload)
        .catch(err => localStorage.setItem('last_error', err))
}