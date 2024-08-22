document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector("#followButton");
    if(followButton){
        followButton.addEventListener('click', () => followUnfollow());
    }

    const likeButton = document.querySelectorAll(".like-button");
    likeButton.forEach(button => {
        button.addEventListener('click', () => likeUnlike(button))
    })

    const editButton = document.querySelectorAll(".edit-button");
    editButton.forEach(button => {
        button.addEventListener('click', editPost(button))
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
    const likes = document.querySelector(`#like-count-${postId}`);
    let counter = Number(likes.innerText);

    const isLiked = button.classList.contains('liked');

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

function editPost(button){
    
    button.addEventListener('click', () => {
        const postId = button.dataset.postId;
        
        document.querySelector(`.editButton-${postId}`).style.display = "none";
        document.querySelector(`#editor-${postId}`).style.display = "block";

        document.querySelector(`.editForm-${postId}`).onsubmit = function(){

            fetch(`/edit/${postId}`, {
                method:"PUT",
                body: JSON.stringify({
                    "text": document.querySelector(`#editedText-${postId}`).value
                })
            })
            .then(data => {
                document.querySelector(`.editButton-${postId}`).style.display = "block";
                document.querySelector(`#editor-${postId}`).style.display = "none";
                document.querySelector(`#postBody-${postId}`).innerHTML = document.querySelector(`#editedText-${postId}`).value
            })

            return false;
        }
    })
}
