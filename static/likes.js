$(function() {
    $('.like-button').on('click', async function(event) {
        event.preventDefault()
        event.stopPropagation()
        let id = $(event.target).closest('button').data().id
        let response = await getLikes(id);
        console.log(response); // do logic here

        const btn = $(event.target).closest('button')
        btn.toggleClass('btn-primary')
        btn.toggleClass('btn-secondary')
    })

async function getLikes(message_id) {
    let response = await axios.post(`/messages/${message_id}/like`, {method: "POST"});
    console.log(response);
    return response;
}
});

