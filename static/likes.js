$(function() {
    $('.like-button').on('click', async function(event){
        let id = $(event.target).closest('button').data().id
        let response = await getLikes(id);
        console.log(response); // do logic here
    })

async function getLikes(message_id) {
    let response = await axios.post(`/messages/${message_id}/like`, {method: "POST"});
    console.log(response);
    return response;
}
});

