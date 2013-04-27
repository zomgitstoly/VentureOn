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
var maxPostSize = 500;
var currentPostSize = 0;
// var editor = new wysihtml5.Editor("textarea", { // id of textarea element
//   toolbar:      "toolbar", // id of toolbar element
//   parserRules:  wysihtml5ParserRules // defined in parser rules set 
// });

$(".textarea").wysihtml5({
  "font-styles": false, //Font styling, e.g. h1, h2, etc. Default true
  "emphasis": true, //Italics, bold, etc. Default true
  "lists": false, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
  "html": false, //Button which allows you to edit the generated HTML. Default false
  "link": true, //Button to insert a link. Default true
  "image": true, //Button to insert an image. Default true,
});

$(".tagManager").tagsManager({
  preventSubmitOnEnter: true,
  maxTags: 4,
  blinkBGColor_1: '#FFFF9C',
  blinkBGColor_2: '#CDE69C'
});

var wysihtml5Editor = $('.textarea').data("wysihtml5").editor;
wysihtml5Editor.on("load", function() {
  var doc = $(wysihtml5Editor.composer.doc);
  var post;
  doc.keyup(function(evt){
    
    console.log(evt.key + " hey!");
    post = $(".textarea").val();
    var newSize = 0;
    if(evt.which == 32){
      currentPostSize = currentPostSize + 1; 
    }
    else {
      currentPostSize = post.length + 1
    }
    console.log(post.length);
    console.log(post);
    $("#numChar").text((500 - currentPostSize) + " characters left ");
    $("#postOutput").html(post);
  });
});


});

