
function loadData() {

  $.ajax(
  {
    // requesting from the server
    url : "/blog/.json",
    datatype : "json",
  })
  .done(function(response)
  {
    console.log(response);
    // for(var i = 0; i < response.length; i++)
    // {
    //   $("#blog-posts").append("<li>" + response[i]["content"] + "</li>");
    // }
  })
  .fail(function()
  {
    console.log("error");
  });

  return false;
  };

 // pass function to submit button on click
 $('#form-container').submit(loadData);
}

// pass function to submit button on click
$('#form-container').submit(loadData);

