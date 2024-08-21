document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector("#followButton");
    if(followButton){
        followButton.addEventListener('click', () => followUnfollow());
    }

    const like = document.querySelectorAll("#like");
    like.forEach(button => {
        button.addEventListener('click', () => likeUnlike(button))
    })
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
    
function likeUnlike(button){
    const postId = button.dataset.postId;

    const likes = document.querySelector(".count")
    counter = Number(likes.innerText)

    const isLiked = button.classList.contains('liked');
    console.log(isLiked)

    fetch(`/like/${postId}`, {
        method: "PUT",
        body: JSON.stringify({ action: !isLiked })
    })
    .then(data => {
        if(!isLiked){
            counter++;
            button.classList.add('liked');
            likes.innerText = counter;
        }
        else{
            counter--;
            button.classList.remove('liked')
            likes.innerText = counter;
        }
    })
}