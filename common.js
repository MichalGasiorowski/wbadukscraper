//***********************************************************************************
// Author      : seo.h.y
// Create Date : 2009-11-20
// Description : ?? ???? ? ?? ?? (???????)
//***********************************************************************************


//#####  ?? Function  ################################################################################################

//menu
function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}
function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
	var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
	if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}
function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
	d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}
function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

//??? ?? ???
function reloadHeight(frm){
	var objBody = eval(frm + ".document.body");
	var objFrame = document.all[frm];

	objFrame.style.height = objBody.scrollHeight + (objBody.offsetHeight - objBody.clientHeight);
}

//?? ?? ??
function getlength(item){
	var onchar
	var ochar
	var tcount=0

	var aaa = eval("document.all." + item)
	onechar	=	aaa.value;
	leng	=	onechar.length;

	for(i=0 ; i< leng ;i++){
		ochar=onechar.charAt(i)
		if(escape(ochar).length > 4){
			tcount+=2;
		}else if (ochar!='\r') {
			tcount++;
		}

	}
	return tcount
}

//window open
function open_pop(url,name,width,height){	
	window.open(url,name,'toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width='+width+',height='+height+',top=200,left=200');
}

//delete check
function ComDelCheck(val){
	sure = confirm("Delete?")
	if(sure){
		location.href = val
	}
}

//login check
function loginCheck(user_id){
	if(user_id == "" || user_id == undefined){
		alert("Left login");
		parent.form_login.id.focus();
	}
}

//??? ??
function setCookie(name, value, expiredays){ 
	if(typeof expiredays == "undefined" || expiredays == null){
		var expiredays = 1; //?? ??
	}
	var todayDate = new Date();
	todayDate.setDate( todayDate.getDate() + expiredays );
	document.cookie = name + "=" + escape( value ) + "; path=/; expires=" + todayDate.toGMTString() + ";"
}

//??? ????
function getCookie(name) {
   var key = name + "=" ;
   var key_len = key.length ;
   var cookie_len = document.cookie.length;
   var i = 0;
   while (i < cookie_len ) {
	  var j = i + key_len;
	  if ( document.cookie.substring( i, j ) == key ) {
		 var cookie_end = document.cookie.indexOf(";",j);
		 if (cookie_end == -1) {
			cookie_end = document.cookie.length;
		 }
		 return document.cookie.substring(j,cookie_end );
	  }
	  i++
   }
   return ""
}


//??? ??1
function inputCheck(name, msg){		
	var aaa = eval("document.all." + name)
	if (aaa.value == ""){
		alert(msg);
		aaa.focus();
		return true;
	}
}

//??? ??2 (??? X)
function inputCheck2(name, msg){	
	var aaa = eval("document.all." + name)
	if(aaa.value == ""){
		alert(msg);
		return true;
	}
}

//?? ??
var temp00 = "";
function checkLength(field, field2, limit) {
	var f = eval("document.all." + field)
	var f2 = eval("document.all." + field2)
	
	if ( countBytes(f.value) > limit) {
		alert('Please write the subject up to ' + limit + ' letters.');
		f.value = temp00;
	}else{
		f2.innerHTML = countBytes(f.value);
		temp00 = f.value;
	}
}

//?? ???
function countBytes(field) {
	var tcount   = 0;
	var tmpStr   = new String(field);
	var tmpCount = tmpStr.length;
	var onechar;

	for ( k=0; k<tmpCount; k++ ) {
		oneChar = tmpStr.charAt(k);
		if (escape(oneChar).length > 4) {
			tcount += 2;
		} else {
			tcount += 1;
		}
	}
	return tcount;
}

//?????? ??? ???(??)
function centerWindow(url,w,h) {
	LeftPosition = (screen.width) ? (screen.width-w)/2 : 0;
	TopPosition = (screen.height) ? (screen.height-h)/2 : 0;
	settings = 'height='+h+',width='+w+',top='+TopPosition+',left='+LeftPosition
	winName = url.substr(1,1);
	window.open(url, winName, settings);
}


//#####  WBaduk ? Function  ################################################################################################

//gibo
function gibo_load(gibonum) {
	window.open('/gibo/gibo_view.asp?gb_no='+gibonum,'gibo','toolbar=no,location=no,diectories=yes,status=yes,scrollbars=no,menubar=no,resizable=yes,width=915,height=710');
}

//??
function Lecture_load(lectnum) {
	window.open('/lecture/lecture_text_view.asp?lecture_no='+lectnum,'gibo','toolbar=no,location=no,diectories=yes,status=yes,scrollbars=no,menubar=no,resizable=yes,width=915,height=710');
}

//??? ??
function Lecture_Movie(no, tp) {	
	if(tp == 1){
		centerWindow('/lecture/lecture_movie_view.asp?movie_no='+no, 674, 665);	//640*360
	}else{
		centerWindow('/lecture/lecture_movie_view.asp?movie_no='+no, 800, 620); //500*500
	}
}


//?? ??

//function IsInstall() {
//	delayTime();
//}

//function delayTime() {   
//	waitTime = window.setTimeout("oro2000()", 100);	  
//}

function gameRun(COM_PROGRAM_FILE) {
	var check;
	
	check = SChecker.IsOro("Cyberoro\\English","Dirpath Info","oropath","upcheck");

	if(check == 2) {
		if(confirm("Program is not installed. Setup Thist Program ?")) {
		   location.href = COM_PROGRAM_FILE ;
		}
	} else {
		SChecker.ExeOro("Cyberoro\\English","Dirpath Info","oropath","upcheck");
	}
}


function STRING_CHECK(content){
	search_str = "shutdown^drop^declare^varchar^sysobjects^exec^truncate^declare";
    search_str = search_str + "^master^alert(^script";
    search_str = search_str + "^--^##^??^\^%20%61%6E%64%20%31%3D%31^%201=1%20";

	arr_search_str = search_str.split("^");

	for (i=0; i<arr_search_str.length; i++){	
		if(content.toLowerCase().indexOf(arr_search_str[i]) > -1 && arr_search_str[i] != ""){
			alert( "[ " + arr_search_str[i] + " ] is a forbidden word"  );
			return false;
		}
	}
}
