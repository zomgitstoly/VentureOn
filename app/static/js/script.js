function vote(direction, postId, curVote){
  console.log("pressed")
  console.log(direction, postId)
 /* vote = parseInt(curVote, 10)
  if(direction == "up"){
    vote += 1
    $("vote" + postId).text(vote)
  }
  else if(direction == "down"){
    vote -= 1
    $("vote" + postId).text(vote)
  }*/
  $.post('/vote',{
    direction : direction,
    postId : postId
  }).done(function(voted) {
    $("#vote" + postId).text(voted)
  }).fail(function(voted) {
    console.log("vote failed")
  });
}

