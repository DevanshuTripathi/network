document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector("#followButton");
    if(followButton){
        followButton.addEventListener('click', () => followUnfollow());
    }
})

function followUnfollow(){
    const userId = Number(window.location.pathname.split('/').filter(Boolean).pop());

    const text = document.querySelector("#followButton");
    const followStatus = text.innerText === 'Follow';

    fetch(`/follow_unfollow/${userId}`, {
        method: "PUT",
        body: JSON.stringify({ follow: !followStatus })
    })
    .then(data => {
        if (followStatus) {
            text.innerText = 'Unfollow';
        } else {
            text.innerText = 'Follow';
        }
    })
}
    
