
function loadData()
{
  $.getJSON("https://jsonplaceholder.typicode.com/posts", function(data)
  {
    console.log(data);
  })
  .fail(function()
  {
  	// handling error
    alert("error");
  });

  return false;
}

// pass function to submit button on click
$('#form-container').submit(loadData);

