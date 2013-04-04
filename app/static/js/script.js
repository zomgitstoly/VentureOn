function vote(direction, postId){
  console.log("pressed")
  console.log(direction, postId)
  $.post('/vote',{
    direction : direction,
    postId : postId
  }).done(function(voted) {
    console.log("successfully voted" + voted)
  }).fail(function(voted) {
    console.log("vote failed")
  });
}

