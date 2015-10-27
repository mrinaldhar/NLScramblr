    var inputdata;
   function dataload() {
	inputdata = ajaxCall('/getnew', {}, 'GET', false);
    inputdata["chunks"].each(function(i) {
    	$('#sortable').append("<li>"+inputdata["chunks"][i]+"</li>");
    });
   }
  $(document).ready(function() {
    $( "#sortable" ).sortable();
    $( "#sortable" ).disableSelection();
  });
  function submitthis() {
  	var result = [];
  	var elements = $('#sortable').children('li');
  	elements.each(function(i) { 
    	result.push(elements[i].innerHTML);
	});
  	console.log(result);
  	data = {"result":result, "original":inputdata["id"]};
  	ajaxCall('/process', data, 'POST', false);
  	alert("Thank you! Your response has been saved. Keep going!");
  	dataload();
  }


$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

function ajaxCall(endpoint, objToSend, ajaxmethod, asyncVal) {
    var res;
$.ajax({
  url: endpoint,
  data: objToSend,
  dataType: "json",
  async: asyncVal,  
type: ajaxmethod,
  success: function(data) {
    res = data;
  }
});
return res;
}