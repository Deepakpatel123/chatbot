var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js";
var url="/faqbot";

var urlMap=new Map();
	urlMap.set("passwordReset","/password/reset");

$(document).ready(function(){
    $(".chat-closed").on("click",function(e){
        $(".chat-header,.chat-content").removeClass("hide");
        $(this).addClass("hide");
    });

    $(".chat-header").on("click",function(e){
        $(".chat-header,.chat-content").addClass("hide");
        $(".chat-closed").removeClass("hide");
    });

    $(".close-header").on("click",function(e){
    	$('.discussion li:not(:first):not(:last)').remove();
 });
});

/*$(document).ready(function(){
	$('#start-record-btn').on("click",function(e){
		popup();
		$(this).addClass("hide");
		
	});
});
function popup(){
	document.getElementById("speech_ok").style.display = "block";
}*/


function addIn(input) {
/* 	$("#edit").html($("#edit").html()+ "<br />"+ input+'\r'+'\n');
 */	
	today = new Date()
	dayindex = today.toLocaleString(navigator.language, {
    hour: '2-digit',
    minute:'2-digit'
  });
	var user = "<li class='self'><div class='avatar'><img alt='chatbox' src='static/user.png'/>"+
				"</div><div class='messages'><p>"+input+"</p></div></li>"+
				"<div class='time'><p>"+dayindex+"</p></div>";
	
	document.getElementById("ref").insertAdjacentHTML('beforebegin', user);
	var elem = document.getElementById('main');
	  elem.scrollTop = elem.scrollHeight;
 }
 
function addOut(output) {
	/* 	$("#edit").html($("#edit").html()+ "<br />"+ input+'\r'+'\n');
	 */	
	today = new Date()
	dayindex = today.toLocaleString(navigator.language, {
    hour: '2-digit',
    minute:'2-digit'
  });
	var AI = "<li class='other'><div class='avatar'><img alt='chatbox' src='static/Logoed.PNG' id='image'/>"+
				"</div><div class='messages-out'><p>"+output+"</p></div></li>"+
				"<div class='time-out'><p>"+dayindex+"</p></div>";
	
	document.getElementById("ref").insertAdjacentHTML('beforebegin', AI);
	var elem = document.getElementById('main');
	  elem.scrollTop = elem.scrollHeight;
	  console.log(output);
	  console.log(typeof output);
}

$(document).ready(function() {
     //added missing-v quotes 
     $('#close').click(function() {
        location.reload();     
     });    
   });  
 
function txtbox(ele) {
    if(event.key === 'Enter') {
        alert(ele.value);        
    }
}
	
$("#edit").change(function() {
	  scrollToBottom();
	});
	
function scrollToBottom() {
	  $('#edit').scrollTop($('#object')[0].scrollHeight);
	}
function statement(){
	var response = "No"
	addIn(response);
  var x = "Ok. How else can I help you?"
  addOut(x);
  /*document.getElementsByClassName("sendemail")[0].style.display = "none";
  document.getElementsByClassName("okstatement-p")[0].style.display = "none";*/
  $('#input').focus();
}

$(document).ready(function() {
    $('#mainscreen').submit(
        function(event) {
            var input = $('#input').val();
           	var send= input+'\r'+'\n';
           	addIn(send);
            $('#input').val("");
            var data = 'input='
                    + encodeURIComponent(input);
            $.ajax({
                url: url,
                data : data,
                type : "POST",
                success : function(response) {                   
                    if (response == "water"){
					   response = "Sorry I didn't get you.<br><br>"
					   var string = "Would you Like to send this query to HR?"
					   var displayed = "<p><div class='buttons'><div class='emailing'>"+
										"<address><a class='sendemail' style='display:inline; text-decoration:none;' href='mailto:hrmumbai@bcone.com'>Yes</a></address></div>"+
										"<p class='okstatement-p' onclick='statement()' style='display:inline;'>No</p></div></p>"
						response = response + string + displayed;
					   }
					else{
						response = response;
						/*document.getElementsByClassName("sendemail")[0].style.display = "none";
						document.getElementsByClassName("okstatement-p")[0].style.display = "none";*/
					}
					var newSend= response+'\r'+'\n';
                   addOut(newSend);
                   $('#input').focus();
                },
                error : function(xhr, status, error) {
                    alert(xhr.responseText);
                }
            });
            return false;
        });
    });
