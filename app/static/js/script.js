function vote(direction, postId){
  console.log("pressed")
  console.log(direction, postId)
  $.post('/vote',{
    direction : direction,
    postId : postId
  }).done(function(voted) {
    $("#vote" + postId).text(voted)
  }).fail(function(voted) {
    console.log("vote failed")
  });
}

$(document).ready(function() {

var editor = new wysihtml5.Editor("textarea", { // id of textarea element
  toolbar:      "toolbar", // id of toolbar element
  parserRules:  wysihtml5ParserRules // defined in parser rules set 
});

$(".tagManager").tagsManager({
  preventSubmitOnEnter: true,
  maxTags: 4,
  blinkBGColor_1: '#FFFF9C',
  blinkBGColor_2: '#CDE69C'
});

});

