document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector("#followButton");
    console.log(followButton.innerText)
    if(followButton){
        followButton.addEventListener('click', () => followUnfollow());
    }
})

function followUnfollow(){
    const userId = Number(window.location.pathname.split('/').filter(Boolean).pop());
    console.log(userId)

    fetch(`/follow_unfollow/${userId}`,{
        method:"POST",
        body: JSON.stringify({

        })
    })
    .then(response => response.json())
    .then(result => {

    });
}