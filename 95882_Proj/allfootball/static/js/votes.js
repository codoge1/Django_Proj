function increase_likes() {
    const topic_id = $('#likes').attr("topic_id");
    $.get('/increase_likes', {id:topic_id}, (data) => {
        $('#likes_count').html(data);
    })
}

function increase_favorates() {
    const topic_id = $('#favorates').attr("topic_id")
    $.get('/increase_favorates', {id:topic_id}, (data) => {
        $('#favorates_count').html(data)
    })
}

